#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
09_generate_figures.py
=======================
BƯỚC 10 — Sinh 5 biểu đồ trực quan hóa kết quả pipeline (5 nhãn).

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản 5 nhãn
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:  data/processed/final_labeled_dataset.xlsx
          data/reports/classification_metrics.xlsx
          data/reports/final_impact_report.xlsx
  Output (5 biểu đồ):
    outputs/figures/label_distribution.png       — Phân bố nhãn
    outputs/figures/confusion_matrix.png         — Confusion Matrix 5x5
    outputs/figures/impact_score_by_label.png    — Impact Score theo nhãn
    outputs/figures/impact_score_by_domain.png   — Impact Score theo domain
    outputs/figures/impact_score_by_actor.png    — Impact Score theo chủ thể

Sử dụng:
  py src/09_generate_figures.py
  py src/09_generate_figures.py --help
"""

import argparse
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Backend không cần GUI — an toàn trên mọi môi trường
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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

# ─── Màu sắc nhất quán cho 5 nhãn ────────────────────────────────────────────
LABEL_COLORS = {
    "BENEFIT_QUANTITATIVE": "#2ecc71",    # xanh lá đậm
    "BENEFIT_QUALITATIVE":  "#a8e6cf",    # xanh lá nhạt
    "COST_QUANTITATIVE":    "#e74c3c",    # đỏ đậm
    "COST_QUALITATIVE":     "#f1948a",    # đỏ nhạt
    "CONSTRAINT":           "#f39c12",    # cam
    "UNKNOWN":              "#bdc3c7",    # xám
}
LABELS_5 = [
    "BENEFIT_QUANTITATIVE",
    "BENEFIT_QUALITATIVE",
    "COST_QUANTITATIVE",
    "COST_QUALITATIVE",
    "CONSTRAINT",
]
LABEL_ABBR = {
    "BENEFIT_QUANTITATIVE": "BQ",
    "BENEFIT_QUALITATIVE":  "BQL",
    "COST_QUANTITATIVE":    "CQ",
    "COST_QUALITATIVE":     "CQL",
    "CONSTRAINT":           "CON",
}

# ─── Font cấu hình ───────────────────────────────────────────────────────────
plt.rcParams["font.family"] = ["DejaVu Sans", "Arial", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ─── Biểu đồ 1: Phân bố nhãn ─────────────────────────────────────────────────
def plot_label_distribution(df: pd.DataFrame, output_path: Path) -> bool:
    """Biểu đồ cột phân bố 5 nhãn (human_label vs llm_label vs final_label).
    Trả về True nếu xuất thành công."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.suptitle("Phan bo nhan phan loai (5 nhan)", fontsize=14, fontweight="bold", y=1.02)

    label_cols = [
        ("human_label", "Human Label"),
        ("llm_label", "LLM Label"),
        ("final_label", "Final Label"),
    ]
    any_data = False
    for ax, (col, title) in zip(axes, label_cols):
        if col not in df.columns:
            ax.set_title(f"{title}\n(khong co du lieu)")
            ax.axis("off")
            continue

        counts = df[col].value_counts().reindex(LABELS_5, fill_value=0)
        colors = [LABEL_COLORS.get(lbl, "#bdc3c7") for lbl in counts.index]
        abbrs = [LABEL_ABBR.get(lbl, lbl[:5]) for lbl in counts.index]

        bars = ax.bar(abbrs, counts.values, color=colors, edgecolor="white", linewidth=0.5)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_xlabel("Nhan")
        ax.set_ylabel("So ban ghi")
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

        for bar, val in zip(bars, counts.values):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                        str(val), ha="center", va="bottom", fontsize=9)
        any_data = True

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã xuất: {output_path}")
    return any_data


