#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
09_build_final_labeled_dataset.py
===================================
BƯỚC 9 — Xây dựng final_labeled_dataset sau adjudication.

Logic chính theo docs/adjudication_protocol.md:
    - Metric LLM đã được tính ở script 08 bằng class_human vs class_llm.
    - Bước này KHÔNG tính lại metric LLM bằng final_label.
    - final_label được chốt từ review_decision nếu bản ghi cần adjudication.
    - Bản ghi bất đồng class_human != class_llm bắt buộc phải có review_decision.
"""

import logging
import sys
from pathlib import Path

import pandas as pd
import yaml

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
ALIAS_MAP = {
    "BQ": "BENEFIT_QUANTITATIVE", "BQL": "BENEFIT_QUALITATIVE",
    "CQ": "COST_QUANTITATIVE", "CQL": "COST_QUALITATIVE", "CON": "CONSTRAINT",
}
VALID_REVIEW_DECISIONS = {
    "KEEP_HUMAN",
    "ACCEPT_LLM",
    "NEW_LABEL",
    "AMBIGUOUS_KEEP_HUMAN",
    "NEED_EXPERT_REVIEW",
    "NO_REVIEW_AGREEMENT",
}
REVIEW_COLUMNS = [
    "review_decision", "review_final_label", "final_reason", "review_note",
    "error_type", "reviewer", "reviewed_at", "class_needs_review",
]


def load_config():
    with open(PROJECT_ROOT / "config" / "project_config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_blank(val) -> bool:
    return val is None or pd.isna(val) or str(val).strip() == ""


def first_nonblank(*values):
    for val in values:
        if not is_blank(val):
            return val
    return None


def normalize_label(val) -> str | None:
    if is_blank(val):
        return None
    s = str(val).strip().upper()
    if s in LABEL_ORDER:
        return s
    return ALIAS_MAP.get(s)


def normalize_decision(val) -> str | None:
    if is_blank(val):
        return None
    s = str(val).strip().upper()
    return s if s in VALID_REVIEW_DECISIONS else s


def ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df


def infer_error_type(row: pd.Series) -> str:
    human = row.get("class_human_norm")
    llm = row.get("class_llm_norm")
    if human == llm:
        return "NO_ERROR_AGREEMENT"
    pair = {human, llm}
    if pair == {"COST_QUALITATIVE", "CONSTRAINT"}:
        return "LLM_CQL_CON_CONFUSION"
    if llm in {"COST_QUANTITATIVE", "BENEFIT_QUANTITATIVE"} and human != llm:
        return "LLM_QUANTITATIVE_OVERDETECTION"
    if llm in {"BENEFIT_QUANTITATIVE", "BENEFIT_QUALITATIVE"} and human not in {"BENEFIT_QUANTITATIVE", "BENEFIT_QUALITATIVE"}:
        return "LLM_BENEFIT_OVERDETECTION"
    return "LLM_MISREAD_LEGAL_SIGNAL"


def merge_review_file(df: pd.DataFrame, review_path: Path) -> pd.DataFrame:
    """Merge quyết định adjudication từ class_review_dataset.xlsx nếu có."""
    df = ensure_columns(df, REVIEW_COLUMNS)
    if not review_path.exists():
        logger.warning(f"  ⚠️  Không tìm thấy {review_path.name}; các dòng bất đồng sẽ yêu cầu review_decision trong file human nếu có.")
        return df

    review = pd.read_excel(review_path, dtype=str)
    if "source_id" not in review.columns:
        logger.warning(f"  ⚠️  {review_path.name} không có source_id, bỏ qua merge review.")
        return df

    rename_map = {}
    if "final_label" in review.columns:
        rename_map["final_label"] = "review_final_label"
    review = review.rename(columns=rename_map)

    review_cols = [c for c in REVIEW_COLUMNS if c in review.columns]
    if not review_cols:
        logger.warning(f"  ⚠️  {review_path.name} chưa có cột adjudication; hãy tạo lại script 08 hoặc bổ sung thủ công.")
        return df

    review_small = review[["source_id"] + review_cols].copy()
    review_small = review_small.rename(columns={c: f"{c}__review" for c in review_cols})
    df = df.merge(review_small, on="source_id", how="left")
    for col in review_cols:
        review_col = f"{col}__review"
        df[col] = df.apply(lambda r: first_nonblank(r.get(review_col), r.get(col), ""), axis=1)
        df = df.drop(columns=[review_col])
    return df


def resolve_final_label(row: pd.Series) -> tuple[str | None, str, str, bool]:
    human = row.get("class_human_norm")
    llm = row.get("class_llm_norm")
    decision = normalize_decision(row.get("review_decision"))
    reviewed_label = normalize_label(row.get("review_final_label"))
    is_disagreement = human != llm

    if not is_disagreement and decision is None:
        return human, "NO_REVIEW_AGREEMENT", "Human và LLM đồng thuận; chấp nhận nhanh theo adjudication protocol.", False

    if is_disagreement and decision is None:
        return None, "", "", True

    if decision == "KEEP_HUMAN":
        return human, decision, first_nonblank(row.get("final_reason"), "Giữ class_human vì reviewer xác nhận human đúng, LLM sai."), False
    if decision == "ACCEPT_LLM":
        return llm, decision, first_nonblank(row.get("final_reason"), "Chấp nhận class_llm vì reviewer xác nhận nhãn human ban đầu sai."), False
    if decision == "NEW_LABEL":
        return reviewed_label, decision, first_nonblank(row.get("final_reason"), "Reviewer chọn nhãn mới vì cả human và LLM chưa phù hợp."), reviewed_label is None
    if decision == "AMBIGUOUS_KEEP_HUMAN":
        return human, decision, first_nonblank(row.get("final_reason"), "Bản ghi còn mơ hồ; tạm giữ class_human và đánh dấu cần review."), False
    if decision == "NEED_EXPERT_REVIEW":
        final_label = reviewed_label or human
        return final_label, decision, first_nonblank(row.get("final_reason"), "Cần chuyên gia review; tạm giữ nhãn tốt nhất hiện có."), final_label is None
    if decision == "NO_REVIEW_AGREEMENT":
        return human, decision, first_nonblank(row.get("final_reason"), "Human và LLM đồng thuận; chấp nhận nhanh theo adjudication protocol."), human is None

    return None, str(decision or ""), first_nonblank(row.get("final_reason"), "review_decision không hợp lệ."), True


def main():
    cfg = load_config()

    logger.info("=" * 60)
    logger.info("  BƯỚC 9 — Xây dựng final_labeled_dataset sau adjudication")
    logger.info("=" * 60)

    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_data"]

    class_cfg = cfg.get("classification", {})
    human_col = class_cfg.get("human_label_column", "class_human")
    llm_col = class_cfg.get("llm_label_column", "class_llm")
    final_col = class_cfg.get("final_label_column", "final_label")

    class_human_path = interim_dir / cfg["interim_files"]["class_human_labeled_dataset"]
    class_llm_path = interim_dir / cfg["interim_files"]["class_llm_labeled_dataset"]
    class_review_path = interim_dir / cfg["interim_files"].get("class_review_dataset", "class_review_dataset.xlsx")
    env_final_path = processed_dir / cfg["processed_files"]["env_final_dataset"]

    for p in [class_human_path, env_final_path]:
        if not p.exists():
            logger.error(f"Không tìm thấy: {p}")
            sys.exit(1)

    logger.info("[Bước 9.1] Đọc dữ liệu")
    df = pd.read_excel(class_human_path, dtype=str)
    df_env = pd.read_excel(env_final_path, dtype=str)
    logger.info(f"  class_human: {len(df)}, env_final: {len(df_env)}")

    if class_llm_path.exists():
        df_llm = pd.read_excel(class_llm_path, dtype=str)
        llm_merge_cols = ["source_id"] + [c for c in [
            llm_col, "class_llm_reason", "class_evidence_span", "class_confidence",
            "class_needs_human_review", "rule_applied", "quantity_interpretation",
            "class_llm_error"
        ] if c in df_llm.columns and c not in df.columns]
        df = df.merge(df_llm[llm_merge_cols], on="source_id", how="left")
    else:
        logger.warning(f"  ⚠️  Không tìm thấy {class_llm_path.name}; không thể kiểm tra bất đồng với LLM.")

    df = ensure_columns(df, REVIEW_COLUMNS)
    df = merge_review_file(df, class_review_path)

    logger.info("[Bước 9.2] Chốt final_label theo review_decision")
    df["class_human_norm"] = df[human_col].apply(normalize_label)
    df["class_llm_norm"] = df[llm_col].apply(normalize_label) if llm_col in df.columns else None
    df["is_disagreement"] = df["class_human_norm"] != df["class_llm_norm"]

    resolved = df.apply(resolve_final_label, axis=1, result_type="expand")
    resolved.columns = [final_col, "review_decision_resolved", "final_reason_resolved", "needs_adjudication_fix"]
    df[final_col] = resolved[final_col]
    df["review_decision"] = resolved["review_decision_resolved"]
    df["final_reason"] = df.apply(lambda r: first_nonblank(r.get("final_reason"), r.get("final_reason_resolved"), ""), axis=1)
    df["needs_adjudication_fix"] = resolved["needs_adjudication_fix"].astype(bool)
    df["error_type"] = df.apply(lambda r: first_nonblank(r.get("error_type"), infer_error_type(r)), axis=1)

    # Với trường hợp mơ hồ/chuyên gia, giữ cờ cần review.
    df["class_needs_review"] = df.apply(
        lambda r: "TRUE" if str(r.get("review_decision", "")).upper() in {"AMBIGUOUS_KEEP_HUMAN", "NEED_EXPERT_REVIEW"} else first_nonblank(r.get("class_needs_review"), "FALSE"),
        axis=1,
    )

    invalid_final = df[~df[final_col].isin(LABEL_ORDER)].copy()
    missing_disagreement_review = df[df["is_disagreement"] & df["needs_adjudication_fix"]].copy()
    missing_final_reason = df[df["is_disagreement"] & df["final_reason"].apply(is_blank)].copy()

    if len(invalid_final) > 0 or len(missing_disagreement_review) > 0 or len(missing_final_reason) > 0:
        logger.error("  ❌ Chưa đạt điều kiện xuất final_labeled_dataset theo adjudication_protocol.md")
        if len(invalid_final) > 0:
            logger.error(f"  - final_label thiếu/không hợp lệ: {len(invalid_final)} dòng. Ví dụ: {invalid_final['source_id'].head(10).tolist()}")
        if len(missing_disagreement_review) > 0:
            logger.error(f"  - Bất đồng thiếu review_decision/final_label: {len(missing_disagreement_review)} dòng. Ví dụ: {missing_disagreement_review['source_id'].head(10).tolist()}")
        if len(missing_final_reason) > 0:
            logger.error(f"  - Bất đồng thiếu final_reason: {len(missing_final_reason)} dòng. Ví dụ: {missing_final_reason['source_id'].head(10).tolist()}")
        logger.error(f"  Hãy mở {class_review_path.name}, điền review_decision/final_label/final_reason, rồi chạy lại bước 9.")
        sys.exit(1)

    df = df.drop(columns=["review_decision_resolved", "final_reason_resolved"], errors="ignore")

    label_dist = df[final_col].value_counts()
    n_disagree = int(df["is_disagreement"].sum())
    logger.info(f"""
  ─── PHÂN PHỐI FINAL_LABEL ────────────────────────────
{label_dist.to_string()}

  Tổng: {len(df)}
  Bất đồng đã kiểm tra: {n_disagree}
  Thiếu final_label: {int(df[final_col].isna().sum())}
  ─────────────────────────────────────────────────────
""")

    output_path = processed_dir / cfg["processed_files"]["final_labeled_dataset"]
    processed_dir.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)
    logger.info(f"  ✅ final_labeled_dataset.xlsx ({len(df)} dòng)")

    logger.info("")
    logger.info("=" * 60)
    logger.info("  HOÀN THÀNH — Bước tiếp theo:")
    logger.info("  py src/09b_build_actor_domain_review.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
