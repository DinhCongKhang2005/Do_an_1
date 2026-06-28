#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_generate_figures.py
=======================
BƯỚC 7 — Xuất biểu đồ và cập nhật báo cáo tổng hợp.

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản không tranh biện
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:
    - data/processed/final_labeled_dataset.xlsx  (cho label_distribution + confusion_matrix)
    - data/reports/final_impact_report.xlsx       (cho impact_score_bar)
  Output:
    - outputs/figures/label_distribution.png
    - outputs/figures/confusion_matrix.png
    - outputs/figures/impact_score_bar.png

Sử dụng:
  python src/07_generate_figures.py
  python src/07_generate_figures.py --help
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend cho server/CI
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

# ─── Style chung ──────────────────────────────────────────────────────────────
COLORS = {
    "BENEFIT": "#2ecc71",    # Xanh lá
    "COST": "#e74c3c",       # Đỏ
    "CONSTRAINT": "#f39c12", # Cam
    "UNKNOWN": "#95a5a6",    # Xám
}
FIGURE_DPI = 150

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
    "axes.facecolor": "#f8f9fa",
    "axes.grid": True,
    "grid.alpha": 0.4,
    "grid.linestyle": "--",
})


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ─── Biểu đồ 1: Phân phối nhãn ───────────────────────────────────────────────
def plot_label_distribution(df: pd.DataFrame, output_path: Path):
    """
    Vẽ biểu đồ cột so sánh phân phối nhãn Human vs LLM.
    """
    labels = ["BENEFIT", "COST", "CONSTRAINT"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), sharey=False)
    fig.suptitle(
        "Phân phối nhãn phân loại: Human vs LLM\n"
        "(Dữ liệu pilot study — Phiên bản không tranh biện)",
        fontsize=13, fontweight="bold", y=1.02
    )

    for ax, (col_name, title) in zip(
        axes,
        [("human_label", "Nhãn người (Human Label)"), ("llm_label", "Nhãn LLM")],
    ):
        if col_name not in df.columns:
            ax.text(0.5, 0.5, f"Không có cột\n'{col_name}'", ha="center", va="center", transform=ax.transAxes)
            ax.set_title(title)
            continue

        counts = df[col_name].astype(str).str.strip().str.upper().value_counts()
        bar_labels = []
        bar_counts = []
        bar_colors = []
        for lbl in labels:
            bar_labels.append(lbl)
            bar_counts.append(counts.get(lbl, 0))
            bar_colors.append(COLORS.get(lbl, "#888"))

        bars = ax.bar(bar_labels, bar_counts, color=bar_colors, edgecolor="white", linewidth=1.5, width=0.6)
        ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Nhãn", fontsize=10)
        ax.set_ylabel("Số điều khoản", fontsize=10)
        ax.set_ylim(0, max(bar_counts) * 1.3 if bar_counts else 1)

        # Ghi số lên cột
        for bar, count in zip(bars, bar_counts):
            if count > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.3,
                    str(count),
                    ha="center", va="bottom", fontsize=11, fontweight="bold",
                )

        # Tổng
        total = sum(bar_counts)
        ax.text(
            0.98, 0.96, f"Tổng: {total}",
            ha="right", va="top", transform=ax.transAxes,
            fontsize=9, color="#555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#ccc", alpha=0.8),
        )

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ phân phối nhãn → {output_path}")


