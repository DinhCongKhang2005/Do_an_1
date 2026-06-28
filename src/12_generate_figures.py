#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12_generate_figures.py
========================
BƯỚC 12 — Tạo biểu đồ phân tích Impact Score.

Đề tài: Đánh giá tác động chính sách môi trường — Khung định lượng chi phí,
lợi ích, rủi ro.

Vị trí trong pipeline:
    Bước 11 : Tính scored_dataset.xlsx, scoring_summary.xlsx và
              final_impact_report.xlsx.
    Bước 12 : Tạo các biểu đồ trực quan hóa Impact Score.
    Bước 13 : Tổng hợp báo cáo pipeline cuối cùng.

Input:
    data/processed/scored_dataset.xlsx
        Dataset đã có M_i, S_i, D_i, R_i, W_i, C_i, C_i_norm, direction_i và
        ImpactScore_i.

Output:
    outputs/figures/impact_score_histogram.png
    outputs/figures/impact_score_by_label.png
    outputs/figures/impact_score_by_domain.png
    outputs/figures/impact_score_by_actor.png
    outputs/figures/impact_score_by_impact_signal.png
    outputs/figures/score_component_distribution.png

Tài liệu và cấu hình liên quan:
    - config/project_config.yaml
    - data/processed/scored_dataset.xlsx
    - data/reports/scoring_summary.xlsx

Biểu đồ được tạo:
    1. impact_score_histogram.png:
       Phân phối ImpactScore_i, tách phần điểm dương/âm/trung tính.
    2. impact_score_by_label.png:
       Phân phối ImpactScore_i theo final_label.
    3. impact_score_by_domain.png:
       Impact Score trung bình theo domain_primary đã chuẩn hóa; nếu thiếu thì
       fallback về domain raw.
    4. impact_score_by_actor.png:
       Impact Score trung bình theo actor_group đã chuẩn hóa; nếu thiếu thì
       fallback về actor raw.
    5. impact_score_by_impact_signal.png:
       Impact Score trung bình theo tín hiệu tác động/pháp lý. Script ưu tiên
       cột legal_signal; nếu thiếu thì dùng tin_hieu_tac_dong.
    6. score_component_distribution.png:
       Phân phối điểm thành phần M_i, S_i, D_i, R_i.

Cơ chế hoạt động:
    1. Đọc scored_dataset.xlsx.
    2. Ép các cột điểm về dạng số để vẽ biểu đồ ổn định.
    3. Tạo từng biểu đồ bằng matplotlib/seaborn.
    4. Lưu ảnh vào outputs/figures theo tên cấu hình trong project_config.yaml.

Ý nghĩa phương pháp:
    Các biểu đồ không thay đổi kết quả tính điểm. Chúng giúp người nghiên cứu
    kiểm tra phân phối tác động, phát hiện nhóm nhãn/domain/actor có điểm bất
    thường, và đưa hình ảnh minh họa vào báo cáo.

Sử dụng:
    py src/12_generate_figures.py
    py src/12_generate_figures.py --dpi 300

Bước tiếp theo:
    py src/13_generate_pipeline_summary.py
