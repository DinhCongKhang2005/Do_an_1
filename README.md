# DTM: Hệ thống Đánh giá Tác động Chính sách Môi trường

DTM là hệ thống phần mềm hỗ trợ lượng hóa bán định lượng tác động chính sách môi trường từ văn bản quy phạm pháp luật. Hệ thống kết hợp giữa xử lý ngôn ngữ tự nhiên tự động bằng Mô hình ngôn ngữ lớn (Google Gemini) và cơ chế rà soát có con người kiểm chứng (Human-in-the-loop) để đảm bảo độ tin cậy khoa học cao nhất.

Hệ thống được áp dụng thực nghiệm trên **Luật Bảo vệ môi trường năm 2020** với $581$ bản ghi pháp lý độc lập.

---

## 1. Yêu cầu hệ thống và cài đặt

### Yêu cầu tiên quyết
* Python 3.10 trở lên
* Khóa API Google Gemini (`GEMINI_API_KEY`)

### Cài đặt các thư viện cần thiết
Cài đặt các gói phụ thuộc bằng lệnh sau:
```bash
pip install pandas numpy matplotlib seaborn google-generativeai openpyxl
```

### Cấu hình biến môi trường API Key
Để chạy các mô-đun LLM, thiết lập API key của bạn:

* **Trên Windows PowerShell:**
  ```powershell
  $env:GEMINI_API_KEY="khóa-api-gemini-của-bạn"
  ```
* **Trên Windows Command Prompt (cmd):**
  ```cmd
  set GEMINI_API_KEY=khóa-api-gemini-của-bạn
  ```

---

## 2. Chuỗi xử lý tuần tự (Pipeline Scripts)

Pipeline của hệ thống gồm 13 bước thực thi tuần tự. Hãy chạy các script theo thứ tự dưới đây:

### Pha 1: Chuẩn bị và Kiểm định
1. **Kiểm tra cấu trúc schema đầu vào:**
   ```bash
   py src/01_validate_input_schema.py
   ```
   *Kiểm tra tính toàn vẹn của tệp dữ liệu JSON gốc.*

### Pha 2: Lọc tác động môi trường (Tầng 1)
2. **Khởi tạo file gán nhãn thủ công:**
   ```bash
   py src/02_build_env_manual_label_file.py
   ```
3. **LLM dự đoán nhãn lọc nhị phân:**
   ```bash
   py src/03_run_llm_env_filtering.py
   ```
4. **Tính toán metric và phát hiện bất đồng:**
   ```bash
   py src/04_eval_env_filtering_accuracy.py
   ```
5. **Gộp nhãn sau khi phân xử bất đồng nhãn:**
   ```bash
   py src/05_build_env_final_dataset.py
   ```

### Pha 3: Phân loại tác động chính sách (Tầng 2)
6. **Khởi tạo file gán nhãn tác động 5 lớp:**
   ```bash
   py src/06_build_class_manual_label_file.py
   ```
7. **LLM phân loại 5 lớp tác động chính sách:**
   ```bash
   py src/07_run_llm_class_labeling.py
   ```
8. **Đo hiệu năng học máy và xuất file rà soát bất đồng:**
   ```bash
   py src/08_eval_class_labeling_accuracy.py
   ```
9. **Chốt dữ liệu nhãn tác động cuối cùng:**
   ```bash
   py src/09_build_final_labeled_dataset.py
   ```

### Pha 3b: Chuẩn hóa ngữ nghĩa chủ thể và lĩnh vực
10. **Tạo bảng rà soát chủ thể và lĩnh vực:**
    ```bash
    py src/09b_build_actor_domain_review.py
    ```
11. **Xác thực dữ liệu Actor và Domain:**
    ```bash
    py src/09c_validate_actor_domain.py
    ```

### Pha 4: Lượng hóa điểm tác động (MSDR)
12. **Tạo biểu mẫu chấm điểm:**
    ```bash
    py src/10_build_scoring_input.py
    ```
    *Người nghiên cứu thực hiện chấm điểm các tiêu chí $M_i, S_i, D_i, R_i$ trong tệp Excel.*
13. **Tính toán điểm tác động chính sách:**
    ```bash
    py src/11_calculate_impact_score.py
    ```

### Pha 5: Trực quan hóa và Kết xuất
14. **Sinh các biểu đồ phân tích:**
    ```bash
    py src/12_generate_figures.py
    ```
15. **Kết xuất báo cáo tổng kết chất lượng:**
    ```bash
    py src/13_generate_pipeline_summary.py
    ```

---

## 3. Cấu trúc thư mục dự án

```text
├── data/                  # Chứa dữ liệu đầu vào và các tệp báo cáo Excel (.xlsx)
├── docs/                  # Bản thảo báo cáo đồ án và các hướng dẫn nghiệp vụ
│   ├── guidelines/        # Hướng dẫn chi tiết (gán nhãn, chấm điểm, phân xử)
│   └── Ban_thao_do_an_lan_3.md # Bản thảo báo cáo đồ án đã rút gọn
├── outputs/               # Chứa các biểu đồ phân tích kết quả dạng .png
├── src/                   # Mã nguồn Python chạy pipeline hệ thống
│   ├── prompts/           # Lưu trữ các tệp prompt thô đầy đủ cho Tầng 1 và Tầng 2
│   └── utils/             # Các hàm bổ trợ đọc/ghi và kết nối API
├── .gitignore             # Danh sách loại trừ đồng bộ Git
└── README.md              # Tài liệu hướng dẫn sử dụng này
```
