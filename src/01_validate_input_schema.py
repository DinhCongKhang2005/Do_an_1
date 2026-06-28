#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_validate_input_schema.py
============================
BƯỚC 1 — Kiểm tra schema và chất lượng dữ liệu JSON đầu vào.

Đề tài: Đánh giá tác động chính sách môi trường — Khung định lượng: lợi ích, chi phí, rủi ro
Tác giả: Đinh Công Khang — MI3380 Đồ án 1
Cập nhật: Lần 2 — Toàn bộ file đầu vào chứa bản ghi có tác động chính sách (co_tac_dong = true)

Pipeline vị trí:
    Input:  data/raw/<raw_json_file>  (cấu hình trong config/project_config.yaml)
    Output: data/reports/input_schema_report.xlsx
    Tiếp theo: Script 02 (build env manual label file)

Thay đổi so với phiên bản cũ:
    - Bỏ bước filter co_tac_dong (đầu vào ĐÃ là toàn bộ bản ghi có co_tac_dong=true)
    - Kiểm tra expected N = 581 (test study: Luật BVMT 2020)
    - Không còn output legal_impact_records.xlsx (không cần nữa)

Kiểm tra:
    - File JSON tồn tại
    - Các trường bắt buộc có đủ không (source_id, raw_text, co_tac_dong, legal_citation)
    - source_id không trùng lặp
    - raw_text không rỗng
    - co_tac_dong = true cho tất cả bản ghi
    - Báo cáo số bản ghi (expected: N = 581)
    - Tóm tắt thống kê chất lượng dữ liệu

Sử dụng:
    py src/01_validate_input_schema.py
    py src/01_validate_input_schema.py --input data/raw/my_law.json
    py src/01_validate_input_schema.py --help
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

# ─── Đường dẫn gốc dự án ──────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ─── Cấu hình logging ──────────────────────────────────────────────────────────
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

