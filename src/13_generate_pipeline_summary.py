#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
13_generate_pipeline_summary.py
================================
BƯỚC 13 — Tổng hợp báo cáo cuối cùng của toàn bộ pipeline.

Đề tài: Đánh giá tác động chính sách môi trường — Khung định lượng chi phí,
lợi ích, rủi ro.

Vị trí trong pipeline:
    Bước 01-09 : Chuẩn hóa dữ liệu, lọc môi trường, phân loại 5 nhãn và chốt
                 final_label.
    Bước 09b   : Chuẩn hóa/gợi ý actor và domain.
    Bước 09c   : Validate actor/domain và xuất actor_domain_dataset.xlsx.
    Bước 10    : Tạo scoring_input.xlsx.
    Bước 11    : Validate điểm chấm và tính Impact Score.
    Bước 12    : Tạo biểu đồ.
    Bước 13    : Tổng hợp các kết quả thành pipeline_summary_report.xlsx.

Input chính:
    data/reports/env_filter_metrics.xlsx
        Metric tầng 1: lọc tác động môi trường.

    data/reports/classification_metrics.xlsx
        Metric tầng 2: phân loại 5 nhãn.

    data/reports/actor_domain_validation_report.xlsx
        Báo cáo validate actor/domain trước scoring.

    data/reports/scoring_validation_report.xlsx
        Báo cáo validate điểm M, S, D, R, W trước khi tính Impact Score.

    data/reports/scoring_summary.xlsx
        Tổng hợp Impact Score.

    data/processed/scored_dataset.xlsx
        Dataset chi tiết đã tính điểm.

Output:
    data/reports/pipeline_summary_report.xlsx
        Báo cáo tổng hợp cuối cùng của pipeline.

Các sheet chính trong báo cáo:
    pipeline_overview:
        Tóm tắt số lượng bản ghi, metric chính và kết luận tổng thể.

    env_filter_results:
        Kết quả tầng 1 nếu file metric tồn tại.

    classification_results:
        Kết quả tầng 2 nếu file metric tồn tại.

    actor_domain_validation:
        Kết quả kiểm định actor/domain nếu file report tồn tại.

    scoring_validation:
        Kết quả kiểm định điểm scoring nếu file report tồn tại.

    impact_score_results:
        Tổng hợp Impact Score nếu file scoring_summary tồn tại.

    methodology_notes:
        Ghi chú phương pháp để người đọc hiểu cách hệ thống tạo kết quả.

Cơ chế hoạt động:
    1. Đọc các file báo cáo và dataset thành phần nếu tồn tại.
    2. Đếm số bản ghi ở các mốc chính: env_final, final_labeled,
       actor_domain và scored.
    3. Trích xuất các metric quan trọng từ báo cáo tầng 1, tầng 2 và scoring.
    4. Tạo pipeline_overview để nhìn nhanh toàn bộ trạng thái hệ thống.
    5. Ghi kèm methodology_notes để giải thích logic human-in-the-loop,
       actor/domain guideline, scoring validation và công thức Impact Score.

Ý nghĩa phương pháp:
    Bước này không tính lại nhãn hay điểm. Nó gom toàn bộ kết quả đã sinh ở các
    bước trước thành một báo cáo cuối, giúp người nghiên cứu kiểm tra tính đầy
    đủ, tính nhất quán và khả năng giải thích của pipeline.

Sử dụng:
    py src/13_generate_pipeline_summary.py

Kết quả cuối cùng:
    Mở data/reports/pipeline_summary_report.xlsx để xem tóm tắt toàn bộ hệ thống.
