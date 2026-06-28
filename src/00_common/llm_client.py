"""
src/00_common/llm_client.py
============================
Module gọi LLM (Google Vertex AI / Google AI Studio) dùng chung cho pipeline DTM.

Lý do tách ra module riêng:
    - Cả 2 script gọi LLM (03 và 07) dùng chung cùng logic retry, logging, parse JSON
    - Thay đổi model hoặc provider chỉ cần sửa ở đây
    - Dễ mock khi chạy test mà không cần gọi API thật

Cơ chế hoạt động:
    - LLM được điều kiện hóa bởi prompt để dự đoán theo tiêu chí đã định nghĩa.
    - KHÔNG nói: "LLM học từ prompt" (vì đây là in-context conditioning, không phải training)
"""

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Thư viện Google Generative AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    VERTEX_AVAILABLE = True
except ImportError:
    VERTEX_AVAILABLE = False

from .config_loader import get_project_config
from .io_utils import get_project_root

logger = logging.getLogger(__name__)


# =============================================================================
# Khởi tạo LLM client
# =============================================================================

class LLMClient:
    """
    Client gọi LLM cho pipeline DTM.
    
    Hỗ trợ:
        - Google AI Studio (API key) — dùng cho dev/test
        - Google Vertex AI (Service Account) — dùng cho production
    
    Cách dùng:
        client = LLMClient()
        result = client.predict(prompt_text, record_text)
    """
    
    def __init__(self):
        cfg = get_project_config()
        llm_cfg = cfg.get("llm", {})
        
        self.model_name = os.getenv("LLM_MODEL_NAME", llm_cfg.get("model", "gemini-2.5-flash"))
        self.temperature = float(os.getenv("LLM_TEMPERATURE", llm_cfg.get("temperature", 0.0)))
        self.delay_seconds = float(os.getenv("LLM_DELAY_SECONDS", llm_cfg.get("delay_seconds", 0.5)))
        self.provider = os.getenv("LLM_PROVIDER", "google_ai_studio")
        
        self._model = None
        self._initialize()
    
    def _initialize(self):
        """Khởi tạo kết nối LLM dựa trên provider."""
        if self.provider == "vertex_ai":
            self._init_vertex()
        else:
            self._init_genai()
    
    def _init_genai(self):
        """Khởi tạo Google AI Studio."""
        if not GENAI_AVAILABLE:
            raise ImportError("Thiếu thư viện google-generativeai. Chạy: pip install google-generativeai")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Thiếu GOOGLE_API_KEY trong .env")
        
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=genai.GenerationConfig(
                temperature=self.temperature,
                response_mime_type="application/json",
            )
        )
        logger.info(f"✅ Khởi tạo Google AI Studio: model={self.model_name}")
    
    def _init_vertex(self):
        """Khởi tạo Vertex AI."""
        if not VERTEX_AVAILABLE:
            raise ImportError("Thiếu thư viện google-cloud-aiplatform. Chạy: pip install google-cloud-aiplatform")
        
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        if not project:
            raise ValueError("Thiếu GOOGLE_CLOUD_PROJECT trong .env")
        
        if credentials_path:
            # resolve relative path từ project root
            cred_path = get_project_root() / credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_path)
        
        vertexai.init(project=project, location=location)
        self._model = GenerativeModel(self.model_name)
        logger.info(f"✅ Khởi tạo Vertex AI: project={project}, model={self.model_name}")
    
    # =========================================================================
    # Gọi LLM
    # =========================================================================
    
    def predict(
        self,
        system_prompt: str,
        record_text: str,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Gọi LLM với system prompt và nội dung bản ghi.
        
        Args:
            system_prompt: Nội dung system prompt (từ prompts/*.txt)
            record_text: Nội dung bản ghi đã được format vào prompt
            max_retries: Số lần retry nếu LLM lỗi
            retry_delay: Thời gian chờ giữa các retry (giây)
        
        Returns:
            Dict: JSON response đã parse
            - Nếu thành công: dict với các trường theo format prompt
            - Nếu lỗi: {"error": str, "raw_response": str}
        
        Lý do dùng retry:
            API LLM đôi khi bị rate limit hoặc timeout, cần retry để tránh mất dữ liệu
        """
        full_prompt = f"{system_prompt}\n\n{record_text}"
        
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                response = self._call_model(full_prompt)
                parsed = self._parse_json_response(response)
                
                if self.delay_seconds > 0:
                    time.sleep(self.delay_seconds)
                
                return parsed
                
            except Exception as e:
                last_error = e
                logger.warning(f"  ⚠️  Attempt {attempt}/{max_retries} thất bại: {type(e).__name__}: {e}")
                if attempt < max_retries:
                    time.sleep(retry_delay * attempt)  # Exponential backoff
        
        # Tất cả retry thất bại
        logger.error(f"  ❌ Tất cả {max_retries} lần retry thất bại. Lỗi cuối: {last_error}")
        return {
            "error": str(last_error),
            "raw_response": None,
        }
    
    def _call_model(self, prompt: str) -> str:
        """Gọi model và trả về raw text response."""
        if self.provider == "vertex_ai":
            response = self._model.generate_content(prompt)
            return response.text
        else:
            response = self._model.generate_content(prompt)
            return response.text
    
    def _parse_json_response(self, raw_text: str) -> Dict:
        """
        Parse JSON từ response của LLM.
        
        Xử lý các trường hợp LLM trả về:
        1. JSON thuần  → parse trực tiếp
        2. ```json ... ``` → strip markdown fences trước khi parse
        3. Text lẫn JSON → dùng regex tìm JSON block
        
        Args:
            raw_text: Text response từ LLM
        
        Returns:
            Dict: JSON đã parse
        
        Raises:
            json.JSONDecodeError: Nếu không parse được
        """
        if not raw_text:
            raise ValueError("LLM trả về response rỗng")
        
        text = raw_text.strip()
        
        # Thử parse trực tiếp
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Strip markdown code fences
        patterns = [
            r"```json\s*([\s\S]*?)\s*```",
            r"```\s*([\s\S]*?)\s*```",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    return json.loads(match.group(1).strip())
                except json.JSONDecodeError:
                    pass
        
        # Tìm JSON object đầu tiên trong text
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        
        raise json.JSONDecodeError(
            f"Không thể parse JSON từ response. Raw: {text[:200]}...",
            text, 0
        )


# =============================================================================
# Singleton instance
# =============================================================================

_client_instance: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """
    Trả về singleton LLMClient.
    Khởi tạo lần đầu khi gọi, tái sử dụng cho các lần sau.
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = LLMClient()
    return _client_instance


def reset_client() -> None:
    """Reset client (dùng khi test)."""
    global _client_instance
    _client_instance = None
