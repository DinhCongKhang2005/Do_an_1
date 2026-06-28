#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_build_manual_label_file.py
==============================
BƯỚC 2 — Tạo file Excel template cho nhà nghiên cứu gán nhãn thủ công.

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản không tranh biện
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:  data/interim/impact_true_records.xlsx
  Output: data/interim/manual_label_template.xlsx  (template chờ nhà nghiên cứu điền)

Sau khi chạy:
  → Nhà nghiên cứu điền vào cột 'human_label' và 'human_reason'
  → Lưu file với tên: data/interim/human_labeled_dataset.xlsx

Sử dụng:
  python src/02_build_manual_label_file.py
  python src/02_build_manual_label_file.py --input data/interim/impact_true_records.xlsx
  python src/02_build_manual_label_file.py --help
"""

import argparse
import logging
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

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


LABELING_INSTRUCTION = """HƯỚNG DẪN GÁN NHÃN THỦ CÔNG
=================================
Điền vào cột 'human_label' với đúng một trong ba nhãn:
  BENEFIT    → Điều khoản mang lại tác động tích cực (môi trường/xã hội/kinh tế)
  COST       → Điều khoản áp đặt chi phí, nghĩa vụ, gánh nặng tuân thủ
  CONSTRAINT → Điều khoản đặt ngưỡng kỹ thuật, giới hạn, điều kiện ràng buộc

Ưu tiên CONSTRAINT nếu điều khoản chứa giá trị số biểu thị ngưỡng/giới hạn kỹ thuật.

Điền vào cột 'human_reason' lý do ngắn gọn (1-2 câu).

Sau khi hoàn thành, lưu file này với tên: human_labeled_dataset.xlsx
"""


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_manual_label_template(df_input: pd.DataFrame) -> pd.DataFrame:
    """
    Tạo DataFrame template cho nhà nghiên cứu gán nhãn thủ công.
    Thêm các cột cần điền và giữ lại thông tin cần thiết.
    """
    # Chọn các cột thông tin quan trọng
    info_cols = [
        "source_id",
        "legal_citation",
        "noi_dung_dieu_khoan",
        "matched_keywords",
        "chu_the",
        "loai_phap_ly",
        "tin_hieu_phap_ly",
        "doi_tuong",
        "dieu_kien",
        "gia_tri_dinh_luong",
        "co_tac_dong_original",
    ]
    existing_cols = [c for c in info_cols if c in df_input.columns]
    df = df_input[existing_cols].copy()

    # Thêm cột dành cho nhà nghiên cứu điền
    df.insert(1, "human_label", "")   # BENEFIT / COST / CONSTRAINT
    df.insert(2, "human_reason", "")  # Lý do gán nhãn
    df.insert(3, "labeler_name", "")  # Tên người gán nhãn
    df.insert(4, "labeled_at", "")    # Ngày gán nhãn

    return df


def export_template_excel(df: pd.DataFrame, output_path: Path):
    """Xuất template Excel với định dạng hỗ trợ nhà nghiên cứu."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Gán nhãn thủ công")
        ws = writer.sheets["Gán nhãn thủ công"]

        # Điều chỉnh độ rộng cột
        ws.column_dimensions["A"].width = 30   # source_id
        ws.column_dimensions["B"].width = 15   # human_label
        ws.column_dimensions["C"].width = 40   # human_reason
        ws.column_dimensions["D"].width = 20   # labeler_name
        ws.column_dimensions["E"].width = 15   # labeled_at
        ws.column_dimensions["F"].width = 22   # legal_citation
        ws.column_dimensions["G"].width = 80   # noi_dung_dieu_khoan
        ws.column_dimensions["H"].width = 30   # matched_keywords

        # Thêm sheet hướng dẫn
        ws_guide = writer.book.create_sheet(title="Hướng dẫn")
        for row_idx, line in enumerate(LABELING_INSTRUCTION.strip().split("\n"), start=1):
            ws_guide.cell(row=row_idx, column=1, value=line)
        ws_guide.column_dimensions["A"].width = 80

    logger.info(f"Đã xuất template → {output_path} ({len(df)} bản ghi)")


def main():
    parser = argparse.ArgumentParser(
        description="Bước 2: Tạo file template cho nhà nghiên cứu gán nhãn thủ công"
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
        help="Đường dẫn file Excel đầu vào (ghi đè cấu hình)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Đường dẫn file Excel template đầu ra (ghi đè cấu hình)",
    )
    args = parser.parse_args()

    # ── Đọc cấu hình ──────────────────────────────────────────────────────────
    logger.info(f"{'='*65}")
    logger.info(f"  BƯỚC 2: TẠO FILE TEMPLATE GÁN NHÃN THỦ CÔNG")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*65}")

    config = load_config(args.config)
    interim_dir = PROJECT_ROOT / config["paths"]["interim_data"]

    input_path = args.input or (interim_dir / config["interim_files"]["impact_true_records"])
    output_path = args.output or (interim_dir / config["interim_files"]["manual_label_template"])

    # ── Kiểm tra file đầu vào ─────────────────────────────────────────────────
    if not input_path.exists():
        logger.error(f"Không tìm thấy file đầu vào: {input_path}")
        logger.error(f"Vui lòng chạy trước: python src/01_load_and_filter_impact_true.py")
        sys.exit(1)

    # ── Đọc dữ liệu ───────────────────────────────────────────────────────────
    df_input = pd.read_excel(input_path)
    logger.info(f"Đọc được {len(df_input)} bản ghi từ: {input_path}")

    # ── Tạo template ──────────────────────────────────────────────────────────
    df_template = build_manual_label_template(df_input)

    # ── Xuất template ─────────────────────────────────────────────────────────
    export_template_excel(df_template, output_path)

    logger.info(f"")
    logger.info(f"✅ BƯỚC 2 HOÀN TẤT")
    logger.info(f"   File template đã tạo: {output_path}")
    logger.info(f"   Số bản ghi cần gán nhãn: {len(df_template)}")
    logger.info(f"")
    logger.info(f"   *** DỪNG — BƯỚC THỦ CÔNG ***")
    logger.info(f"   1. Mở file: {output_path}")
    logger.info(f"   2. Điền cột 'human_label' (BENEFIT/COST/CONSTRAINT) và 'human_reason'")
    logger.info(f"   3. Lưu file với tên: human_labeled_dataset.xlsx (cùng thư mục)")
    logger.info(f"   4. Chạy: python src/03_llm_classify.py")


if __name__ == "__main__":
    main()
