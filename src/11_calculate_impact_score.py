#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
11_calculate_impact_score.py
=============================
BƯỚC 11 — Validate điểm chấm và tính Impact Score.

Đề tài: Đánh giá tác động chính sách môi trường — Khung định lượng chi phí,
lợi ích, rủi ro.

Vị trí trong pipeline:
    Bước 10 : Tạo scoring_input.xlsx và người nghiên cứu điền M_i, S_i, D_i,
              R_i, W_i.
    Bước 11 : Kiểm tra tính hợp lệ của điểm chấm và tính Impact Score.
    Bước 12 : Tạo biểu đồ phân tích Impact Score.
    Bước 13 : Tổng hợp báo cáo pipeline cuối cùng.

Input:
    data/interim/scoring_input.xlsx
        File đã được người nghiên cứu điền điểm M_i, S_i, D_i, R_i, W_i và
        scoring_note nếu cần.

Outputs:
    data/reports/scoring_validation_report.xlsx
        Báo cáo kiểm định điểm chấm trước khi tính Impact Score.

    data/processed/scored_dataset.xlsx
        Dataset chi tiết sau khi tính C_i, C_i_norm, direction_i và
        ImpactScore_i.

    data/reports/scoring_summary.xlsx
        Bảng tổng hợp điểm theo toàn bộ văn bản, theo final_label, theo domain
        và theo actor.

    data/reports/final_impact_report.xlsx
        Báo cáo tác động cuối cùng, gồm tổng quan và top bản ghi có tác động lớn.

Tài liệu và cấu hình liên quan:
    - docs/scoring_rubric_MSDR.md
    - config/scoring_config.yaml
    - config/labels.yaml
    - config/actor_domain_config.yaml

Công thức tính:
    C_i = alpha*M_i + beta*S_i + gamma*D_i + delta*R_i

    C_i_norm = (C_i - score_min) / (score_max - score_min)

    ImpactScore_i = direction_i * W_i * C_i_norm

Trong đó:
    M_i:
        Magnitude — cường độ tác động.
    S_i:
        Scope — phạm vi tác động.
    D_i:
        Duration — thời gian tác động.
    R_i:
        Risk/Reversibility — rủi ro và khả năng phục hồi.
    W_i:
        Weight — trọng số đối tượng/domain.
    direction_i:
        +1 cho nhóm lợi ích; -1 cho nhóm chi phí/ràng buộc.

Cơ chế validate trước khi tính điểm:
    1. Kiểm tra các cột bắt buộc: source_id, final_label, M_i, S_i, D_i, R_i, W_i.
    2. Kiểm tra M_i, S_i, D_i, R_i nằm trong thang điểm cấu hình, mặc định [1, 5].
    3. Kiểm tra W_i là số dương.
    4. Yêu cầu scoring_note nếu:
           - W_i khác giá trị mặc định.
           - M_i hoặc R_i đạt mức tối đa.
           - actor/domain từng được đánh dấu needs_review.
           - S_i nằm ngoài suggested_S_range.
           - R_i nằm ngoài suggested_R_range.
           - domain rủi ro cao nhưng R_i thấp.
    5. Nếu còn ERROR, script dừng và chỉ xuất scoring_validation_report.xlsx.
    6. Nếu chỉ có WARNING, script vẫn tính điểm nhưng giữ cảnh báo trong report.

Ý nghĩa phương pháp:
    Bước này không chỉ tính điểm, mà còn là lớp kiểm soát chất lượng trước khi
    lượng hóa tác động. Mục tiêu là tránh trường hợp điểm được tính từ dữ liệu
    thiếu căn cứ hoặc không thể giải thích.

Sử dụng:
    py src/11_calculate_impact_score.py

    Có thể truyền trọng số tùy chỉnh:
    py src/11_calculate_impact_score.py --weights 0.3 0.2 0.3 0.2

Bước tiếp theo:
    Nếu scoring_validation_report.xlsx có errors = 0:
        py src/12_generate_figures.py

    Nếu errors > 0:
        Mở data/interim/scoring_input.xlsx, sửa điểm hoặc bổ sung scoring_note,
        rồi chạy lại script này.
