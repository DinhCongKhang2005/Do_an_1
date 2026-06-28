#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_compare_llm_vs_human.py
===========================
BƯỚC 4 — So sánh nhãn LLM với nhãn người và tính các chỉ số phân loại.

Đề tài: Đánh giá tác động chính sách môi trường — Phiên bản không tranh biện
Tác giả: Đinh Công Khang — MI3380 Đồ án 1

Pipeline:
  Input:  data/processed/llm_labeled_dataset.xlsx  (có cột llm_label)
          data/interim/human_labeled_dataset.xlsx   (có cột human_label)
  Output:
    - data/reports/classification_metrics.xlsx
    - data/processed/final_labeled_dataset.xlsx  (nhãn cuối = human_label nếu có)

Chỉ số tính:
  - Accuracy
  - Precision (weighted, macro, per-class)
  - Recall (weighted, macro, per-class)
  - F1 (weighted, macro, per-class)
  - Macro F1
  - Confusion Matrix

Sử dụng:
  python src/04_compare_llm_vs_human.py
  python src/04_compare_llm_vs_human.py --help
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

# ─── Đường dẫn gốc dự án ─────────────────────────────────────────────────────
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

VALID_LABELS = ["BENEFIT", "COST", "CONSTRAINT"]


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def merge_llm_and_human(df_llm: pd.DataFrame, df_human: pd.DataFrame) -> pd.DataFrame:
    """
    Ghép nhãn LLM và nhãn người dựa trên source_id.
    Trả về DataFrame gộp.
    """
    if "source_id" not in df_llm.columns or "source_id" not in df_human.columns:
        logger.warning("Không tìm thấy cột 'source_id' — thử ghép theo chỉ số dòng")
        df_merged = df_llm.copy()
        if "human_label" in df_human.columns:
            min_len = min(len(df_llm), len(df_human))
            df_merged = df_merged.iloc[:min_len].copy()
            df_merged["human_label"] = df_human["human_label"].values[:min_len]
            df_merged["human_reason"] = df_human.get("human_reason", pd.Series([""] * min_len)).values[:min_len]
        return df_merged

    if "human_label" not in df_human.columns:
        logger.warning("File nhãn người không có cột 'human_label' — không thể tính metrics.")
        return df_llm.copy()

    # Nếu file LLM được tạo từ human_labeled_dataset.xlsx thì nó đã có sẵn
    # các cột human_*. Loại bỏ bản cũ trước khi merge để tránh sinh
    # human_label_x/human_label_y và làm mất tên cột chuẩn.
    stale_human_cols = [
        c for c in ("human_label", "human_reason", "labeler_name")
        if c in df_llm.columns
    ]
    df_llm_base = df_llm.drop(columns=stale_human_cols) if stale_human_cols else df_llm

    # Ghép theo source_id
    human_cols = ["source_id", "human_label"]
    if "human_reason" in df_human.columns:
        human_cols.append("human_reason")
    if "labeler_name" in df_human.columns:
        human_cols.append("labeler_name")

    df_human_sub = df_human[[c for c in human_cols if c in df_human.columns]]
    df_merged = df_llm_base.merge(df_human_sub, on="source_id", how="left")
    logger.info(f"Ghép nhãn người: {df_merged['human_label'].notna().sum()}/{len(df_merged)} bản ghi có nhãn người")

    return df_merged


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, labels: list) -> dict:
    """
    Tính toán toàn bộ các chỉ số phân loại.
    """
    # Chỉ xét các bản ghi có cả hai nhãn hợp lệ
    mask = pd.Series(y_true).isin(labels) & pd.Series(y_pred).isin(labels)
    y_true_f = y_true[mask]
    y_pred_f = y_pred[mask]

    if len(y_true_f) == 0:
        logger.error("Không có bản ghi nào có cả human_label và llm_label hợp lệ!")
        return {}

    accuracy = accuracy_score(y_true_f, y_pred_f)
    f1_macro = f1_score(y_true_f, y_pred_f, average="macro", zero_division=0, labels=labels)
    f1_weighted = f1_score(y_true_f, y_pred_f, average="weighted", zero_division=0, labels=labels)
    precision_macro = precision_score(y_true_f, y_pred_f, average="macro", zero_division=0, labels=labels)
    recall_macro = recall_score(y_true_f, y_pred_f, average="macro", zero_division=0, labels=labels)

    # Chỉ số theo từng nhãn
    report_dict = classification_report(
        y_true_f, y_pred_f, labels=labels, output_dict=True, zero_division=0
    )

    # Confusion Matrix
    cm = confusion_matrix(y_true_f, y_pred_f, labels=labels)

    return {
        "n_evaluated": int(len(y_true_f)),
        "n_total": int(len(y_true)),
        "accuracy": round(float(accuracy), 4),
        "f1_macro": round(float(f1_macro), 4),
        "f1_weighted": round(float(f1_weighted), 4),
        "precision_macro": round(float(precision_macro), 4),
        "recall_macro": round(float(recall_macro), 4),
        "per_class": report_dict,
        "confusion_matrix": cm.tolist(),
        "labels": labels,
        "y_true": y_true_f.tolist(),
        "y_pred": y_pred_f.tolist(),
    }


