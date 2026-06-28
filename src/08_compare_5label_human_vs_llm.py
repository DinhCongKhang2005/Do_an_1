#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
08_compare_5label_human_vs_llm.py
====================================
BƯỚC 8 — So sánh class_human và class_llm, tính metric Tầng 2.

Đề tài: Đánh giá tác động chính sách môi trường — Pipeline 2 tầng
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Vị trí trong pipeline:
    Input:  data/interim/class_human_labeled_dataset.xlsx
            data/interim/class_llm_labeled_dataset.xlsx
    Output: data/reports/classification_metrics.xlsx
            data/reports/class_error_analysis.xlsx
            data/interim/class_review_dataset.xlsx
            outputs/figures/confusion_matrix.png
            outputs/figures/normalized_confusion_matrix.png
            outputs/figures/classification_metric_by_label.png
            outputs/figures/top_error_pairs.png
    Bổ sung: End-to-end Accuracy (nếu có env_human, env_llm)
    Tiếp theo: [Human review class_review_dataset] → Script 09

QUAN TRỌNG:
    - Metric được tính class_human vs class_llm (KHÔNG phải final_label)
    - Script này phải chạy TRƯỚC khi human review bất kỳ nhãn nào
    - Xem docs/adjudication_protocol.md

Sử dụng:
    py src/08_compare_5label_human_vs_llm.py
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from sklearn.metrics import (
    accuracy_score, confusion_matrix, f1_score,
    precision_score, recall_score
)

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

LABEL_ORDER = [
    "BENEFIT_QUANTITATIVE", "BENEFIT_QUALITATIVE",
    "COST_QUANTITATIVE", "COST_QUALITATIVE", "CONSTRAINT"
]
LABEL_SHORT = ["BQ", "BQL", "CQ", "CQL", "CON"]
ALIAS_MAP = {
    "BQ": "BENEFIT_QUANTITATIVE", "BQL": "BENEFIT_QUALITATIVE",
    "CQ": "COST_QUANTITATIVE", "CQL": "COST_QUALITATIVE", "CON": "CONSTRAINT",
}


def load_config():
    with open(PROJECT_ROOT / "config" / "project_config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize_label(val) -> str | None:
    if not val or (isinstance(val, float) and str(val) == "nan"):
        return None
    s = str(val).strip().upper()
    if s in LABEL_ORDER:
        return s
    return ALIAS_MAP.get(s)


def compute_per_class_metrics(y_true, y_pred) -> list:
    rows = []
    for label, short in zip(LABEL_ORDER, LABEL_SHORT):
        y_t_bin = (y_true == label).astype(int)
        y_p_bin = (y_pred == label).astype(int)
        support = int(y_t_bin.sum())
        tp = int(((y_t_bin == 1) & (y_p_bin == 1)).sum())
        fp = int(((y_t_bin == 0) & (y_p_bin == 1)).sum())
        fn = int(((y_t_bin == 1) & (y_p_bin == 0)).sum())
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2*prec*rec/(prec+rec) if (prec+rec) > 0 else 0.0
        rows.append({
            "Label": label,
            "Code": short,
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1": round(f1, 4),
            "Support": support,
        })
    return rows


def plot_confusion_matrix_heatmap(y_true, y_pred, output_path: Path, normalize: bool = False):
    cm = confusion_matrix(y_true, y_pred, labels=LABEL_ORDER)
    
    if normalize:
        cm_display = cm.astype(float)
        row_sums = cm.sum(axis=1, keepdims=True)
        cm_display = np.divide(cm_display, row_sums, out=np.zeros_like(cm_display), where=row_sums != 0)
        fmt = ".2f"
        title_suffix = "(Chuẩn hóa theo hàng)"
    else:
        cm_display = cm
        fmt = "d"
        title_suffix = "(Số lượng)"
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm_display, annot=True, fmt=fmt, cmap="Blues",
        xticklabels=LABEL_SHORT,
        yticklabels=LABEL_SHORT,
        ax=ax
    )
    ax.set_title(f"Confusion Matrix 5×5 — Tầng 2 {title_suffix}\n(class_human vs class_llm)", fontsize=11)
    ax.set_ylabel("class_human (Human Reference)", fontsize=10)
    ax.set_xlabel("class_llm (LLM Prediction)", fontsize=10)
    
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"  ✅ Figure: {output_path.name}")


