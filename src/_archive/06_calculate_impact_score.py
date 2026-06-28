#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_calculate_impact_score.py
=============================
BƯỚC 6 — Tính Impact Score tất định theo công thức đã định nghĩa.

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản không tranh biện
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:  data/interim/scoring_input.xlsx  (đã điền M/S/D/R)
  Output:
    - data/reports/final_impact_report.xlsx

Công thức Impact Score (tất định):
  C_i = alpha*M_i + beta*S_i + gamma*D_i + delta*R_i
  C_i_norm = (C_i - 1) / 4                         [chuẩn hóa về [0, 1]]
  ImpactScore_i = direction_i * object_weight_i * C_i_norm

  Trong đó alpha=beta=gamma=delta=0.25 (giả định trọng số bằng nhau — xem docs/methodology.md)

Lưu ý học thuật:
  - Đây là tính điểm TẤT ĐỊNH, không có Monte Carlo
  - Monte Carlo là hướng nghiên cứu tương lai (xem docs/limitations_and_future_work.md)

Sử dụng:
  python src/06_calculate_impact_score.py
  python src/06_calculate_impact_score.py --input data/interim/scoring_input.xlsx
  python src/06_calculate_impact_score.py --help
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
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


def safe_float(val, default: float = 3.0, scale_min: float = 1.0, scale_max: float = 5.0) -> float:
    """Chuyển đổi giá trị sang float hợp lệ trong phạm vi thang điểm."""
    try:
        f = float(val)
        if scale_min <= f <= scale_max:
            return f
        # Clip nếu nằm ngoài phạm vi
        return max(scale_min, min(scale_max, f))
    except (TypeError, ValueError):
        return default


def calculate_composite_score(
    M: float, S: float, D: float, R: float,
    alpha: float, beta: float, gamma: float, delta: float,
) -> float:
    """
    Tính C_i theo công thức:
      C_i = alpha*M + beta*S + gamma*D + delta*R

    Với alpha=beta=gamma=delta=0.25 (giả định trọng số bằng nhau):
      C_i = 0.25 * (M + S + D + R)

    Xem giải thích tại docs/methodology.md
    """
    return alpha * M + beta * S + gamma * D + delta * R


def normalize_score(C: float, scale_min: float = 1.0, scale_max: float = 5.0) -> float:
    """
    Chuẩn hóa về [0, 1]:
      C_norm = (C - scale_min) / (scale_max - scale_min)
             = (C - 1) / 4   [khi thang 1–5]
    """
    denom = scale_max - scale_min
    if denom == 0:
        return 0.0
    return (C - scale_min) / denom


def compute_impact_score_row(row: pd.Series, scoring_cfg: dict) -> dict:
    """
    Tính Impact Score cho một điều khoản.
    Trả về dict kết quả.
    """
    alpha = scoring_cfg.get("alpha", 0.25)
    beta = scoring_cfg.get("beta", 0.25)
    gamma = scoring_cfg.get("gamma", 0.25)
    delta = scoring_cfg.get("delta", 0.25)
    scale_min = scoring_cfg.get("scale_min", 1.0)
    scale_max = scoring_cfg.get("scale_max", 5.0)

    # Đọc giá trị biến (với fallback 3.0 = giá trị trung bình thang Likert)
    M = safe_float(row.get("M_i", ""), default=3.0, scale_min=scale_min, scale_max=scale_max)
    S = safe_float(row.get("S_i", ""), default=3.0, scale_min=scale_min, scale_max=scale_max)
    D = safe_float(row.get("D_i", ""), default=3.0, scale_min=scale_min, scale_max=scale_max)
    R = safe_float(row.get("R_i", ""), default=3.0, scale_min=scale_min, scale_max=scale_max)
    w = safe_float(row.get("object_weight", 1.0), default=1.0, scale_min=0.1, scale_max=3.0)

    # Hướng tác động
    direction_raw = row.get("direction", 0)
    direction_map = {"BENEFIT": 1, "COST": -1, "CONSTRAINT": -1}
    final_label = str(row.get("final_label", "")).strip().upper()

    if str(direction_raw) in ("-1", "1"):
        direction = int(direction_raw)
    else:
        direction = direction_map.get(final_label, 0)

    # Tính toán
    C_i = calculate_composite_score(M, S, D, R, alpha, beta, gamma, delta)
    C_i_norm = normalize_score(C_i, scale_min, scale_max)
    impact_score = direction * w * C_i_norm

    # Cờ thiếu dữ liệu
    missing_vars = []
    for var_name, var_col in [("M_i", "M_i"), ("S_i", "S_i"), ("D_i", "D_i"), ("R_i", "R_i")]:
        val = row.get(var_col, "")
        try:
            float(val)
        except (TypeError, ValueError):
            missing_vars.append(var_name)

    return {
        "M_i": M,
        "S_i": S,
        "D_i": D,
        "R_i": R,
        "object_weight": w,
        "direction": direction,
        "C_i": round(C_i, 4),
        "C_i_norm": round(C_i_norm, 4),
        "ImpactScore_i": round(impact_score, 4),
        "scoring_note": f"Thiếu biến: {', '.join(missing_vars)}" if missing_vars else "OK",
    }


