#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_llm_filter_environmental_impact.py
=======================================
BƯỚC 3 — LLM dự đoán env_llm cho từng bản ghi.

Đề tài: Đánh giá tác động chính sách môi trường — Pipeline 2 tầng
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Vị trí trong pipeline:
    Input:  data/raw/Luat_bao_ve_moi_truong_2020.json
    Prompt: prompts/env_filter_system_prompt.txt
    Output: data/interim/env_llm_labeled_dataset.xlsx
            outputs/logs/env_filter.log
    Tiếp theo: Script 04 (so sánh env_human vs env_llm)

Nguyên lý:
    LLM được điều kiện hóa bởi system prompt để dự đoán theo tiêu chí đã định nghĩa.
    Script này KHÔNG tự đánh giá kết quả LLM — việc đó thuộc script 04.

    env_llm và env_human phải được lưu RIÊNG BIỆT.
    Metric LLM được tính ở script 04 TRƯỚC KHI adjudication.

Output của mỗi bản ghi:
    - env_llm: 0 hoặc 1 (từ JSON field "env_label")
    - env_llm_reason: giải thích của LLM
    - env_evidence_span: bằng chứng văn bản
    - env_confidence: độ tự tin [0, 1]
    - env_needs_human_review: True/False
    - env_llm_domain: domain môi trường (nếu env_llm=1)
    - env_llm_error: thông báo lỗi (nếu LLM thất bại)
    - env_llm_raw_response: raw JSON response (để debug)

Sử dụng:
    py src/03_llm_filter_environmental_impact.py
    py src/03_llm_filter_environmental_impact.py --limit 10  # Test 10 bản ghi đầu
    py src/03_llm_filter_environmental_impact.py --resume    # Tiếp tục từ bản ghi cuối
"""

import argparse
import json
import logging
import os
import sys
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from threading import Event, Lock

import pandas as pd
import yaml
from dotenv import load_dotenv

# ─── Project root ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ─── Load .env ─────────────────────────────────────────────────────────────────
load_dotenv(PROJECT_ROOT / ".env")

# ─── Logging ───────────────────────────────────────────────────────────────────
LOG_DIR = PROJECT_ROOT / "outputs" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "env_filter.log"

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


# ==============================================================================
# Load config & prompt
# ==============================================================================

def load_config():
    with open(PROJECT_ROOT / "config" / "project_config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompt(cfg: dict) -> str:
    prompt_path = PROJECT_ROOT / cfg["llm"]["prompt_env_filter"]
    if not prompt_path.exists():
        raise FileNotFoundError(f"Không tìm thấy prompt: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def load_json_data(filepath: Path) -> list:
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "records" in data:
        return data["records"]
    return [data]


# ==============================================================================
# Khởi tạo LLM
# ==============================================================================

def init_llm(cfg: dict):
    """Khởi tạo LLM client dựa trên provider trong .env"""
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


# ==============================================================================
# Format bản ghi thành prompt input
# ==============================================================================

def format_record_for_prompt(rec: dict) -> str:
    """Format một bản ghi thành phần user input của prompt."""
    return f"""source_id: {rec.get('source_id', 'N/A')}