# ─── Biểu đồ 2: Confusion Matrix 5x5 ───────────────────────────────────────────
def plot_confusion_matrix(df: pd.DataFrame, output_path: Path) -> bool:
    """Heatmap Confusion Matrix 5x5. Trả về True nếu xuất thành công."""
    if "human_label" not in df.columns or "llm_label" not in df.columns:
        logger.warning("Thiếu cột human_label hoặc llm_label — bỏ qua Confusion Matrix")
        return False

    mask = df["human_label"].isin(LABELS_5) & df["llm_label"].isin(LABELS_5)
    df_eval = df[mask]
    if df_eval.empty:
        logger.warning("Không có dữ liệu hợp lệ cho Confusion Matrix")
        return False

    cm = np.zeros((5, 5), dtype=int)
    for _, row in df_eval.iterrows():
        i = LABELS_5.index(row["human_label"])
        j = LABELS_5.index(row["llm_label"])
        cm[i][j] += 1

    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    plt.colorbar(im, ax=ax)

    abbrs = [LABEL_ABBR[l] for l in LABELS_5]
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xticklabels(abbrs, rotation=30, ha="right")
    ax.set_yticklabels(abbrs)
    ax.set_xlabel("LLM Label (Du doan)", fontweight="bold")
    ax.set_ylabel("Human Label (Dung)", fontweight="bold")
    ax.set_title("Confusion Matrix 5x5\nHang=Human, Cot=LLM", fontsize=12, fontweight="bold")

    # Điền số vào ô
    thresh = cm.max() / 2.0
    for i in range(5):
        for j in range(5):
            ax.text(j, i, str(cm[i, j]),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontsize=11, fontweight="bold")

    # Chú thích viết tắt
    legend_text = "  ".join(f"{LABEL_ABBR[l]}={l}" for l in LABELS_5)
    fig.text(0.5, -0.02, legend_text, ha="center", fontsize=8, style="italic")

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã xuất: {output_path}")
    return True


