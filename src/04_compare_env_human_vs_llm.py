#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_compare_env_human_vs_llm.py
================================
BƯỚC 4 — So sánh env_human và env_llm, tính metric Tầng 1.

Đề tài: Đánh giá tác động chính sách môi trường — Pipeline 2 tầng
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Vị trí trong pipeline:
    Input:  data/interim/env_human_labeled_dataset.xlsx  (từ người nghiên cứu)
            data/interim/env_llm_labeled_dataset.xlsx    (từ script 03)
    Output: data/reports/env_filter_metrics.xlsx
            data/reports/env_error_analysis.xlsx
            data/interim/env_review_dataset.xlsx
            outputs/figures/env_confusion_matrix.png
            outputs/figures/env_metric_summary.png
    Tiếp theo: [Human review env_review_dataset.xlsx] → Script 05

QUAN TRỌNG — Nguyên tắc bất di bất dịch:
    - Metric được tính DỰA TRÊN env_human vs env_llm
    - KHÔNG dùng final_label để tính metric LLM
    - env_review_dataset chứa các bản ghi cần adjudication → Human review
    - CHỈ SAU KHI chạy script này, human mới được phép sửa nhãn

Metrics tính:
    - Confusion Matrix 2×2
    - Accuracy_env, Precision_env, Recall_env, F1_env
    - Human Correction Rate
    - Error Analysis: loại lỗi FP và FN phổ biến nhất

Sử dụng:
    py src/04_compare_env_human_vs_llm.py
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Backend không cần GUI
import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score
)

# ─── Project root ──────────────────────────────────────────────────────────────
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


# ==============================================================================
# Load config
# ==============================================================================

def load_config():
    with open(PROJECT_ROOT / "config" / "project_config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize_env_label(val) -> int | None:
    """Chuẩn hóa giá trị nhãn env về 0 hoặc 1."""
    if val is None or (isinstance(val, float) and str(val) == "nan"):
        return None
    s = str(val).strip().lower()
    if s in ("1", "true"):
        return 1
    elif s in ("0", "false"):
        return 0
    return None


# ==============================================================================
# Tính metric
# ==============================================================================

def compute_metrics(y_true, y_pred) -> dict:
    """Tính toàn bộ metric binary classification."""
    n = len(y_true)
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, pos_label=1, zero_division=0)
    rec = recall_score(y_true, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label=1, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)
    
    return {
        "N":                    n,
        "Accuracy_env":         round(acc, 4),
        "Precision_env":        round(prec, 4),
        "Recall_env":           round(rec, 4),
        "F1_env":               round(f1, 4),
        "HCR_env":              round(1 - acc, 4),
        "TP":                   int(tp),
        "TN":                   int(tn),
        "FP":                   int(fp),
        "FN":                   int(fn),
        "N_agree":              int(tp + tn),
        "N_disagree":           int(fp + fn),
    }


# ==============================================================================
# Vẽ biểu đồ
# ==============================================================================

def plot_confusion_matrix(y_true, y_pred, output_path: Path):
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=["Pred=0\n(Không MT)", "Pred=1\n(Có MT)"],
        yticklabels=["True=0\n(Không MT)", "True=1\n(Có MT)"],
        ax=ax
    )
    ax.set_title("Confusion Matrix — Tầng 1: Lọc Môi Trường\n(env_human vs env_llm)", fontsize=12)
    ax.set_ylabel("env_human (Human Reference)", fontsize=10)
    ax.set_xlabel("env_llm (LLM Prediction)", fontsize=10)
    
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"  ✅ Lưu figure: {output_path.name}")


def plot_metric_summary(metrics: dict, output_path: Path):
    metric_names = ["Accuracy_env", "Precision_env", "Recall_env", "F1_env"]
    values = [metrics[k] for k in metric_names]
    display_names = ["Accuracy", "Precision\n(pos=1)", "Recall\n(pos=1)", "F1\n(pos=1)"]
    
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(display_names, values, color=["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"], alpha=0.85)
    ax.set_ylim(0, 1.1)
    ax.axhline(y=0.7, color="red", linestyle="--", alpha=0.5, label="Ngưỡng tối thiểu (0.70)")
    
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{val:.4f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    
    ax.set_title(f"Metric Tầng 1 — Lọc Môi Trường (N={metrics['N']})", fontsize=12)
    ax.set_ylabel("Giá trị metric")
    ax.legend()
    
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"  ✅ Lưu figure: {output_path.name}")


# ==============================================================================
# Main
# ==============================================================================

