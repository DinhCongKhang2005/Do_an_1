#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
08_calculate_impact_score.py
=============================
BƯỚC 9 — Tính Impact Score theo công thức mô hình toán học (5 nhãn).

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản 5 nhãn
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:  data/interim/scoring_input.xlsx  (đã điền M_i, S_i, D_i, R_i, W_i)
  Output: data/reports/final_impact_report.xlsx

Công thức:
  C_i      = alpha*M_i + beta*S_i + gamma*D_i + delta*R_i
  C_i_norm = (C_i - 1) / 4                    → C_i_norm ∈ [0,1]
  direction_i = +1 (BENEFIT_*), -1 (COST_*, CONSTRAINT)
  ImpactScore_i = direction_i * W_i * C_i_norm → ImpactScore_i ∈ [-1,1]

Tổng hợp theo:
  - Toàn bộ (TotalImpact)
  - Theo nhãn final_label
  - Theo domain (trường 'domain' hoặc 'tin_hieu_tac_dong')
  - Theo chủ thể (trường 'chu_the')

Sử dụng:
  python src/08_calculate_impact_score.py
  python src/08_calculate_impact_score.py --help
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

# Direction map cho 5 nhãn (theo đặc tả README Mục 8)
DIRECTION_MAP = {
    "BENEFIT_QUANTITATIVE": +1,
    "BENEFIT_QUALITATIVE":  +1,
    "COST_QUANTITATIVE":    -1,
    "COST_QUALITATIVE":     -1,
    "CONSTRAINT":           -1,
}


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def compute_impact_scores(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Tính C_i, C_i_norm, direction_i, ImpactScore_i cho từng record.
    """
    scoring = config.get("scoring", {})
    alpha = scoring.get("alpha", 0.25)
    beta  = scoring.get("beta",  0.25)
    gamma = scoring.get("gamma", 0.25)
    delta = scoring.get("delta", 0.25)
    scale_min = scoring.get("scale_min", 1)
    scale_max = scoring.get("scale_max", 5)
    default_w = scoring.get("default_object_weight", 1.0)

    df = df.copy()

    # Đọc biến điểm — điền mặc định nếu thiếu (sẽ cảnh báo)
    def safe_float(series, default, col_name):
        result = pd.to_numeric(series, errors="coerce")
        n_missing = result.isna().sum()
        if n_missing > 0:
            logger.warning(f"Cột '{col_name}' có {n_missing} giá trị thiếu — điền giá trị trung bình {default}")
            result = result.fillna(default)
        return result

    mid = (scale_min + scale_max) / 2  # Giá trị mặc định = 3.0

    df["M_i"] = safe_float(df.get("M_i", pd.Series([mid] * len(df))), mid, "M_i")
    df["S_i"] = safe_float(df.get("S_i", pd.Series([mid] * len(df))), mid, "S_i")
    df["D_i"] = safe_float(df.get("D_i", pd.Series([mid] * len(df))), mid, "D_i")
    df["R_i"] = safe_float(df.get("R_i", pd.Series([mid] * len(df))), mid, "R_i")
    df["W_i"] = safe_float(df.get("W_i", pd.Series([default_w] * len(df))), default_w, "W_i")

    # Clamp về [scale_min, scale_max]
    for col in ("M_i", "S_i", "D_i", "R_i"):
        df[col] = df[col].clip(scale_min, scale_max)

    # Tính C_i (điểm thành phần)
    df["C_i"] = alpha * df["M_i"] + beta * df["S_i"] + gamma * df["D_i"] + delta * df["R_i"]

    # Chuẩn hóa C_i về [0,1]
    df["C_i_norm"] = (df["C_i"] - scale_min) / (scale_max - scale_min)

    # Direction theo 5 nhãn
    label_col = "final_label" if "final_label" in df.columns else "llm_label"
    df["direction_i"] = df[label_col].map(DIRECTION_MAP).fillna(0).astype(int)

    # Tính Impact Score
    df["ImpactScore_i"] = df["direction_i"] * df["W_i"] * df["C_i_norm"]

    # Làm tròn
    for col in ("C_i", "C_i_norm", "ImpactScore_i"):
        df[col] = df[col].round(4)

    return df


def build_summary_tables(df: pd.DataFrame) -> dict:
    """
    Tổng hợp Impact Score theo nhãn, domain, chủ thể.
    """
    summaries = {}

    # Tổng hợp toàn bộ
    total = df["ImpactScore_i"].sum()
    summaries["total"] = round(total, 4)

    # Theo nhãn
    if "final_label" in df.columns:
        by_label = (
            df.groupby("final_label")["ImpactScore_i"]
            .agg(["sum", "mean", "count"])
            .rename(columns={"sum": "TotalImpact", "mean": "MeanImpact", "count": "N"})
            .reset_index()
            .rename(columns={"final_label": "Nhãn"})
        )
        by_label["TotalImpact"] = by_label["TotalImpact"].round(4)
        by_label["MeanImpact"] = by_label["MeanImpact"].round(4)
        summaries["by_label"] = by_label

    # Theo domain — dùng tin_hieu_tac_dong nếu domain = general_environment
    domain_col = None
    if "tin_hieu_tac_dong" in df.columns:
        domain_col = "tin_hieu_tac_dong"
    elif "domain" in df.columns:
        domain_col = "domain"

    if domain_col:
        by_domain = (
            df[df[domain_col].notna()]
            .groupby(domain_col)["ImpactScore_i"]
            .agg(["sum", "mean", "count"])
            .rename(columns={"sum": "TotalImpact", "mean": "MeanImpact", "count": "N"})
            .reset_index()
            .rename(columns={domain_col: "Domain/TinHieu"})
            .sort_values("TotalImpact", ascending=True)
        )
        by_domain["TotalImpact"] = by_domain["TotalImpact"].round(4)
        by_domain["MeanImpact"] = by_domain["MeanImpact"].round(4)
        summaries["by_domain"] = by_domain

    # Theo chủ thể
    if "chu_the" in df.columns:
        by_actor = (
            df[df["chu_the"].notna() & (df["chu_the"] != "")]
            .groupby("chu_the")["ImpactScore_i"]
            .agg(["sum", "mean", "count"])
            .rename(columns={"sum": "TotalImpact", "mean": "MeanImpact", "count": "N"})
            .reset_index()
            .rename(columns={"chu_the": "ChuThe"})
            .sort_values("TotalImpact", ascending=True)
        )
        by_actor["TotalImpact"] = by_actor["TotalImpact"].round(4)
        by_actor["MeanImpact"] = by_actor["MeanImpact"].round(4)
        summaries["by_actor"] = by_actor

    return summaries


def export_impact_report(df: pd.DataFrame, summaries: dict, output_path: Path):
    """Xuất báo cáo Impact Score đầy đủ ra Excel nhiều sheet."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Chọn cột hiển thị trong sheet chi tiết
    detail_cols = [
        "source_id", "legal_citation", "final_label", "direction_i",
        "M_i", "S_i", "D_i", "R_i", "W_i",
        "C_i", "C_i_norm", "ImpactScore_i",
        "chu_the", "tin_hieu_tac_dong", "raw_text",
    ]
    existing = [c for c in detail_cols if c in df.columns]
    df_detail = df[existing]

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Sheet 1: Chi tiết từng record
        df_detail.to_excel(writer, index=False, sheet_name="Chi tiết Impact Score")
        ws = writer.sheets["Chi tiết Impact Score"]
        ws.column_dimensions["A"].width = 22
        ws.column_dimensions["B"].width = 22
        # Tìm và mở rộng cột raw_text nếu có
        from openpyxl.utils import get_column_letter
        for i, col_name in enumerate(df_detail.columns, 1):
            if col_name == "raw_text":
                ws.column_dimensions[get_column_letter(i)].width = 70

        # Sheet 2: Tổng hợp theo nhãn
        if "by_label" in summaries:
            summaries["by_label"].to_excel(writer, index=False,
                                            sheet_name="Theo nhãn")
            ws2 = writer.sheets["Theo nhãn"]
            ws2.column_dimensions["A"].width = 28

        # Sheet 3: Tổng hợp theo domain
        if "by_domain" in summaries:
            summaries["by_domain"].to_excel(writer, index=False,
                                             sheet_name="Theo domain")
            ws3 = writer.sheets["Theo domain"]
            ws3.column_dimensions["A"].width = 55

        # Sheet 4: Tổng hợp theo chủ thể
        if "by_actor" in summaries:
            summaries["by_actor"].to_excel(writer, index=False,
                                            sheet_name="Theo chủ thể")
            ws4 = writer.sheets["Theo chủ thể"]
            ws4.column_dimensions["A"].width = 45

        # Sheet 5: Tóm tắt tổng
        summary_rows = [
            {"Chỉ số": "Tổng số bản ghi tính điểm", "Giá trị": len(df)},
            {"Chỉ số": "Tổng TotalImpact (toàn bộ)", "Giá trị": summaries["total"]},
            {"Chỉ số": "Impact Score trung bình", "Giá trị": round(df["ImpactScore_i"].mean(), 4)},
            {"Chỉ số": "Impact Score lớn nhất", "Giá trị": round(df["ImpactScore_i"].max(), 4)},
            {"Chỉ số": "Impact Score nhỏ nhất", "Giá trị": round(df["ImpactScore_i"].min(), 4)},
            {"Chỉ số": "Số điều khoản Impact > 0 (lợi ích)", "Giá trị": int((df["ImpactScore_i"] > 0).sum())},
            {"Chỉ số": "Số điều khoản Impact < 0 (chi phí/ràng buộc)", "Giá trị": int((df["ImpactScore_i"] < 0).sum())},
            {"Chỉ số": "Thời gian xuất báo cáo", "Giá trị": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        ]
        pd.DataFrame(summary_rows).to_excel(writer, index=False, sheet_name="Tóm tắt")
        ws5 = writer.sheets["Tóm tắt"]
        ws5.column_dimensions["A"].width = 40
        ws5.column_dimensions["B"].width = 20

    logger.info(f"Đã xuất báo cáo Impact Score → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Bước 9: Tính Impact Score theo công thức mô hình toán học (5 nhãn)"
    )
    parser.add_argument("--config", type=Path,
                        default=PROJECT_ROOT / "config" / "project_config.yaml")
    parser.add_argument("--input", type=Path, default=None,
                        help="File scoring_input.xlsx (ghi đè config)")
    parser.add_argument("--output", type=Path, default=None,
                        help="File báo cáo Excel (ghi đè config)")
    args = parser.parse_args()

    logger.info("=" * 65)
    logger.info("  BƯỚC 9: TÍNH IMPACT SCORE (5 NHÃN)")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 65)

    config = load_config(args.config)
    interim_dir = PROJECT_ROOT / config["paths"]["interim_data"]
    reports_dir = PROJECT_ROOT / config["paths"]["reports"]

    input_path = args.input or (interim_dir / config["interim_files"]["scoring_input"])
    output_path = args.output or (reports_dir / config["report_files"]["final_impact_report"])

    if not input_path.exists():
        logger.error(f"Không tìm thấy file: {input_path}")
        logger.error("Chạy trước: python src/07_build_scoring_input.py")
        sys.exit(1)

    df = pd.read_excel(input_path)
    logger.info(f"Đọc được {len(df)} bản ghi từ: {input_path}")

    # Kiểm tra có biến điểm chưa
    score_cols = ["M_i", "S_i", "D_i", "R_i"]
    missing_cols = [c for c in score_cols if c not in df.columns]
    if missing_cols:
        logger.error(f"Thiếu cột: {missing_cols}")
        logger.error("Hãy chạy: python src/07_build_scoring_input.py")
        sys.exit(1)

    n_unfilled = df[score_cols].isna().any(axis=1).sum()
    if n_unfilled > 0:
        logger.warning(f"{n_unfilled}/{len(df)} record chưa điền đủ M_i/S_i/D_i/R_i — dùng giá trị mặc định")

    df_scored = compute_impact_scores(df, config)
    summaries = build_summary_tables(df_scored)
    export_impact_report(df_scored, summaries, output_path)

    # In tóm tắt
    logger.info("")
    logger.info("=== TÓM TẮT IMPACT SCORE ===")
    logger.info(f"  Số bản ghi tính điểm  : {len(df_scored)}")
    logger.info(f"  TotalImpact (tổng)     : {summaries['total']:.4f}")
    logger.info(f"  Score TB               : {df_scored['ImpactScore_i'].mean():.4f}")
    logger.info(f"  Score lớn nhất         : {df_scored['ImpactScore_i'].max():.4f}")
    logger.info(f"  Score nhỏ nhất         : {df_scored['ImpactScore_i'].min():.4f}")
    logger.info(f"  Điều khoản lợi ích (>0): {(df_scored['ImpactScore_i'] > 0).sum()}")
    logger.info(f"  Điều khoản gánh nặng(<0): {(df_scored['ImpactScore_i'] < 0).sum()}")

    logger.info("")
    logger.info("✅ BƯỚC 9 HOÀN TẤT")
    logger.info(f"   File báo cáo: {output_path}")
    logger.info("")
    logger.info("   BƯỚC TIẾP THEO:")
    logger.info("   python src/09_generate_figures.py")


if __name__ == "__main__":
    main()