def plot_per_class_metrics(per_class_data: list, output_path: Path):
    labels = [r["Code"] for r in per_class_data]
    prec = [r["Precision"] for r in per_class_data]
    rec = [r["Recall"] for r in per_class_data]
    f1 = [r["F1"] for r in per_class_data]
    
    x = np.arange(len(labels))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width, prec, width, label="Precision", color="#2196F3", alpha=0.85)
    ax.bar(x, rec, width, label="Recall", color="#FF9800", alpha=0.85)
    ax.bar(x + width, f1, width, label="F1", color="#4CAF50", alpha=0.85)
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.axhline(y=0.7, color="red", linestyle="--", alpha=0.4, label="Ngưỡng 0.70")
    ax.set_title("Metric theo từng nhãn — Tầng 2 (5-label)", fontsize=12)
    ax.set_ylabel("Giá trị metric")
    ax.legend()
    
    # Thêm giá trị F1 trên cột
    for xi, fi in zip(x, f1):
        ax.text(xi + width, fi + 0.02, f"{fi:.2f}", ha="center", va="bottom", fontsize=8)
    
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"  ✅ Figure: {output_path.name}")


def plot_top_error_pairs(df_disagree: pd.DataFrame, output_path: Path, top_n: int = 10):
    if len(df_disagree) == 0:
        return
    
    pair_counts = df_disagree.groupby(["y_human", "y_llm"]).size().reset_index(name="count")
    pair_counts = pair_counts.sort_values("count", ascending=False).head(top_n)
    pair_counts["pair"] = pair_counts["y_human"].str[:3] + " → " + pair_counts["y_llm"].str[:3]
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(pair_counts["pair"][::-1], pair_counts["count"][::-1], color="#E91E63", alpha=0.8)
    ax.set_xlabel("Số lần nhầm")
    ax.set_title(f"Top {min(top_n, len(pair_counts))} cặp nhầm lẫn (Human → LLM)", fontsize=11)
    
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"  ✅ Figure: {output_path.name}")