"""

import logging
import sys
from datetime import datetime
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


def load_config() -> dict:
    with open(PROJECT_ROOT / "config" / "project_config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def safe_read_excel(path: Path, sheet_name=0) -> pd.DataFrame | None:
    if not path.exists():
        logger.warning(f"  Không tìm thấy: {path.name}")
        return None
    try:
        return pd.read_excel(path, sheet_name=sheet_name, dtype=str)
    except Exception as exc:
        logger.warning(f"  Lỗi đọc {path.name}: {exc}")
        return None


def metric_dict(df: pd.DataFrame | None, key_col: str, value_col: str) -> dict:
    if df is None or key_col not in df.columns:
        return {}
    out = {}
    for _, row in df.iterrows():
        out[str(row.get(key_col, "")).strip()] = row.get(value_col, "N/A")
    return out


def build_pipeline_overview(cfg: dict, counts: dict, env_metrics: dict, class_metrics: dict, impact_metrics: dict) -> pd.DataFrame:
    total_impact = impact_metrics.get("TotalImpact", "N/A")
    try:
        total_float = float(total_impact)
        conclusion = "Tác động tích cực tổng thể" if total_float > 0 else "Tác động tiêu cực tổng thể" if total_float < 0 else "Tác động trung lập"
    except (TypeError, ValueError):
        conclusion = "N/A"

    rows = [
        ("Dự án", cfg.get("project", {}).get("name_vi", "DTM")),
        ("Tác giả", cfg.get("project", {}).get("author", "")),
        ("Phiên bản", cfg.get("project", {}).get("version", "")),
        ("Ngày báo cáo", datetime.now().strftime("%Y-%m-%d %H:%M")),
        ("N đầu vào sau lọc môi trường", counts.get("n_env_final", 0)),
        ("N final_labeled_dataset", counts.get("n_final_labeled", 0)),
        ("N actor_domain_dataset", counts.get("n_actor_domain", 0)),
        ("N scored_dataset", counts.get("n_scored", 0)),
        ("Accuracy_env", env_metrics.get("Accuracy_env", "N/A")),
        ("F1_env", env_metrics.get("F1_env", "N/A")),
        ("Accuracy_class", class_metrics.get("Accuracy_class", "N/A")),
        ("Macro-F1_class", class_metrics.get("Macro-F1_class", "N/A")),
        ("TotalImpact", total_impact),
        ("MeanImpact", impact_metrics.get("MeanImpact", "N/A")),
        ("StdImpact", impact_metrics.get("StdImpact", "N/A")),
        ("Nhận xét tổng thể", conclusion),
    ]
    return pd.DataFrame(rows, columns=["Chỉ số", "Giá trị"])


def build_methodology_notes(cfg: dict) -> pd.DataFrame:
    rows = [
        ("Phân loại LLM", "Human-in-the-loop: nhãn người nghiên cứu và nhãn LLM được so sánh, sau đó adjudication để chốt final_label."),
        ("LLM sử dụng", cfg.get("llm", {}).get("model", "gemini-3.5-flash")),
        ("Metric LLM", "Metric tầng 1 và tầng 2 được tính trước adjudication, không dùng final_label để tự đánh giá LLM."),
        ("Chuẩn hóa actor", "Theo docs/guideline_identify_actor.md và config/actor_domain_config.yaml; output chốt ở actor_domain_dataset.xlsx."),
        ("Chuẩn hóa domain", "Theo docs/guideline_identify_domain.md và config/actor_domain_config.yaml; output chốt ở actor_domain_dataset.xlsx."),
        ("Kiểm định trước scoring", "09c kiểm định actor/domain; 11 kiểm định M/S/D/R/W, suggested ranges và scoring_note trước khi tính điểm."),
        ("Impact Score", "C_i = alpha*M_i + beta*S_i + gamma*D_i + delta*R_i; C_norm = (C_i - min)/(max - min); ImpactScore = direction*W_i*C_norm."),
        ("W_i", "Mặc định W_i = 1.0; mọi thay đổi phải có scoring_note."),
        ("Tài liệu scoring", "docs/scoring_rubric_MSDR.md"),
    ]
    return pd.DataFrame(rows, columns=["Hạng mục", "Mô tả"])


def main():
    cfg = load_config()

    logger.info("=" * 60)
    logger.info("  BƯỚC 13 - Tổng hợp báo cáo pipeline")
    logger.info("=" * 60)

    report_dir = PROJECT_ROOT / cfg["paths"]["reports"]
    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_data"]

    logger.info("[Bước 13.1] Đọc báo cáo thành phần")
    df_env_metrics = safe_read_excel(report_dir / cfg["report_files"]["env_filter_metrics"])
    df_class_metrics = safe_read_excel(report_dir / cfg["report_files"]["classification_metrics"])
    df_score_summary = safe_read_excel(report_dir / cfg["report_files"]["scoring_summary"])
    df_actor_domain_validation = safe_read_excel(report_dir / cfg["report_files"].get("actor_domain_validation_report", "actor_domain_validation_report.xlsx"))
    df_scoring_validation = safe_read_excel(report_dir / cfg["report_files"].get("scoring_validation_report", "scoring_validation_report.xlsx"))

    df_env_final = safe_read_excel(processed_dir / cfg["processed_files"]["env_final_dataset"])
    df_final_labeled = safe_read_excel(processed_dir / cfg["processed_files"]["final_labeled_dataset"])
    df_actor_domain = safe_read_excel(processed_dir / cfg["processed_files"].get("actor_domain_dataset", "actor_domain_dataset.xlsx"))
    df_scored = safe_read_excel(processed_dir / cfg["processed_files"].get("scored_dataset", "scored_dataset.xlsx"))

    counts = {
        "n_env_final": 0 if df_env_final is None else len(df_env_final),
        "n_final_labeled": 0 if df_final_labeled is None else len(df_final_labeled),
        "n_actor_domain": 0 if df_actor_domain is None else len(df_actor_domain),
        "n_scored": 0 if df_scored is None else len(df_scored),
    }

    env_metrics = metric_dict(df_env_metrics, "Metric", "Giá trị")
    class_metrics = metric_dict(df_class_metrics, "Metric", "Giá trị")
    impact_metrics = metric_dict(df_score_summary, "Chỉ số", "Giá trị")

    logger.info("[Bước 13.2] Ghi pipeline_summary_report.xlsx")
    output_path = report_dir / cfg["report_files"]["pipeline_summary_report"]
    report_dir.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        build_pipeline_overview(cfg, counts, env_metrics, class_metrics, impact_metrics).to_excel(
            writer, sheet_name="pipeline_overview", index=False
        )
        if df_env_metrics is not None:
            df_env_metrics.to_excel(writer, sheet_name="env_filter_results", index=False)
        if df_class_metrics is not None:
            df_class_metrics.to_excel(writer, sheet_name="classification_results", index=False)
        if df_actor_domain_validation is not None:
            df_actor_domain_validation.to_excel(writer, sheet_name="actor_domain_validation", index=False)
        if df_scoring_validation is not None:
            df_scoring_validation.to_excel(writer, sheet_name="scoring_validation", index=False)
        if df_score_summary is not None:
            df_score_summary.to_excel(writer, sheet_name="impact_score_results", index=False)
        build_methodology_notes(cfg).to_excel(writer, sheet_name="methodology_notes", index=False)

    logger.info(f"  Đã lưu: {output_path.name}")
    logger.info("=" * 60)
    logger.info("  PIPELINE HOÀN THÀNH")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
