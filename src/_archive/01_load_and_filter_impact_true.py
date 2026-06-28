#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_load_and_filter_impact_true.py
==================================
BƯỚC 1 — Đọc file JSON pháp lý và lọc các điều khoản có tác động (impact=true).

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản không tranh biện
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:  data/raw/<raw_json_file> (cấu hình trong config/project_config.yaml)
  Output:
    - data/interim/impact_true_records.xlsx  (điều khoản được lọc)

Sử dụng:
  python src/01_load_and_filter_impact_true.py
  python src/01_load_and_filter_impact_true.py --input data/raw/my_law.json
  python src/01_load_and_filter_impact_true.py --help
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

# ─── Đường dẫn gốc dự án ─────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ─── Cấu hình logging ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ─── Đảm bảo tiếng Việt hiển thị đúng trên Windows ──────────────────────────
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_config(config_path: Path) -> dict:
    """Đọc file cấu hình YAML."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json_data(json_path: Path) -> list:
    """
    Đọc file JSON pháp lý.
    Hỗ trợ cả định dạng: list gốc, dict có key 'items'/'data', hoặc dict values.
    """
    logger.info(f"Đọc dữ liệu JSON: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, list):
        return raw
    elif isinstance(raw, dict):
        # Thử các key phổ biến
        for key in ("items", "data", "clauses", "records"):
            if key in raw:
                logger.info(f"Phát hiện cấu trúc dict với key '{key}'")
                return raw[key]
        # Fallback: lấy value đầu tiên là list
        first_val = next(iter(raw.values()), None)
        if isinstance(first_val, list):
            return first_val
    raise ValueError(f"Không thể xác định cấu trúc dữ liệu JSON từ: {json_path}")


def normalize_record(item: dict, idx: int, doc_id: str, source_file: str) -> dict:
    """
    Chuẩn hóa một bản ghi JSON thành schema thống nhất.
    Sinh source_id duy nhất để truy vết.
    """
    raw_source_id = item.get("source_id", "")
    if not raw_source_id:
        raw_source_id = f"gen_{idx}"
    unique_source_id = f"{doc_id}_{raw_source_id}_{idx}"

    return {
        "source_id": unique_source_id,
        "document_id": doc_id,
        "source_file": source_file,
        "legal_citation": item.get("legal_citation", "Không rõ"),
        "noi_dung_dieu_khoan": item.get("noi_dung_dieu_khoan", ""),
        "chu_the": item.get("chu_the", None),
        "loai_phap_ly": item.get("loai_phap_ly", None),
        "tin_hieu_phap_ly": item.get("tin_hieu_phap_ly", None),
        "doi_tuong": item.get("doi_tuong", None),
        "dieu_kien": item.get("dieu_kien", None),
        "gia_tri_dinh_luong": item.get("gia_tri_dinh_luong", None),
        "co_tac_dong_original": item.get("co_tac_dong", item.get("impact", False)),
        "matched_keywords": "",
        "filter_reason": "",
    }


def check_impact_flag(record: dict, impact_fields: list) -> bool:
    """
    Kiểm tra xem bản ghi có cờ tác động không.
    Hỗ trợ nhiều tên trường khác nhau (co_tac_dong, impact, ...).
    """
    val = record.get("co_tac_dong_original", False)
    return str(val).strip().lower() in ("true", "1", "yes", "có")


def check_keyword_match(record: dict, keywords: list) -> list:
    """
    Kiểm tra khớp từ khóa môi trường trên nhiều trường văn bản.
    Trả về danh sách từ khóa khớp được.
    """
    text_parts = [
        str(record.get("noi_dung_dieu_khoan", "") or ""),
        str(record.get("chu_the", "") or ""),
        str(record.get("doi_tuong", "") or ""),
        str(record.get("dieu_kien", "") or ""),
        str(record.get("tin_hieu_phap_ly", "") or ""),
        str(record.get("legal_citation", "") or ""),
    ]
    search_space = " | ".join(text_parts).lower()
    return [kw for kw in keywords if kw in search_space]


def filter_impact_records(
    records: list, impact_fields: list, env_keywords: list
) -> tuple:
    """
    Lọc danh sách bản ghi theo 2 tầng:
      Tầng 1: Boolean flag (co_tac_dong=True)
      Tầng 2: Semantic filter (khớp từ khóa môi trường)

    Returns:
        (accepted, rejected)
    """
    accepted = []
    rejected = []

    for record in records:
        # Tầng 1: Boolean filter
        if not check_impact_flag(record, impact_fields):
            record["filter_reason"] = "co_tac_dong=FALSE — không có tác động pháp lý"
            rejected.append(record)
            continue

        # Tầng 2: Keyword filter
        matched_kws = check_keyword_match(record, env_keywords)
        if matched_kws:
            record["matched_keywords"] = ", ".join(matched_kws)
            record["filter_reason"] = f"Giữ lại: co_tac_dong=TRUE, khớp từ khóa: {', '.join(matched_kws[:3])}"
            accepted.append(record)
        else:
            record["filter_reason"] = "Bị loại: co_tac_dong=TRUE nhưng không khớp từ khóa môi trường/năng lượng"
            rejected.append(record)

    return accepted, rejected


def export_to_excel(records: list, output_path: Path, sheet_name: str = "Sheet1"):
    """Xuất danh sách bản ghi ra file Excel với định dạng cơ bản."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(records)

    # Sắp xếp cột theo thứ tự ưu tiên
    priority_cols = [
        "source_id", "legal_citation", "noi_dung_dieu_khoan",
        "co_tac_dong_original", "matched_keywords", "filter_reason",
        "chu_the", "loai_phap_ly", "tin_hieu_phap_ly",
        "doi_tuong", "dieu_kien", "gia_tri_dinh_luong",
        "document_id", "source_file",
    ]
    existing_cols = [c for c in priority_cols if c in df.columns]
    other_cols = [c for c in df.columns if c not in priority_cols]
    df = df[existing_cols + other_cols]

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        ws = writer.sheets[sheet_name]
        # Điều chỉnh độ rộng cột chính
        ws.column_dimensions["A"].width = 30   # source_id
        ws.column_dimensions["B"].width = 22   # legal_citation
        ws.column_dimensions["C"].width = 80   # noi_dung_dieu_khoan
        ws.column_dimensions["E"].width = 30   # matched_keywords
        ws.column_dimensions["F"].width = 50   # filter_reason

    logger.info(f"Đã xuất {len(df)} bản ghi → {output_path}")
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Bước 1: Lọc điều khoản pháp lý có tác động môi trường (impact=true)"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "config" / "project_config.yaml",
        help="Đường dẫn file cấu hình YAML (mặc định: config/project_config.yaml)",
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
        help="Đường dẫn file Excel đầu ra (ghi đè cấu hình)",
    )
    args = parser.parse_args()

    # ── Đọc cấu hình ──────────────────────────────────────────────────────────
    logger.info(f"{'='*65}")
    logger.info(f"  BƯỚC 1: LỌC ĐIỀU KHOẢN impact=true")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*65}")

    config = load_config(args.config)

    # Đường dẫn file JSON
    if args.input:
        json_path = args.input
    else:
        raw_dir = PROJECT_ROOT / config["paths"]["raw_data"]
        json_path = raw_dir / config["input"]["raw_json_file"]

    # Đường dẫn file Excel đầu ra
    if args.output:
        output_path = args.output
    else:
        interim_dir = PROJECT_ROOT / config["paths"]["interim_data"]
        output_path = interim_dir / config["interim_files"]["impact_true_records"]

    # Từ khóa và trường flag
    env_keywords = config.get("environment_keywords", [])
    impact_fields = config["input"].get("impact_flag_fields", ["co_tac_dong"])

    # ── Kiểm tra file đầu vào ─────────────────────────────────────────────────
    if not json_path.exists():
        logger.error(f"Không tìm thấy file JSON: {json_path}")
        logger.error(f"Vui lòng đặt file JSON vào: {json_path.parent}/")
        sys.exit(1)

    # ── Đọc và chuẩn hóa dữ liệu ─────────────────────────────────────────────
    raw_data = load_json_data(json_path)
    logger.info(f"Tổng số bản ghi đọc được: {len(raw_data)}")

    doc_id = json_path.stem
    source_file = json_path.name

    normalized = [normalize_record(item, idx, doc_id, source_file) for idx, item in enumerate(raw_data)]
    logger.info(f"Chuẩn hóa xong: {len(normalized)} bản ghi")

    # ── Lọc ──────────────────────────────────────────────────────────────────
    accepted, rejected = filter_impact_records(normalized, impact_fields, env_keywords)

    logger.info(f"Kết quả lọc:")
    logger.info(f"  → Giữ lại (impact=true + khớp từ khóa): {len(accepted)}")
    logger.info(f"  → Loại bỏ: {len(rejected)}")

    if not accepted:
        logger.warning("Không có bản ghi nào được giữ lại. Kiểm tra lại cấu hình từ khóa và tên trường flag.")
        sys.exit(0)

    # ── Xuất kết quả ─────────────────────────────────────────────────────────
    df = export_to_excel(accepted, output_path, sheet_name="impact_true_records")

    logger.info(f"")
    logger.info(f"✅ BƯỚC 1 HOÀN TẤT")
    logger.info(f"   Số điều khoản có tác động: {len(accepted)}/{len(normalized)}")
    logger.info(f"   File đầu ra: {output_path}")
    logger.info(f"")
    logger.info(f"   BƯỚC TIẾP THEO:")
    logger.info(f"   python src/02_build_manual_label_file.py")


if __name__ == "__main__":
    main()
