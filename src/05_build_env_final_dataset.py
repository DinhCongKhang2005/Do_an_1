#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_build_env_final_dataset.py
================================
BƯỚC 5 — Xây dựng D_env sau adjudication tầng 1.

Logic theo docs/adjudication_protocol.md:
    - Metric env_human vs env_llm đã được tính ở script 04.
    - Bước này chốt env_final từ review_decision nếu bản ghi cần adjudication.
    - Bản ghi bất đồng env_human != env_llm bắt buộc phải có review_decision.
"""

import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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

VALID_REVIEW_DECISIONS = {
    "KEEP_HUMAN",
    "ACCEPT_LLM",
    "NEW_LABEL",
    "AMBIGUOUS_KEEP_HUMAN",
    "NEED_EXPERT_REVIEW",
    "NO_REVIEW_AGREEMENT",
}
REVIEW_COLUMNS = [
    "review_decision", "review_env_final", "final_reason", "review_note",
    "error_type", "reviewer", "reviewed_at", "env_needs_review",
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


def normalize_env_label(val) -> int | None:
    if is_blank(val):
        return None
    s = str(val).strip().lower()
    if s in ("1", "true", "yes", "có", "co"):
        return 1
    if s in ("0", "false", "no", "không", "khong"):
        return 0
    return None


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


def merge_review_file(df: pd.DataFrame, review_path: Path) -> pd.DataFrame:
    df = ensure_columns(df, REVIEW_COLUMNS)
    if not review_path.exists():
        logger.warning(f"  ⚠️  Không tìm thấy {review_path.name}; các dòng bất đồng sẽ yêu cầu review_decision trong file human nếu có.")
        return df

    review = pd.read_excel(review_path, dtype=str)
    if "source_id" not in review.columns:
        logger.warning(f"  ⚠️  {review_path.name} không có source_id, bỏ qua merge review.")
        return df

    if "env_final" in review.columns:
        review = review.rename(columns={"env_final": "review_env_final"})

    review_cols = [c for c in REVIEW_COLUMNS if c in review.columns]
    if not review_cols:
        logger.warning(f"  ⚠️  {review_path.name} chưa có cột adjudication; hãy tạo lại script 04 hoặc bổ sung thủ công.")
        return df

    review_small = review[["source_id"] + review_cols].copy()
    review_small = review_small.rename(columns={c: f"{c}__review" for c in review_cols})
    df = df.merge(review_small, on="source_id", how="left")
    for col in review_cols:
        review_col = f"{col}__review"
        df[col] = df.apply(lambda r: first_nonblank(r.get(review_col), r.get(col), ""), axis=1)
        df = df.drop(columns=[review_col])
    return df


def resolve_env_final(row: pd.Series) -> tuple[int | None, str, str, bool]:
    human = row.get("env_human_norm")
    llm = row.get("env_llm_norm")
    decision = normalize_decision(row.get("review_decision"))
    reviewed_label = normalize_env_label(row.get("review_env_final"))
    is_disagreement = human != llm

    if not is_disagreement and decision is None:
        return human, "NO_REVIEW_AGREEMENT", "Human và LLM đồng thuận; chấp nhận nhanh theo adjudication protocol.", False

    if is_disagreement and decision is None:
        return None, "", "", True

    if decision == "KEEP_HUMAN":
        return human, decision, first_nonblank(row.get("final_reason"), "Giữ env_human vì reviewer xác nhận human đúng, LLM sai."), False
    if decision == "ACCEPT_LLM":
        return llm, decision, first_nonblank(row.get("final_reason"), "Chấp nhận env_llm vì reviewer xác nhận human ban đầu sai."), False
    if decision == "NEW_LABEL":
        return reviewed_label, decision, first_nonblank(row.get("final_reason"), "Reviewer chọn nhãn mới vì cả human và LLM chưa phù hợp."), reviewed_label is None
    if decision == "AMBIGUOUS_KEEP_HUMAN":
        return human, decision, first_nonblank(row.get("final_reason"), "Bản ghi còn mơ hồ; tạm giữ env_human và đánh dấu cần review."), False
    if decision == "NEED_EXPERT_REVIEW":
        final_label = reviewed_label if reviewed_label is not None else human
        return final_label, decision, first_nonblank(row.get("final_reason"), "Cần chuyên gia review; tạm giữ nhãn tốt nhất hiện có."), final_label is None
    if decision == "NO_REVIEW_AGREEMENT":
        return human, decision, first_nonblank(row.get("final_reason"), "Human và LLM đồng thuận; chấp nhận nhanh theo adjudication protocol."), human is None

    return None, str(decision or ""), first_nonblank(row.get("final_reason"), "review_decision không hợp lệ."), True


def plot_data_funnel(n_total: int, n_env: int, output_path: Path):
    fig, ax = plt.subplots(figsize=(7, 5))
    stages = ["D_impact\n(N tổng)", "D_env\n(env_final=1)"]
    values = [n_total, n_env]
    colors = ["#2196F3", "#4CAF50"]
    bars = ax.barh(stages, values, color=colors, alpha=0.85, height=0.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                f"{val:,} bản ghi ({val / n_total * 100:.1f}%)",
                va="center", fontsize=11, fontweight="bold")
    ax.set_xlabel("Số bản ghi")
    ax.set_title("Pipeline Funnel — Tầng 1: Lọc Môi Trường", fontsize=12)
    ax.set_xlim(0, n_total * 1.25)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info(f"  ✅ Lưu figure: {output_path.name}")


def main():
    cfg = load_config()

    logger.info("=" * 60)
    logger.info("  BƯỚC 5 — Xây dựng D_env sau adjudication")
    logger.info("=" * 60)

    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_data"]
    figure_dir = PROJECT_ROOT / cfg["paths"]["figures"]

    env_filter_cfg = cfg.get("env_filter", {})
    human_col = env_filter_cfg.get("human_label_column", "env_human")
    llm_col = env_filter_cfg.get("llm_label_column", "env_llm")
    final_col = env_filter_cfg.get("final_label_column", "env_final")

    human_path = interim_dir / cfg["interim_files"]["env_human_labeled_dataset"]
    llm_path = interim_dir / cfg["interim_files"]["env_llm_labeled_dataset"]
    review_path = interim_dir / cfg["interim_files"].get("env_review_dataset", "env_review_dataset.xlsx")

    if not human_path.exists():
        logger.error(f"File human không tồn tại: {human_path}")
        sys.exit(1)

    logger.info(f"[Bước 5.1] Đọc file human: {human_path.name}")
    df = pd.read_excel(human_path, dtype=str)
    logger.info(f"  → {len(df)} bản ghi")

    if llm_path.exists():
        df_llm = pd.read_excel(llm_path, dtype=str)
        llm_cols = ["source_id"] + [c for c in [
            llm_col, "env_llm_reason", "env_evidence_span", "env_confidence",
            "env_needs_human_review", "env_llm_domain", "env_llm_error"
        ] if c in df_llm.columns and c not in df.columns]
        df = df.merge(df_llm[llm_cols], on="source_id", how="left")
        logger.info(f"  → Sau merge với LLM: {len(df)} bản ghi")
    else:
        logger.warning(f"  ⚠️  Không tìm thấy {llm_path.name}; không thể kiểm tra bất đồng với LLM.")

    df = ensure_columns(df, REVIEW_COLUMNS)
    df = merge_review_file(df, review_path)

    logger.info("[Bước 5.2] Chốt env_final theo review_decision")
    df["env_human_norm"] = df[human_col].apply(normalize_env_label)
    df["env_llm_norm"] = df[llm_col].apply(normalize_env_label) if llm_col in df.columns else None
    df["is_disagreement"] = df["env_human_norm"] != df["env_llm_norm"]

    resolved = df.apply(resolve_env_final, axis=1, result_type="expand")
    resolved.columns = [final_col, "review_decision_resolved", "final_reason_resolved", "needs_adjudication_fix"]
    df[final_col] = resolved[final_col]
    df["review_decision"] = resolved["review_decision_resolved"]
    df["final_reason"] = df.apply(lambda r: first_nonblank(r.get("final_reason"), r.get("final_reason_resolved"), ""), axis=1)
    df["needs_adjudication_fix"] = resolved["needs_adjudication_fix"].astype(bool)
    df["error_type"] = df.apply(
        lambda r: first_nonblank(
            r.get("error_type"),
            "LLM_FALSE_POSITIVE_ENV" if r.get("env_llm_norm") == 1 and r.get("env_human_norm") == 0 else
            "LLM_FALSE_NEGATIVE_ENV" if r.get("env_llm_norm") == 0 and r.get("env_human_norm") == 1 else
            "NO_ERROR_AGREEMENT",
        ),
        axis=1,
    )
    df["env_needs_review"] = df.apply(
        lambda r: "TRUE" if str(r.get("review_decision", "")).upper() in {"AMBIGUOUS_KEEP_HUMAN", "NEED_EXPERT_REVIEW"} else first_nonblank(r.get("env_needs_review"), "FALSE"),
        axis=1,
    )

    invalid_final = df[~df[final_col].isin([0, 1])].copy()
    missing_disagreement_review = df[df["is_disagreement"] & df["needs_adjudication_fix"]].copy()
    missing_final_reason = df[df["is_disagreement"] & df["final_reason"].apply(is_blank)].copy()

    if len(invalid_final) > 0 or len(missing_disagreement_review) > 0 or len(missing_final_reason) > 0:
        logger.error("  ❌ Chưa đạt điều kiện xuất env_final_dataset theo adjudication_protocol.md")
        if len(invalid_final) > 0:
            logger.error(f"  - env_final thiếu/không hợp lệ: {len(invalid_final)} dòng. Ví dụ: {invalid_final['source_id'].head(10).tolist()}")
        if len(missing_disagreement_review) > 0:
            logger.error(f"  - Bất đồng thiếu review_decision/env_final: {len(missing_disagreement_review)} dòng. Ví dụ: {missing_disagreement_review['source_id'].head(10).tolist()}")
        if len(missing_final_reason) > 0:
            logger.error(f"  - Bất đồng thiếu final_reason: {len(missing_final_reason)} dòng. Ví dụ: {missing_final_reason['source_id'].head(10).tolist()}")
        logger.error(f"  Hãy mở {review_path.name}, điền review_decision/env_final/final_reason, rồi chạy lại bước 5.")
        sys.exit(1)

    df = df.drop(columns=["review_decision_resolved", "final_reason_resolved"], errors="ignore")

    n_total = len(df)
    n_env1 = int((df[final_col] == 1).sum())
    n_env0 = int((df[final_col] == 0).sum())
    n_missing = int(df[final_col].isna().sum())
    n_disagree = int(df["is_disagreement"].sum())

    logger.info(f"""
  ─── FUNNEL TẦNG 1 ────────────────────────────────────
  D_impact (tổng đầu vào):  {n_total}
  env_final = 1 (có MT):    {n_env1} ({n_env1 / n_total * 100:.1f}%)
  env_final = 0 (không MT): {n_env0} ({n_env0 / n_total * 100:.1f}%)
  Thiếu nhãn:               {n_missing}
  Bất đồng đã kiểm tra:     {n_disagree}
  ─────────────────────────────────────────────────────
  |D_env| = {n_env1} bản ghi sẽ vào Tầng 2
  ─────────────────────────────────────────────────────
""")

    logger.info("[Bước 5.3] Lưu env_final_dataset.xlsx")
    processed_dir.mkdir(parents=True, exist_ok=True)
    out_path = processed_dir / cfg["processed_files"]["env_final_dataset"]
    df.to_excel(out_path, index=False)
    logger.info(f"  ✅ {out_path.name} ({len(df):,} dòng)")

    logger.info("[Bước 5.4] Vẽ data funnel chart")
    plot_data_funnel(n_total, n_env1, figure_dir / cfg["figure_files"]["data_funnel"])

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"  HOÀN THÀNH — D_env có {n_env1} bản ghi")
    logger.info("  Bước tiếp theo:")
    logger.info("    py src/06_build_class_manual_label_file.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
