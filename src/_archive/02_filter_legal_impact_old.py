#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_filter_legal_impact.py
==========================
BƯỚC 2 — Lọc các bản ghi có co_tac_dong = true (tác động pháp lý).

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản 5 nhãn
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:  data/raw/<raw_json_file>  (cấu hình trong config/project_config.yaml)
  Output: data/interim/legal_impact_records.xlsx

Quy tắc lọc:
  - Giữ lại record nếu co_tac_dong = true (hoặc impact = true)
  - Hỗ trợ các giá trị: True, "true", "True", "1", "yes", "có"

Sử dụng:
  python src/02_filter_legal_impact.py
  python src/02_filter_legal_impact.py --input data/raw/my_law.json
  python src/02_filter_legal_impact.py --help
"""

import argparse
import json
import logging
import sys
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


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json_data(json_path: Path) -> list:
    """Đọc file JSON pháp lý."""
    logger.info(f"Đọc dữ liệu JSON: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if isinstance(raw, list):
        return raw
    elif isinstance(raw, dict):
        for key in ("items", "data", "clauses", "records"):
            if key in raw and isinstance(raw[key], list):
                return raw[key]
        first_val = next(iter(raw.values()), None)
        if isinstance(first_val, list):
            return first_val
    raise ValueError(f"Không thể xác định cấu trúc dữ liệu JSON: {json_path}")


def normalize_record(item: dict, idx: int) -> dict:
    """
    Chuẩn hóa bản ghi JSON về schema thống nhất theo README mới.
    Alias: noi_dung_dieu_khoan → raw_text, tin_hieu_phap_ly → tin_hieu_tac_dong, v.v.
    """
    source_id = str(item.get("source_id", "")).strip() or f"gen_{idx}"

    # Lấy raw_text — ưu tiên raw_text, fallback noi_dung_dieu_khoan
    raw_text = (
        item.get("raw_text", "")
        or item.get("noi_dung_dieu_khoan", "")
        or ""
    )

    # Lấy tin_hieu_tac_dong — alias từ tin_hieu_phap_ly
    tin_hieu = (
        item.get("tin_hieu_tac_dong", "")
        or item.get("tin_hieu_phap_ly", "")
        or ""
    )

    # Lấy dieu_kien_ap_dung — alias từ dieu_kien
    dieu_kien = (
        item.get("dieu_kien_ap_dung", "")
        or item.get("dieu_kien", "")
        or ""
    )

    return {
        "source_id": source_id,
        "legal_citation": item.get("legal_citation", "Không rõ"),
        "raw_text": str(raw_text).strip(),
        "co_tac_dong": item.get("co_tac_dong", item.get("impact", False)),
        "chu_the": item.get("chu_the", None),
        "tin_hieu_tac_dong": str(tin_hieu).strip() or None,
        "domain": item.get("domain", None),
        "gia_tri_dinh_luong": item.get("gia_tri_dinh_luong", None),
        "dieu_kien_ap_dung": str(dieu_kien).strip() or None,
        "muc_do_ro_rang": item.get("muc_do_ro_rang", None),
        "ly_do": item.get("ly_do", None),
        "unit_index": item.get("unit_index", idx),
        "source_file": item.get("source_file", ""),
    }


def is_impact_true(record: dict, impact_fields: list) -> bool:
    """Kiểm tra cờ tác động pháp lý."""
    for field in impact_fields:
        val = record.get(field, None)
        if val is None:
            continue
        if str(val).strip().lower() in ("true", "1", "yes", "có"):
            return True
    return False


def export_to_excel(records: list, output_path: Path, sheet_name: str = "legal_impact_records"):
    """Xuất danh sách bản ghi ra Excel."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(records)

    priority_cols = [
        "source_id", "legal_citation", "raw_text", "co_tac_dong",
        "chu_the", "tin_hieu_tac_dong", "domain",
        "gia_tri_dinh_luong", "dieu_kien_ap_dung",
        "muc_do_ro_rang", "ly_do", "unit_index", "source_file",
    ]
    existing = [c for c in priority_cols if c in df.columns]
    other = [c for c in df.columns if c not in priority_cols]
    df = df[existing + other]

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        ws = writer.sheets[sheet_name]
        ws.column_dimensions["A"].width = 22   # source_id
        ws.column_dimensions["B"].width = 22   # legal_citation
        ws.column_dimensions["C"].width = 80   # raw_text
        ws.column_dimensions["D"].width = 14   # co_tac_dong
        ws.column_dimensions["F"].width = 45   # tin_hieu_tac_dong

    logger.info(f"Đã xuất {len(df)} bản ghi → {output_path}")
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Bước 2: Lọc bản ghi có co_tac_dong = true (tác động pháp lý)"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "config" / "project_config.yaml",
    )
    parser.add_argument("--input", type=Path, default=None,
                        help="File JSON đầu vào (ghi đè config)")
    parser.add_argument("--output", type=Path, default=None,
                        help="File Excel đầu ra (ghi đè config)")
    args = parser.parse_args()

    logger.info("=" * 65)
    logger.info("  BƯỚC 2: LỌC BẢN GHI CÓ co_tac_dong = true")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 65)

    config = load_config(args.config)

    json_path = args.input or (
        PROJECT_ROOT / config["paths"]["raw_data"] / config["input"]["raw_json_file"]
    )
    output_path = args.output or (
        PROJECT_ROOT / config["paths"]["interim_data"]
        / config["pipeline_outputs"]["legal_impact_records"]
    )
    impact_fields = config["input"].get("impact_flag_fields", ["co_tac_dong"])

    if not json_path.exists():
        logger.error(f"Không tìm thấy file JSON: {json_path}")
        logger.error("Chạy trước: python src/01_validate_input_schema.py")
        sys.exit(1)

    raw_data = load_json_data(json_path)
    logger.info(f"Tổng số records đọc được: {len(raw_data)}")

    # Chuẩn hóa tất cả records
    normalized = [normalize_record(item, idx) for idx, item in enumerate(raw_data)]

    # Lọc theo cờ tác động
    accepted = [r for r in normalized if is_impact_true(r, impact_fields)]
    rejected_count = len(normalized) - len(accepted)

    logger.info(f"  → Giữ lại (co_tac_dong=true): {len(accepted)}")
    logger.info(f"  → Loại bỏ (co_tac_dong=false): {rejected_count}")

    if not accepted:
        logger.warning("Không có bản ghi nào được giữ lại! Kiểm tra tên trường co_tac_dong.")
        sys.exit(0)

    export_to_excel(accepted, output_path)

    logger.info("")
    logger.info("✅ BƯỚC 2 HOÀN TẤT")
    logger.info(f"   Tỷ lệ giữ lại: {len(accepted)}/{len(normalized)} = {100*len(accepted)/len(normalized):.1f}%")
    logger.info(f"   File đầu ra: {output_path}")
    logger.info("")
    logger.info("   BƯỚC TIẾP THEO:")
    logger.info("   python src/03_filter_environmental_impact.py")


if __name__ == "__main__":
    main()