def print_metrics_summary(metrics: dict):
    """In tóm tắt chỉ số phân loại ra console."""
    logger.info(f"\n{'='*60}")
    logger.info(f"  KẾT QUẢ SO SÁNH LLM vs HUMAN")
    logger.info(f"{'='*60}")
    logger.info(f"  Số bản ghi đánh giá: {metrics['n_evaluated']}/{metrics['n_total']}")
    logger.info(f"  Accuracy:            {metrics['accuracy']:.4f}")
    logger.info(f"  F1 Macro:            {metrics['f1_macro']:.4f}")
    logger.info(f"  F1 Weighted:         {metrics['f1_weighted']:.4f}")
    logger.info(f"  Precision Macro:     {metrics['precision_macro']:.4f}")
    logger.info(f"  Recall Macro:        {metrics['recall_macro']:.4f}")
    logger.info(f"")
    logger.info(f"  Theo nhãn:")
    for label in metrics["labels"]:
        pc = metrics["per_class"].get(label, {})
        logger.info(
            f"    {label:<12}: P={pc.get('precision', 0):.3f}  "
            f"R={pc.get('recall', 0):.3f}  "
            f"F1={pc.get('f1-score', 0):.3f}  "
            f"n={int(pc.get('support', 0))}"
        )
    logger.info(f"")
    logger.info(f"  Confusion Matrix ({'/'.join(metrics['labels'])}):")
    cm = np.array(metrics["confusion_matrix"])
    for i, label in enumerate(metrics["labels"]):
        row_str = "  ".join(f"{v:>4}" for v in cm[i])
        logger.info(f"    {label:<12}: {row_str}")
    logger.info(f"{'='*60}\n")