"""

import argparse
import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from textwrap import fill

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# ─── Cài đặt style mặc định ───────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 18,
    "axes.titleweight": "bold",
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.dpi": 200,
    "savefig.dpi": 300,
    "savefig.facecolor": "white",
})
sns.set_theme(style="whitegrid", context="notebook")

LABEL_SHORT = {
    "BENEFIT_QUANTITATIVE": "BQ",
    "BENEFIT_QUALITATIVE":  "BQL",
    "COST_QUANTITATIVE":    "CQ",
    "COST_QUALITATIVE":     "CQL",
    "CONSTRAINT":           "CON",
}
LABEL_COLORS = {
    "BENEFIT_QUANTITATIVE": "#2B6CB0",
    "BENEFIT_QUALITATIVE":  "#2F855A",
    "COST_QUANTITATIVE":    "#C53030",
    "COST_QUALITATIVE":     "#DD6B20",
    "CONSTRAINT":           "#805AD5",
}

LABEL_DISPLAY = {
    "BQ": "Lợi ích\nđịnh lượng\n(BQ)",
    "BQL": "Lợi ích\nđịnh tính\n(BQL)",
    "CQ": "Chi phí\nđịnh lượng\n(CQ)",
    "CQL": "Chi phí\nđịnh tính\n(CQL)",
    "CON": "Ràng buộc\n(CON)",
}


def load_config():
    with open(PROJECT_ROOT / "config" / "project_config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_figure(fig, path: Path, dpi: int = 300):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    logger.info(f"  ✅ {path.name}")


def polish_axes(ax, xgrid: bool = False, ygrid: bool = True):
    ax.set_facecolor("white")
    if ygrid:
        ax.grid(axis="y", color="#D9D9D9", linewidth=0.9, alpha=0.8)
    if xgrid:
        ax.grid(axis="x", color="#D9D9D9", linewidth=0.9, alpha=0.8)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#BDBDBD")
    ax.spines["bottom"].set_color("#BDBDBD")
    ax.tick_params(axis="both", colors="#333333")


def add_zero_line(ax):
    ax.axhline(y=0, color="#D32F2F", linestyle="--", linewidth=1.4, alpha=0.85)


def wrap_labels(labels, width=34):
    return [fill(str(label), width=width) for label in labels]


def first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def ensure_required_columns(df: pd.DataFrame, columns: list[str]):
    missing = [col for col in columns if col not in df.columns]
    if missing:
        logger.error(f"scored_dataset.xlsx thiếu cột bắt buộc cho bước 12: {', '.join(missing)}")
        sys.exit(1)


def annotate_barh(ax, bars, values, counts=None):
    values = list(values)
    counts = list(counts) if counts is not None else None
    if not values:
        return
    max_abs = max(abs(float(v)) for v in values) or 1.0
    offset = max_abs * 0.025
    for idx, (bar, val) in enumerate(zip(bars, values)):
        text = f"{val:+.3f}"
        if counts is not None:
            text += f" (n={int(counts[idx])})"
        if val >= 0:
            x = val + offset
            ha = "left"
        else:
            x = val - offset
            ha = "right"
        ax.text(x, bar.get_y() + bar.get_height() / 2, text,
                va="center", ha=ha, fontsize=10.5, color="#222222")


# ==============================================================================
# Figure 1: Histogram ImpactScore
# ==============================================================================

def fig_impact_histogram(df: pd.DataFrame, output_path: Path, dpi: int):
    fig, ax = plt.subplots(figsize=(11, 6.5), constrained_layout=True)

    scores = df["ImpactScore_i"].astype(float).dropna()

    bins = np.linspace(-1, 1, 31)
    ax.hist(scores[scores > 0], bins=bins, color="#2F855A", alpha=0.82,
            edgecolor="white", linewidth=0.7, label="Tích cực (>0)")
    ax.hist(scores[scores < 0], bins=bins, color="#C53030", alpha=0.82,
            edgecolor="white", linewidth=0.7, label="Tiêu cực (<0)")
    ax.hist(scores[scores == 0], bins=bins, color="#718096", alpha=0.82,
            edgecolor="white", linewidth=0.7, label="Trung tính (=0)")

    ax.axvline(x=0, color="#111111", linestyle="--", linewidth=1.4, label="x=0")
    ax.axvline(x=scores.mean(), color="#2B6CB0", linestyle=":", linewidth=2.0,
               label=f"Mean={scores.mean():+.3f}")

    ax.set_xlabel("ImpactScore_i")
    ax.set_ylabel("Số điều khoản")
    ax.set_title(f"Phân phối Impact Score (N={len(scores)})")
    ax.set_xlim(-1.02, 1.02)
    ax.legend(frameon=True, facecolor="white", edgecolor="#D9D9D9", loc="upper left")
    polish_axes(ax)

    save_figure(fig, output_path, dpi)


# ==============================================================================
# Figure 2: ImpactScore theo nhãn (box + strip)
# ==============================================================================

def fig_impact_by_label(df: pd.DataFrame, output_path: Path, dpi: int):
    df_plot = df.copy()
    df_plot["label_short"] = df_plot["final_label"].map(LABEL_SHORT)
    df_plot["ImpactScore_i"] = df_plot["ImpactScore_i"].astype(float)
    df_plot = df_plot[df_plot["label_short"].notna() & df_plot["ImpactScore_i"].notna()].copy()

    all_label_order = ["BQ", "BQL", "CQ", "CQL", "CON"]
    palette = {v: LABEL_COLORS[k] for k, v in LABEL_SHORT.items()}
    counts = df_plot["label_short"].value_counts().reindex(all_label_order, fill_value=0)
    label_order = [label for label in all_label_order if counts[label] > 0]
    empty_labels = [label for label in all_label_order if counts[label] == 0]
    if not label_order:
        logger.warning("  ⚠️  Không có dữ liệu final_label để vẽ")
        return
    tick_labels = [f"{LABEL_DISPLAY[label]}\nn={counts[label]}" for label in label_order]

    fig, ax = plt.subplots(figsize=(12, 7.2), constrained_layout=True)
    sns.boxplot(data=df_plot, x="label_short", y="ImpactScore_i",
                hue="label_short", order=label_order, hue_order=label_order,
                palette=palette, width=0.48, ax=ax, linewidth=1.4,
                fliersize=4, legend=False)
    sns.stripplot(data=df_plot, x="label_short", y="ImpactScore_i",
                  order=label_order, color="#111111", alpha=0.28, size=3.2,
                  jitter=0.18, ax=ax)

    add_zero_line(ax)
    ax.set_xlabel("Nhãn tác động cuối cùng (final_label)")
    ax.set_ylabel("ImpactScore_i")
    ax.set_title("Phân phối Impact Score theo nhãn tác động")
    ax.set_xticks(range(len(label_order)))
    ax.set_xticklabels(tick_labels)
    ax.set_ylim(-1.05, 1.05)
    polish_axes(ax)

    means = df_plot.groupby("label_short")["ImpactScore_i"].mean()
    for i, label in enumerate(label_order):
        mean_val = means[label]
        ax.scatter(i, mean_val, marker="D", s=54, color="white",
                   edgecolor="#111111", linewidth=1.1, zorder=5)
        y_text = min(mean_val + 0.08, 0.96) if mean_val >= 0 else max(mean_val - 0.08, -0.96)
        va = "bottom" if mean_val >= 0 else "top"
        ax.text(i, y_text, f"mean={mean_val:+.3f}", ha="center", va=va,
                fontsize=10.5, color="#222222",
                bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                          edgecolor="#D9D9D9", alpha=0.9))
    if empty_labels:
        empty_text = ", ".join(empty_labels)
        ax.text(0.01, 0.03, f"Không có bản ghi: {empty_text}",
                transform=ax.transAxes, ha="left", va="bottom", fontsize=10.5,
                color="#666666",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor="#D9D9D9", alpha=0.92))

    save_figure(fig, output_path, dpi)


# ==============================================================================
# Figure 3: ImpactScore theo domain
# ==============================================================================

def fig_impact_by_domain(df: pd.DataFrame, output_path: Path, dpi: int):
    domain_col = "domain_primary" if "domain_primary" in df.columns else "domain"
    if domain_col not in df.columns:
        logger.warning("  ⚠️  Không có cột domain/domain_primary, bỏ qua fig_impact_by_domain")
        return

    df_plot = df[df[domain_col].notna() & (df[domain_col].astype(str).str.strip() != "")].copy()
    df_plot["ImpactScore_i"] = df_plot["ImpactScore_i"].astype(float)

    domain_summary = (
        df_plot.groupby(domain_col)["ImpactScore_i"]
        .agg(mean="mean", count="count")
        .sort_values("mean", ascending=True)
    )
    if domain_summary.empty:
        logger.warning("  ⚠️  Không có dữ liệu domain để vẽ")
        return

    fig, ax = plt.subplots(figsize=(12, max(6, len(domain_summary) * 0.58)), constrained_layout=True)
    colors = ["#2F855A" if v >= 0 else "#C53030" for v in domain_summary["mean"]]
    bars = ax.barh(domain_summary.index, domain_summary["mean"], color=colors, alpha=0.8)
    annotate_barh(ax, bars, domain_summary["mean"], domain_summary["count"])

    ax.axvline(x=0, color="#111111", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Mean ImpactScore")
    ax.set_title("Impact Score trung bình theo Domain môi trường")
    ax.set_yticks(range(len(domain_summary.index)))
    ax.set_yticklabels(wrap_labels(domain_summary.index, width=32))
    max_abs = max(abs(domain_summary["mean"].min()), abs(domain_summary["mean"].max()), 0.2)
    ax.set_xlim(-max_abs * 1.22, max_abs * 1.22)
    polish_axes(ax, xgrid=True, ygrid=False)

    save_figure(fig, output_path, dpi)


# ==============================================================================
# Figure 4: ImpactScore theo actor
# ==============================================================================

def fig_impact_by_actor(df: pd.DataFrame, output_path: Path, dpi: int):
    actor_col = "actor_group" if "actor_group" in df.columns else "actor"
    if actor_col not in df.columns:
        return

    df_plot = df[df[actor_col].notna() & (df[actor_col].astype(str).str.strip() != "")].copy()
    df_plot["ImpactScore_i"] = df_plot["ImpactScore_i"].astype(float)

    actor_summary = (
        df_plot.groupby(actor_col)["ImpactScore_i"]
        .agg(mean="mean", count="count")
        .sort_values("count", ascending=False)
        .head(15)  # Top 15 actor phổ biến nhất
    )
    if actor_summary.empty:
        logger.warning("  ⚠️  Không có dữ liệu actor để vẽ")
        return

    actor_summary = actor_summary.sort_values("mean", ascending=True)
    fig, ax = plt.subplots(figsize=(12, max(6, len(actor_summary) * 0.56)), constrained_layout=True)
    colors = ["#2F855A" if v >= 0 else "#C53030" for v in actor_summary["mean"]]
    bars = ax.barh(actor_summary.index, actor_summary["mean"], color=colors, alpha=0.8)
    annotate_barh(ax, bars, actor_summary["mean"], actor_summary["count"])

    ax.axvline(x=0, color="#111111", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Mean ImpactScore")
    ax.set_title("Impact Score trung bình theo Actor Group")
    ax.set_yticks(range(len(actor_summary.index)))
    ax.set_yticklabels(wrap_labels(actor_summary.index, width=34))
    max_abs = max(abs(actor_summary["mean"].min()), abs(actor_summary["mean"].max()), 0.2)
    ax.set_xlim(-max_abs * 1.22, max_abs * 1.22)
    polish_axes(ax, xgrid=True, ygrid=False)

    save_figure(fig, output_path, dpi)


# ==============================================================================
# Figure 5: ImpactScore theo tín hiệu tác động/pháp lý
# ==============================================================================

def fig_impact_by_impact_signal(df: pd.DataFrame, output_path: Path, dpi: int):
    signal_col = first_existing_column(df, ["legal_signal", "tin_hieu_tac_dong", "impact_signal"])
    if signal_col is None:
        logger.warning("  ⚠️  Không có cột legal_signal/tin_hieu_tac_dong, bỏ qua fig_impact_by_impact_signal")
        return

    df_plot = df[df[signal_col].notna() & (df[signal_col].astype(str).str.strip() != "")].copy()
    df_plot["ImpactScore_i"] = df_plot["ImpactScore_i"].astype(float)
    df_plot["impact_signal_plot_source"] = df_plot[signal_col].astype(str).str.strip()

    max_categories = 20
    value_counts = df_plot["impact_signal_plot_source"].value_counts()
    if len(value_counts) > max_categories:
        top_signals = set(value_counts.head(max_categories - 1).index)
        df_plot["legal_signal_plot"] = np.where(
            df_plot["impact_signal_plot_source"].isin(top_signals),
            df_plot["impact_signal_plot_source"],
            "OTHER_SIGNALS",
        )
        logger.info(
            f"  {signal_col} có {len(value_counts)} nhóm; hiển thị top {max_categories - 1} và gom phần còn lại vào OTHER_SIGNALS"
        )
    else:
        df_plot["legal_signal_plot"] = df_plot["impact_signal_plot_source"]

    signal_summary = (
        df_plot.groupby("legal_signal_plot")["ImpactScore_i"]
        .agg(mean="mean", count="count")
        .sort_values("mean", ascending=True)
    )
    if signal_summary.empty:
        logger.warning("  ⚠️  Không có dữ liệu tín hiệu tác động/pháp lý để vẽ")
        return

    fig, ax = plt.subplots(figsize=(12, max(5, len(signal_summary) * 0.58)), constrained_layout=True)
    colors = ["#2F855A" if v >= 0 else "#C53030" for v in signal_summary["mean"]]
    bars = ax.barh(signal_summary.index, signal_summary["mean"], color=colors, alpha=0.8)
    annotate_barh(ax, bars, signal_summary["mean"], signal_summary["count"])
    ax.axvline(x=0, color="#111111", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Mean ImpactScore")
    ax.set_title(f"Impact Score theo tín hiệu tác động/pháp lý ({signal_col})")
    ax.set_yticks(range(len(signal_summary.index)))
    ax.set_yticklabels(wrap_labels(signal_summary.index, width=34))
    max_abs = max(abs(signal_summary["mean"].min()), abs(signal_summary["mean"].max()), 0.2)
    ax.set_xlim(-max_abs * 1.22, max_abs * 1.22)
    polish_axes(ax, xgrid=True, ygrid=False)

    save_figure(fig, output_path, dpi)


# ==============================================================================
# Figure 6: Phân phối điểm thành phần M, S, D, R
# ==============================================================================

def fig_score_component_distribution(df: pd.DataFrame, output_path: Path, dpi: int):
    dims = ["M_i", "S_i", "D_i", "R_i"]
    dim_labels = ["Magnitude (M)", "Scope (S)", "Duration (D)", "Risk (R)"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    axes = axes.flatten()
    colors = ["#2196F3", "#FF9800", "#4CAF50", "#F44336"]

    for i, (dim, label, color) in enumerate(zip(dims, dim_labels, colors)):
        if dim not in df.columns:
            continue
        vals = pd.to_numeric(df[dim], errors="coerce").dropna()
        counts = vals.value_counts().sort_index()

        axes[i].bar(counts.index, counts.values, color=color, alpha=0.8,
                    edgecolor="white", linewidth=1.0)
        axes[i].set_xticks([1, 2, 3, 4, 5])
        axes[i].set_xlabel("Điểm (1–5)")
        axes[i].set_ylabel("Số điều khoản")
        axes[i].set_title(f"{label}\nMean={vals.mean():.2f}, Median={vals.median():.0f}")
        axes[i].set_ylim(0, max(counts.max() * 1.16, 1))
        polish_axes(axes[i])

        # Thêm số trên mỗi cột
        for x, y in zip(counts.index, counts.values):
            axes[i].text(x, y + max(counts.max() * 0.025, 0.2), str(y),
                         ha="center", fontsize=10, color="#222222")

    fig.suptitle("Phân phối điểm thành phần M, S, D, R", fontsize=18, fontweight="bold")
    save_figure(fig, output_path, dpi)


# ==============================================================================
# Main
# ==============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dpi", type=int, default=300, help="DPI cho output figures")
    args = parser.parse_args()

    cfg = load_config()

    logger.info("=" * 60)
    logger.info("  BƯỚC 12 — Tạo biểu đồ Impact Score")
    logger.info("=" * 60)

    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_data"]
    figure_dir    = PROJECT_ROOT / cfg["paths"]["figures"]

    scored_path = processed_dir / cfg["processed_files"]["scored_dataset"]
    if not scored_path.exists():
        logger.error(f"Không tìm thấy: {scored_path}. Chạy script 11 trước!")
        sys.exit(1)

    logger.info(f"[Bước 12.1] Đọc: {scored_path.name}")
    df = pd.read_excel(scored_path, dtype=str)
    ensure_required_columns(df, ["ImpactScore_i", "final_label", "M_i", "S_i", "D_i", "R_i"])

    # Convert numeric columns
    for col in ["ImpactScore_i", "C_i", "C_i_norm", "M_i", "S_i", "D_i", "R_i", "W_i"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    logger.info(f"  → {len(df)} bản ghi")
    logger.info("")
    logger.info("[Bước 12.2] Vẽ biểu đồ...")

    fig_keys = cfg.get("figure_files", {})
    dpi = args.dpi

    fig_impact_histogram(df, figure_dir / fig_keys.get("impact_score_histogram", "impact_score_histogram.png"), dpi)
    fig_impact_by_label(df, figure_dir / fig_keys.get("impact_score_by_label", "impact_score_by_label.png"), dpi)
    fig_impact_by_domain(df, figure_dir / fig_keys.get("impact_score_by_domain", "impact_score_by_domain.png"), dpi)
    fig_impact_by_actor(df, figure_dir / fig_keys.get("impact_score_by_actor", "impact_score_by_actor.png"), dpi)
    signal_fig_name = fig_keys.get(
        "impact_score_by_impact_signal",
        fig_keys.get("impact_score_by_legal_signal", "impact_score_by_impact_signal.png"),
    )
    fig_impact_by_impact_signal(df, figure_dir / signal_fig_name, dpi)
    fig_score_component_distribution(df, figure_dir / fig_keys.get("score_component_distribution", "score_component_distribution.png"), dpi)

    logger.info("")
    logger.info("=" * 60)
    logger.info("  HOÀN THÀNH — Tất cả biểu đồ đã được lưu")
    logger.info(f"  Thư mục: {figure_dir}")
    logger.info(f"  Bước tiếp theo: py src/13_generate_pipeline_summary.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