def main():
    cfg = load_config()
    
    logger.info("=" * 60)
    logger.info("  BƯỚC 8 — So sánh class_human vs class_llm (Tầng 2)")
    logger.info("=" * 60)
    logger.info("")
    logger.info("  ⚠️  Script này phải chạy TRƯỚC khi human review bất kỳ nhãn nào!")
    logger.info("")
    
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    report_dir = PROJECT_ROOT / cfg["paths"]["reports"]
    figure_dir = PROJECT_ROOT / cfg["paths"]["figures"]
    
    class_cfg = cfg.get("classification", {})
    human_col = class_cfg.get("human_label_column", "class_human")
    llm_col = class_cfg.get("llm_label_column", "class_llm")
    
    # ── Đọc dữ liệu ──
    human_path = interim_dir / cfg["interim_files"]["class_human_labeled_dataset"]
    llm_path = interim_dir / cfg["interim_files"]["class_llm_labeled_dataset"]
    
    for p in [human_path, llm_path]:
        if not p.exists():
            logger.error(f"Không tìm thấy: {p}")
            sys.exit(1)
    
    logger.info(f"[Bước 8.1] Đọc dữ liệu")
    df_human = pd.read_excel(human_path, dtype=str)
    df_llm = pd.read_excel(llm_path, dtype=str)
    logger.info(f"  Human: {len(df_human)}, LLM: {len(df_llm)}")
    
    # ── Merge ──
    merge_cols = ["source_id", llm_col] + [
        c for c in ["class_llm_reason", "class_evidence_span", "class_confidence",
                     "class_needs_human_review", "rule_applied", "quantity_interpretation",
                     "class_llm_error"] if c in df_llm.columns
    ]
    df = df_human.merge(df_llm[merge_cols], on="source_id", how="inner")
    
    # ── Normalize ──
    df["y_human"] = df[human_col].apply(normalize_label)
    df["y_llm"] = df[llm_col].apply(normalize_label)
    
    df_valid = df.dropna(subset=["y_human", "y_llm"]).copy()
    n_invalid = len(df) - len(df_valid)
    
    logger.info(f"  Hợp lệ: {len(df_valid)}, Thiếu nhãn: {n_invalid}")
    
    y_human = df_valid["y_human"]
    y_llm = df_valid["y_llm"]
    
    # ── Metric tổng ──
    acc = accuracy_score(y_human, y_llm)
    macro_f1 = f1_score(y_human, y_llm, labels=LABEL_ORDER, average="macro", zero_division=0)
    hcr = 1 - acc
    n_agree = int((y_human == y_llm).sum())
    n_disagree = len(df_valid) - n_agree
    
    logger.info(f"""
  ─── KẾT QUẢ METRIC TẦNG 2 ───────────────────────────
  N (hợp lệ):           {len(df_valid)}
  Accuracy_class:        {acc:.4f}
  Macro-F1_class:        {macro_f1:.4f}
  HumanCorrectionRate:   {hcr:.4f}
  Đồng thuận:            {n_agree} / {len(df_valid)}
  Bất đồng:              {n_disagree} / {len(df_valid)}
  ─────────────────────────────────────────────────────
""")
    
    # ── Per-class metrics ──
    per_class = compute_per_class_metrics(y_human, y_llm)
    logger.info("  Per-class F1:")
    for r in per_class:
        logger.info(f"    {r['Code']}: F1={r['F1']:.4f}, P={r['Precision']:.4f}, R={r['Recall']:.4f}, N={r['Support']}")
    
    # ── Review dataset theo adjudication_protocol.md ──
    df_valid["is_disagreement"] = y_human.values != y_llm.values

    confidence = pd.to_numeric(df_valid.get("class_confidence"), errors="coerce") if "class_confidence" in df_valid.columns else pd.Series(index=df_valid.index, dtype=float)
    llm_needs_review = df_valid.get("class_needs_human_review", "").astype(str).str.lower().isin(["true", "1", "yes"])
    high_risk_quant = df_valid["y_human"].isin(["BENEFIT_QUANTITATIVE", "COST_QUANTITATIVE"]) | df_valid["y_llm"].isin(["BENEFIT_QUANTITATIVE", "COST_QUANTITATIVE"])
    low_confidence = confidence.notna() & (confidence < 0.60)

    review_mask = df_valid["is_disagreement"] | llm_needs_review | high_risk_quant | low_confidence
    df_review = df_valid[review_mask].copy()

    def build_review_trigger(row):
        triggers = []
        if bool(row.get("is_disagreement")):
            triggers.append("DISAGREEMENT")
        if str(row.get("class_needs_human_review", "")).lower() in ["true", "1", "yes"]:
            triggers.append("LLM_NEEDS_REVIEW")
        try:
            if pd.notna(row.get("class_confidence")) and float(row.get("class_confidence")) < 0.60:
                triggers.append("LOW_CONFIDENCE")
        except (TypeError, ValueError):
            pass
        if row.get("y_human") in ["BENEFIT_QUANTITATIVE", "COST_QUANTITATIVE"] or row.get("y_llm") in ["BENEFIT_QUANTITATIVE", "COST_QUANTITATIVE"]:
            triggers.append("BQ_CQ_RISK_CHECK")
        return ";".join(triggers)

    def infer_error_type(row):
        if not bool(row.get("is_disagreement")):
            return "NO_ERROR_AGREEMENT"
        pair = {row.get("y_human"), row.get("y_llm")}
        if pair == {"COST_QUALITATIVE", "CONSTRAINT"}:
            return "LLM_CQL_CON_CONFUSION"
        if row.get("y_llm") in {"COST_QUANTITATIVE", "BENEFIT_QUANTITATIVE"} and row.get("y_human") != row.get("y_llm"):
            return "LLM_QUANTITATIVE_OVERDETECTION"
        if row.get("y_llm") in {"BENEFIT_QUANTITATIVE", "BENEFIT_QUALITATIVE"} and row.get("y_human") not in {"BENEFIT_QUANTITATIVE", "BENEFIT_QUALITATIVE"}:
            return "LLM_BENEFIT_OVERDETECTION"
        return "LLM_MISREAD_LEGAL_SIGNAL"

    df_review["review_trigger"] = df_review.apply(build_review_trigger, axis=1)
    df_review["review_decision"] = ""
    df_review["final_label"] = ""
    df_review["final_reason"] = ""
    df_review["review_note"] = ""
    df_review["error_type"] = df_review.apply(infer_error_type, axis=1)
    df_review["reviewer"] = ""
    df_review["reviewed_at"] = ""
    df_review["class_needs_review"] = df_review.apply(
        lambda r: "TRUE" if "LOW_CONFIDENCE" in str(r.get("review_trigger", "")) or "LLM_NEEDS_REVIEW" in str(r.get("review_trigger", "")) else "FALSE",
        axis=1,
    )

    review_path = interim_dir / cfg["interim_files"]["class_review_dataset"]
    df_review.to_excel(review_path, index=False)
    logger.info(f"\n  → Review dataset: {len(df_review)} dòng cần kiểm tra ({n_disagree} bất đồng) → {review_path.name}")
    logger.info("  → Hãy điền review_decision/final_label/final_reason trước khi chạy bước 9.")
    df_disagree = df_valid[df_valid["is_disagreement"]].copy()
    
    # ── Lưu báo cáo ──
    report_dir.mkdir(parents=True, exist_ok=True)
    
    metrics_summary = pd.DataFrame([{
        "Metric": "Accuracy_class", "Giá trị": round(acc, 4), "N": len(df_valid),
        "Thời điểm": datetime.now().strftime("%Y-%m-%d %H:%M")
    }, {
        "Metric": "Macro-F1_class", "Giá trị": round(macro_f1, 4), "N": len(df_valid),
        "Thời điểm": datetime.now().strftime("%Y-%m-%d %H:%M")
    }, {
        "Metric": "HCR_class", "Giá trị": round(hcr, 4), "N": len(df_valid),
        "Thời điểm": datetime.now().strftime("%Y-%m-%d %H:%M")
    }])
    
    metrics_path = report_dir / cfg["report_files"]["classification_metrics"]
    with pd.ExcelWriter(metrics_path, engine="openpyxl") as writer:
        metrics_summary.to_excel(writer, sheet_name="summary", index=False)
        pd.DataFrame(per_class).to_excel(writer, sheet_name="per_class", index=False)
    
    error_path = report_dir / cfg["report_files"]["class_error_analysis"]
    df_disagree.to_excel(error_path, index=False)
    
    logger.info(f"\n[Bước 8.4] Vẽ biểu đồ")
    plot_confusion_matrix_heatmap(y_human, y_llm, figure_dir / cfg["figure_files"]["confusion_matrix"])
    plot_confusion_matrix_heatmap(y_human, y_llm, figure_dir / cfg["figure_files"]["normalized_confusion_matrix"], normalize=True)
    plot_per_class_metrics(per_class, figure_dir / cfg["figure_files"]["classification_metric_by_label"])
    plot_top_error_pairs(df_disagree, figure_dir / cfg["figure_files"]["top_error_pairs"])
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("  HOÀN THÀNH — Bước tiếp theo:")
    logger.info(f"  1. Mở: {review_path.name} ({n_disagree} bản ghi bất đồng)")
    logger.info(f"  2. Review theo docs/adjudication_protocol.md")
    logger.info(f"  3. Điền review_decision/final_label/final_reason trong file review")
    logger.info(f"  4. Chạy: py src/09_build_final_labeled_dataset.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()



