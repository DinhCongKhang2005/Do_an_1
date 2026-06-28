#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10_build_scoring_input.py
==========================
BƯỚC 10 — Tạo file scoring_input.xlsx để người nghiên cứu chấm điểm M, S, D, R, W.

Đề tài: Đánh giá tác động chính sách môi trường — Khung định lượng chi phí,
lợi ích, rủi ro.

Vị trí trong pipeline:
    Bước 09  : Chốt final_label sau adjudication nhãn 5 lớp.
    Bước 09b : Tạo template review actor/domain.
    Bước 09c : Validate và chốt actor_domain_dataset.xlsx.
    Bước 10  : Tạo scoring_input.xlsx để chấm M_i, S_i, D_i, R_i, W_i.
    Bước 11  : Validate điểm và tính Impact Score.

Input:
    data/processed/actor_domain_dataset.xlsx
        Dataset đã có final_label, actor_group, domain_primary,
        domain_secondary, suggested_S_range và suggested_R_range.

Output:
    data/interim/scoring_input.xlsx
        File Excel để người nghiên cứu điền điểm M_i, S_i, D_i, R_i, W_i.
        File gồm:
            - Sheet scoring_template: dữ liệu chính cần chấm điểm.
            - Sheet rubric_reference: tóm tắt thang điểm M, S, D, R.
            - Sheet actor_reference: nhóm actor và gợi ý Scope.
            - Sheet domain_reference: domain và gợi ý Risk.

Tài liệu và cấu hình liên quan:
    - docs/scoring_rubric_MSDR.md
    - docs/guideline_identify_actor.md
    - docs/guideline_identify_domain.md
    - config/scoring_config.yaml
    - config/actor_domain_config.yaml

Cơ chế hoạt động:
    1. Đọc actor_domain_dataset.xlsx đã qua bước 09c.
    2. Chỉ giữ các dòng có final_label hợp lệ trong 5 nhãn:
           BENEFIT_QUANTITATIVE, BENEFIT_QUALITATIVE,
           COST_QUANTITATIVE, COST_QUALITATIVE, CONSTRAINT.
    3. Mang sang các thông tin giải thích cần thiết:
           raw_text, final_label, actor_group, actor_reason,
           domain_primary, domain_secondary, domain_reason.
    4. Thêm suggested_S_range dựa trên actor_group và suggested_R_range dựa
       trên domain_primary để hỗ trợ người nghiên cứu chấm điểm nhất quán.
    5. Thêm scoring_warning cho các dòng cần chú ý, ví dụ:
           - actor/domain từng được đánh dấu needs_review.
           - final_label là CONSTRAINT.
           - domain rủi ro cao.
           - actor thuộc nhóm chung, cần cân nhắc Scope.
    6. Tạo các cột trống M_i, S_i, D_i, R_i và điền W_i mặc định từ
       config/scoring_config.yaml.

Ý nghĩa các cột scoring:
    M_i:
        Magnitude — cường độ/mức độ lớn của tác động.
    S_i:
        Scope — phạm vi không gian hoặc nhóm đối tượng chịu tác động.
    D_i:
        Duration — thời gian tác động kéo dài.
    R_i:
        Risk/Reversibility — rủi ro và khả năng phục hồi.
    W_i:
        Weight — trọng số đối tượng/domain; mặc định là 1.0 nếu chưa có căn cứ
        chuyên gia để thay đổi.
    scoring_note:
        Ghi chú bắt buộc khi điểm vượt gợi ý, W_i khác mặc định, hoặc bản ghi
        có cảnh báo cần giải thích.

Lưu ý phương pháp:
    Script này KHÔNG tự chấm điểm. Nó tạo file đầu vào có cấu trúc, có rubric và
    có cảnh báo để người nghiên cứu chấm điểm minh bạch, nhất quán và có thể
    truy vết.

Sử dụng:
    py src/10_build_scoring_input.py

Bước tiếp theo:
    1. Mở data/interim/scoring_input.xlsx.
    2. Điền M_i, S_i, D_i, R_i cho từng bản ghi.
    3. Giữ W_i = 1.0 trừ khi có căn cứ rõ ràng để điều chỉnh.
    4. Điền scoring_note cho các dòng có scoring_warning hoặc điểm nằm ngoài
       suggested_S_range/suggested_R_range.
    5. Chạy: py src/11_calculate_impact_score.py
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

VALID_LABELS = [
    "BENEFIT_QUANTITATIVE",
    "BENEFIT_QUALITATIVE",
    "COST_QUANTITATIVE",
    "COST_QUALITATIVE",
    "CONSTRAINT",
]