def calculate_all_scores(df: pd.DataFrame, scoring_cfg: dict) -> pd.DataFrame:
    """Tính Impact Score cho toàn bộ DataFrame."""
    logger.info(f"Tính Impact Score cho {len(df)} điều khoản...")

    results = []
    for _, row in df.iterrows():
        result = compute_impact_score_row(row, scoring_cfg)
        results.append(result)

    df_scores = pd.DataFrame(results)

    # Gộp vào dataframe gốc
    df_result = df.copy()
    for col in ["C_i", "C_i_norm", "ImpactScore_i", "scoring_note"]:
        df_result[col] = df_scores[col].values

    # Cập nhật lại các cột biến đã tính
    for col in ["M_i", "S_i", "D_i", "R_i", "object_weight", "direction"]:
        df_result[col] = df_scores[col].values

    return df_result


def print_score_summary(df: pd.DataFrame):
    """In tóm tắt kết quả tính điểm."""
    logger.info(f"\n{'='*60}")
    logger.info(f"  KẾT QUẢ IMPACT SCORE (TẤT ĐỊNH)")
    logger.info(f"{'='*60}")

    valid = df[df["ImpactScore_i"].notna()]
    logger.info(f"  Số điều khoản đã tính điểm: {len(valid)}")
    logger.info(f"  Impact Score tổng hợp (tổng): {valid['ImpactScore_i'].sum():.4f}")
    logger.info(f"  Impact Score trung bình:       {valid['ImpactScore_i'].mean():.4f}")
    logger.info(f"  Impact Score max:              {valid['ImpactScore_i'].max():.4f}")
    logger.info(f"  Impact Score min:              {valid['ImpactScore_i'].min():.4f}")
    logger.info(f"")

    # Theo nhãn
    for label in ["BENEFIT", "COST", "CONSTRAINT"]:
        sub = valid[valid["final_label"].str.upper() == label]
        if len(sub) > 0:
            logger.info(
                f"  {label:<12}: n={len(sub):>3}, "
                f"tổng={sub['ImpactScore_i'].sum():>+8.4f}, "
                f"TB={sub['ImpactScore_i'].mean():>+8.4f}"
            )

    missing = df[df["scoring_note"] != "OK"]
    if len(missing) > 0:
        logger.warning(f"  ⚠️  {len(missing)} bản ghi thiếu biến → dùng giá trị mặc định 3.0")

    logger.info(f"{'='*60}\n")


