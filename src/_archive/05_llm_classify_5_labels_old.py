#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_llm_classify_5_labels.py
============================
BƯỚC 6 — Gọi LLM phân loại 5 nhãn cho từng điều khoản pháp lý.

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản 5 nhãn
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:  data/interim/human_labeled_dataset.xlsx  (ưu tiên nếu có)
          data/interim/environmental_impact_records.xlsx  (fallback)
  Output: data/processed/llm_labeled_dataset.xlsx

Schema JSON trả về từ LLM (7 trường):
  label, reason, evidence_span, confidence,
  needs_human_review, rule_applied, quantity_interpretation

Sử dụng:
  python src/05_llm_classify_5_labels.py
  python src/05_llm_classify_5_labels.py --dry-run  (không gọi API)
  python src/05_llm_classify_5_labels.py --input data/interim/human_labeled_dataset.xlsx
  python src/05_llm_classify_5_labels.py --help
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

# ─── Nhãn hợp lệ 5 lớp ────────────────────────────────────────────────────────
VALID_LABELS_5 = {
    "BENEFIT_QUANTITATIVE",
    "BENEFIT_QUALITATIVE",
    "COST_QUANTITATIVE",
    "COST_QUALITATIVE",
    "CONSTRAINT",
}


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_system_prompt(prompt_path: Path) -> str:
    """Đọc file system prompt cho LLM."""
    if not prompt_path.exists():
        logger.warning(f"Không tìm thấy prompt: {prompt_path} — dùng prompt dự phòng")
        return (
            "Phân loại điều khoản pháp lý môi trường vào đúng một trong 5 nhãn: "
            "BENEFIT_QUANTITATIVE, BENEFIT_QUALITATIVE, COST_QUANTITATIVE, "
            "COST_QUALITATIVE, CONSTRAINT. "
            'Trả về JSON: {"label": "...", "reason": "...", "evidence_span": "...", '
            '"confidence": 0.0, "needs_human_review": false, '
            '"rule_applied": "...", "quantity_interpretation": "none"}'
        )
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def init_llm_client(provider: str):
    """Khởi tạo LLM client: google_ai_studio hoặc vertex_ai."""
    if provider == "google_ai_studio":
        try:
            import google.generativeai as genai
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Thiếu GOOGLE_API_KEY trong file .env")
            genai.configure(api_key=api_key)
            return ("google_ai_studio", genai)
        except ImportError:
            raise ImportError("pip install google-generativeai")

    elif provider == "vertex_ai":
        try:
            from google import genai as vertex_genai
            project = os.environ.get("GOOGLE_CLOUD_PROJECT")
            location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
            if not project:
                raise ValueError("Thiếu GOOGLE_CLOUD_PROJECT trong file .env")
            client = vertex_genai.Client(vertexai=True, project=project, location=location)
            return ("vertex_ai", client)
        except ImportError:
            raise ImportError("pip install google-cloud-aiplatform")

    raise ValueError(f"Provider không hợp lệ: {provider}")


def call_llm(text: str, system_prompt: str, client_info: tuple, model_name: str) -> dict:
    """Gọi một LLM duy nhất để phân loại 5 nhãn."""
    provider, client = client_info
    user_prompt = (
        f"Hãy phân loại điều khoản pháp lý môi trường sau:\n\n"
        f"{text}\n\n"
        f"Trả về JSON hợp lệ theo đúng schema trong system prompt."
    )

    if provider == "google_ai_studio":
        import google.generativeai as genai
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.0,
                response_mime_type="application/json",
            ),
        )
        response = model.generate_content(user_prompt)
        raw = response.text.strip()

    elif provider == "vertex_ai":
        from google.genai import types
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.0,
                response_mime_type="application/json",
            ),
        )
        raw = response.text.strip()
    else:
        raise ValueError(f"Provider không hợp lệ: {provider}")

    # Làm sạch markdown code block nếu có
    for prefix in ("```json", "```"):
        if raw.startswith(prefix):
            raw = raw[len(prefix):]
    if raw.endswith("```"):
        raw = raw[:-3]

    return json.loads(raw.strip())


