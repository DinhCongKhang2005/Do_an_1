#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_llm_classify_5_labels.py
============================
BƯỚC 7 — LLM phân loại 5 nhãn tác động cho từng bản ghi trong D_env.

Đề tài: Đánh giá tác động chính sách môi trường — Khung định lượng: lợi ích, chi phí, rủi
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Vị trí trong pipeline:
    Input:  data/processed/env_final_dataset.xlsx  (D_env, env_final=1)
    Prompt: prompts/classify_5_labels_system_prompt.txt
    Output: data/interim/class_llm_labeled_dataset.xlsx
            outputs/logs/classify_5labels.log
    Tiếp theo: Script 08 (so sánh class_human vs class_llm)

Nguyên lý:
    LLM được điều kiện hóa bởi system prompt để dự đoán 1 trong 5 nhãn.
    Script chỉ thu thập dự đoán LLM — không đánh giá, không quyết định final.
    
    ⚠️ QUAN TRỌNG: class_llm phải được thu thập TRƯỚC KHI xem class_human
    (để đảm bảo LLM không bị ảnh hưởng bởi nhãn human).

Output của mỗi bản ghi:
    - class_llm: Một trong 5 nhãn đầy đủ
    - class_llm_reason: Giải thích của LLM
    - class_evidence_span: Bằng chứng văn bản
    - class_confidence: Độ tự tin [0,1]
    - class_needs_human_review: True/False
    - rule_applied: Quy tắc phân biệt nhãn (QT1-QT6)
    - quantity_interpretation: Giải thích số trong văn bản
    - class_llm_error: Lỗi (nếu có)

Sử dụng:
    py src/07_llm_classify_5_labels.py
    py src/07_llm_classify_5_labels.py --limit 10
    py src/07_llm_classify_5_labels.py --resume
"""

import json
import logging
import os
import re
import sys
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Event, Lock

import pandas as pd
import yaml
from dotenv import load_dotenv

# ─── Project root ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

LOG_DIR = PROJECT_ROOT / "outputs" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "classify_5labels.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

VALID_5_LABELS = [
    "BENEFIT_QUANTITATIVE", "BENEFIT_QUALITATIVE",
    "COST_QUANTITATIVE", "COST_QUALITATIVE", "CONSTRAINT"
]
ALIAS_MAP = {
    "BQ": "BENEFIT_QUANTITATIVE", "BQL": "BENEFIT_QUALITATIVE",
    "CQ": "COST_QUANTITATIVE", "CQL": "COST_QUALITATIVE", "CON": "CONSTRAINT",
}


def load_config():
    with open(PROJECT_ROOT / "config" / "project_config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompt(cfg: dict) -> str:
    prompt_path = PROJECT_ROOT / cfg["llm"]["prompt_classify_5"]
    if not prompt_path.exists():
        raise FileNotFoundError(f"Không tìm thấy prompt: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def init_llm(cfg: dict):
    """Khởi tạo LLM giống script 03."""
    provider = os.getenv("LLM_PROVIDER", cfg["llm"].get("provider", "google_ai_studio"))
    model_name = os.getenv("LLM_MODEL_NAME", cfg["llm"].get("model", "gemini-2.5-flash"))
    temperature = float(os.getenv("LLM_TEMPERATURE", cfg["llm"].get("temperature", 0.0)))
    
    if provider == "vertex_ai_express":
        from google import genai
        from google.genai import types

        api_key = os.getenv("VERTEX_AI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Thiếu VERTEX_AI_API_KEY trong .env")

        client = genai.Client(
            vertexai=True,
            api_key=api_key,
            http_options=types.HttpOptions(api_version="v1"),
        )
        gen_config = types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="application/json",
        )
        logger.info(f"✅ Vertex AI Express/API key: {model_name}")
        return client, model_name, gen_config, provider
    elif provider == "vertex_ai":
        from google import genai
        from google.genai import types

        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(PROJECT_ROOT / cred_path)

        client = genai.Client(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "global"),
            http_options=types.HttpOptions(api_version="v1"),
        )
        gen_config = types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="application/json",
        )
        logger.info(f"✅ Vertex AI service account: {model_name}")
        return client, model_name, gen_config, provider
    else:
        from google import genai
        from google.genai import types

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Thiếu GOOGLE_API_KEY trong .env")

        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(api_version="v1"),
        )
        gen_config = types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="application/json",
        )
        logger.info(f"✅ Google AI Studio: {model_name}")
        return client, model_name, gen_config, provider


def format_record(rec: dict) -> str:
    return f"""source_id: {rec.get('source_id', 'N/A')}
