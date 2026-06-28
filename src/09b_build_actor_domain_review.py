#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
09b_build_actor_domain_review.py
=================================
BƯỚC 09b — Tạo file review chuẩn hóa ACTOR và DOMAIN trước khi chấm điểm.

Đề tài: Đánh giá tác động chính sách môi trường — Khung định lượng chi phí,
lợi ích, rủi ro.

Vị trí trong pipeline:
    Bước 09  : Chốt final_label sau adjudication nhãn 5 lớp.
    Bước 09b : Chuẩn hóa/gợi ý actor và domain cho từng bản ghi đã có final_label.
    Bước 09c : Validate actor/domain và xuất dataset đã chốt.
    Bước 10  : Tạo scoring_input.xlsx để người nghiên cứu chấm M, S, D, R, W.

Input:
    data/processed/final_labeled_dataset.xlsx
        Dataset đã có final_label cuối cùng sau khi xử lý bất đồng giữa
        class_human và class_llm.

Output:
    data/interim/actor_domain_review_template.xlsx
        File Excel để người nghiên cứu xem lại actor/domain trước khi chấm điểm.
        File gồm:
            - Sheet actor_domain_template: dữ liệu chính và các cột gợi ý.
            - Sheet actor_groups: danh mục nhóm actor chuẩn.
            - Sheet domains: danh mục domain chuẩn.

Tài liệu và cấu hình liên quan:
    - docs/guideline_identify_actor.md
    - docs/guideline_identify_domain.md
    - config/actor_domain_config.yaml

Cơ chế hoạt động:
    1. Đọc toàn bộ bản ghi trong final_labeled_dataset.xlsx có final_label hợp lệ.
    2. Tìm actor từ các trường như actor/chu_the và nội dung raw_text.
    3. Tìm domain từ domain raw, raw_text, legal_signal và điều kiện áp dụng.
    4. So khớp keyword theo config/actor_domain_config.yaml.
    5. Nếu có nhiều khả năng, chọn theo priority trong config và đánh dấu
       actor_needs_review/domain_needs_review để người nghiên cứu kiểm tra.
    6. Ghi rõ actor_reason/domain_reason để mọi gợi ý đều có thể giải thích được.

Ý nghĩa các cột chính:
    actor_raw:
        Actor ban đầu từ dữ liệu nguồn, nếu có.
    actor_primary:
        Actor/đối tượng chính được dùng để tham chiếu khi chấm Scope (S_i).
    actor_group:
        Nhóm actor chuẩn, ví dụ BUSINESS_FACILITY, STATE_AGENCY,
        GENERAL_ORGANIZATION_INDIVIDUAL.
    actor_reason:
        Lý do hệ thống gợi ý actor_group.
    actor_needs_review:
        TRUE nếu actor có dấu hiệu mơ hồ hoặc chỉ được suy luận gián tiếp.
    domain_raw:
        Domain ban đầu từ dữ liệu nguồn, nếu có.
    domain_primary:
        Domain chính dùng để tham chiếu Risk (R_i) và phân tích theo domain.
    domain_secondary:
        Domain phụ nếu điều khoản chạm đến nhiều lĩnh vực.
    domain_group:
        Nhóm domain cấp cao phục vụ tổng hợp báo cáo.
    domain_reason:
        Lý do hệ thống gợi ý domain_primary.
    domain_needs_review:
        TRUE nếu domain có dấu hiệu mơ hồ hoặc có nhiều domain cạnh tranh.
    review_actor_group/review_domain_primary/review_domain_secondary/review_note:
        Các cột để người nghiên cứu sửa hoặc ghi chú trước khi chạy bước 09c.

Lưu ý phương pháp:
    Script này KHÔNG tự chốt tuyệt đối actor/domain. Nó chỉ tạo gợi ý có giải
    thích và đánh dấu điểm cần review. Việc chốt hợp lệ được thực hiện ở bước
    09c_validate_actor_domain.py.

Sử dụng:
    py src/09b_build_actor_domain_review.py

Bước tiếp theo:
    1. Mở data/interim/actor_domain_review_template.xlsx.
    2. Kiểm tra các dòng actor_needs_review/domain_needs_review = TRUE.
    3. Nếu cần, điền review_actor_group, review_domain_primary,
       review_domain_secondary hoặc review_note.
    4. Chạy: py src/09c_validate_actor_domain.py