def export_metrics_excel(metrics: dict, output_path: Path):
    """Xuất chỉ số phân loại ra file Excel nhiều sheet."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Sheet 1: Tổng hợp
    summary_rows = [
        {"Chỉ số": "Số bản ghi đánh giá", "Giá trị": metrics["n_evaluated"]},
        {"Chỉ số": "Số bản ghi tổng", "Giá trị": metrics["n_total"]},
        {"Chỉ số": "Accuracy", "Giá trị": metrics["accuracy"]},
        {"Chỉ số": "F1 Macro", "Giá trị": metrics["f1_macro"]},
        {"Chỉ số": "F1 Weighted", "Giá trị": metrics["f1_weighted"]},
        {"Chỉ số": "Precision Macro", "Giá trị": metrics["precision_macro"]},
        {"Chỉ số": "Recall Macro", "Giá trị": metrics["recall_macro"]},
    ]
    df_summary = pd.DataFrame(summary_rows)

    # Sheet 2: Per-class metrics
    per_class_rows = []
    for label in metrics["labels"]:
        pc = metrics["per_class"].get(label, {})
        per_class_rows.append({
            "Nhãn": label,
            "Precision": round(pc.get("precision", 0), 4),
            "Recall": round(pc.get("recall", 0), 4),
            "F1-score": round(pc.get("f1-score", 0), 4),
            "Support": int(pc.get("support", 0)),
        })
    df_per_class = pd.DataFrame(per_class_rows)

    # Sheet 3: Confusion Matrix
    labels = metrics["labels"]
    cm = np.array(metrics["confusion_matrix"])
    df_cm = pd.DataFrame(cm, index=[f"True_{l}" for l in labels], columns=[f"Pred_{l}" for l in labels])

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_summary.to_excel(writer, index=False, sheet_name="Tổng hợp")
        df_per_class.to_excel(writer, index=False, sheet_name="Chi tiết theo nhãn")
        df_cm.to_excel(writer, sheet_name="Confusion Matrix")

        # Format
        for sheet_name in writer.sheets:
            ws = writer.sheets[sheet_name]
            ws.column_dimensions["A"].width = 25
            ws.column_dimensions["B"].width = 15

    logger.info(f"Đã xuất metrics → {output_path}")


def build_final_labeled_dataset(df_merged: pd.DataFrame) -> pd.DataFrame:
    """
    Tạo final_labeled_dataset với final_label = human_label nếu có, ngược lại dùng llm_label.
    """
    df = df_merged.copy()

    def resolve_label(row):
        human = str(row.get("human_label", "")).strip().upper()
        if human in ("BENEFIT", "COST", "CONSTRAINT"):
            return human, "human"
        llm = str(row.get("llm_label", "")).strip().upper()
        if llm in ("BENEFIT", "COST", "CONSTRAINT"):
            return llm, "llm"
        return "UNKNOWN", "none"

    final_labels = []
    label_sources = []
    for _, row in df.iterrows():
        lbl, src = resolve_label(row)
        final_labels.append(lbl)
        label_sources.append(src)

    df["final_label"] = final_labels
    df["final_label_source"] = label_sources  # "human" hoặc "llm"
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Bước 4: So sánh nhãn LLM vs nhãn người, tính metrics phân loại"
    )
    parser.add_argument("--config", type=Path, default=PROJECT_ROOT / "config" / "project_config.yaml")
    parser.add_argument("--llm-file", type=Path, default=None, help="File LLM labeled dataset")
    parser.add_argument("--human-file", type=Path, default=None, help="File human labeled dataset")
    parser.add_argument("--output-metrics", type=Path, default=None, help="File output metrics Excel")
    parser.add_argument("--output-final", type=Path, default=None, help="File output final labeled dataset")
    args = parser.parse_args()

    logger.info(f"{'='*65}")
    logger.info(f"  BƯỚC 4: SO SÁNH LLM vs HUMAN — TÍNH METRICS")
    logger.info(f"  Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*65}")

    config = load_config(args.config)
    interim_dir = PROJECT_ROOT / config["paths"]["interim_data"]
    processed_dir = PROJECT_ROOT / config["paths"]["processed_data"]
    reports_dir = PROJECT_ROOT / config["paths"]["reports"]

    llm_path = args.llm_file or (processed_dir / config["processed_files"]["llm_labeled_dataset"])
    human_path = args.human_file or (interim_dir / config["interim_files"]["human_labeled_dataset"])
    metrics_path = args.output_metrics or (reports_dir / config["report_files"]["classification_metrics"])
    final_path = args.output_final or (processed_dir / config["processed_files"]["final_labeled_dataset"])

    # ── Kiểm tra file ─────────────────────────────────────────────────────────
    if not llm_path.exists():
        logger.error(f"Không tìm thấy file LLM: {llm_path}")
        logger.error("Chạy trước: python src/03_llm_classify.py")
        sys.exit(1)

    df_llm = pd.read_excel(llm_path)
    logger.info(f"Đọc LLM dataset: {len(df_llm)} bản ghi từ {llm_path}")

    if not human_path.exists():
        logger.warning(f"Không tìm thấy file nhãn người: {human_path}")
        logger.warning("Sẽ chỉ xuất final_labeled_dataset mà không tính metrics so sánh.")
        df_merged = df_llm.copy()
        df_merged["human_label"] = ""
        df_merged["human_reason"] = ""
    else:
        df_human = pd.read_excel(human_path)
        logger.info(f"Đọc human dataset: {len(df_human)} bản ghi từ {human_path}")
        df_merged = merge_llm_and_human(df_llm, df_human)

    # ── Tính metrics nếu có nhãn người ────────────────────────────────────────
    has_human_labels = (
        "human_label" in df_merged.columns
        and df_merged["human_label"].notna().any()
        and df_merged["human_label"].str.strip().str.upper().isin(VALID_LABELS).any()
    )

    if has_human_labels and "llm_label" in df_merged.columns:
        y_true = df_merged["human_label"].str.strip().str.upper().fillna("").values
        y_pred = df_merged["llm_label"].str.strip().str.upper().fillna("").values

        metrics = compute_metrics(y_true, y_pred, VALID_LABELS)
        if metrics:
            print_metrics_summary(metrics)
            export_metrics_excel(metrics, metrics_path)
    else:
        logger.warning("Chưa có đủ nhãn người để tính metrics. Bỏ qua bước so sánh.")
        logger.warning("Điền nhãn người vào data/interim/human_labeled_dataset.xlsx rồi chạy lại.")

    # ── Tạo final_labeled_dataset ─────────────────────────────────────────────
    df_final = build_final_labeled_dataset(df_merged)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_excel(final_path, index=False, engine="openpyxl")
    logger.info(f"Đã xuất final_labeled_dataset → {final_path}")

    logger.info(f"")
    logger.info(f"✅ BƯỚC 4 HOÀN TẤT")
    logger.info(f"   BƯỚC TIẾP THEO:")
    logger.info(f"   python src/05_build_scoring_input.py")


if __name__ == "__main__":
    main()