def normalize_label_5(raw_label: str) -> str:
    """Chuẩn hóa nhãn trả về từ LLM về một trong 5 nhãn hợp lệ."""
    if not raw_label:
        return "UNKNOWN"
    upper = raw_label.strip().upper().replace(" ", "_")
    if upper in VALID_LABELS_5:
        return upper
    # Khớp từng phần
    for valid in VALID_LABELS_5:
        if valid in upper or upper in valid:
            return valid
    # Fallback tiếng Việt
    lower = raw_label.strip().lower()
    if any(k in lower for k in ["lợi ích", "benefit", "tích cực", "hỗ trợ"]):
        if any(k in lower for k in ["định lượng", "quantitative", "số", "tiền", "tỷ lệ"]):
            return "BENEFIT_QUANTITATIVE"
        return "BENEFIT_QUALITATIVE"
    if any(k in lower for k in ["chi phí", "cost", "gánh nặng", "phí", "nghĩa vụ"]):
        if any(k in lower for k in ["định lượng", "quantitative", "số tiền", "tỷ lệ"]):
            return "COST_QUANTITATIVE"
        return "COST_QUALITATIVE"
    if any(k in lower for k in ["ràng buộc", "constraint", "ngưỡng", "giới hạn", "cấm", "điều kiện"]):
        return "CONSTRAINT"
    return "UNKNOWN"


def classify_dataframe(
    df: pd.DataFrame,
    system_prompt: str,
    client_info: tuple,
    model_name: str,
    text_field: str,
    delay_seconds: float = 0.5,
    dry_run: bool = False,
) -> pd.DataFrame:
    """Phân loại toàn bộ DataFrame bằng LLM đơn (không debate)."""
    # Reset index để đảm bảo enumerate cho số thứ tự đúng
    df = df.reset_index(drop=True)
    total = len(df)
    logger.info(f"Bắt đầu phân loại {total} bản ghi | model={model_name} | text_field={text_field}")
    logger.info(f"Chế độ: {'DRY RUN — không gọi API' if dry_run else 'THỰC TẾ — gọi Gemini API'}")

    # Kiểm tra text_field có tồn tại không
    if text_field not in df.columns:
        available = [c for c in df.columns if "text" in c.lower() or "noi_dung" in c.lower()]
        fallback = available[0] if available else None
        if fallback:
            logger.warning(f"Cột '{text_field}' không có trong file — dùng fallback '{fallback}'")
            text_field = fallback
        else:
            logger.error(f"Không tìm thấy cột văn bản phù hợp. Các cột có: {list(df.columns)}")
            raise ValueError(f"text_field '{text_field}' không tồn tại")

    results = {
        "llm_label": [],
        "llm_reason": [],
        "llm_evidence_span": [],
        "llm_confidence": [],
        "llm_needs_human_review": [],
        "llm_rule_applied": [],
        "llm_quantity_interpretation": [],
        "llm_error": [],
    }

    # Dùng enumerate để có số thứ tự sequential đúng (1, 2, 3...)
    for seq_idx, (_, row) in enumerate(df.iterrows(), start=1):
        source_id = str(row.get("source_id", f"idx_{seq_idx}"))
        text = str(row.get(text_field, "") or "").strip()

        print(f"  [{seq_idx:>4}/{total}] {source_id[:30]:<30} ", end="", flush=True)

        if dry_run:
            results["llm_label"].append("BENEFIT_QUALITATIVE")
            results["llm_reason"].append("[DRY RUN] Không gọi API")
            results["llm_evidence_span"].append("")
            results["llm_confidence"].append(0.0)
            results["llm_needs_human_review"].append(False)
            results["llm_rule_applied"].append("DRY_RUN")
            results["llm_quantity_interpretation"].append("none")
            results["llm_error"].append("")
            print("→ [DRY RUN]")
            continue

        if not text:
            results["llm_label"].append("UNKNOWN")
            results["llm_reason"].append("Văn bản trống")
            results["llm_evidence_span"].append("")
            results["llm_confidence"].append(0.0)
            results["llm_needs_human_review"].append(True)
            results["llm_rule_applied"].append("")
            results["llm_quantity_interpretation"].append("none")
            results["llm_error"].append("empty_text")
            print("→ ⚠️  Văn bản trống")
            continue

        try:
            # Retry tối đa 3 lần nếu lỗi tạm thời (quota, network)
            last_err = None
            result = None
            for attempt in range(3):
                try:
                    result = call_llm(text, system_prompt, client_info, model_name)
                    break
                except json.JSONDecodeError as e:
                    last_err = e
                    break  # JSON lỗi → không retry
                except Exception as e:
                    last_err = e
                    err_str = str(e).lower()
                    # Chỉ retry nếu là lỗi quota/network (không retry lỗi auth)
                    if any(k in err_str for k in ("quota", "rate", "timeout", "unavailable", "503", "429")):
                        wait = delay_seconds * (2 ** attempt)
                        logger.warning(f"Thử lại {attempt+1}/3 sau {wait:.1f}s: {str(e)[:60]}")
                        time.sleep(wait)
                    else:
                        break  # Lỗi không thể retry

            if result is None:
                raise last_err if last_err is not None else RuntimeError("Không có kết quả từ LLM sau 3 lần thử")

            raw_label = result.get("label", "UNKNOWN")
            normalized = normalize_label_5(raw_label)
            confidence = float(result.get("confidence", 0.5))
            needs_review = bool(result.get("needs_human_review", False))

            results["llm_label"].append(normalized)
            results["llm_reason"].append(result.get("reason", ""))
            results["llm_evidence_span"].append(result.get("evidence_span", ""))
            results["llm_confidence"].append(confidence)
            results["llm_needs_human_review"].append(needs_review)
            results["llm_rule_applied"].append(result.get("rule_applied", ""))
            results["llm_quantity_interpretation"].append(
                result.get("quantity_interpretation", "none")
            )
            results["llm_error"].append("")

            flag = "⚠️ " if confidence < 0.7 or needs_review else "✅"
            review_note = " [review]" if needs_review else ""
            print(f"→ {flag} {normalized} (conf={confidence:.2f}){review_note}")

        except json.JSONDecodeError as e:
            err = f"JSON parse error: {str(e)[:80]}"
            logger.error(f"Lỗi JSON dòng {seq_idx}: {err}")
            _append_error(results, "PARSE_ERROR", err, "json_parse_error")
            print("→ ❌ JSON Error")

        except Exception as e:
            err = str(e)[:120]
            logger.error(f"Lỗi API dòng {seq_idx}: {err}")
            _append_error(results, "API_ERROR", f"Lỗi API: {err}", "api_error")
            print(f"→ ❌ API Error: {err[:40]}")

        time.sleep(delay_seconds)

    df_result = df.copy()
    for col, vals in results.items():
        df_result[col] = vals

    return df_result