# ─── Biểu đồ 2: Confusion Matrix ─────────────────────────────────────────────
def plot_confusion_matrix(df: pd.DataFrame, output_path: Path):
    """
    Vẽ Confusion Matrix LLM vs Human.
    """
    labels = ["BENEFIT", "COST", "CONSTRAINT"]

    if "human_label" not in df.columns or "llm_label" not in df.columns:
        logger.warning("Thiếu cột human_label hoặc llm_label — bỏ qua confusion matrix")
        return

    # Lọc bản ghi có cả hai nhãn hợp lệ
    mask = (
        df["human_label"].astype(str).str.strip().str.upper().isin(labels)
        & df["llm_label"].astype(str).str.strip().str.upper().isin(labels)
    )
    df_eval = df[mask]

    if len(df_eval) == 0:
        logger.warning("Không có bản ghi có cả human_label và llm_label hợp lệ — bỏ qua confusion matrix")
        return

    from sklearn.metrics import confusion_matrix as sk_confusion_matrix
    y_true = df_eval["human_label"].astype(str).str.strip().str.upper().values
    y_pred = df_eval["llm_label"].astype(str).str.strip().str.upper().values
    cm = sk_confusion_matrix(y_true, y_pred, labels=labels)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")

    # Colorbar
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel("Số bản ghi", rotation=-90, va="bottom", fontsize=9)

    # Nhãn trục
    tick_marks = np.arange(len(labels))
    ax.set_xticks(tick_marks)
    ax.set_yticks(tick_marks)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_yticklabels(labels, fontsize=11)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")

    # Ghi số vào ô
    thresh = cm.max() / 2.0
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(
                j, i, format(cm[i, j], "d"),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black",
                fontsize=13, fontweight="bold",
            )

    ax.set_ylabel("Nhãn thực (Human Label)", fontsize=11)
    ax.set_xlabel("Nhãn dự đoán (LLM Label)", fontsize=11)
    ax.set_title(
        f"Confusion Matrix — LLM vs Human\n(n={len(df_eval)} bản ghi đánh giá)",
        fontsize=12, fontweight="bold", pad=15,
    )

    # Tính accuracy và hiển thị
    accuracy = cm.diagonal().sum() / cm.sum() if cm.sum() > 0 else 0
    ax.text(
        0.98, -0.15, f"Accuracy = {accuracy:.2%}",
        ha="right", va="top", transform=ax.transAxes,
        fontsize=10, color="#333",
    )

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ Confusion Matrix → {output_path}")