def main():
    cfg = load_config()
    
    logger.info("=" * 60)
    logger.info("  BƯỚC 4 — So sánh env_human vs env_llm (Tầng 1)")
    logger.info("=" * 60)
    logger.info("")
    logger.info("  ⚠️  CẢNH BÁO: Script này phải chạy TRƯỚC khi human review bất kỳ nhãn nào!")
    logger.info("  Metric sẽ phản ánh đúng khả năng của LLM khi chưa có can thiệp.")
    logger.info("")
    
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    report_dir = PROJECT_ROOT / cfg["paths"]["reports"]
    figure_dir = PROJECT_ROOT / cfg["paths"]["figures"]
    
    # ── Đọc dữ liệu ──
    logger.info("[Bước 4.1] Đọc dữ liệu human và LLM")
    
    human_path = interim_dir / cfg["interim_files"]["env_human_labeled_dataset"]
    llm_path = interim_dir / cfg["interim_files"]["env_llm_labeled_dataset"]
    
    if not human_path.exists():
        logger.error(f"File human chưa có: {human_path}")
        logger.error("Hãy hoàn thành việc gán nhãn env_human trước!")
        sys.exit(1)
    
    if not llm_path.exists():
        logger.error(f"File LLM chưa có: {llm_path}")
        logger.error("Chạy script 03 trước!")
        sys.exit(1)
    
    df_human = pd.read_excel(human_path, dtype=str)
    df_llm = pd.read_excel(llm_path, dtype=str)
    
    logger.info(f"  Human: {len(df_human)} bản ghi")
    logger.info(f"  LLM:   {len(df_llm)} bản ghi")
    
    # ── Merge ──
    logger.info("[Bước 4.2] Merge dữ liệu theo source_id")
    env_filter_cfg = cfg.get("env_filter", {})
    human_col = env_filter_cfg.get("human_label_column", "env_human")
    llm_col = env_filter_cfg.get("llm_label_column", "env_llm")
    
    df = df_human.merge(
        df_llm[["source_id", llm_col, "env_llm_reason", "env_evidence_span",
                "env_confidence", "env_needs_human_review", "env_llm_domain", "env_llm_error"]],
        on="source_id", how="inner"
    )
    logger.info(f"  → Sau merge: {len(df)} bản ghi")
    
    # ── Normalize nhãn ──
    df["y_human"] = df[human_col].apply(normalize_env_label)
    df["y_llm"]   = df[llm_col].apply(normalize_env_label)
    
    df_valid = df.dropna(subset=["y_human", "y_llm"]).copy()
    df_invalid = df[df["y_human"].isna() | df["y_llm"].isna()]
    
    logger.info(f"  → Bản ghi hợp lệ: {len(df_valid)}")
    if len(df_invalid) > 0:
        logger.warning(f"  ⚠️  Bản ghi thiếu nhãn (bỏ qua khi tính metric): {len(df_invalid)}")
    
    y_human = df_valid["y_human"].astype(int)
    y_llm = df_valid["y_llm"].astype(int)
    
    # ── Tính metric ──
    logger.info("[Bước 4.3] Tính metric")
    metrics = compute_metrics(y_human, y_llm)
    
    logger.info(f"""
  ─── KẾT QUẢ METRIC TẦNG 1 ───────────────────────────
  N (bản ghi hợp lệ):  {metrics['N']}
  Accuracy_env:         {metrics['Accuracy_env']:.4f}
  Precision_env:        {metrics['Precision_env']:.4f}  (dương tính = có MT)
  Recall_env:           {metrics['Recall_env']:.4f}  ← ưu tiên cao
  F1_env:               {metrics['F1_env']:.4f}
  HumanCorrectionRate:  {metrics['HCR_env']:.4f}
  
  Confusion Matrix (True=row, Pred=col):
    TN={metrics['TN']}  FP={metrics['FP']}
    FN={metrics['FN']}  TP={metrics['TP']}
  
  Đồng thuận:  {metrics['N_agree']} / {metrics['N']}
  Bất đồng:    {metrics['N_disagree']} / {metrics['N']}
  ─────────────────────────────────────────────────────
""")
    
    # ── Review dataset theo adjudication_protocol.md ──
    logger.info("[Bước 4.4] Tạo env_review_dataset (bản ghi cần adjudication)")
    df_valid["is_disagreement"] = y_human.values != y_llm.values
    df_valid["error_type"] = df_valid.apply(
        lambda r: "LLM_FALSE_POSITIVE_ENV" if r["y_llm"] == 1 and r["y_human"] == 0 else "LLM_FALSE_NEGATIVE_ENV" if r["y_llm"] == 0 and r["y_human"] == 1 else "NO_ERROR_AGREEMENT",
        axis=1,
    )
    confidence = pd.to_numeric(df_valid.get("env_confidence"), errors="coerce") if "env_confidence" in df_valid.columns else pd.Series(index=df_valid.index, dtype=float)
    llm_needs_review = df_valid.get("env_needs_human_review", "").astype(str).str.lower().isin(["true", "1", "yes"])
    low_confidence = confidence.notna() & (confidence < 0.60)
    review_mask = df_valid["is_disagreement"] | llm_needs_review | low_confidence
    df_review = df_valid[review_mask].copy()

    def build_review_trigger(row):
        triggers = []
        if bool(row.get("is_disagreement")):
            triggers.append("DISAGREEMENT")
        if str(row.get("env_needs_human_review", "")).lower() in ["true", "1", "yes"]:
            triggers.append("LLM_NEEDS_REVIEW")
        try:
            if pd.notna(row.get("env_confidence")) and float(row.get("env_confidence")) < 0.60:
                triggers.append("LOW_CONFIDENCE")
        except (TypeError, ValueError):
            pass
        return ";".join(triggers)

    df_review["review_trigger"] = df_review.apply(build_review_trigger, axis=1)
    df_review["review_decision"] = ""
    df_review["env_final"] = ""
    df_review["final_reason"] = ""
    df_review["review_note"] = ""
    df_review["error_type"] = df_review.apply(
        lambda r: "LLM_FALSE_POSITIVE_ENV" if r["y_llm"] == 1 and r["y_human"] == 0 else "LLM_FALSE_NEGATIVE_ENV" if r["y_llm"] == 0 and r["y_human"] == 1 else "NO_ERROR_AGREEMENT",
        axis=1,
    )
    df_review["reviewer"] = ""
    df_review["reviewed_at"] = ""
    df_review["env_needs_review"] = df_review.apply(
        lambda r: "TRUE" if "LOW_CONFIDENCE" in str(r.get("review_trigger", "")) or "LLM_NEEDS_REVIEW" in str(r.get("review_trigger", "")) else "FALSE",
        axis=1,
    )

    review_path = interim_dir / cfg["interim_files"]["env_review_dataset"]
    df_review.to_excel(review_path, index=False)
    df_disagree = df_valid[df_valid["is_disagreement"]].copy()
    logger.info(f"  → Bản ghi bất đồng: {len(df_disagree)}")
    logger.info(f"  → Dòng cần review: {len(df_review)}")
    logger.info(f"  → Đã lưu: {review_path.name}")
    logger.info("  → Hãy điền review_decision/env_final/final_reason trước khi chạy bước 5 nếu có bất đồng.")
    
    # ── Error analysis ──
    error_summary = df_disagree["error_type"].value_counts().reset_index()
    error_summary.columns = ["error_type", "count"]
    
    # ── Lưu báo cáo metric ──
    logger.info("[Bước 4.5] Lưu báo cáo metric")
    
    df_metrics = pd.DataFrame([{
        "Metric": k, "Giá trị": v,
        "Thời điểm tính": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "N_valid": metrics["N"]
    } for k, v in metrics.items()])
    
    report_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = report_dir / cfg["report_files"]["env_filter_metrics"]
    
    with pd.ExcelWriter(metrics_path, engine="openpyxl") as writer:
        df_metrics.to_excel(writer, sheet_name="env_metrics", index=False)
        error_summary.to_excel(writer, sheet_name="error_analysis", index=False)
    
    logger.info(f"  ✅ Báo cáo metric: {metrics_path.name}")
    
    # ── Lưu error analysis riêng ──
    error_path = report_dir / cfg["report_files"]["env_error_analysis"]
    df_disagree.to_excel(error_path, index=False)
    logger.info(f"  ✅ Error analysis: {error_path.name}")
    
    # ── Biểu đồ ──
    logger.info("[Bước 4.6] Vẽ biểu đồ")
    plot_confusion_matrix(y_human, y_llm, figure_dir / cfg["figure_files"]["env_confusion_matrix"])
    plot_metric_summary(metrics, figure_dir / cfg["figure_files"]["env_metric_summary"])
    
    # ── Kết luận ──
    logger.info("")
    logger.info("=" * 60)
    logger.info("  HOÀN THÀNH — Bước tiếp theo:")
    logger.info(f"  1. Mở: {review_path.name} ({len(df_disagree)} bản ghi bất đồng)")
    logger.info(f"  2. Review theo docs/adjudication_protocol.md")
    logger.info(f"  3. Điền review_decision/env_final/final_reason trong file review")
    logger.info(f"  4. Chạy: py src/05_build_env_final_dataset.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()



