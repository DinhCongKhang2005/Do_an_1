#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
09c_validate_actor_domain.py
=============================
BƯỚC 09c — Validate và chốt ACTOR/DOMAIN trước khi tạo scoring input.

Đề tài: Đánh giá tác động chính sách môi trường — Khung định lượng chi phí,
lợi ích, rủi ro.

Vị trí trong pipeline:
    Bước 09b : Tạo actor_domain_review_template.xlsx với gợi ý actor/domain.
    Bước 09c : Kiểm tra tính hợp lệ và chốt actor/domain.
    Bước 10  : Dùng actor_domain_dataset.xlsx để tạo scoring_input.xlsx.
    Bước 11  : Validate điểm M, S, D, R, W và tính Impact Score.

Input:
    data/interim/actor_domain_review_template.xlsx
        File được tạo từ bước 09b. Người nghiên cứu có thể chỉnh các cột
        review_actor_group, review_domain_primary, review_domain_secondary,
        review_note trước khi chạy bước này.

Output:
    data/processed/actor_domain_dataset.xlsx
        Dataset đã chốt actor/domain, là đầu vào chính thức cho bước 10.

    data/reports/actor_domain_validation_report.xlsx
        Báo cáo kiểm định actor/domain, gồm:
            - Sheet summary: số dòng, số lỗi chặn, số cảnh báo.
            - Sheet issues: danh sách lỗi/cảnh báo theo source_id.

Tài liệu và cấu hình liên quan:
    - docs/guideline_identify_actor.md
    - docs/guideline_identify_domain.md
    - config/actor_domain_config.yaml
    - data/interim/actor_domain_review_template.xlsx

Cơ chế hoạt động:
    1. Đọc sheet actor_domain_template từ actor_domain_review_template.xlsx.
    2. Áp dụng phần chỉnh tay của người nghiên cứu:
           review_actor_group        -> ghi đè actor_group
           review_domain_primary     -> ghi đè domain_primary
           review_domain_secondary   -> ghi đè domain_secondary
    3. Kiểm tra actor_group có thuộc danh mục actor chuẩn hay không.
    4. Kiểm tra domain_primary/domain_secondary có thuộc danh mục domain chuẩn
       hay không.
    5. Cảnh báo các trường hợp cần chú ý, ví dụ:
           - actor/domain từng được đánh dấu needs_review nhưng chưa có review_note.
           - general_environment được dùng khi có dấu hiệu domain cụ thể hơn.
           - domain hành chính/kỹ thuật đang là primary trong khi có domain nội dung.
           - domain rủi ro cao như climate_carbon, hazardous_substances,
             biodiversity_natural_heritage.
    6. Nếu còn ERROR, script dừng và không xuất actor_domain_dataset.xlsx.
    7. Nếu chỉ còn WARNING, script vẫn xuất actor_domain_dataset.xlsx để bước
       scoring tiếp tục, nhưng cảnh báo được giữ trong validation report.

Phân biệt ERROR và WARNING:
    ERROR:
        Lỗi chặn pipeline, ví dụ actor_group/domain_primary không thuộc danh mục
        chuẩn hoặc thiếu source_id. Cần sửa trước khi chấm điểm.

    WARNING:
        Không chặn pipeline, nhưng người nghiên cứu nên kiểm tra. Ví dụ dòng còn
        needs_review nhưng đã có gợi ý hợp lệ và lý do giải thích.

Ý nghĩa phương pháp:
    Bước này là "cổng kiểm định" trước scoring. Nó đảm bảo các biến định tính
    actor/domain được chuẩn hóa trước khi người nghiên cứu chấm M_i, S_i, D_i,
    R_i. Nhờ đó, điểm S_i và R_i có căn cứ rõ ràng và có thể truy vết lại.

Sử dụng:
    py src/09c_validate_actor_domain.py

Bước tiếp theo:
    Nếu report có errors = 0:
        py src/10_build_scoring_input.py

    Nếu report có errors > 0:
        Mở data/interim/actor_domain_review_template.xlsx, sửa các cột review_*,
        rồi chạy lại script này.
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


def split_multi(value) -> list[str]:
    if is_blank(value):
        return []
    return [p.strip() for p in str(value).replace(",", ";").split(";") if p.strip()]


def add_issue(issues: list[dict], severity: str, source_id: str, field: str, message: str):
    issues.append({
        "severity": severity,
        "source_id": source_id,
        "field": field,
        "message": message,
    })


