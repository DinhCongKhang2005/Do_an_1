# Các bước chạy hệ thống DTM — Hướng dẫn chi tiết

> **Phiên bản:** 3.0.0 (Cập nhật lần 2 — Pipeline 2 tầng)  
> **Cập nhật:** Tháng 6/2026  
> Tài liệu này mô tả chi tiết từng bước chạy pipeline, bao gồm lý do, đầu vào, đầu ra và các điểm kiểm tra.

---

## ⚠️ Đọc trước khi chạy

### Nguyên tắc bất di bất dịch

| Quy tắc | Hậu quả nếu vi phạm |
|---|---|
| **Metric Tầng 1 (script 04) phải chạy TRƯỚC khi sửa env_human** | Metric bị inflate — không phản ánh khả năng LLM |
| **Metric Tầng 2 (script 08) phải chạy TRƯỚC khi sửa class_human** | Tương tự |
| **Không dùng `env_llm` hay `class_llm` làm `final_label` trực tiếp** | Vi phạm nguyên tắc human-in-the-loop |
| **Impact Score chỉ tính từ `final_label`** | Dùng nhãn LLM thô → điểm không đáng tin cậy |
| **W_i = 1.0 nếu không có cơ sở thay đổi** | Trọng số tùy tiện → Impact Score không có giá trị học thuật |

---

## GIAI ĐOẠN 0 — Chuẩn bị (Một lần duy nhất)

### 0.1 Kiểm tra môi trường

```bash
python --version        # Cần Python >= 3.10
pip install -r requirements.txt
```

### 0.2 Cấu hình credentials

```bash
cp .env.example .env
```

Chỉnh sửa `.env`:
```env
# Google AI Studio (cho dev/test)
GOOGLE_API_KEY=your_api_key_here
LLM_PROVIDER=google_ai_studio

# Hoặc Vertex AI (cho production)
# LLM_PROVIDER=vertex_ai
# GOOGLE_CLOUD_PROJECT=your_project_id
# GOOGLE_CLOUD_LOCATION=us-central1
# GOOGLE_APPLICATION_CREDENTIALS=secrets/gcp_key.json

# Model và tham số
LLM_MODEL_NAME=gemini-2.5-flash
LLM_TEMPERATURE=0.0
LLM_DELAY_SECONDS=0.5
```

---

## GIAI ĐOẠN 1 — Kiểm tra đầu vào

### Script 01: `01_validate_input_schema.py`

**Mục đích:** Kiểm tra file JSON đầu vào có đúng schema không trước khi chạy pipeline.

**Đầu vào:** `data/raw/Luat_bao_ve_moi_truong_2020.json`  
**Đầu ra:** `data/reports/input_schema_report.xlsx`

```bash
python src/01_validate_input_schema.py
```

**Kiểm tra kết quả:**
- ✅ `N = 581` bản ghi (nếu khác, kiểm tra lại file JSON)
- ✅ Không có `source_id` trùng lặp
- ✅ Không có `raw_text` rỗng
- ✅ Tất cả bản ghi có `co_tac_dong = true`

---

## GIAI ĐOẠN 2 — Tầng 1: Lọc Môi Trường

### Script 02: `02_build_env_manual_label_file.py`

**Mục đích:** Tạo file template Excel để gán nhãn `env_human`.

```bash
python src/02_build_env_manual_label_file.py
```

**Đầu ra:** `data/interim/env_manual_label_template.xlsx`

**Hướng dẫn gán nhãn thủ công:**
1. 📖 Đọc `docs/environmental_filter_guideline.md`
2. Mở `env_manual_label_template.xlsx`
3. Điền cột **`env_human`** (màu vàng):
   - `1` = Có tác động môi trường
   - `0` = Không có tác động môi trường
4. Điền **`env_human_reason`**: Tên domain môi trường + lý do ngắn gọn
5. Điền **`env_needs_review`**: `True` nếu còn nghi ngờ
6. 💾 **Lưu thành:** `data/interim/env_human_labeled_dataset.xlsx`

---

### Script 03: `03_llm_filter_environmental_impact.py`

**Mục đích:** LLM dự đoán `env_llm` độc lập với `env_human`.

```bash
# Chạy đầy đủ
python src/03_llm_filter_environmental_impact.py

# Test 10 bản ghi đầu
python src/03_llm_filter_environmental_impact.py --limit 10

# Tiếp tục nếu bị gián đoạn
python src/03_llm_filter_environmental_impact.py --resume
```

**Đầu ra:** `data/interim/env_llm_labeled_dataset.xlsx`, `outputs/logs/env_filter.log`

**Lưu ý:** Với 581 bản ghi và delay 0.5s, dự kiến ~5–7 phút.

---

### Script 04: `04_compare_env_human_vs_llm.py`

