"""
src/00_common/metric_utils.py
=============================
Tính toán metric đánh giá LLM dùng chung cho cả 2 tầng pipeline.

Lý do tách ra module riêng:
    - Đảm bảo cả tầng 1 (env) và tầng 2 (5-label) dùng cùng cách tính metric
    - Dễ kiểm tra (unit test) từng hàm metric độc lập
    - Khi cần thêm metric mới, chỉ sửa ở đây

QUAN TRỌNG:
    - Tất cả metric phải được tính trên (human_label, llm_label)
    - KHÔNG BAO GIỜ tính metric trên (human_label, final_label)
    - Xem docs/adjudication_protocol.md và docs/metric_definition.md
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


# =============================================================================
# TẦNG 1 — Metric lọc môi trường (Binary Classification)
# =============================================================================

def compute_env_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
) -> Dict:
    """
    Tính toàn bộ metric cho Tầng 1 (lọc môi trường).
    
    Args:
        y_true: Series nhãn human (env_human), giá trị 0/1
        y_pred: Series nhãn LLM (env_llm), giá trị 0/1
    
    Returns:
        Dict chứa: accuracy_env, precision_env, recall_env, f1_env,
                   human_correction_rate_env, confusion_matrix_2x2,
                   n_total, n_valid, n_agree, n_disagree
    
    Lưu ý:
        - positive class = 1 (có tác động môi trường)
        - Recall quan trọng hơn Precision trong ngữ cảnh này
    """
    # Chỉ tính trên các bản ghi có cả 2 nhãn hợp lệ
    mask = y_true.notna() & y_pred.notna()
    y_t = y_true[mask].astype(int)
    y_p = y_pred[mask].astype(int)
    
    n_total = len(y_true)
    n_valid = int(mask.sum())
    n_agree = int((y_t == y_p).sum())
    n_disagree = n_valid - n_agree
    
    if n_valid == 0:
        return {
            "accuracy_env": None,
            "precision_env": None,
            "recall_env": None,
            "f1_env": None,
            "human_correction_rate_env": None,
            "confusion_matrix_2x2": None,
            "n_total": n_total,
            "n_valid": 0,
            "n_agree": 0,
            "n_disagree": 0,
            "warning": "Không có bản ghi hợp lệ để tính metric"
        }
    
    cm = confusion_matrix(y_t, y_p, labels=[0, 1])
    acc = accuracy_score(y_t, y_p)
    prec = precision_score(y_t, y_p, pos_label=1, zero_division=0)
    rec = recall_score(y_t, y_p, pos_label=1, zero_division=0)
    f1 = f1_score(y_t, y_p, pos_label=1, zero_division=0)
    hcr = 1 - acc  # Human Correction Rate
    
    # Confusion matrix dạng dict rõ ràng
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)
    
    return {
        "accuracy_env": round(acc, 4),
        "precision_env": round(prec, 4),
        "recall_env": round(rec, 4),
        "f1_env": round(f1, 4),
        "human_correction_rate_env": round(hcr, 4),
        "confusion_matrix_2x2": {
            "TN": int(tn), "FP": int(fp),
            "FN": int(fn), "TP": int(tp)
        },
        "n_total": n_total,
        "n_valid": n_valid,
        "n_agree": n_agree,
        "n_disagree": n_disagree,
    }


# =============================================================================
# TẦNG 2 — Metric phân loại 5 nhãn (Multi-class)
# =============================================================================

LABEL_ORDER = [
    "BENEFIT_QUANTITATIVE",
    "BENEFIT_QUALITATIVE",
    "COST_QUANTITATIVE",
    "COST_QUALITATIVE",
    "CONSTRAINT",
]


def compute_class_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
    label_order: Optional[List[str]] = None,
) -> Dict:
    """
    Tính toàn bộ metric cho Tầng 2 (phân loại 5 nhãn).
    
    Args:
        y_true: Series nhãn human (class_human), giá trị là tên nhãn đầy đủ
        y_pred: Series nhãn LLM (class_llm)
        label_order: Thứ tự nhãn trong confusion matrix (mặc định: LABEL_ORDER)
    
    Returns:
        Dict chứa: accuracy_class, precision/recall/f1 per class, macro_f1,
                   human_correction_rate_class, confusion_matrix_5x5, support, ...
    """
    if label_order is None:
        label_order = LABEL_ORDER
    
    # Chỉ tính trên các bản ghi có cả 2 nhãn hợp lệ và nhãn nằm trong label_order
    mask = y_true.isin(label_order) & y_pred.isin(label_order)
    y_t = y_true[mask]
    y_p = y_pred[mask]
    
    n_total = len(y_true)
    n_valid = int(mask.sum())
    n_agree = int((y_t == y_p).sum())
    n_disagree = n_valid - n_agree
    
    if n_valid == 0:
        return {
            "accuracy_class": None,
            "macro_f1_class": None,
            "human_correction_rate_class": None,
            "n_total": n_total,
            "n_valid": 0,
            "n_agree": 0,
            "n_disagree": 0,
            "warning": "Không có bản ghi hợp lệ để tính metric"
        }
    
    acc = accuracy_score(y_t, y_p)
    macro_f1 = f1_score(y_t, y_p, labels=label_order, average="macro", zero_division=0)
    hcr = 1 - acc
    
    # Per-class metrics
    per_class = {}
    for label in label_order:
        mask_label = y_t == label
        support_k = int(mask_label.sum())
        if support_k == 0:
            per_class[label] = {
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
                "support": 0
            }
            continue
        
        # Binary: label vs rest
        y_t_bin = (y_t == label).astype(int)
        y_p_bin = (y_p == label).astype(int)
        
        per_class[label] = {
            "precision": round(float(precision_score(y_t_bin, y_p_bin, zero_division=0)), 4),
            "recall":    round(float(recall_score(y_t_bin, y_p_bin, zero_division=0)), 4),
            "f1":        round(float(f1_score(y_t_bin, y_p_bin, zero_division=0)), 4),
            "support":   support_k
        }
    
    # Confusion matrix 5x5
    labels_present = [l for l in label_order if l in y_t.values or l in y_p.values]
    cm = confusion_matrix(y_t, y_p, labels=label_order)
    
    return {
        "accuracy_class": round(acc, 4),
        "macro_f1_class": round(macro_f1, 4),
        "human_correction_rate_class": round(hcr, 4),
        "per_class": per_class,
        "confusion_matrix_5x5": cm.tolist(),
        "confusion_matrix_labels": label_order,
        "n_total": n_total,
        "n_valid": n_valid,
        "n_agree": n_agree,
        "n_disagree": n_disagree,
    }


# =============================================================================
# End-to-End Accuracy
# =============================================================================

def compute_end_to_end_accuracy(
    env_human: pd.Series,
    env_llm: pd.Series,
    class_human: pd.Series,
    class_llm: pd.Series,
    source_ids: Optional[pd.Series] = None,
) -> Dict:
    """
    Tính End-to-end Accuracy: LLM đúng cả Tầng 1 VÀ Tầng 2.
    
    Định nghĩa:
        Bản ghi đúng e2e khi:
        - env_human = 0: env_llm == env_human (lọc đúng)
        - env_human = 1: env_llm == env_human AND class_llm == class_human
    
    Args:
        env_human, env_llm: Nhãn tầng 1 (0/1)
        class_human, class_llm: Nhãn tầng 2 (tên nhãn đầy đủ)
        source_ids: ID bản ghi (tùy chọn, để truy vết)
    
    Returns:
        Dict: accuracy_e2e, n_correct_e2e, n_total, n_env_correct, n_class_correct
    """
    n = len(env_human)
    
    # Normalize env labels
    eh = env_human.apply(lambda x: 1 if str(x).strip().lower() in ("1", "true") else 0)
    el = env_llm.apply(lambda x: 1 if str(x).strip().lower() in ("1", "true") else 0)
    
    env_correct = (eh == el)
    
    # Chỉ tính class cho bản ghi env_human = 1
    class_correct = pd.Series(False, index=eh.index)
    env1_mask = eh == 1
    if env1_mask.sum() > 0:
        class_correct[env1_mask] = (class_human[env1_mask] == class_llm[env1_mask])
    
    # e2e đúng: env đúng VÀ (nếu env_human=0: ok, nếu env_human=1: class cũng đúng)
    e2e_correct = env_correct & ((eh == 0) | (class_correct))
    
    acc_e2e = float(e2e_correct.mean())
    
    return {
        "accuracy_e2e": round(acc_e2e, 4),
        "n_correct_e2e": int(e2e_correct.sum()),
        "n_env_correct": int(env_correct.sum()),
        "n_class_correct_given_env1": int(class_correct[env1_mask].sum()) if env1_mask.sum() > 0 else 0,
        "n_env1": int(env1_mask.sum()),
        "n_total": n,
    }


# =============================================================================
# Tiện ích xuất báo cáo
# =============================================================================

def metrics_to_dataframe(metrics_env: Dict, metrics_class: Dict, metrics_e2e: Dict) -> pd.DataFrame:
    """
    Tổng hợp tất cả metric vào một DataFrame dạng bảng để xuất Excel.
    
    Returns:
        pd.DataFrame: Cột [Metric, Tầng, Giá trị, Mô tả]
    """
    rows = []
    
    # Tầng 1
    for key in ["accuracy_env", "precision_env", "recall_env", "f1_env", "human_correction_rate_env"]:
        rows.append({
            "Metric": key,
            "Tầng": "1 — Env Filter",
            "Giá trị": metrics_env.get(key),
            "Mô tả": f"N_valid={metrics_env.get('n_valid')}, N_disagree={metrics_env.get('n_disagree')}"
        })
    
    # Tầng 2 — tổng
    for key in ["accuracy_class", "macro_f1_class", "human_correction_rate_class"]:
        rows.append({
            "Metric": key,
            "Tầng": "2 — 5-Label",
            "Giá trị": metrics_class.get(key),
            "Mô tả": f"N_valid={metrics_class.get('n_valid')}, N_disagree={metrics_class.get('n_disagree')}"
        })
    
    # Tầng 2 — per class
    for label, m in (metrics_class.get("per_class") or {}).items():
        rows.append({
            "Metric": f"F1_{label[:3]}",
            "Tầng": "2 — Per Class",
            "Giá trị": m.get("f1"),
            "Mô tả": f"Support={m.get('support')}, P={m.get('precision')}, R={m.get('recall')}"
        })
    
    # End-to-end
    rows.append({
        "Metric": "accuracy_e2e",
        "Tầng": "E2E",
        "Giá trị": metrics_e2e.get("accuracy_e2e"),
        "Mô tả": f"N_correct={metrics_e2e.get('n_correct_e2e')}/{metrics_e2e.get('n_total')}"
    })
    
    return pd.DataFrame(rows)