legal_citation: {rec.get('legal_citation', 'N/A')}
raw_text: {rec.get('raw_text', '')}
actor: {rec.get('actor', '')}
legal_signal: {rec.get('legal_signal', '')}
domain: {rec.get('domain', '')}
quantitative_value: {rec.get('quantitative_value', '')}
condition: {rec.get('condition', '')}
env_final: true  [Đã xác nhận có tác động môi trường]"""


def call_llm_with_retry(client, model_name: str, gen_config, prompt_text: str, max_retries: int | None = None, delay: float | None = None):
    """Gọi LLM với retry/backoff, đặc biệt cho lỗi 429 quota/rate-limit."""
    if max_retries is None:
        max_retries = int(os.getenv("LLM_MAX_RETRIES", "6"))
    if delay is None:
        delay = float(os.getenv("LLM_RETRY_BASE_SECONDS", "3.0"))

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_text,
                config=gen_config,
            )
            return response.text
        except Exception as e:
            if is_fatal_llm_config_error(e):
                raise RuntimeError(
                    "Lỗi cấu hình LLM: model không tồn tại hoặc project/location không có quyền truy cập. "
                    "Kiểm tra LLM_MODEL_NAME, GOOGLE_CLOUD_PROJECT và GOOGLE_CLOUD_LOCATION trong .env."
                ) from e

            retryable = is_retryable_llm_error(e)
            logger.warning(f"    ⚠️  Attempt {attempt}/{max_retries}: {e}")
            if attempt >= max_retries or not retryable:
                break

            # Exponential backoff + jitter để tránh nhiều worker retry cùng lúc.
            sleep_seconds = min(delay * (2 ** (attempt - 1)), 60.0) + random.uniform(0.0, 1.5)
            logger.info(f"    ⏳ Chờ {sleep_seconds:.1f}s rồi retry...")
            time.sleep(sleep_seconds)

    raise RuntimeError(f"Tất cả {max_retries} lần retry đều thất bại")


def is_retryable_llm_error(error: Exception) -> bool:
    msg = str(error).lower()
    retryable_markers = [
        "429",
        "resource_exhausted",
        "rate limit",
        "quota",
        "try again later",
        "timeout",
        "deadline exceeded",
        "503",
        "unavailable",
        "500",
        "internal",
    ]
    return any(marker in msg for marker in retryable_markers)

def is_fatal_llm_config_error(error: Exception) -> bool:
    """Các lỗi này không nên retry theo từng bản ghi vì toàn bộ run sẽ thất bại giống nhau."""
    msg = str(error).lower()
    fatal_markers = [
        "publisher model",
        "was not found",
        "does not have access",
        "invalid model",
        "permission denied",
        "unauthenticated",
    ]
    return any(marker in msg for marker in fatal_markers)


def normalize_label(raw_label: str) -> str | None:
    """Chuẩn hóa nhãn LLM: strip + uppercase + alias map."""
    if not raw_label:
        return None
    normalized = str(raw_label).strip().upper()
    if normalized in VALID_5_LABELS:
        return normalized
    return ALIAS_MAP.get(normalized)


def parse_class_response(raw_text: str) -> dict:
    """Parse JSON response từ LLM cho bài toán 5 nhãn."""
    # Parse JSON
    try:
        data = json.loads(raw_text.strip())
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
        if match:
            data = json.loads(match.group(1).strip())
        else:
            match = re.search(r"\{[\s\S]*\}", raw_text)
            if match:
                data = json.loads(match.group(0))
            else:
                raise ValueError(f"Không parse được JSON: {raw_text[:200]}")
    
    raw_label = str(data.get("label", ""))
    class_llm = normalize_label(raw_label)
    
    return {
        "class_llm":               class_llm or raw_label,  # Giữ nguyên raw nếu không normalize được
        "class_llm_valid":         class_llm is not None,   # Có normalize thành công không
        "class_llm_reason":        str(data.get("reason", "")),
        "class_evidence_span":     str(data.get("evidence_span", "")),
        "class_confidence":        float(data.get("confidence", 0.0)),
        "class_needs_human_review": bool(data.get("needs_human_review", False)),
        "rule_applied":            str(data.get("rule_applied", "")),
        "quantity_interpretation": str(data.get("quantity_interpretation", "")),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="LLM phân loại 5 nhãn tác động môi trường"
    )
    parser.add_argument("--limit",  type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--workers", type=int, default=1, metavar="N",
        help="Số worker song song gọi LLM (mặc định=1). Khuyến nghị 4–8 với Vertex AI Express."
    )
    args = parser.parse_args()
    
    cfg = load_config()
    
    logger.info("=" * 60)
    logger.info("  BƯỚC 7 — LLM phân loại 5 nhãn (class_llm)")
    logger.info("=" * 60)
    
    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_data"]
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    
    # ── Đọc D_env ──
    env_path = processed_dir / cfg["processed_files"]["env_final_dataset"]
    if not env_path.exists():
        logger.error(f"Không tìm thấy D_env: {env_path}. Chạy script 05 trước!")
        sys.exit(1)
    
    df_env = pd.read_excel(env_path, dtype=str)
    df = df_env[df_env["env_final"].astype(str).str.strip().isin(["1", "True", "true"])].copy()
    records = df.to_dict("records")
    logger.info(f"  → D_env: {len(records)} bản ghi")
    
    if args.limit:
        records = records[:args.limit]
        logger.info(f"  → Giới hạn test: {len(records)}")
    
    # ── Resume ──
    output_path = interim_dir / cfg["interim_files"]["class_llm_labeled_dataset"]
    processed_ids = set()
    existing_rows = []
    if args.resume and output_path.exists():
        df_ex = pd.read_excel(output_path, dtype=str)
        processed_ids = set(df_ex["source_id"].dropna().tolist())
        existing_rows = df_ex.to_dict("records")
        logger.info(f"  → Resume: đã có {len(processed_ids)} bản ghi")
    
    # ── Load prompt và LLM ──
    logger.info("[Bước 7.1] Load prompt và khởi tạo LLM")
    system_prompt = load_prompt(cfg)
    client, model_name, gen_config, provider = init_llm(cfg)
    delay = float(os.getenv("LLM_DELAY_SECONDS", cfg["llm"].get("delay_seconds", 0.5)))
    n_workers = max(1, args.workers)

    # ── Hàm xử lý 1 bản ghi (thread-safe) ─────────────────────────────────
    stop_event = Event()
    invalid_lock = Lock()
    invalid_count = [0]

    def process_one(rec: dict) -> dict:
        """Gọi LLM cho 1 bản ghi. Thread-safe.

        Lý do bắt KeyboardInterrupt riêng:
            `except Exception` trong thread con sẽ nuốt mất KeyboardInterrupt
            từ time.sleep(). Bắt riêng và re-raise để main thread nhận được.
        """
        if stop_event.is_set():
            return None

        sid = str(rec.get("source_id", ""))
        row = {
            "source_id":               sid,
            "legal_citation":          rec.get("legal_citation", ""),
            "raw_text":                str(rec.get("raw_text", "")),
            "class_llm":               None,
            "class_llm_valid":         None,
            "class_llm_reason":        "",
            "class_evidence_span":     "",
            "class_confidence":        None,
            "class_needs_human_review": None,
            "rule_applied":            "",
            "quantity_interpretation": "",
            "class_llm_error":         "",
            "class_llm_raw_response":  "",
        }
        record_input = format_record(rec)
        full_prompt = f"{system_prompt}\n\n{record_input}"
        try:
            raw_response = call_llm_with_retry(client, model_name, gen_config, full_prompt)
            parsed = parse_class_response(raw_response)
            row.update(parsed)
            row["class_llm_raw_response"] = raw_response[:500]
            if not parsed.get("class_llm_valid"):
                with invalid_lock:
                    invalid_count[0] += 1
                logger.warning(f"  ⚠️  Nhãn không hợp lệ source_id={sid}: '{parsed['class_llm']}'")
        except KeyboardInterrupt:
            stop_event.set()
            raise
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:200]}"
            logger.error(f"  ❌ Lỗi source_id={sid}: {error_msg}")
            if is_fatal_llm_config_error(e):
                stop_event.set()
            row["class_llm_error"] = error_msg

        try:
            if delay > 0:
                time.sleep(delay)
        except KeyboardInterrupt:
            stop_event.set()
            raise
        return row

    # ── Gọi LLM (sequential hoặc parallel) ─────────────────────────────────
    todo = [r for r in records if str(r.get("source_id", "")) not in processed_ids]
    logger.info(
        f"[Bước 7.2] Gọi LLM cho {len(todo)} bản ghi "
        f"({'song song ' + str(n_workers) + ' workers' if n_workers > 1 else 'tuần tự'})..."
    )
    results = list(existing_rows)
    results_lock = Lock()  # bảo vệ results khi append từ nhiều thread
    counter_lock = Lock()
    done_count = [0]
    order_index = {str(rec.get("source_id", "")): i for i, rec in enumerate(records)}

    def save_results_checkpoint(reason: str = "") -> pd.DataFrame:
        """Lưu kết quả hiện có, thread-safe, để có thể --resume khi bị ngắt."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with results_lock:
            snapshot = list(results)
        df_checkpoint = pd.DataFrame(snapshot)
        if not df_checkpoint.empty and "source_id" in df_checkpoint.columns:
            df_checkpoint["_order"] = df_checkpoint["source_id"].astype(str).map(order_index).fillna(10**9)
            df_checkpoint = df_checkpoint.sort_values("_order").drop(columns=["_order"])
        df_checkpoint.to_excel(output_path, index=False)
        if reason:
            logger.info(f"  💾 Đã lưu checkpoint ({reason}): {output_path.name} ({len(df_checkpoint):,} dòng)")
        return df_checkpoint

    if n_workers == 1:
        # ── Sequential ───────────────────────────────────────────────────────
        try:
            for i, rec in enumerate(todo, 1):
                if stop_event.is_set():
                    save_results_checkpoint("fatal error")
                    logger.error("  Fatal error gặp phải, dừng pipeline. Sửa cấu hình và chạy lại với --resume.")
                    sys.exit(1)
                if i % 50 == 0 or i == 1:
                    logger.info(f"  [{i}/{len(todo)}] source_id={rec.get('source_id','')}")
                row = process_one(rec)
                if row:
                    results.append(row)
                if i % 25 == 0:
                    save_results_checkpoint(f"{i}/{len(todo)}")
        except KeyboardInterrupt:
            save_results_checkpoint("KeyboardInterrupt")
            logger.warning("  Đã dừng theo yêu cầu. Chạy lại với --resume để tiếp tục.")
            sys.exit(130)
    else:
        # ── Parallel ───────────────────────────────────────────────────────
        future_to_rec = {}
        executor = ThreadPoolExecutor(max_workers=n_workers)
        try:
            for rec in todo:
                if stop_event.is_set():
                    break
                fut = executor.submit(process_one, rec)
                future_to_rec[fut] = rec

            for fut in as_completed(future_to_rec):
                try:
                    row = fut.result()
                except KeyboardInterrupt:
                    raise  # đẩy lên except KeyboardInterrupt bên dưới
                except Exception:
                    continue  # lỗi từng bản ghi đã xử lý trong process_one
                if row is None:
                    continue
                with results_lock:
                    results.append(row)
                with counter_lock:
                    done_count[0] += 1
                    n_done = done_count[0]
                if n_done % 50 == 0 or n_done == 1:
                    logger.info(f"  [{n_done}/{len(todo)}] hoàn thành (parallel)")
                if n_done % 25 == 0:
                    save_results_checkpoint(f"{n_done}/{len(todo)}")
        except KeyboardInterrupt:
            stop_event.set()
            for fut in future_to_rec:
                fut.cancel()
            save_results_checkpoint("KeyboardInterrupt")
            logger.warning("  Đã dừng theo yêu cầu. Chạy lại với --resume để tiếp tục.")
            sys.exit(130)
        finally:
            # shutdown chỉ gọi 1 lần trong finally, tránh double-call
            executor.shutdown(wait=False, cancel_futures=True)

        if stop_event.is_set():
            save_results_checkpoint("fatal error")
            logger.error("  Fatal error gặp phải, dừng pipeline. Sửa cấu hình và chạy lại với --resume.")
            sys.exit(1)
    
    # ── Lưu ──
    logger.info(f"[Bước 7.3] Lưu: {output_path.name}")
    df_result = save_results_checkpoint("final")
    
    # ── Thống kê phân phối nhãn ──
    label_counts = df_result["class_llm"].value_counts()
    n_success = int(df_result["class_llm"].notna().sum())
    n_error = int(df_result["class_llm_error"].astype(bool).sum())
    n_invalid_label = int((df_result["class_llm_valid"].astype(str).str.lower() == "false").sum())
    
    logger.info(f"""
  ─── KẾT QUẢ class_llm ────────────────────────────────
  Tổng:              {len(df_result):,}
  Thành công:        {n_success:,}
  Lỗi LLM:           {n_error:,}
  Nhãn không chuẩn:  {n_invalid_label:,}
  
  Phân phối nhãn LLM:
{label_counts.to_string()}
  ─────────────────────────────────────────────────────
  Log: {LOG_FILE.name}
  Tiếp theo: py src/08_compare_5label_human_vs_llm.py
  ─────────────────────────────────────────────────────
""")


if __name__ == "__main__":
    main()