> ⚠️ **QUAN TRỌNG: Chạy script này TRƯỚC khi review bất kỳ nhãn nào!**

**Mục đích:** Tính metric Tầng 1 và tạo review dataset cho bản ghi bất đồng.

```bash
python src/04_compare_env_human_vs_llm.py
```

**Đầu ra:**
- `data/reports/env_filter_metrics.xlsx` — Accuracy, Precision, Recall, F1
- `data/reports/env_error_analysis.xlsx` — Phân tích FP/FN
- `data/interim/env_review_dataset.xlsx` — Bản ghi bất đồng cần review
- `outputs/figures/env_confusion_matrix.png`
- `outputs/figures/env_metric_summary.png`

**Xem kết quả:** Metric được in ra terminal. **Ghi lại `Recall_env`** (ưu tiên cao nhất).

**Hướng dẫn review:**
1. 📖 Đọc `docs/adjudication_protocol.md`
2. Mở `env_review_dataset.xlsx`
3. Xem xét từng bản ghi bất đồng (FP và FN)
4. Nếu `env_human` sai → sửa trong `env_human_labeled_dataset.xlsx`
5. Nếu `env_llm` sai nhưng `env_human` đúng → không sửa

---

### Script 05: `05_build_env_final_dataset.py`

**Mục đích:** Chốt `env_final = env_human` (sau review) và tạo D_env.

```bash
python src/05_build_env_final_dataset.py
```

**Đầu ra:**
- `data/processed/env_final_dataset.xlsx` — Toàn bộ 581 bản ghi với `env_final`
- `outputs/figures/data_funnel.png`

---

## GIAI ĐOẠN 3 — Tầng 2: Phân loại 5 nhãn

### Script 06: `06_build_class_manual_label_file.py`

**Mục đích:** Tạo template gán nhãn 5 lớp từ D_env.

```bash
python src/06_build_class_manual_label_file.py
```

**Đầu ra:** `data/interim/class_manual_label_template.xlsx`

**Hướng dẫn gán nhãn:**
1. 📖 Đọc `docs/label_guideline_5_labels.md`
2. Mở `class_manual_label_template.xlsx` (sheet: `class_label_template`)
3. Tham khảo sheet `labels_reference` cho mô tả nhãn
4. Điền cột **`class_human`** (màu vàng) — viết ĐÚNG tên nhãn:
   - `BENEFIT_QUANTITATIVE` | `BENEFIT_QUALITATIVE`
   - `COST_QUANTITATIVE` | `COST_QUALITATIVE` | `CONSTRAINT`
5. Điền **`class_human_reason`**: Quy tắc đã dùng (QT1-QT6) + lý do
6. Điền **`class_needs_review`**: `True` nếu còn mơ hồ
7. 💾 **Lưu thành:** `data/interim/class_human_labeled_dataset.xlsx`

---

### Script 07: `07_llm_classify_5_labels.py`

**Mục đích:** LLM phân loại 5 nhãn độc lập.

```bash
python src/07_llm_classify_5_labels.py
python src/07_llm_classify_5_labels.py --limit 10  # Test
python src/07_llm_classify_5_labels.py --resume    # Tiếp tục
```

**Đầu ra:** `data/interim/class_llm_labeled_dataset.xlsx`, `outputs/logs/classify_5labels.log`

---

### Script 08: `08_compare_5label_human_vs_llm.py`

> ⚠️ **QUAN TRỌNG: Chạy script này TRƯỚC khi review bất kỳ nhãn nào!**

```bash
python src/08_compare_5label_human_vs_llm.py
```

**Đầu ra:**
- `data/reports/classification_metrics.xlsx` — Accuracy, Macro-F1, per-class
- `data/reports/class_error_analysis.xlsx`
- `data/interim/class_review_dataset.xlsx`
- `outputs/figures/confusion_matrix.png`
- `outputs/figures/normalized_confusion_matrix.png`
- `outputs/figures/classification_metric_by_label.png`
- `outputs/figures/top_error_pairs.png`

**Review adjudication:**
1. 📖 Đọc `docs/adjudication_protocol.md`
2. Xem `class_review_dataset.xlsx`
3. Xem xét từng bản ghi bất đồng
4. Nếu cần sửa → sửa trong `class_human_labeled_dataset.xlsx`

---

### Script 09: `09_build_final_labeled_dataset.py`

```bash
python src/09_build_final_labeled_dataset.py
```

**Đầu ra:** `data/processed/final_labeled_dataset.xlsx`
---

## GIAI ĐOẠN 3b — Chuẩn hóa và Kiểm duyệt Actor / Domain

### Script 09b: `09b_build_actor_domain_review.py`

**Mục đích:** Hệ thống tự động phân loại, gợi ý nhóm chủ thể (`actor_group`) và lĩnh vực môi trường chính (`domain_primary`) dựa trên từ khóa pháp lý nhằm hỗ trợ chuẩn hóa dữ liệu trước khi chấm điểm.

