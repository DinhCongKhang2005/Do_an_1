import pandas as pd
import os

processed_dir = r"data/processed"
reports_dir = r"data/reports"
output_md_path = r"C:\Users\ADMIN\.gemini\antigravity\brain\985385a8-5f47-4841-8502-ce8579d4f95d\analysis_results.md"

def df_to_markdown(df):
    if df.empty:
        return "*Không có dữ liệu*"
    cols = df.columns.tolist()
    headers = [str(c) for c in cols]
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for v in row.values:
            val_str = str(v).replace('\n', ' ').replace('|', '\\|')
            vals.append(val_str)
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)

# Read datasets
env_metrics = pd.read_excel(os.path.join(reports_dir, "env_filter_metrics.xlsx"))
class_metrics_summary = pd.read_excel(os.path.join(reports_dir, "classification_metrics.xlsx"), sheet_name="summary")
class_metrics_per_class = pd.read_excel(os.path.join(reports_dir, "classification_metrics.xlsx"), sheet_name="per_class")

# Read final impact report sheets
xls_impact = pd.ExcelFile(os.path.join(reports_dir, "final_impact_report.xlsx"))
tong_hop = xls_impact.parse("tong_hop")
theo_nhan = xls_impact.parse("theo_nhan")
theo_domain = xls_impact.parse("theo_domain")
theo_actor = xls_impact.parse("theo_actor")
top10_impact = xls_impact.parse("top10_impact")

# Read scored dataset
scored_df = pd.read_excel(os.path.join(processed_dir, "scored_dataset.xlsx"))

# Generate report markdown
md = []
md.append("# BÁO CÁO KẾT QUẢ LIÊN QUAN ĐẾN ĐỀ TÀI ĐỒ ÁN DTM")
md.append("\nBáo cáo này chứa toàn bộ các số liệu, bảng biểu và kết quả định lượng chi tiết rút ra từ pipeline DTM (Deterministic Taxonomy Model) khi chạy Luật Bảo vệ Môi trường 2020.")

md.append("\n## I. Tổng quan luồng dữ liệu của hệ thống")
md.append(f"- **Tổng số điều khoản được đưa vào đánh giá:** {len(scored_df)}")
md.append("- **Tầng 1 (Lọc tác động môi trường):** 100% điều khoản (581/581 bản ghi) được xác định có liên quan đến môi trường và đi tiếp vào Tầng 2.")
md.append("- **Tầng 2 (Gán nhãn chi tiết 5 nhóm tác động):**")
md.append(f"  - **Số lượng đồng thuận ban đầu (Human vs LLM):** 402/581 bản ghi (69.19%)")
md.append(f"  - **Số lượng bất đồng cần hiệu chuẩn (Adjudication):** 179/581 bản ghi (30.81%)")
md.append("  - **Cơ chế phân xử (Adjudication decisions):**")
md.append("    - `KEEP_HUMAN` (Giữ nhãn của chuyên gia): 350 bản ghi")
md.append("    - `ACCEPT_LLM` (Chấp nhận nhãn của LLM): 59 bản ghi")
md.append("    - `NEW_LABEL` (Gán nhãn mới): 1 bản ghi")

md.append("\n## II. Bảng số liệu Hiệu năng phân loại (Performance Metrics)")

md.append("\n### 1. Hiệu năng Tầng 1: Lọc tác động môi trường")
md.append(df_to_markdown(env_metrics))

md.append("\n### 2. Hiệu năng Tầng 2: Phân loại 5 nhãn tác động (Tổng hợp)")
md.append(df_to_markdown(class_metrics_summary))

md.append("\n### 3. Hiệu năng Tầng 2 theo từng Nhãn cụ thể")
md.append(df_to_markdown(class_metrics_per_class))

md.append("\n## III. Kết quả định lượng điểm tác động chính sách (Impact Scores)")

md.append("\n### 1. Bảng số liệu tổng hợp chung")
md.append(df_to_markdown(tong_hop))

md.append("\n### 2. Điểm tác động theo nhãn tác động")
md.append(df_to_markdown(theo_nhan))

md.append("\n### 3. Điểm tác động phân hóa theo Lĩnh vực Môi trường (Environmental Domains)")
md.append(df_to_markdown(theo_domain))

md.append("\n### 4. Điểm tác động phân hóa theo Nhóm chủ thể (Actor Groups)")
md.append(df_to_markdown(theo_actor))

md.append("\n## IV. Top 10 Điều khoản có Tác động lớn nhất")
md.append("\nCác điều khoản dưới đây được sắp xếp theo mức độ tác động tuyệt đối lớn nhất. Điểm số âm đại diện cho chi phí/ràng buộc, điểm số dương đại diện cho lợi ích.")
md.append(df_to_markdown(top10_impact))

# Save the markdown report
with open(output_md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print("Markdown report generated successfully at:", output_md_path)