"""

import logging
import re
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


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_blank(value) -> bool:
    return value is None or pd.isna(value) or str(value).strip() == ""


def clean_text(value) -> str:
    if is_blank(value):
        return ""
    return str(value).strip()


def lower_join(*values) -> str:
    return " ".join(clean_text(v).lower() for v in values if not is_blank(v))


def first_col(row: pd.Series, candidates: list[str]) -> str:
    for col in candidates:
        if col in row.index and not is_blank(row.get(col)):
            return clean_text(row.get(col))
    return ""


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    hits = []
    for kw in keywords or []:
        kw_l = str(kw).lower().strip()
        if kw_l and kw_l in text:
            hits.append(str(kw))
    return hits


def split_raw_domains(raw: str) -> list[str]:
    if not raw:
        return []
    parts = re.split(r"[;,|/]+", raw)
    return [p.strip() for p in parts if p.strip()]


def infer_actor(row: pd.Series, actor_cfg: dict) -> dict:
    actor_raw = first_col(row, ["actor", "chu_the", "subject", "doi_tuong"])
    raw_text = first_col(row, ["raw_text", "text", "noi_dung_dieu_khoan"])
    legal_signal = first_col(row, ["legal_signal", "tin_hieu_tac_dong"])
    context = lower_join(actor_raw, raw_text, legal_signal)

    group_hits = {}
    for group in actor_cfg.get("actor_priority", []):
        spec = actor_cfg["actor_groups"].get(group, {})
        hits = keyword_hits(context, spec.get("keywords", []))
        if hits:
            group_hits[group] = hits

    if group_hits:
        actor_group = next(g for g in actor_cfg["actor_priority"] if g in group_hits)
        actor_needs_review = len(group_hits) > 1
        reason = f"Khớp keyword actor: {', '.join(group_hits[actor_group][:5])}"
        if len(group_hits) > 1:
            other = [g for g in group_hits if g != actor_group]
            reason += f"; có thêm nhóm phụ cần kiểm tra: {', '.join(other)}"
    else:
        actor_group = "GENERAL_ORGANIZATION_INDIVIDUAL"
        actor_needs_review = True
        reason = "Không khớp keyword actor rõ ràng; tạm xếp nhóm chung và yêu cầu review."

    spec = actor_cfg["actor_groups"].get(actor_group, {})
    secondary = [g for g in actor_cfg.get("actor_priority", []) if g in group_hits and g != actor_group]

    return {
        "actor_raw": actor_raw,
        "actor_primary": actor_raw or spec.get("label_vi", actor_group),
        "actor_secondary": "; ".join(secondary),
        "actor_group": actor_group,
        "actor_reason": reason,
        "actor_needs_review": bool(actor_needs_review),
        "suggested_S_range": format_range(spec.get("suggested_S_range")),
    }


def infer_domain(row: pd.Series, domain_cfg: dict) -> dict:
    domain_raw = first_col(row, ["domain", "mien_tac_dong", "environmental_domain"])
    raw_text = first_col(row, ["raw_text", "text", "noi_dung_dieu_khoan"])
    legal_signal = first_col(row, ["legal_signal", "tin_hieu_tac_dong"])
    condition = first_col(row, ["condition", "dieu_kien_ap_dung"])
    context = lower_join(domain_raw, raw_text, legal_signal, condition)

    domains = domain_cfg.get("domains", {})
    raw_matches = [d for d in split_raw_domains(domain_raw) if d in domains]

    keyword_matches = {}
    for domain, spec in domains.items():
        hits = keyword_hits(context, spec.get("keywords", []))
        if hits:
            keyword_matches[domain] = hits

    candidates = set(raw_matches) | set(keyword_matches)
    priority = domain_cfg.get("domain_priority", list(domains))
    ordered = [d for d in priority if d in candidates]

    if ordered:
        domain_primary = ordered[0]
        secondary = ordered[1:4]
        primary_hits = keyword_matches.get(domain_primary, [])
        reason = "Khớp domain theo "
        reason += "raw domain + keyword" if domain_primary in raw_matches and primary_hits else "keyword" if primary_hits else "raw domain"
        if primary_hits:
            reason += f": {', '.join(primary_hits[:5])}"
        domain_needs_review = len(ordered) > 2
    else:
        domain_primary = "general_environment"
        secondary = []
        reason = "Không khớp domain chuyên biệt; tạm xếp general_environment và yêu cầu review."
        domain_needs_review = True

    content_domains = set(domain_cfg.get("content_domains", []))
    tool_domains = set(domain_cfg.get("tool_domains", []))
    if domain_primary == "general_environment" and (set(keyword_matches) & content_domains):
        domain_needs_review = True
        reason += "; có dấu hiệu domain nội dung nhưng đang là general_environment."
    if domain_primary in tool_domains and (set(keyword_matches) & content_domains):
        domain_needs_review = True
        reason += "; domain công cụ hành chính đi kèm domain nội dung, cần kiểm tra domain_primary."

    spec = domains.get(domain_primary, {})
    return {
        "domain_raw": domain_raw,
        "domain_primary": domain_primary,
        "domain_secondary": "; ".join(secondary),
        "domain_group": spec.get("group", ""),
        "domain_reason": reason,
        "domain_needs_review": bool(domain_needs_review),
        "suggested_R_range": format_range(spec.get("suggested_R_range")),
    }


def format_range(values) -> str:
    if not values or len(values) != 2:
        return ""
    return f"{values[0]}-{values[1]}"


def build_reference_sheets(actor_domain_cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    actor_rows = []
    for group, spec in actor_domain_cfg.get("actor_groups", {}).items():
        actor_rows.append({
            "actor_group": group,
            "label_vi": spec.get("label_vi", ""),
            "suggested_S_range": format_range(spec.get("suggested_S_range")),
            "keywords": "; ".join(spec.get("keywords", [])),
        })

    domain_rows = []
    for domain, spec in actor_domain_cfg.get("domains", {}).items():
        domain_rows.append({
            "domain": domain,
            "domain_group": spec.get("group", ""),
            "label_vi": spec.get("label_vi", ""),
            "suggested_R_range": format_range(spec.get("suggested_R_range")),
            "keywords": "; ".join(spec.get("keywords", [])),
        })

    return pd.DataFrame(actor_rows), pd.DataFrame(domain_rows)


def main():
    cfg = load_yaml(PROJECT_ROOT / "config" / "project_config.yaml")
    actor_domain_cfg = load_yaml(PROJECT_ROOT / "config" / "actor_domain_config.yaml")

    logger.info("=" * 60)
    logger.info("  BƯỚC 9b - Tạo template review actor/domain")
    logger.info("=" * 60)

    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_data"]
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    final_path = processed_dir / cfg["processed_files"]["final_labeled_dataset"]
    output_path = interim_dir / cfg["interim_files"]["actor_domain_review_template"]

    if not final_path.exists():
        logger.error(f"Không tìm thấy: {final_path}. Chạy script 09 trước.")
        sys.exit(1)

    logger.info(f"[Bước 9b.1] Đọc: {final_path.name}")
    df = pd.read_excel(final_path, dtype=str)
    if "final_label" not in df.columns:
        logger.error("final_labeled_dataset.xlsx thiếu cột final_label.")
        sys.exit(1)

    df = df[df["final_label"].astype(str).str.strip().isin(VALID_LABELS)].copy()
    logger.info(f"  -> {len(df)} bản ghi có final_label hợp lệ")

    rows = []
    keep_cols = [
        "source_id", "legal_citation", "raw_text", "final_label",
        "final_reason", "legal_signal", "tin_hieu_tac_dong",
        "quantitative_value", "gia_tri_dinh_luong", "condition", "dieu_kien_ap_dung",
    ]

    for _, row in df.iterrows():
        base = {col: row.get(col, "") for col in keep_cols if col in df.columns}
        actor_info = infer_actor(row, actor_domain_cfg)
        domain_info = infer_domain(row, actor_domain_cfg)
        base.update(actor_info)
        base.update(domain_info)
        base["review_actor_group"] = ""
        base["review_domain_primary"] = ""
        base["review_domain_secondary"] = ""
        base["review_note"] = ""
        rows.append(base)

    out = pd.DataFrame(rows)
    actor_ref, domain_ref = build_reference_sheets(actor_domain_cfg)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        out.to_excel(writer, sheet_name="actor_domain_template", index=False)
        actor_ref.to_excel(writer, sheet_name="actor_groups", index=False)
        domain_ref.to_excel(writer, sheet_name="domains", index=False)

    n_actor_review = int(out["actor_needs_review"].astype(bool).sum())
    n_domain_review = int(out["domain_needs_review"].astype(bool).sum())
    logger.info(f"[Bước 9b.2] Đã lưu: {output_path.name} ({len(out)} dòng)")
    logger.info(f"  actor_needs_review={n_actor_review}, domain_needs_review={n_domain_review}")
    logger.info("  Bước tiếp theo: mở file này để sửa review_* nếu cần, rồi chạy py src/09c_validate_actor_domain.py")


if __name__ == "__main__":
    main()