```bash
python src/09b_build_actor_domain_review.py
```

**Đầu ra:** `data/interim/actor_domain_review_template.xlsx`

**Hướng dẫn rà soát thủ công:**
1. 📖 Đọc `docs/guideline_identify_actor.md` và `docs/guideline_identify_domain.md`
2. Mở file `actor_domain_review_template.xlsx`
3. Kiểm tra các dòng có `actor_needs_review` hoặc `domain_needs_review` được đánh dấu `TRUE`
4. Nếu gợi ý của hệ thống chưa chuẩn xác, điền đè giá trị hiệu chuẩn vào các cột màu vàng:
   - **`review_actor_group`**: Điền nhóm chủ thể chính xác (ví dụ: `BUSINESS_FACILITY`, `STATE_AGENCY`)
   - **`review_domain_primary`**: Điền domain chính (ví dụ: `waste`, `water`)
   - **`review_domain_secondary`**: Điền domain phụ nếu bản ghi liên quan đến nhiều lĩnh vực
   - **`review_note`**: Ghi chú giải thích cho việc sửa đổi
5. 💾 **Lưu lại file** (giữ nguyên tên và vị trí)

---

### Script 09c: `09c_validate_actor_domain.py`

**Mục đích:** Kiểm tra tính hợp lệ của các nhóm chủ thể và lĩnh vực môi trường sau khi người nghiên cứu hiệu chuẩn ở bước 09b. Ngăn chặn các lỗi cấu trúc (lệch nhóm, sai chính tả) trước khi bước vào chấm điểm.

```bash
python src/09c_validate_actor_domain.py
```

**Đầu ra:**
- `data/processed/actor_domain_dataset.xlsx` (Chỉ xuất khi kiểm định không còn lỗi chặn `ERROR`)
- `data/reports/actor_domain_validation_report.xlsx` (Báo cáo tổng hợp số lỗi `ERROR` và cảnh báo `WARNING`)

---

## GIAI ĐOẠN 4 — Tính điểm Impact Score

### Script 10: `10_build_scoring_input.py`

**Mục đích:** Tạo template để người nghiên cứu chấm điểm tác động bán định lượng (M_i, S_i, D_i, R_i, W_i).

**Đầu vào:** `data/processed/actor_domain_dataset.xlsx`  
**Đầu ra:** `data/interim/scoring_input.xlsx`

```bash
python src/10_build_scoring_input.py
```

**Hướng dẫn chấm điểm:**
1. 📖 Đọc `docs/scoring_rubric_MSDR.md`
2. Mở `scoring_input.xlsx`
3. Tham khảo sheet `rubric_reference`
4. Điền **M_i, S_i, D_i, R_i** (1–5) cho từng bản ghi
5. Giữ **W_i = 1.0** trừ khi có cơ sở học thuật để thay đổi
6. 💾 Lưu file lại (cùng tên)

---

### Script 11: `11_calculate_impact_score.py`

```bash
python src/11_calculate_impact_score.py

# Với trọng số tùy chỉnh (sensitivity analysis)
python src/11_calculate_impact_score.py --weights 0.3 0.2 0.3 0.2
```

**Đầu ra:**
- `data/processed/scored_dataset.xlsx`
- `data/reports/scoring_summary.xlsx`
- `data/reports/final_impact_report.xlsx`

---

### Script 12: `12_generate_figures.py`

```bash
python src/12_generate_figures.py
python src/12_generate_figures.py --dpi 300  # Chất lượng cao hơn
```

---

### Script 13: `13_generate_pipeline_summary.py`

```bash
python src/13_generate_pipeline_summary.py
```

**Đầu ra:** `data/reports/pipeline_summary_report.xlsx`

---

## Kiểm tra nhanh đầu ra

```bash
# Kiểm tra tất cả file reports
Get-ChildItem data/reports -Name
Get-ChildItem outputs/figures -Name
Get-ChildItem data/processed -Name
```

---

## Giải quyết sự cố thường gặp

| Lỗi | Nguyên nhân | Giải pháp |
|---|---|---|
| `FileNotFoundError` cho file interim | Chưa chạy script trước | Chạy đúng thứ tự scripts |
| LLM trả về nhãn không hợp lệ | Model không follow prompt | Kiểm tra log, xem `class_llm_error` |
| `GOOGLE_API_KEY` không hợp lệ | Sai key hoặc chưa có | Kiểm tra `.env` |
| Metric Tầng 1 thấp (F1 < 0.6) | Prompt chưa đủ rõ hoặc data noise | Xem error analysis FP/FN |
| `W_i = 0` hoặc âm | Lỗi nhập liệu | Script 11 sẽ tự sửa về 1.0 |