legal_citation: {rec.get('legal_citation', 'N/A')}
raw_text: {rec.get('raw_text', '')}
actor: {rec.get('actor', '')}
legal_signal: {rec.get('legal_signal', rec.get('tin_hieu_tac_dong', ''))}
domain: {rec.get('domain', '')}
quantitative_value: {rec.get('quantitative_value', rec.get('gia_tri_dinh_luong', ''))}
condition: {rec.get('condition', rec.get('dieu_kien_ap_dung', ''))}"""


# ==============================================================================
# Gọi LLM và parse response
# ==============================================================================

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


def parse_env_response(raw_text: str) -> dict:
    """Parse JSON response từ LLM cho bài toán lọc môi trường."""
    import re
    
    # Thử parse trực tiếp
    try:
        data = json.loads(raw_text.strip())
    except json.JSONDecodeError:
        # Strip markdown
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
        if match:
            data = json.loads(match.group(1).strip())
        else:
            match = re.search(r"\{[\s\S]*\}", raw_text)
            if match:
                data = json.loads(match.group(0))
            else:
                raise ValueError(f"Không parse được JSON: {raw_text[:200]}")
    
    # Normalize env_label → 0/1
    raw_label = data.get("env_label", False)
    if isinstance(raw_label, bool):
        env_llm = 1 if raw_label else 0
    elif str(raw_label).lower() in ("true", "1"):
        env_llm = 1
    else:
        env_llm = 0
    
    return {
        "env_llm":               env_llm,
        "env_llm_reason":        str(data.get("reason", "")),
        "env_evidence_span":     str(data.get("evidence_span", "")),
        "env_confidence":        float(data.get("confidence", 0.0)),
        "env_needs_human_review": bool(data.get("needs_human_review", False)),
        "env_llm_domain":        str(data.get("domain", "")),
    }


# ==============================================================================
# Main
# ==============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="LLM dự đoán env_llm cho Tầng 1 lọc môi trường"
    )
    parser.add_argument("--input",   type=str, default=None, help="Path đến JSON đầu vào")
    parser.add_argument("--output",  type=str, default=None, help="Path Excel output")
    parser.add_argument("--limit",   type=int, default=None, help="Số bản ghi tối đa để test")
    parser.add_argument("--resume",  action="store_true",    help="Tiếp tục từ file output đã có")
    parser.add_argument(
        "--workers", type=int, default=1, metavar="N",
        help="Số worker song song gọi LLM (mặc định=1). Khuyến nghị 4–8 với Vertex AI Express."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    cfg = load_config()
    
    logger.info("=" * 60)
    logger.info("  BƯỚC 3 — LLM lọc tác động môi trường (env_llm)")
    logger.info("=" * 60)
    
    # ── Đường dẫn ──
    raw_dir = PROJECT_ROOT / cfg["paths"]["raw_data"]
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    
    input_path = Path(args.input) if args.input else raw_dir / cfg["input"]["raw_json_file"]
    output_path = Path(args.output) if args.output else interim_dir / cfg["interim_files"]["env_llm_labeled_dataset"]
    
    if not input_path.is_absolute():
        input_path = PROJECT_ROOT / input_path
    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path
    
    # ── Load dữ liệu ──
    logger.info(f"[Bước 3.1] Đọc dữ liệu: {input_path}")
    records = load_json_data(input_path)
    logger.info(f"  → {len(records):,} bản ghi")
    
    if args.limit:
        records = records[:args.limit]
        logger.info(f"  → Giới hạn test: {len(records)} bản ghi")
    
    # ── Resume logic ──
    processed_ids = set()
    existing_rows = []
    if args.resume and output_path.exists():
        df_existing = pd.read_excel(output_path, dtype=str)
        processed_ids = set(df_existing["source_id"].dropna().tolist())
        existing_rows = df_existing.to_dict("records")
        logger.info(f"  → Resume: đã có {len(processed_ids)} bản ghi, bỏ qua")
    
    # ── Load prompt và khởi tạo LLM ──
    logger.info("[Bước 3.2] Load prompt và khởi tạo LLM")
    system_prompt = load_prompt(cfg)
    client, model_name, gen_config, provider = init_llm(cfg)
    delay = float(os.getenv("LLM_DELAY_SECONDS", cfg["llm"].get("delay_seconds", 0.5)))
    n_workers = max(1, args.workers)

    # ── Hàm xử lý 1 bản ghi (dùng cho cả sequential và parallel) ──────────────
    # stop_event: khi có fatal error, set event để các worker khác dừng lại
    stop_event = Event()

    def process_one(rec: dict) -> dict:
        """Gọi LLM cho 1 bản ghi. Thread-safe.

        Lý do bắt KeyboardInterrupt riêng:
            Trong ThreadPoolExecutor, KeyboardInterrupt từ các hàm như time.sleep()
            sẽ bị bắt bởi `except Exception` nếu không xử lý riêng, làm mất tín hiệu dừng.
            Bắt nó rả và set stop_event để main thread xử lý chính xác hơn.
        """
        if stop_event.is_set():
            return None

        sid = str(rec.get("source_id", ""))
        record_input = format_record_for_prompt(rec)
        full_prompt = f"{system_prompt}\n\n{record_input}"

        row = {
            "source_id":              sid,
            "legal_citation":         rec.get("legal_citation", ""),
            "raw_text":               str(rec.get("raw_text", "")),
            "actor":                  str(rec.get("actor", "")),
            "env_llm":                None,
            "env_llm_reason":         "",
            "env_evidence_span":      "",
            "env_confidence":         None,
            "env_needs_human_review": None,
            "env_llm_domain":         "",
            "env_llm_error":          "",
            "env_llm_raw_response":   "",
        }
        try:
            raw_response = call_llm_with_retry(client, model_name, gen_config, full_prompt)
            parsed = parse_env_response(raw_response)
            row.update(parsed)
            row["env_llm_raw_response"] = raw_response[:500]
        except KeyboardInterrupt:
            stop_event.set()
            raise
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:200]}"
            logger.error(f"  ❌ Lỗi source_id={sid}: {error_msg}")
            if is_fatal_llm_config_error(e):
                stop_event.set()
            row["env_llm_error"] = error_msg

        try:
            if delay > 0:
                time.sleep(delay)
        except KeyboardInterrupt:
            stop_event.set()
            raise
        return row

    # ── Gọi LLM (sequential hoặc parallel) ────────────────────────────────────
    todo = [r for r in records if str(r.get("source_id", "")) not in processed_ids]
    logger.info(
        f"[Bước 3.3] Gọi LLM cho {len(todo)} bản ghi "
        f"({'song song ' + str(n_workers) + ' workers' if n_workers > 1 else 'tuần tự'})..."
    )
    results = list(existing_rows)
    results_lock = Lock()  # bảo vệ results khi append từ nhiều thread
    counter_lock = Lock()
    done_count = [0]  # dùng list để mutate trong closure
    order_index = {str(rec.get("source_id", "")): i for i, rec in enumerate(records)}

    def save_results_checkpoint(reason: str = "") -> pd.DataFrame:
        """Lưu kết quả hiện có để có thể chạy tiếp bằng --resume nếu bị ngắt."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with results_lock:  # snapshot an toàn
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
        # ── Sequential (mặc định, dễ debug) ───────────────────────────────────
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
        # ── Parallel với ThreadPoolExecutor ───────────────────────────────────
        # Lý do dùng Thread: bottleneck là I/O (HTTP), không phải CPU
        # results_lock đảm bảo thread-safe khi nhiều worker cùng append
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
                    continue  # lỗi từng bản ghi đã được xử lý trong process_one
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
            executor.shutdown(wait=False, cancel_futures=True)
            logger.warning("  Đã dừng theo yêu cầu. Chạy lại với --resume để tiếp tục.")
            sys.exit(130)
        finally:
            executor.shutdown(wait=False, cancel_futures=True)
        if stop_event.is_set():
            save_results_checkpoint("fatal error")
            logger.error("  Fatal error gặp phải, dừng pipeline. Sửa cấu hình và chạy lại với --resume.")
            sys.exit(1)
    
    # ── Lưu kết quả ──
    logger.info(f"[Bước 3.4] Lưu kết quả: {output_path}")
    df_result = save_results_checkpoint("final")
    
    # ── Thống kê ──
    n_success = int(df_result["env_llm"].notna().sum())
    n_error = int(df_result["env_llm_error"].astype(bool).sum())
    n_env1 = int((df_result["env_llm"] == 1).sum())
    n_env0 = int((df_result["env_llm"] == 0).sum())
    
    logger.info("")
    logger.info("=" * 60)
    logger.info(f"  HOÀN THÀNH — Kết quả env_llm:")
    logger.info(f"  Tổng bản ghi:   {len(df_result):,}")
    logger.info(f"  Thành công:     {n_success:,}")
    logger.info(f"  Lỗi:            {n_error:,}")
    logger.info(f"  env_llm = 1:    {n_env1:,} ({n_env1/max(n_success,1)*100:.1f}%)")
    logger.info(f"  env_llm = 0:    {n_env0:,} ({n_env0/max(n_success,1)*100:.1f}%)")
    logger.info(f"  Log:            {LOG_FILE}")
    logger.info(f"  Tiếp theo:      py src/04_compare_env_human_vs_llm.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