def _append_error(results: dict, label: str, reason: str, error_type: str):
    results["llm_label"].append(label)
    results["llm_reason"].append(reason)
    results["llm_evidence_span"].append("")
    results["llm_confidence"].append(0.0)
    results["llm_needs_human_review"].append(True)
    results["llm_rule_applied"].append("")
    results["llm_quantity_interpretation"].append("none")
    results["llm_error"].append(error_type)


def print_summary(df: pd.DataFrame):
    """In thống kê phân phối nhãn LLM."""
    logger.info(f"\n{'='*55}")
    logger.info("  THỐNG KÊ NHÃN LLM (5 NHÃN)")
    logger.info(f"{'='*55}")
    counts = df["llm_label"].value_counts()
    for label, count in counts.items():
        bar = "█" * min(count, 30)
        logger.info(f"  {label:<25}: {count:>4}  {bar}")
    errors = (df["llm_error"] != "").sum()
    needs_review = df["llm_needs_human_review"].sum() if "llm_needs_human_review" in df.columns else 0
    if errors > 0:
        logger.warning(f"  {'LỖI':<25}: {errors:>4}  *** Cần kiểm tra ***")
    if needs_review > 0:
        logger.info(f"  {'Cần review thủ công':<25}: {needs_review:>4}")
    logger.info(f"{'='*55}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Bước 6: Phân loại 5 nhãn bằng LLM đơn (không debate)"
    )
    parser.add_argument(
        "--config", type=Path,
        default=PROJECT_ROOT / "config" / "project_config.yaml",
    )
    parser.add_argument("--input", type=Path, default=None,
                        help="File Excel đầu vào")
    parser.add_argument("--output", type=Path, default=None,
                        help="File Excel đầu ra")
    parser.add_argument("--dry-run", action="store_true",
                        help="Chạy thử không gọi API")
    args = parser.parse_args()

    logger.info("=" * 65)
    logger.info("  BƯỚC 6: PHÂN LOẠI 5 NHÃN BẰNG LLM ĐƠN (KHÔNG DEBATE)")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 65)

    config = load_config(args.config)
    interim_dir = PROJECT_ROOT / config["paths"]["interim_data"]
    processed_dir = PROJECT_ROOT / config["paths"]["processed_data"]

    # Ưu tiên dùng human_labeled_dataset để source_id khớp khi so sánh
    human_file = interim_dir / config["interim_files"]["human_labeled_dataset"]
    env_file = interim_dir / config["pipeline_outputs"]["environmental_impact_records"]

    if args.input:
        input_path = args.input
    elif human_file.exists():
        input_path = human_file
        logger.info(f"Dùng file đã gán nhãn người: {input_path}")
    else:
        input_path = env_file
        logger.info(f"Dùng file lọc môi trường (chưa có nhãn người): {input_path}")

    output_path = args.output or (
        processed_dir / config["processed_files"]["llm_labeled_dataset"]
    )

    model_name = os.environ.get("LLM_MODEL_NAME") or config["llm"].get("model", "gemini-2.5-flash")
    temperature = float(os.environ.get("LLM_TEMPERATURE") or config["llm"].get("temperature") or 0.0)
    delay_seconds = float(os.environ.get("LLM_DELAY_SECONDS") or config["llm"].get("delay_seconds") or 0.5)
    text_field = config["input"].get("text_field", "raw_text")
    provider = os.environ.get("LLM_PROVIDER", "google_ai_studio")
    prompt_path = PROJECT_ROOT / config["paths"]["prompts"] / "classify_system_prompt.txt"

    if not input_path.exists():
        logger.error(f"Không tìm thấy file đầu vào: {input_path}")
        sys.exit(1)

    df = pd.read_excel(input_path)
    logger.info(f"Đọc được {len(df)} bản ghi từ: {input_path}")

    system_prompt = load_system_prompt(prompt_path)
    logger.info(f"Đã nạp system prompt ({len(system_prompt)} ký tự)")

    client_info = None
    if not args.dry_run:
        try:
            client_info = init_llm_client(provider)
            logger.info(f"Đã khởi tạo LLM (provider={provider}, model={model_name})")
        except Exception as e:
            logger.error(f"Lỗi khởi tạo LLM: {e}")
            sys.exit(1)
    else:
        client_info = ("dry_run", None)

    df_result = classify_dataframe(
        df=df,
        system_prompt=system_prompt,
        client_info=client_info,
        model_name=model_name,
        text_field=text_field,
        delay_seconds=delay_seconds,
        dry_run=args.dry_run,
    )

    # Xuất kết quả
    output_path.parent.mkdir(parents=True, exist_ok=True)
    from openpyxl.utils import get_column_letter
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_result.to_excel(writer, index=False, sheet_name="llm_labeled")
        ws = writer.sheets["llm_labeled"]
        for col_idx, col_name in enumerate(df_result.columns, start=1):
            col_letter = get_column_letter(col_idx)
            if col_name == "raw_text":
                ws.column_dimensions[col_letter].width = 80
            elif col_name == "llm_label":
                ws.column_dimensions[col_letter].width = 25
            elif col_name in ("llm_reason", "llm_evidence_span"):
                ws.column_dimensions[col_letter].width = 55
            elif col_name == "source_id":
                ws.column_dimensions[col_letter].width = 25

    print_summary(df_result)
    logger.info("✅ BƯỚC 6 HOÀN TẤT")
    logger.info(f"   File kết quả LLM: {output_path}")
    logger.info("")
    logger.info("   BƯỚC TIẾP THEO:")
    logger.info("   python src/06_compare_llm_vs_human.py")


if __name__ == "__main__":
    main()
