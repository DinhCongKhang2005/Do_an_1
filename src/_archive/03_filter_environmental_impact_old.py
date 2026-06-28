#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_filter_environmental_impact.py
===================================
BƯỚC 3 — Lọc bản ghi có tác động môi trường từ tập legal_impact_records.

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản 5 nhãn
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:  data/interim/legal_impact_records.xlsx  (output của Bước 2)
  Output:
    - data/interim/environmental_impact_records.xlsx  (giữ lại)
    - Thống kê về từ khóa khớp được

Cơ chế lọc (2 tầng):
  Tầng 1 (từ khóa môi trường): Lọc theo environment_keywords trong config
          trên các trường raw_text và tin_hieu_tac_dong
  Tầng 2 (xem xét thủ công): record có muc_do_ro_rang = "ro_rang" được ưu tiên

Lưu ý về trường 'domain':
  File Luat_bao_ve_moi_truong_2020.json có domain = 'general_environment' cho
  tất cả records. Thông tin domain thực sự nằm trong tin_hieu_tac_dong.
  Script này lọc chủ yếu dựa trên raw_text và tin_hieu_tac_dong.

Sử dụng:
  python src/03_filter_environmental_impact.py
  python src/03_filter_environmental_impact.py --input data/interim/legal_impact_records.xlsx
  python src/03_filter_environmental_impact.py --help