def export_impact_report(df: pd.DataFrame, output_path: Path, scoring_cfg: dict):
    """Xuất báo cáo Impact Score ra Excel nhiều sheet."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Sheet 1: Chi tiết từng điều khoản
    detail_cols = [
        "source_id", "legal_citation", "final_label", "direction",
        "M_i", "S_i", "D_i", "R_i", "object_weight",
        "C_i", "C_i_norm", "ImpactScore_i", "scoring_note",
        "noi_dung_dieu_khoan",
    ]
    existing_detail = [c for c in detail_cols if c in df.columns]
    df_detail = df[existing_detail].copy()

    # Sheet 2: Tổng hợp theo nhãn
    summary_rows = []
    for label in ["BENEFIT", "COST", "CONSTRAINT"]:
        sub = df[df["final_label"].str.upper() == label]
        if len(sub) > 0:
            summary_rows.append({
                "Nhãn": label,
                "Số điều khoản": len(sub),
                "Tổng ImpactScore": round(sub["ImpactScore_i"].sum(), 4),
                "Trung bình ImpactScore": round(sub["ImpactScore_i"].mean(), 4),
                "Max ImpactScore": round(sub["ImpactScore_i"].max(), 4),
                "Min ImpactScore": round(sub["ImpactScore_i"].min(), 4),
            })
    total_score = df["ImpactScore_i"].sum()
    summary_rows.append({
        "Nhãn": "TỔNG CỘNG",
        "Số điều khoản": len(df),
        "Tổng ImpactScore": round(total_score, 4),
        "Trung bình ImpactScore": round(df["ImpactScore_i"].mean(), 4),
        "Max ImpactScore": round(df["ImpactScore_i"].max(), 4),
        "Min ImpactScore": round(df["ImpactScore_i"].min(), 4),
    })
    df_summary = pd.DataFrame(summary_rows)

    # Sheet 3: Thông tin cấu hình
    alpha = scoring_cfg.get("alpha", 0.25)
    config_rows = [
        {"Tham số": "alpha (trọng số M)", "Giá trị": alpha, "Ghi chú": "Giả định bằng nhau"},
        {"Tham số": "beta (trọng số S)", "Giá trị": scoring_cfg.get("beta", 0.25), "Ghi chú": "Giả định bằng nhau"},
        {"Tham số": "gamma (trọng số D)", "Giá trị": scoring_cfg.get("gamma", 0.25), "Ghi chú": "Giả định bằng nhau"},
        {"Tham số": "delta (trọng số R)", "Giá trị": scoring_cfg.get("delta", 0.25), "Ghi chú": "Giả định bằng nhau"},
        {"Tham số": "scale_min", "Giá trị": scoring_cfg.get("scale_min", 1), "Ghi chú": "Thang Likert 1-5"},
        {"Tham số": "scale_max", "Giá trị": scoring_cfg.get("scale_max", 5), "Ghi chú": "Thang Likert 1-5"},
        {"Tham số": "Phương pháp", "Giá trị": "Tất định (Deterministic)", "Ghi chú": "Không có Monte Carlo"},
        {"Tham số": "Monte Carlo", "Giá trị": "Không thực thi", "Ghi chú": "Hướng nghiên cứu tương lai"},
    ]
    df_config = pd.DataFrame(config_rows)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_detail.to_excel(writer, index=False, sheet_name="Chi tiết Impact Score")
        df_summary.to_excel(writer, index=False, sheet_name="Tổng hợp theo nhãn")
        df_config.to_excel(writer, index=False, sheet_name="Cấu hình tính điểm")

        # Định dạng
        ws1 = writer.sheets["Chi tiết Impact Score"]
        ws1.column_dimensions["A"].width = 30
        ws1.column_dimensions["B"].width = 22
        ws1.column_dimensions["C"].width = 14
        ws1.column_dimensions["N"].width = 80

        ws2 = writer.sheets["Tổng hợp theo nhãn"]
        ws2.column_dimensions["A"].width = 18
        for col_letter in ["B", "C", "D", "E", "F"]:
            ws2.column_dimensions[col_letter].width = 22

    logger.info(f"Đã xuất báo cáo Impact Score → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Bước 6: Tính Impact Score tất định (không Monte Carlo)"
    )
    parser.add_argument("--config", type=Path, default=PROJECT_ROOT / "config" / "project_config.yaml")
    parser.add_argument("--input", type=Path, default=None, help="File scoring_input.xlsx đã điền biến")
    parser.add_argument("--output", type=Path, default=None, help="File final_impact_report.xlsx đầu ra")
    args = parser.parse_args()

    logger.info(f"{'='*65}")
    logger.info(f"  BƯỚC 6: TÍNH IMPACT SCORE TẤT ĐỊNH")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*65}")
    logger.info(f"  [Lưu ý] Đây là tính điểm TẤT ĐỊNH. Monte Carlo là hướng tương lai.")

    config = load_config(args.config)
    interim_dir = PROJECT_ROOT / config["paths"]["interim_data"]
    reports_dir = PROJECT_ROOT / config["paths"]["reports"]

    input_path = args.input or (interim_dir / config["interim_files"]["scoring_input"])
    output_path = args.output or (reports_dir / config["report_files"]["final_impact_report"])
    scoring_cfg = config["scoring"]

    if not input_path.exists():
        logger.error(f"Không tìm thấy file: {input_path}")
        logger.error("Chạy trước: python src/05_build_scoring_input.py")
        logger.error("Sau đó điền biến M/S/D/R vào file đó.")
        sys.exit(1)

    df = pd.read_excel(input_path)
    logger.info(f"Đọc được {len(df)} bản ghi từ: {input_path}")

    # Log cấu hình trọng số
    alpha = scoring_cfg.get("alpha", 0.25)
    logger.info(f"Trọng số: alpha={alpha}, beta={scoring_cfg.get('beta',0.25)}, "
                f"gamma={scoring_cfg.get('gamma',0.25)}, delta={scoring_cfg.get('delta',0.25)}")
    logger.info(f"(alpha=beta=gamma=delta={alpha} — Giả định trọng số bằng nhau)")

    # Tính điểm
    df_result = calculate_all_scores(df, scoring_cfg)

    # In tóm tắt
    print_score_summary(df_result)

    # Xuất báo cáo
    export_impact_report(df_result, output_path, scoring_cfg)

    logger.info(f"✅ BƯỚC 6 HOÀN TẤT")
    logger.info(f"   Báo cáo Impact Score: {output_path}")
    logger.info(f"   Tổng Impact Score: {df_result['ImpactScore_i'].sum():.4f}")
    logger.info(f"")
    logger.info(f"   BƯỚC TIẾP THEO:")
    logger.info(f"   python src/07_generate_figures.py")


if __name__ == "__main__":
    main()