"""

import argparse
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

VALID_LABELS = {
    "BENEFIT_QUANTITATIVE",
    "BENEFIT_QUALITATIVE",
    "COST_QUANTITATIVE",
    "COST_QUALITATIVE",
    "CONSTRAINT",
}

DIRECTION_FALLBACK = {
    "BENEFIT_QUANTITATIVE": 1,
    "BENEFIT_QUALITATIVE": 1,
    "COST_QUANTITATIVE": -1,
    "COST_QUALITATIVE": -1,
    "CONSTRAINT": -1,
}


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_blank(value) -> bool:
    return value is None or pd.isna(value) or str(value).strip() == ""


def clean(value) -> str:
    if is_blank(value):
        return ""
    return str(value).strip()


def boolish(value) -> bool:
    return clean(value).lower() in {"true", "1", "yes", "y", "x", "có", "co"}


def parse_range(value: str) -> tuple[float, float] | None:
    text = clean(value)
    if not text or "-" not in text:
        return None
    left, right = text.split("-", 1)
    try:
        return float(left.strip()), float(right.strip())
    except ValueError:
        return None


def parse_score(value, col: str, sid: str, issues: list[dict], score_min: float, score_max: float) -> float | None:
    if is_blank(value):
        add_issue(issues, "ERROR", sid, col, f"Thiếu {col}.")
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        add_issue(issues, "ERROR", sid, col, f"{col} không phải số: {value}")
        return None
    if not (score_min <= parsed <= score_max):
        add_issue(issues, "ERROR", sid, col, f"{col}={parsed} nằm ngoài [{score_min}, {score_max}].")
        return None
    return parsed


def add_issue(issues: list[dict], severity: str, source_id: str, field: str, message: str):
    issues.append({
        "severity": severity,
        "source_id": source_id,
        "field": field,
        "message": message,
    })


def get_direction(label: str, labels_cfg: dict) -> int:
    direction_map = labels_cfg.get("impact_direction", {}) if labels_cfg else {}
    return int(direction_map.get(label, DIRECTION_FALLBACK.get(label, -1)))


def validate_rows(
    df: pd.DataFrame,
    scoring_cfg: dict,
    actor_domain_cfg: dict,
    default_w: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    score_min = float(scoring_cfg.get("score_range", {}).get("min", 1))
    score_max = float(scoring_cfg.get("score_range", {}).get("max", 5))
    high_risk_domains = set(actor_domain_cfg.get("high_risk_domains", []))

    issues = []
    parsed_rows = []
    required_cols = ["source_id", "final_label", "M_i", "S_i", "D_i", "R_i", "W_i"]
    for col in required_cols:
        if col not in df.columns:
            add_issue(issues, "ERROR", "FILE", col, f"Thiếu cột bắt buộc: {col}")

    if any(i["source_id"] == "FILE" for i in issues):
        return df, pd.DataFrame(issues)

    for _, row in df.iterrows():
        sid = clean(row.get("source_id"))
        label = clean(row.get("final_label"))
        note = clean(row.get("scoring_note"))
        review_note = clean(row.get("review_note"))
        combined_note = note or review_note

        if not sid:
            sid = "UNKNOWN"
            add_issue(issues, "ERROR", sid, "source_id", "Thiếu source_id.")

        if label not in VALID_LABELS:
            add_issue(issues, "ERROR", sid, "final_label", f"final_label không hợp lệ: {label}")

        M = parse_score(row.get("M_i"), "M_i", sid, issues, score_min, score_max)
        S = parse_score(row.get("S_i"), "S_i", sid, issues, score_min, score_max)
        D = parse_score(row.get("D_i"), "D_i", sid, issues, score_min, score_max)
        R = parse_score(row.get("R_i"), "R_i", sid, issues, score_min, score_max)

        try:
            W = float(row.get("W_i"))
            if W <= 0:
                add_issue(issues, "ERROR", sid, "W_i", "W_i phải > 0.")
                W = None
        except (TypeError, ValueError):
            add_issue(issues, "ERROR", sid, "W_i", f"W_i không phải số: {row.get('W_i')}")
            W = None

        if W is not None and abs(W - default_w) > 1e-9 and not combined_note:
            add_issue(issues, "ERROR", sid, "scoring_note", "W_i khác mặc định nhưng thiếu scoring_note.")

        if M == score_max and not combined_note:
            add_issue(issues, "ERROR", sid, "scoring_note", "M_i đạt mức tối đa nhưng thiếu scoring_note.")

        if R == score_max and not combined_note:
            add_issue(issues, "ERROR", sid, "scoring_note", "R_i đạt mức tối đa nhưng thiếu scoring_note.")

        if boolish(row.get("actor_needs_review")) or boolish(row.get("domain_needs_review")):
            if not combined_note:
                add_issue(issues, "ERROR", sid, "scoring_note", "Actor/domain từng cần review; cần ghi chú căn cứ trước khi tính điểm.")

        suggested_s = parse_range(row.get("suggested_S_range", ""))
        if S is not None and suggested_s and not (suggested_s[0] <= S <= suggested_s[1]) and not combined_note:
            add_issue(issues, "ERROR", sid, "S_i", f"S_i={S} nằm ngoài suggested_S_range={clean(row.get('suggested_S_range'))} nhưng thiếu scoring_note.")

        suggested_r = parse_range(row.get("suggested_R_range", ""))
        if R is not None and suggested_r and not (suggested_r[0] <= R <= suggested_r[1]) and not combined_note:
            add_issue(issues, "ERROR", sid, "R_i", f"R_i={R} nằm ngoài suggested_R_range={clean(row.get('suggested_R_range'))} nhưng thiếu scoring_note.")

        domain_primary = clean(row.get("domain_primary"))
        if domain_primary in high_risk_domains and R is not None and R <= 2 and not combined_note:
            add_issue(issues, "ERROR", sid, "R_i", "Domain rủi ro cao nhưng R_i <= 2 và thiếu scoring_note.")

        if label == "CONSTRAINT" and R is not None and R <= 2 and not combined_note:
            add_issue(issues, "WARNING", sid, "R_i", "CONSTRAINT có R_i thấp; nên kiểm tra lại hoặc ghi rõ lý do.")

        parsed = row.to_dict()
        parsed.update({"M_i": M, "S_i": S, "D_i": D, "R_i": R, "W_i": W})
        parsed_rows.append(parsed)

    issues_df = pd.DataFrame(issues)
    if issues_df.empty:
        issues_df = pd.DataFrame(columns=["severity", "source_id", "field", "message"])
    return pd.DataFrame(parsed_rows), issues_df


def calculate_impact_score(row: pd.Series, direction: int, weights: tuple[float, float, float, float], score_min: float, score_max: float) -> dict:
    alpha, beta, gamma, delta = weights
    C_i = alpha * row["M_i"] + beta * row["S_i"] + gamma * row["D_i"] + delta * row["R_i"]
    C_i_norm = (C_i - score_min) / (score_max - score_min)
    C_i_norm = max(0.0, min(1.0, C_i_norm))
    impact_score = direction * row["W_i"] * C_i_norm
    return {
        "C_i": round(C_i, 4),
        "C_i_norm": round(C_i_norm, 4),
        "direction_i": direction,
        "ImpactScore_i": round(impact_score, 4),
    }


def summarize(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    if group_col not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby(group_col, dropna=False)["ImpactScore_i"]
        .agg(count="count", mean="mean", sum="sum")
        .reset_index()
        .round(4)
    )


def main():
    parser = argparse.ArgumentParser(description="Tính Impact Score từ scoring_input.xlsx")
    parser.add_argument(
        "--weights",
        nargs=4,
        type=float,
        default=None,
        metavar=("alpha", "beta", "gamma", "delta"),
        help="Trọng số cho M, S, D, R; tổng phải bằng 1.0.",
    )
    args = parser.parse_args()

    cfg = load_yaml(PROJECT_ROOT / "config" / "project_config.yaml")
    scoring_cfg = load_yaml(PROJECT_ROOT / "config" / "scoring_config.yaml")
    labels_cfg = load_yaml(PROJECT_ROOT / "config" / "labels.yaml")
    actor_domain_cfg = load_yaml(PROJECT_ROOT / "config" / "actor_domain_config.yaml")

    logger.info("=" * 60)
    logger.info("  BƯỚC 11 - Validate và tính Impact Score")
    logger.info("=" * 60)

    if args.weights:
        weights = tuple(args.weights)
    else:
        w_cfg = scoring_cfg.get("weights", {})
        weights = (
            float(w_cfg.get("alpha", 0.25)),
            float(w_cfg.get("beta", 0.25)),
            float(w_cfg.get("gamma", 0.25)),
            float(w_cfg.get("delta", 0.25)),
        )
    if abs(sum(weights) - 1.0) > 1e-6:
        logger.error(f"Tổng trọng số = {sum(weights):.4f}, phải bằng 1.0.")
        sys.exit(1)

    score_min = float(scoring_cfg.get("score_range", {}).get("min", 1))
    score_max = float(scoring_cfg.get("score_range", {}).get("max", 5))
    default_w = float(scoring_cfg.get("default_W_i", 1.0))

    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_data"]
    report_dir = PROJECT_ROOT / cfg["paths"]["reports"]

    input_path = interim_dir / cfg["interim_files"]["scoring_input"]
    if not input_path.exists():
        logger.error(f"Không tìm thấy: {input_path}. Chạy py src/10_build_scoring_input.py trước.")
        sys.exit(1)

    logger.info(f"[Bước 11.1] Đọc: {input_path.name}")
    df = pd.read_excel(input_path, sheet_name="scoring_template", dtype=str)

    logger.info("[Bước 11.2] Validate dữ liệu chấm điểm")
    parsed_df, issues_df = validate_rows(df, scoring_cfg, actor_domain_cfg, default_w)
    n_error = int((issues_df["severity"] == "ERROR").sum()) if not issues_df.empty else 0
    n_warning = int((issues_df["severity"] == "WARNING").sum()) if not issues_df.empty else 0

    report_dir.mkdir(parents=True, exist_ok=True)
    validation_path = report_dir / cfg["report_files"]["scoring_validation_report"]
    summary_validation = pd.DataFrame([
        {"metric": "n_records", "value": len(df)},
        {"metric": "n_errors", "value": n_error},
        {"metric": "n_warnings", "value": n_warning},
        {"metric": "can_calculate_score", "value": n_error == 0},
    ])
    with pd.ExcelWriter(validation_path, engine="openpyxl") as writer:
        summary_validation.to_excel(writer, sheet_name="summary", index=False)
        issues_df.to_excel(writer, sheet_name="issues", index=False)
    logger.info(f"  Đã lưu validation report: {validation_path.name} (errors={n_error}, warnings={n_warning})")

    if n_error > 0:
        logger.error("Còn lỗi scoring bắt buộc. Sửa scoring_input.xlsx theo scoring_validation_report.xlsx rồi chạy lại.")
        sys.exit(1)

    logger.info("[Bước 11.3] Tính Impact Score")
    rows = []
    for _, row in parsed_df.iterrows():
        direction = get_direction(clean(row.get("final_label")), labels_cfg)
        scores = calculate_impact_score(row, direction, weights, score_min, score_max)
        row_out = row.to_dict()
        row_out.update(scores)
        rows.append(row_out)

    df_scored = pd.DataFrame(rows)
    total_impact = float(df_scored["ImpactScore_i"].sum())
    mean_impact = float(df_scored["ImpactScore_i"].mean())
    std_impact = float(df_scored["ImpactScore_i"].std()) if len(df_scored) > 1 else 0.0
    max_impact = float(df_scored["ImpactScore_i"].max())
    min_impact = float(df_scored["ImpactScore_i"].min())

    processed_dir.mkdir(parents=True, exist_ok=True)
    scored_path = processed_dir / cfg["processed_files"]["scored_dataset"]
    df_scored.to_excel(scored_path, index=False)
    logger.info(f"  Đã lưu: {scored_path.name} ({len(df_scored)} dòng)")

    summary_overall = pd.DataFrame([
        {"Chỉ số": "TotalImpact", "Giá trị": round(total_impact, 4), "Giải thích": "Tổng Impact Score toàn bộ điều khoản"},
        {"Chỉ số": "MeanImpact", "Giá trị": round(mean_impact, 4), "Giải thích": "Impact Score trung bình"},
        {"Chỉ số": "StdImpact", "Giá trị": round(std_impact, 4), "Giải thích": "Độ lệch chuẩn"},
        {"Chỉ số": "MaxImpact", "Giá trị": round(max_impact, 4), "Giải thích": "Điểm lớn nhất"},
        {"Chỉ số": "MinImpact", "Giá trị": round(min_impact, 4), "Giải thích": "Điểm nhỏ nhất"},
        {"Chỉ số": "N", "Giá trị": len(df_scored), "Giải thích": "Số bản ghi tính điểm"},
        {"Chỉ số": "alpha", "Giá trị": weights[0], "Giải thích": "Trọng số M_i"},
        {"Chỉ số": "beta", "Giá trị": weights[1], "Giải thích": "Trọng số S_i"},
        {"Chỉ số": "gamma", "Giá trị": weights[2], "Giải thích": "Trọng số D_i"},
        {"Chỉ số": "delta", "Giá trị": weights[3], "Giải thích": "Trọng số R_i"},
    ])

    label_summary = summarize(df_scored, "final_label")
    domain_summary = summarize(df_scored, "domain_primary")
    actor_summary = summarize(df_scored, "actor_group")

    summary_path = report_dir / cfg["report_files"]["scoring_summary"]
    with pd.ExcelWriter(summary_path, engine="openpyxl") as writer:
        summary_overall.to_excel(writer, sheet_name="overall", index=False)
        label_summary.to_excel(writer, sheet_name="by_label", index=False)
        domain_summary.to_excel(writer, sheet_name="by_domain", index=False)
        actor_summary.to_excel(writer, sheet_name="by_actor", index=False)
        detail_cols = [c for c in [
            "source_id", "final_label", "actor_group", "domain_primary", "domain_secondary",
            "M_i", "S_i", "D_i", "R_i", "W_i", "C_i", "C_i_norm", "direction_i", "ImpactScore_i", "scoring_note",
        ] if c in df_scored.columns]
        df_scored[detail_cols].to_excel(writer, sheet_name="detail", index=False)
    logger.info(f"  Đã lưu: {summary_path.name}")

    impact_report_path = report_dir / cfg["report_files"]["final_impact_report"]
    df_top = df_scored.copy()
    df_top["abs_score"] = df_top["ImpactScore_i"].abs()
    top_cols = [c for c in [
        "source_id", "legal_citation", "final_label", "actor_group", "domain_primary",
        "ImpactScore_i", "C_i_norm", "scoring_note",
    ] if c in df_top.columns]
    df_top = df_top.nlargest(10, "abs_score")[top_cols]
    with pd.ExcelWriter(impact_report_path, engine="openpyxl") as writer:
        summary_overall.to_excel(writer, sheet_name="tong_hop", index=False)
        label_summary.to_excel(writer, sheet_name="theo_nhan", index=False)
        domain_summary.to_excel(writer, sheet_name="theo_domain", index=False)
        actor_summary.to_excel(writer, sheet_name="theo_actor", index=False)
        df_top.to_excel(writer, sheet_name="top10_impact", index=False)
    logger.info(f"  Đã lưu: {impact_report_path.name}")

    logger.info("=" * 60)
    logger.info(f"  HOÀN THÀNH - TotalImpact={total_impact:+.4f}, MeanImpact={mean_impact:+.4f}")
    logger.info("  Bước tiếp theo: py src/12_generate_figures.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