def apply_review_overrides(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["review_actor_group", "review_domain_primary", "review_domain_secondary", "review_note"]:
        if col not in df.columns:
            df[col] = ""

    df["actor_group_original"] = df.get("actor_group", "")
    df["domain_primary_original"] = df.get("domain_primary", "")
    df["domain_secondary_original"] = df.get("domain_secondary", "")

    df["actor_group"] = df.apply(
        lambda r: clean(r["review_actor_group"]) or clean(r.get("actor_group", "")),
        axis=1,
    )
    df["domain_primary"] = df.apply(
        lambda r: clean(r["review_domain_primary"]) or clean(r.get("domain_primary", "")),
        axis=1,
    )
    df["domain_secondary"] = df.apply(
        lambda r: clean(r["review_domain_secondary"]) or clean(r.get("domain_secondary", "")),
        axis=1,
    )
    df["actor_domain_reviewed"] = df.apply(
        lambda r: bool(clean(r["review_actor_group"]) or clean(r["review_domain_primary"]) or clean(r["review_domain_secondary"]) or clean(r["review_note"])),
        axis=1,
    )
    return df


def validate(df: pd.DataFrame, actor_domain_cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_actors = set(actor_domain_cfg.get("actor_groups", {}))
    valid_domains = set(actor_domain_cfg.get("domains", {}))
    content_domains = set(actor_domain_cfg.get("content_domains", []))
    tool_domains = set(actor_domain_cfg.get("tool_domains", []))
    high_risk_domains = set(actor_domain_cfg.get("high_risk_domains", []))

    issues = []

    for idx, row in df.iterrows():
        sid = clean(row.get("source_id")) or f"row_{idx + 2}"
        actor_group = clean(row.get("actor_group"))
        domain_primary = clean(row.get("domain_primary"))
        domain_secondary = split_multi(row.get("domain_secondary"))
        note = clean(row.get("review_note"))

        if is_blank(row.get("source_id")):
            add_issue(issues, "ERROR", sid, "source_id", "Thiếu source_id.")

        if actor_group not in valid_actors:
            add_issue(issues, "ERROR", sid, "actor_group", f"actor_group không thuộc danh mục chuẩn: {actor_group}")

        if domain_primary not in valid_domains:
            add_issue(issues, "ERROR", sid, "domain_primary", f"domain_primary không thuộc danh mục chuẩn: {domain_primary}")

        for domain in domain_secondary:
            if domain not in valid_domains:
                add_issue(issues, "ERROR", sid, "domain_secondary", f"domain_secondary không thuộc danh mục chuẩn: {domain}")

        if boolish(row.get("actor_needs_review")) and not note and not clean(row.get("review_actor_group")):
            add_issue(issues, "WARNING", sid, "actor_needs_review", "Dòng cần review actor; đang dùng actor_group gợi ý và actor_reason để tiếp tục.")

        if boolish(row.get("domain_needs_review")) and not note and not clean(row.get("review_domain_primary")):
            add_issue(issues, "WARNING", sid, "domain_needs_review", "Dòng cần review domain; đang dùng domain_primary gợi ý và domain_reason để tiếp tục.")

        all_domains = {domain_primary, *domain_secondary}
        if domain_primary == "general_environment" and (all_domains & content_domains):
            add_issue(issues, "WARNING", sid, "domain_primary", "general_environment không nên là primary khi đã có domain nội dung cụ thể.")

        if domain_primary in tool_domains and (set(domain_secondary) & content_domains):
            add_issue(issues, "WARNING", sid, "domain_primary", "Domain công cụ/hành chính đang là primary trong khi có domain nội dung ở secondary.")

        if domain_primary in high_risk_domains:
            add_issue(issues, "WARNING", sid, "domain_primary", "Domain rủi ro cao; khi chấm điểm cần giải thích R_i nếu R_i thấp.")

        if is_blank(row.get("actor_reason")):
            add_issue(issues, "WARNING", sid, "actor_reason", "Thiếu giải thích actor_reason.")

        if is_blank(row.get("domain_reason")):
            add_issue(issues, "WARNING", sid, "domain_reason", "Thiếu giải thích domain_reason.")

    issues_df = pd.DataFrame(issues)
    if issues_df.empty:
        issues_df = pd.DataFrame(columns=["severity", "source_id", "field", "message"])

    return df, issues_df


def main():
    cfg = load_yaml(PROJECT_ROOT / "config" / "project_config.yaml")
    actor_domain_cfg = load_yaml(PROJECT_ROOT / "config" / "actor_domain_config.yaml")

    logger.info("=" * 60)
    logger.info("  BƯỚC 9c - Validate actor/domain trước scoring")
    logger.info("=" * 60)

    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_data"]
    report_dir = PROJECT_ROOT / cfg["paths"]["reports"]

    input_path = interim_dir / cfg["interim_files"]["actor_domain_review_template"]
    output_path = processed_dir / cfg["processed_files"]["actor_domain_dataset"]
    report_path = report_dir / cfg["report_files"]["actor_domain_validation_report"]

    if not input_path.exists():
        logger.error(f"Không tìm thấy: {input_path}. Chạy py src/09b_build_actor_domain_review.py trước.")
        sys.exit(1)

    logger.info(f"[Bước 9c.1] Đọc: {input_path.name}")
    df = pd.read_excel(input_path, sheet_name="actor_domain_template", dtype=str)
    df = apply_review_overrides(df)
    df, issues_df = validate(df, actor_domain_cfg)

    n_error = int((issues_df["severity"] == "ERROR").sum()) if not issues_df.empty else 0
    n_warning = int((issues_df["severity"] == "WARNING").sum()) if not issues_df.empty else 0

    summary_df = pd.DataFrame([
        {"metric": "n_records", "value": len(df)},
        {"metric": "n_errors", "value": n_error},
        {"metric": "n_warnings", "value": n_warning},
        {"metric": "can_continue_to_scoring", "value": n_error == 0},
    ])

    report_dir.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="summary", index=False)
        issues_df.to_excel(writer, sheet_name="issues", index=False)

    logger.info(f"[Bước 9c.2] Đã lưu report: {report_path.name}")
    logger.info(f"  errors={n_error}, warnings={n_warning}")

    if n_error > 0:
        logger.error("Còn lỗi actor/domain cần xử lý. Mở actor_domain_review_template.xlsx và cập nhật review_* trước khi chấm điểm.")
        sys.exit(1)

    processed_dir.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)
    logger.info(f"[Bước 9c.3] Đã lưu dataset chuẩn hóa: {output_path.name} ({len(df)} dòng)")
    logger.info("  Bước tiếp theo: py src/10_build_scoring_input.py")


if __name__ == "__main__":
    main()