"""

import argparse
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


def build_search_text(row: pd.Series) -> str:
    """Xây dựng chuỗi tìm kiếm từ nhiều trường văn bản."""
    parts = [
        str(row.get("raw_text", "") or ""),
        str(row.get("tin_hieu_tac_dong", "") or ""),
        str(row.get("chu_the", "") or ""),
        str(row.get("dieu_kien_ap_dung", "") or ""),
        str(row.get("legal_citation", "") or ""),
        str(row.get("ly_do", "") or ""),
    ]
    return " | ".join(parts).lower()


def match_keywords(search_text: str, keywords: list) -> list:
    """Trả về danh sách từ khóa khớp được."""
    return [kw for kw in keywords if kw.lower() in search_text]


def filter_environmental_records(df: pd.DataFrame, keywords: list) -> tuple:
    """
    Lọc bản ghi có tác động môi trường theo từ khóa.
    Returns: (df_accepted, df_rejected)
    """
    accepted_rows = []
    rejected_rows = []

    for _, row in df.iterrows():
        search_text = build_search_text(row)
        matched = match_keywords(search_text, keywords)

        row_dict = row.to_dict()
        if matched:
            row_dict["matched_env_keywords"] = ", ".join(matched[:5])  # top 5
            row_dict["n_keywords_matched"] = len(matched)
            row_dict["env_filter_reason"] = (
                f"Giữ lại: khớp {len(matched)} từ khóa môi trường"
                f" ({', '.join(matched[:3])}{'...' if len(matched) > 3 else ''})"
            )
            accepted_rows.append(row_dict)
        else:
            row_dict["matched_env_keywords"] = ""
            row_dict["n_keywords_matched"] = 0
            row_dict["env_filter_reason"] = (
                "Loại bỏ: co_tac_dong=true nhưng không khớp từ khóa môi trường"
            )
            rejected_rows.append(row_dict)

    df_accepted = pd.DataFrame(accepted_rows) if accepted_rows else pd.DataFrame()
    df_rejected = pd.DataFrame(rejected_rows) if rejected_rows else pd.DataFrame()
    return df_accepted, df_rejected


def export_to_excel(df: pd.DataFrame, output_path: Path, sheet_name: str):
    """Xuất DataFrame ra Excel với định dạng cơ bản."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Sắp xếp cột ưu tiên
    priority_cols = [
        "source_id", "legal_citation", "raw_text",
        "matched_env_keywords", "n_keywords_matched", "env_filter_reason",
        "chu_the", "tin_hieu_tac_dong", "domain",
        "gia_tri_dinh_luong", "dieu_kien_ap_dung",
        "muc_do_ro_rang", "ly_do",
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
        ws.column_dimensions["D"].width = 40   # matched_env_keywords
        ws.column_dimensions["F"].width = 60   # env_filter_reason

    logger.info(f"Đã xuất {len(df)} bản ghi → {output_path}")


def print_keyword_stats(df_accepted: pd.DataFrame):
    """In thống kê từ khóa khớp được."""
    if df_accepted.empty or "matched_env_keywords" not in df_accepted.columns:
        return

    from collections import Counter
    all_kws = []
    for kws_str in df_accepted["matched_env_keywords"].dropna():
        all_kws.extend([k.strip() for k in str(kws_str).split(",") if k.strip()])

    top_kws = Counter(all_kws).most_common(10)
    logger.info("")
    logger.info("=== TOP 10 TỪ KHÓA MÔI TRƯỜNG KHỚPnhiều nhất ===")
    for kw, count in top_kws:
        bar = "█" * min(count, 25)
        logger.info(f"  {kw:<35}: {count:>4}  {bar}")


def main():
    parser = argparse.ArgumentParser(
        description="Bước 3: Lọc bản ghi có tác động môi trường bằng từ khóa"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "config" / "project_config.yaml",
    )
    parser.add_argument("--input", type=Path, default=None,
                        help="File Excel đầu vào (mặc định: data/interim/legal_impact_records.xlsx)")
    parser.add_argument("--output", type=Path, default=None,
                        help="File Excel đầu ra (mặc định: data/interim/environmental_impact_records.xlsx)")
    args = parser.parse_args()

    logger.info("=" * 65)
    logger.info("  BƯỚC 3: LỌC BẢN GHI CÓ TÁC ĐỘNG MÔI TRƯỜNG")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 65)

    config = load_config(args.config)

    input_path = args.input or (
        PROJECT_ROOT / config["paths"]["interim_data"]
        / config["pipeline_outputs"]["legal_impact_records"]
    )
    output_path = args.output or (
        PROJECT_ROOT / config["paths"]["interim_data"]
        / config["pipeline_outputs"]["environmental_impact_records"]
    )
    keywords = config.get("environment_keywords", [])

    if not input_path.exists():
        logger.error(f"Không tìm thấy file đầu vào: {input_path}")
        logger.error("Chạy trước: python src/02_filter_legal_impact.py")
        sys.exit(1)

    df = pd.read_excel(input_path)
    logger.info(f"Đọc được {len(df)} bản ghi từ: {input_path}")
    logger.info(f"Số từ khóa môi trường: {len(keywords)}")

    df_accepted, df_rejected = filter_environmental_records(df, keywords)

    logger.info("")
    logger.info("=== KẾT QUẢ LỌC TÁC ĐỘNG MÔI TRƯỜNG ===")
    logger.info(f"  Giữ lại (khớp từ khóa): {len(df_accepted)}")
    logger.info(f"  Loại bỏ (không khớp)  : {len(df_rejected)}")
    if len(df) > 0:
        logger.info(f"  Tỷ lệ giữ lại          : {100*len(df_accepted)/len(df):.1f}%")

    if df_accepted.empty:
        logger.warning("Không có bản ghi nào khớp từ khóa môi trường!")
        logger.warning("Kiểm tra lại environment_keywords trong config/project_config.yaml")
        sys.exit(0)

    print_keyword_stats(df_accepted)
    export_to_excel(df_accepted, output_path, "environmental_impact_records")

    logger.info("")
    logger.info("✅ BƯỚC 3 HOÀN TẤT")
    logger.info(f"   File đầu ra: {output_path}")
    logger.info("")
    logger.info("   BƯỚC TIẾP THEO:")
    logger.info("   python src/04_build_manual_label_file.py")


if __name__ == "__main__":
    main()