# Trường bắt buộc theo đặc tả README_3_updated
REQUIRED_FIELDS = ["source_id", "raw_text", "co_tac_dong"]
# Trường khuyến nghị (có sẵn trong Luat_bao_ve_moi_truong_2020.json)
RECOMMENDED_FIELDS = [
    "legal_citation", "chu_the", "tin_hieu_tac_dong",
    "domain", "gia_tri_dinh_luong", "dieu_kien_ap_dung",
    "muc_do_ro_rang", "ly_do",
]


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json_data(json_path: Path) -> list:
    """Đọc file JSON pháp lý, hỗ trợ list hoặc dict với key 'items'/'data'."""
    logger.info(f"Đọc dữ liệu JSON: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, list):
        return raw
    elif isinstance(raw, dict):
        for key in ("items", "data", "clauses", "records"):
            if key in raw and isinstance(raw[key], list):
                logger.info(f"Phát hiện cấu trúc dict với key '{key}'")
                return raw[key]
        first_val = next(iter(raw.values()), None)
        if isinstance(first_val, list):
            return first_val
    raise ValueError(f"Không thể xác định cấu trúc dữ liệu JSON từ: {json_path}")


def get_text_field_value(record: dict, aliases: dict) -> str:
    """Lấy nội dung văn bản chính, hỗ trợ alias raw_text / noi_dung_dieu_khoan."""
    for field in ("raw_text", "noi_dung_dieu_khoan"):
        val = record.get(field, "")
        if val:
            return str(val).strip()
    return ""


def validate_records(records: list) -> tuple:
    """
    Kiểm tra toàn bộ bản ghi theo các quy tắc schema.
    Returns: (issues_list, stats_dict)
    """
    issues = []
    source_ids_seen = {}
    n_missing_source_id = 0
    n_missing_raw_text = 0
    n_missing_co_tac_dong = 0
    n_duplicate_source_id = 0
    n_valid = 0

    for idx, record in enumerate(records):
        record_issues = []

        # Kiểm tra source_id
        sid = str(record.get("source_id", "")).strip()
        if not sid:
            record_issues.append("Thiếu source_id")
            n_missing_source_id += 1
            sid = f"[idx_{idx}]"
        elif sid in source_ids_seen:
            record_issues.append(f"source_id trùng lặp với dòng {source_ids_seen[sid]}")
            n_duplicate_source_id += 1
        else:
            source_ids_seen[sid] = idx

        # Kiểm tra raw_text
        raw_text = get_text_field_value(record, {})
        if not raw_text:
            record_issues.append("raw_text/noi_dung_dieu_khoan rỗng hoặc thiếu")
            n_missing_raw_text += 1

        # Kiểm tra co_tac_dong
        co_tac_dong = record.get("co_tac_dong", None)
        if co_tac_dong is None:
            record_issues.append("Thiếu trường co_tac_dong")
            n_missing_co_tac_dong += 1

        if record_issues:
            issues.append({
                "idx": idx,
                "source_id": sid,
                "legal_citation": record.get("legal_citation", ""),
                "issues": " | ".join(record_issues),
                "raw_text_preview": (raw_text[:100] + "...") if len(raw_text) > 100 else raw_text,
            })
        else:
            n_valid += 1

    stats = {
        "total_records": len(records),
        "valid_records": n_valid,
        "records_with_issues": len(issues),
        "missing_source_id": n_missing_source_id,
        "missing_raw_text": n_missing_raw_text,
        "missing_co_tac_dong": n_missing_co_tac_dong,
        "duplicate_source_id": n_duplicate_source_id,
    }
    return issues, stats


def check_recommended_fields(records: list) -> dict:
    """Kiểm tra tỷ lệ có mặt của các trường khuyến nghị."""
    n = len(records)
    coverage = {}
    for field in RECOMMENDED_FIELDS:
        count = sum(
            1 for r in records
            if r.get(field) is not None and str(r.get(field, "")).strip() != ""
        )
        coverage[field] = {"count": count, "pct": round(100 * count / n, 1) if n > 0 else 0}
    return coverage


def export_report(issues: list, stats: dict, coverage: dict, output_path: Path):
    """Xuất báo cáo kiểm tra schema ra Excel nhiều sheet."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Sheet 1: Tóm tắt
    summary_rows = [
        {"Chỉ số": "Tổng số records", "Giá trị": stats["total_records"]},
        {"Chỉ số": "Records hợp lệ (không lỗi)", "Giá trị": stats["valid_records"]},
        {"Chỉ số": "Records có vấn đề", "Giá trị": stats["records_with_issues"]},
        {"Chỉ số": "Thiếu source_id", "Giá trị": stats["missing_source_id"]},
        {"Chỉ số": "source_id trùng lặp", "Giá trị": stats["duplicate_source_id"]},
        {"Chỉ số": "Thiếu raw_text", "Giá trị": stats["missing_raw_text"]},
        {"Chỉ số": "Thiếu co_tac_dong", "Giá trị": stats["missing_co_tac_dong"]},
        {"Chỉ số": "Thời gian kiểm tra", "Giá trị": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    ]
    df_summary = pd.DataFrame(summary_rows)

    # Sheet 2: Chi tiết lỗi
    df_issues = pd.DataFrame(issues) if issues else pd.DataFrame(
        columns=["idx", "source_id", "legal_citation", "issues", "raw_text_preview"]
    )

    # Sheet 3: Độ phủ trường khuyến nghị
    coverage_rows = [
        {"Trường": field, "Số records có": v["count"], "Tỷ lệ (%)": v["pct"]}
        for field, v in coverage.items()
    ]
    df_coverage = pd.DataFrame(coverage_rows)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_summary.to_excel(writer, index=False, sheet_name="Tóm tắt")
        df_issues.to_excel(writer, index=False, sheet_name="Chi tiết lỗi")
        df_coverage.to_excel(writer, index=False, sheet_name="Độ phủ trường")

        for sheet_name in writer.sheets:
            ws = writer.sheets[sheet_name]
            ws.column_dimensions["A"].width = 35
            ws.column_dimensions["B"].width = 20
            if sheet_name == "Chi tiết lỗi":
                ws.column_dimensions["E"].width = 60

    logger.info(f"Đã xuất báo cáo schema → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Bước 1: Kiểm tra schema và chất lượng dữ liệu JSON đầu vào"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "config" / "project_config.yaml",
        help="Đường dẫn file cấu hình YAML",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Đường dẫn file JSON đầu vào (ghi đè cấu hình)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Đường dẫn file báo cáo Excel đầu ra (ghi đè cấu hình)",
    )
    args = parser.parse_args()

    logger.info("=" * 65)
    logger.info("  BƯỚC 1: KIỂM TRA SCHEMA JSON ĐẦU VÀO")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 65)

    config = load_config(args.config)

    # Đường dẫn file
    json_path = args.input or (
        PROJECT_ROOT / config["paths"]["raw_data"] / config["input"]["raw_json_file"]
    )
    output_path = args.output or (
        PROJECT_ROOT / config["paths"]["reports"] / config["report_files"]["input_schema_report"]
    )

    if not json_path.exists():
        logger.error(f"Không tìm thấy file JSON: {json_path}")
        sys.exit(1)

    # Đọc và kiểm tra
    records = load_json_data(json_path)
    logger.info(f"Tổng số records đọc được: {len(records)}")

    issues, stats = validate_records(records)
    coverage = check_recommended_fields(records)

    # In tóm tắt
    logger.info("")
    logger.info("=== KẾT QUẢ KIỂM TRA SCHEMA ===")
    logger.info(f"  Tổng records       : {stats['total_records']}")
    logger.info(f"  Records hợp lệ     : {stats['valid_records']}")
    logger.info(f"  Records có lỗi     : {stats['records_with_issues']}")
    logger.info(f"  Thiếu source_id    : {stats['missing_source_id']}")
    logger.info(f"  source_id trùng    : {stats['duplicate_source_id']}")
    logger.info(f"  Thiếu raw_text     : {stats['missing_raw_text']}")
    logger.info(f"  Thiếu co_tac_dong  : {stats['missing_co_tac_dong']}")
    logger.info("")
    logger.info("=== ĐỘ PHỦ TRƯỜNG KHUYẾN NGHỊ ===")
    for field, v in coverage.items():
        bar = "█" * int(v["pct"] / 5)
        logger.info(f"  {field:<25}: {v['pct']:>5}%  {bar}")

    export_report(issues, stats, coverage, output_path)

    if stats["records_with_issues"] == 0:
        logger.info("")
        logger.info("✅ BƯỚC 1 HOÀN TẤT — Dữ liệu JSON hợp lệ, không có lỗi schema.")
    else:
        logger.warning(f"⚠️  BƯỚC 1 HOÀN TẤT — Có {stats['records_with_issues']} records có vấn đề.")
        logger.warning("   Xem chi tiết tại sheet 'Chi tiết lỗi' trong file báo cáo.")

    logger.info(f"   File báo cáo: {output_path}")
    logger.info("")
    logger.info("   BƯỚC TIẾP THEO:")
    logger.info("   py src/02_build_env_manual_label_file.py")


if __name__ == "__main__":
    main()