# ─── Biểu đồ 3: Impact Score theo nhãn ───────────────────────────────────────────
def plot_impact_by_label(df_scored: pd.DataFrame, output_path: Path) -> bool:
    """Biểu đồ cột Impact Score tổng hợp theo 5 nhãn. Trả về True nếu xuất thành công."""
    label_col = "final_label" if "final_label" in df_scored.columns else "llm_label"
    if label_col not in df_scored.columns or "ImpactScore_i" not in df_scored.columns:
        logger.warning("Thiếu dữ liệu cho biểu đồ Impact Score by label")
        return False

    grouped = df_scored.groupby(label_col)["ImpactScore_i"].agg(["sum", "count"]).reset_index()
    grouped = grouped.rename(columns={"sum": "TotalImpact", "count": "N"})
    grouped = grouped[grouped[label_col].isin(LABELS_5)]
    if grouped.empty:
        logger.warning("Không có nhãn nào trong LABELS_5 cho biểu đồ Impact by label")
        return False
    grouped = grouped.sort_values("TotalImpact")

    colors = [LABEL_COLORS.get(lbl, "#bdc3c7") for lbl in grouped[label_col]]
    abbrs = [LABEL_ABBR.get(lbl, lbl) for lbl in grouped[label_col]]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(abbrs, grouped["TotalImpact"], color=colors, edgecolor="white")
    ax.axvline(x=0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Total Impact Score")
    ax.set_title("Impact Score tong hop theo nhan (5 nhan)", fontsize=12, fontweight="bold")

    for bar, val, n in zip(bars, grouped["TotalImpact"], grouped["N"]):
        label_x = val + 0.02 if val >= 0 else val - 0.02
        ha = "left" if val >= 0 else "right"
        ax.text(label_x, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f} (n={n})", va="center", ha=ha, fontsize=9)

    # Chú thích
    ax.text(0.01, -0.08, "* Score am = chi phi/rang buoc  |  Score duong = loi ich",
            transform=ax.transAxes, fontsize=8, style="italic", color="gray")

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã xuất: {output_path}")
    return True


# ─── Biểu đồ 4: Impact Score theo domain ───────────────────────────────────────────
def plot_impact_by_domain(df_scored: pd.DataFrame, output_path: Path) -> bool:
    """Biểu đồ cột Impact Score theo domain/tin_hieu_tac_dong. Trả về True nếu xuất thành công."""
    domain_col = None
    if "tin_hieu_tac_dong" in df_scored.columns:
        domain_col = "tin_hieu_tac_dong"
    elif "domain" in df_scored.columns:
        # Bỏ qua nếu toàn bộ domain chỉ có một giá trị duy nhất (ví dụ 'general_environment')
        unique_vals = df_scored["domain"].dropna().unique()
        if len(unique_vals) > 1:
            domain_col = "domain"

    if domain_col is None or "ImpactScore_i" not in df_scored.columns:
        logger.warning("Thiếu dữ liệu domain phù hợp — bỏ qua biểu đồ Impact Score by domain")
        return False

    df_domain = df_scored[
        df_scored[domain_col].notna()
        & (df_scored[domain_col].astype(str).str.strip() != "")
        & (df_scored[domain_col].astype(str).str.lower() != "nan")
    ]
    if df_domain.empty:
        logger.warning("Không có dữ liệu domain hợp lệ")
        return False

    grouped = (
        df_domain.groupby(domain_col)["ImpactScore_i"]
        .agg(["sum", "count"])
        .reset_index()
        .rename(columns={"sum": "TotalImpact", "count": "N"})
        .sort_values("TotalImpact")
    )

    # Giới hạn top 20 domain nếu quá nhiều
    if len(grouped) > 20:
        grouped = pd.concat([grouped.head(10), grouped.tail(10)]).drop_duplicates()

    fig_h = max(6, len(grouped) * 0.4 + 2)
    fig, ax = plt.subplots(figsize=(12, fig_h))

    colors = ["#e74c3c" if v < 0 else "#2ecc71" for v in grouped["TotalImpact"]]
    ax.barh(grouped[domain_col].astype(str), grouped["TotalImpact"],
            color=colors, edgecolor="white")
    ax.axvline(x=0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Total Impact Score")
    ax.set_title("Impact Score theo domain / tin hieu tac dong", fontsize=12, fontweight="bold")
    ax.tick_params(axis="y", labelsize=8)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã xuất: {output_path}")
    return True


# ─── Biểu đồ 5: Impact Score theo chủ thể ───────────────────────────────────────────
def plot_impact_by_actor(df_scored: pd.DataFrame, output_path: Path) -> bool:
    """Biểu đồ cột Impact Score theo chủ thể (chu_the). Trả về True nếu xuất thành công."""
    if "chu_the" not in df_scored.columns or "ImpactScore_i" not in df_scored.columns:
        logger.warning("Thiếu cột chu_the — bỏ qua biểu đồ Impact Score by actor")
        return False

    df_actor = df_scored[
        df_scored["chu_the"].notna()
        & (df_scored["chu_the"].astype(str).str.strip() != "")
        & (df_scored["chu_the"].astype(str).str.lower() != "nan")
    ]
    if df_actor.empty:
        logger.warning("Không có dữ liệu chủ thể hợp lệ")
        return False

    grouped = (
        df_actor.groupby("chu_the")["ImpactScore_i"]
        .agg(["sum", "count"])
        .reset_index()
        .rename(columns={"sum": "TotalImpact", "count": "N"})
        .sort_values("TotalImpact")
    )

    # Giới hạn top 20 chủ thể nếu quá nhiều
    if len(grouped) > 20:
        grouped = pd.concat([grouped.head(10), grouped.tail(10)]).drop_duplicates()

    fig_h = max(6, len(grouped) * 0.45 + 2)
    fig, ax = plt.subplots(figsize=(12, fig_h))

    colors = ["#e74c3c" if v < 0 else "#2ecc71" for v in grouped["TotalImpact"]]
    ax.barh(grouped["chu_the"].astype(str), grouped["TotalImpact"],
            color=colors, edgecolor="white")
    ax.axvline(x=0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Total Impact Score")
    ax.set_title("Impact Score theo chu the chiu tac dong", fontsize=12, fontweight="bold")
    ax.tick_params(axis="y", labelsize=8)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã xuất: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Bước 10: Sinh 5 biểu đồ trực quan hóa kết quả pipeline"
    )
    parser.add_argument("--config", type=Path,
                        default=PROJECT_ROOT / "config" / "project_config.yaml")
    parser.add_argument("--labeled-file", type=Path, default=None,
                        help="final_labeled_dataset.xlsx")
    parser.add_argument("--scored-file", type=Path, default=None,
                        help="final_impact_report.xlsx (sheet Chi tiết Impact Score)")
    args = parser.parse_args()

    logger.info("=" * 65)
    logger.info("  BƯỚC 10: SINH 5 BIỂU ĐỒ TRỰC QUAN HÓA")
    logger.info("=" * 65)

    config = load_config(args.config)
    processed_dir = PROJECT_ROOT / config["paths"]["processed_data"]
    reports_dir = PROJECT_ROOT / config["paths"]["reports"]
    figures_dir = PROJECT_ROOT / config["paths"]["figures"]

    labeled_path = args.labeled_file or (
        processed_dir / config["processed_files"]["final_labeled_dataset"]
    )
    scored_path = args.scored_file or (
        reports_dir / config["report_files"]["final_impact_report"]
    )

    # Đọc dữ liệu
    df_labeled = None
    if labeled_path.exists():
        df_labeled = pd.read_excel(labeled_path)
        logger.info(f"Đọc final_labeled_dataset: {len(df_labeled)} bản ghi")
    else:
        logger.warning(f"Không tìm thấy: {labeled_path}")

    df_scored = None
    if scored_path.exists():
        df_scored = pd.read_excel(scored_path, sheet_name="Chi tiết Impact Score")
        logger.info(f"Đọc final_impact_report (Chi tiết): {len(df_scored)} bản ghi")
    else:
        logger.warning(f"Không tìm thấy: {scored_path}")

    # Nếu có cả hai file, ghép thêm các cột domain/actor từ final_labeled_dataset
    # vào df_scored (để biểu đồ 4 và 5 có dữ liệu)
    if df_scored is not None and df_labeled is not None:
        enrich_cols = [c for c in ("source_id", "tin_hieu_tac_dong", "chu_the", "domain")
                       if c in df_labeled.columns and c not in df_scored.columns]
        if enrich_cols and "source_id" in df_labeled.columns and "source_id" in df_scored.columns:
            df_scored = df_scored.merge(
                df_labeled[["source_id"] + enrich_cols],
                on="source_id", how="left"
            )
            logger.info(f"Bổ sung các cột {enrich_cols} từ final_labeled_dataset vào df_scored")

    figures_dir.mkdir(parents=True, exist_ok=True)
    generated = 0

    # ── Biểu đồ 1: Label Distribution ────────────────────────────────────────
    if df_labeled is not None:
        if plot_label_distribution(
            df_labeled,
            figures_dir / config["figure_files"]["label_distribution"]
        ):
            generated += 1

    # ── Biểu đồ 2: Confusion Matrix ──────────────────────────────────────────
    if df_labeled is not None:
        if plot_confusion_matrix(
            df_labeled,
            figures_dir / config["figure_files"]["confusion_matrix"]
        ):
            generated += 1

    # ── Biểu đồ 3-5: Impact Score ────────────────────────────────────────────
    # Ưu tiên df_scored (có ImpactScore_i), fallback df_labeled nếu cũng có
    df_for_impact = df_scored if df_scored is not None else (
        df_labeled if (df_labeled is not None and "ImpactScore_i" in df_labeled.columns) else None
    )

    if df_for_impact is not None:
        if plot_impact_by_label(
            df_for_impact,
            figures_dir / config["figure_files"]["impact_score_by_label"]
        ):
            generated += 1

        if plot_impact_by_domain(
            df_for_impact,
            figures_dir / config["figure_files"]["impact_score_by_domain"]
        ):
            generated += 1

        if plot_impact_by_actor(
            df_for_impact,
            figures_dir / config["figure_files"]["impact_score_by_actor"]
        ):
            generated += 1

    logger.info("")
    logger.info(f"✅ BƯỚC 10 HOÀN TẤT — Đã sinh {generated}/5 biểu đồ")
    logger.info(f"   Thư mục: {figures_dir}")
    logger.info("")
    logger.info("   Pipeline hoàn tất! Kết quả:")
    logger.info(f"   - Báo cáo metrics : {reports_dir}/classification_metrics.xlsx")
    logger.info(f"   - Error analysis  : {reports_dir}/error_analysis.xlsx")
    logger.info(f"   - Impact report   : {reports_dir}/final_impact_report.xlsx")
    logger.info(f"   - Biểu đồ        : {figures_dir}/")


if __name__ == "__main__":
    main()