RUBRIC_SUMMARY = {
    "M_i": {
        1: "Không đáng kể; thay đổi tối thiểu.",
        2: "Thấp; tác động cục bộ hoặc gián tiếp.",
        3: "Trung bình; thay đổi hành vi/vận hành rõ.",
        4: "Cao; ảnh hưởng quy trình chính hoặc hạ tầng.",
        5: "Rất cao; tác động chuyển đổi toàn ngành/quốc gia.",
    },
    "S_i": {
        1: "Một cơ sở hoặc một dự án đơn lẻ.",
        2: "Nhóm nhỏ hoặc một địa phương.",
        3: "Toàn ngành hoặc cấp tỉnh.",
        4: "Liên vùng hoặc đa ngành.",
        5: "Quốc gia hoặc xuyên biên giới.",
    },
    "D_i": {
        1: "Tạm thời, dưới 1 năm.",
        2: "Ngắn hạn, 1-5 năm.",
        3: "Trung hạn, 5-20 năm.",
        4: "Dài hạn, trên 20 năm.",
        5: "Vĩnh viễn hoặc khó đảo ngược.",
    },
    "R_i": {
        1: "Rủi ro thấp, phục hồi nhanh.",
        2: "Rủi ro thấp-trung bình, phục hồi được.",
        3: "Rủi ro trung bình, cần chi phí đáng kể.",
        4: "Rủi ro cao, khó phục hồi hoàn toàn.",
        5: "Rủi ro rất cao, không phục hồi được.",
    },
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


def format_range(values) -> str:
    if not values or len(values) != 2:
        return ""
    return f"{values[0]}-{values[1]}"


def build_scoring_warning(row: pd.Series, actor_domain_cfg: dict) -> str:
    warnings = []
    high_risk = set(actor_domain_cfg.get("high_risk_domains", []))

    if boolish(row.get("actor_needs_review")) or boolish(row.get("domain_needs_review")):
        warnings.append("Actor/domain từng được đánh dấu cần review; xem actor_reason/domain_reason và review_note.")

    if clean(row.get("final_label")) == "CONSTRAINT":
        warnings.append("CONSTRAINT thường cần giải thích rõ S_i/R_i vì đây là ràng buộc hành vi.")

    if clean(row.get("domain_primary")) in high_risk:
        warnings.append("Domain rủi ro cao; nếu R_i thấp cần nêu lý do trong scoring_note.")

    if clean(row.get("actor_group")) == "GENERAL_ORGANIZATION_INDIVIDUAL":
        warnings.append("Actor ở nhóm chung; kiểm tra S_i theo phạm vi thực tế của điều khoản.")

    return " | ".join(warnings)


def main():
    cfg = load_yaml(PROJECT_ROOT / "config" / "project_config.yaml")
    scoring_cfg = load_yaml(PROJECT_ROOT / "config" / "scoring_config.yaml")
    actor_domain_cfg = load_yaml(PROJECT_ROOT / "config" / "actor_domain_config.yaml")

    logger.info("=" * 60)
    logger.info("  BƯỚC 10 - Tạo template chấm điểm M, S, D, R, W")
    logger.info("=" * 60)

    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_data"]
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_data"]
    input_path = processed_dir / cfg["processed_files"]["actor_domain_dataset"]
    output_path = interim_dir / cfg["interim_files"]["scoring_input"]

    if not input_path.exists():
        logger.error(f"Không tìm thấy: {input_path}")
        logger.error("Chạy py src/09b_build_actor_domain_review.py và py src/09c_validate_actor_domain.py trước.")
        sys.exit(1)

    logger.info(f"[Bước 10.1] Đọc: {input_path.name}")
    df = pd.read_excel(input_path, dtype=str)
    df = df[df["final_label"].astype(str).str.strip().isin(VALID_LABELS)].copy()
    logger.info(f"  -> {len(df)} bản ghi hợp lệ để chấm điểm")

    default_w = float(scoring_cfg.get("default_W_i", 1.0))

    info_cols = [
        "source_id", "legal_citation", "raw_text", "final_label", "final_reason",
        "actor_raw", "actor_primary", "actor_group", "actor_reason",
        "domain_raw", "domain_primary", "domain_secondary", "domain_group", "domain_reason",
        "legal_signal", "tin_hieu_tac_dong", "quantitative_value", "gia_tri_dinh_luong",
    ]
    info_cols = [c for c in info_cols if c in df.columns]
    out = df[info_cols].copy()

    out["suggested_S_range"] = df.get("suggested_S_range", "")
    out["suggested_R_range"] = df.get("suggested_R_range", "")
    out["scoring_warning"] = df.apply(lambda row: build_scoring_warning(row, actor_domain_cfg), axis=1)
    out["M_i"] = ""
    out["S_i"] = ""
    out["D_i"] = ""
    out["R_i"] = ""
    out["W_i"] = default_w
    out["scoring_note"] = ""

    logger.info("[Bước 10.2] Lưu scoring_input.xlsx")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        out.to_excel(writer, sheet_name="scoring_template", index=False)

        rubric_rows = []
        for dim, mapping in RUBRIC_SUMMARY.items():
            for score, desc in mapping.items():
                rubric_rows.append({"dimension": dim, "score": score, "description": desc})
        pd.DataFrame(rubric_rows).to_excel(writer, sheet_name="rubric_reference", index=False)

        actor_rows = []
        for group, spec in actor_domain_cfg.get("actor_groups", {}).items():
            actor_rows.append({
                "actor_group": group,
                "label_vi": spec.get("label_vi", ""),
                "suggested_S_range": format_range(spec.get("suggested_S_range")),
            })
        pd.DataFrame(actor_rows).to_excel(writer, sheet_name="actor_reference", index=False)

        domain_rows = []
        for domain, spec in actor_domain_cfg.get("domains", {}).items():
            domain_rows.append({
                "domain": domain,
                "domain_group": spec.get("group", ""),
                "label_vi": spec.get("label_vi", ""),
                "suggested_R_range": format_range(spec.get("suggested_R_range")),
            })
        pd.DataFrame(domain_rows).to_excel(writer, sheet_name="domain_reference", index=False)

    logger.info(f"  Đã lưu: {output_path.name} ({len(out)} dòng)")
    logger.info("  Bước tiếp theo: điền M_i, S_i, D_i, R_i, W_i và scoring_note nếu cần; sau đó chạy py src/11_calculate_impact_score.py")


if __name__ == "__main__":
    main()