# ─── Biểu đồ 3: Impact Score Bar ─────────────────────────────────────────────
def plot_impact_score_bar(df_report: pd.DataFrame, output_path: Path):
    """
    Vẽ biểu đồ cột ngang Impact Score cho từng điều khoản.
    """
    if "ImpactScore_i" not in df_report.columns:
        logger.warning("Không tìm thấy cột 'ImpactScore_i' — bỏ qua biểu đồ Impact Score")
        return

    df_plot = df_report[df_report["ImpactScore_i"].notna()].copy()
    df_plot = df_plot.sort_values("ImpactScore_i", ascending=True)

    # Giới hạn số lượng hiển thị
    if len(df_plot) > 30:
        logger.info(f"Có {len(df_plot)} điều khoản — chỉ hiển thị top 30 (theo |ImpactScore| lớn nhất)")
        df_plot = df_plot.reindex(
            df_plot["ImpactScore_i"].abs().nlargest(30).index
        ).sort_values("ImpactScore_i", ascending=True)

    fig_height = max(6, len(df_plot) * 0.45)
    fig, ax = plt.subplots(figsize=(12, fig_height))

    scores = df_plot["ImpactScore_i"].values
    labels_col = (
        df_plot.get("legal_citation", df_plot.get("source_id", pd.Series(range(len(df_plot)))))
        .astype(str).str[:35]
    )
    final_labels = df_plot.get("final_label", pd.Series(["UNKNOWN"] * len(df_plot))).astype(str).str.upper()

    bar_colors = [COLORS.get(lbl, "#888") for lbl in final_labels]

    bars = ax.barh(
        range(len(df_plot)), scores,
        color=bar_colors, edgecolor="white", linewidth=0.5, height=0.7,
    )
    ax.set_yticks(range(len(df_plot)))
    ax.set_yticklabels(labels_col.values, fontsize=8)
    ax.axvline(0, color="black", linewidth=1.0, linestyle="-")

    # Ghi giá trị
    for bar, score in zip(bars, scores):
        width = bar.get_width()
        x_pos = width + 0.005 if width >= 0 else width - 0.005
        ax.text(
            x_pos,
            bar.get_y() + bar.get_height() / 2,
            f"{score:+.3f}",
            va="center",
            ha="left" if width >= 0 else "right",
            fontsize=7.5, fontweight="bold",
        )

    ax.set_xlabel("Impact Score (hướng × trọng số × C_i_norm)", fontsize=10)
    ax.set_title(
        "Biểu đồ Impact Score tất định theo từng điều khoản\n"
        "(Màu: ■ BENEFIT  ■ COST  ■ CONSTRAINT)",
        fontsize=12, fontweight="bold", pad=12,
    )

    # Legend thủ công
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS["BENEFIT"], label="BENEFIT (+)"),
        Patch(facecolor=COLORS["COST"], label="COST (-)"),
        Patch(facecolor=COLORS["CONSTRAINT"], label="CONSTRAINT (-)"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9, framealpha=0.9)

    # Tổng
    total_score = scores.sum()
    ax.text(
        0.98, 0.02,
        f"Tổng Impact Score = {total_score:+.4f}",
        ha="right", va="bottom", transform=ax.transAxes,
        fontsize=10, fontweight="bold", color="#333",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#aaa", alpha=0.9),
    )

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ Impact Score Bar → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Bước 7: Xuất biểu đồ phân tích (label distribution, confusion matrix, impact score)"
    )
    parser.add_argument("--config", type=Path, default=PROJECT_ROOT / "config" / "project_config.yaml")
    parser.add_argument("--labeled-file", type=Path, default=None)
    parser.add_argument("--report-file", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    logger.info(f"{'='*65}")
    logger.info(f"  BƯỚC 7: XUẤT BIỂU ĐỒ VÀ BÁO CÁO")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*65}")

    config = load_config(args.config)
    processed_dir = PROJECT_ROOT / config["paths"]["processed_data"]
    reports_dir = PROJECT_ROOT / config["paths"]["reports"]
    figures_dir = PROJECT_ROOT / config["paths"]["figures"]

    labeled_path = args.labeled_file or (processed_dir / config["processed_files"]["final_labeled_dataset"])
    report_path = args.report_file or (reports_dir / config["report_files"]["final_impact_report"])
    out_dir = args.output_dir or figures_dir

    # ── Biểu đồ 1 + 2: Cần final_labeled_dataset ─────────────────────────────
    if labeled_path.exists():
        df_labeled = pd.read_excel(labeled_path)
        logger.info(f"Đọc labeled dataset: {len(df_labeled)} bản ghi")

        plot_label_distribution(
            df_labeled,
            out_dir / config["figure_files"]["label_distribution"],
        )
        plot_confusion_matrix(
            df_labeled,
            out_dir / config["figure_files"]["confusion_matrix"],
        )
    else:
        logger.warning(f"Không tìm thấy: {labeled_path} — bỏ qua biểu đồ 1 và 2")

    # ── Biểu đồ 3: Cần final_impact_report ───────────────────────────────────
    if report_path.exists():
        try:
            df_report = pd.read_excel(report_path, sheet_name="Chi tiết Impact Score")
            logger.info(f"Đọc impact report: {len(df_report)} bản ghi")
            plot_impact_score_bar(
                df_report,
                out_dir / config["figure_files"]["impact_score_bar"],
            )
        except Exception as e:
            logger.warning(f"Lỗi đọc report cho biểu đồ 3: {e}")
    else:
        logger.warning(f"Không tìm thấy: {report_path} — bỏ qua biểu đồ impact score")

    logger.info(f"")
    logger.info(f"✅ BƯỚC 7 HOÀN TẤT — Pipeline hoàn thành!")
    logger.info(f"   Thư mục biểu đồ: {out_dir}")
    logger.info(f"")
    logger.info(f"   TÓM TẮT FILE ĐẦU RA:")
    logger.info(f"   data/interim/impact_true_records.xlsx")
    logger.info(f"   data/interim/manual_label_template.xlsx")
    logger.info(f"   data/interim/human_labeled_dataset.xlsx  ← điền thủ công")
    logger.info(f"   data/processed/llm_labeled_dataset.xlsx")
    logger.info(f"   data/processed/final_labeled_dataset.xlsx")
    logger.info(f"   data/interim/scoring_input.xlsx          ← điền thủ công")
    logger.info(f"   data/reports/classification_metrics.xlsx")
    logger.info(f"   data/reports/final_impact_report.xlsx")
    logger.info(f"   outputs/figures/label_distribution.png")
    logger.info(f"   outputs/figures/confusion_matrix.png")
    logger.info(f"   outputs/figures/impact_score_bar.png")


if __name__ == "__main__":
    main()
