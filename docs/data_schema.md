# Schema Dữ liệu — Pipeline 2 Tầng

> **Dự án:** DTM — Đánh giá tác động chính sách môi trường-Khung định lượng: lợi ích, chi phí, rủi ro
> **Phiên bản:** 2.0 — Cập nhật lần 2

File này mô tả schema (cấu trúc trường dữ liệu) của tất cả các file dữ liệu trong pipeline, từ đầu vào đến đầu ra cuối cùng.

---

## 1. Schema đầu vào — `data/raw/Luat_bao_ve_moi_truong_2020.json`

Mỗi bản ghi (record) trong file JSON đầu vào gồm các trường:

| Trường               | Kiểu        | Bắt buộc | Mô tả                                                        |
| -------------------- | ----------- | :------: | ------------------------------------------------------------ |
| `source_id`          | string      |    ✅    | ID duy nhất của bản ghi (ví dụ: "LBVMT2020_D1_K1")           |
| `legal_citation`     | string      |    ✅    | Trích dẫn pháp lý (ví dụ: "Điều 1, Khoản 2, Luật BVMT 2020") |
| `raw_text`           | string      |    ✅    | Nội dung văn bản đầy đủ của điều khoản                       |
| `co_tac_dong`        | boolean     |    ✅    | `true` = có tác động chính sách (toàn bộ dataset = true)     |
| `actor`              | string/list |    ❌    | Chủ thể bị ảnh hưởng (ví dụ: "doanh nghiệp", "nhà nước")     |
| `legal_signal`       | string      |    ❌    | Tín hiệu pháp lý (ví dụ: "bắt buộc", "cấm", "khuyến khích")  |
| `domain`             | string      |    ❌    | Domain môi trường từ phân tích sơ bộ                         |
| `quantitative_value` | string      |    ❌    | Giá trị định lượng nếu có (ví dụ: "85%", "500 ha")           |
| `condition`          | string      |    ❌    | Điều kiện áp dụng của điều khoản                             |
| `source_document`    | string      |    ❌    | Tài liệu nguồn (mặc định: "Luật BVMT 2020")                  |

**Ràng buộc tính hợp lệ:**

- `source_id` không được trùng lặp
- `raw_text` không được rỗng
- `co_tac_dong` phải là `true` cho tất cả bản ghi trong dataset này

---

## 2. Schema Tầng 1 — Lọc tác động môi trường

### 2.1 `data/interim/env_manual_label_template.xlsx`

Template để người nghiên cứu gán `env_human`. Gồm tất cả trường đầu vào + các cột cần điền:

| Trường                    | Kiểu      | Điền bởi  | Mô tả                              |
| ------------------------- | --------- | --------- | ---------------------------------- |
| _[Tất cả trường đầu vào]_ | —         | Script 02 | Sao chép từ JSON                   |
| `env_human`               | int (0/1) | 👤 Human  | Nhãn lọc môi trường: 1=có, 0=không |
| `env_human_reason`        | string    | 👤 Human  | Lý do gán nhãn, domain nếu =1      |
| `env_needs_review`        | bool      | 👤 Human  | `True` nếu còn mơ hồ               |

### 2.2 `data/interim/env_llm_labeled_dataset.xlsx`

Output của LLM (script 03). Thêm các cột:

| Trường                   | Kiểu        | Điền bởi | Mô tả                            |
| ------------------------ | ----------- | -------- | -------------------------------- |
| `env_llm`                | int (0/1)   | 🤖 LLM   | Dự đoán nhị phân của LLM         |
| `env_llm_reason`         | string      | 🤖 LLM   | Giải thích của LLM               |
| `env_evidence_span`      | string      | 🤖 LLM   | Trích dẫn bằng chứng từ raw_text |
| `env_confidence`         | float [0,1] | 🤖 LLM   | Độ tự tin                        |
| `env_needs_human_review` | bool        | 🤖 LLM   | LLM đề xuất cần review           |

### 2.3 `data/processed/env_final_dataset.xlsx` (D_env)

Dataset sau adjudication:

| Trường                 | Kiểu      | Mô tả                              |
| ---------------------- | --------- | ---------------------------------- |
| _[Tất cả trường trên]_ | —         | —                                  |
| `env_final`            | int (0/1) | Nhãn chốt = `env_human` sau review |

**Kích thước dự kiến:** |D_env| ≤ N = 581

---

## 3. Schema Tầng 2 — Phân loại 5 nhãn

### 3.1 `data/interim/class_manual_label_template.xlsx`

Chỉ chứa bản ghi có `env_final = 1`:

| Trường                         | Kiểu   | Điền bởi  | Mô tả                                                 |
| ------------------------------ | ------ | --------- | ----------------------------------------------------- |
| _[Trường đầu vào + env_final]_ | —      | Script 06 | Từ env_final_dataset                                  |
| `class_human`                  | string | 👤 Human  | Nhãn 5 lớp: BENEFIT_QUANTITATIVE \| ... \| CONSTRAINT |
| `class_human_reason`           | string | 👤 Human  | Lý do gán nhãn, quy tắc đã dùng                       |
| `class_needs_review`           | bool   | 👤 Human  | `True` nếu còn mơ hồ                                  |

### 3.2 `data/interim/class_llm_labeled_dataset.xlsx`

Output của LLM (script 07):

| Trường                     | Kiểu        | Điền bởi | Mô tả                                    |
| -------------------------- | ----------- | -------- | ---------------------------------------- |
| `class_llm`                | string      | 🤖 LLM   | Nhãn 5 lớp                               |
| `class_llm_reason`         | string      | 🤖 LLM   | Giải thích của LLM                       |
| `class_evidence_span`      | string      | 🤖 LLM   | Bằng chứng từ raw_text                   |
| `class_confidence`         | float [0,1] | 🤖 LLM   | Độ tự tin                                |
| `class_needs_human_review` | bool        | 🤖 LLM   | LLM đề xuất cần review                   |
| `rule_applied`             | string      | 🤖 LLM   | Quy tắc phân biệt nhãn đã dùng (QT1-QT6) |
| `quantity_interpretation`  | string      | 🤖 LLM   | Giải thích con số trong văn bản nếu có   |

### 3.3 `data/processed/final_labeled_dataset.xlsx`

| Trường                            | Mô tả                                |
| --------------------------------- | ------------------------------------ |
| _[Tất cả trường tầng 1 + tầng 2]_ | —                                    |
| `final_label`                     | Nhãn chốt = `class_human` sau review |

### 3.4 `data/interim/actor_domain_review_template.xlsx` (Bước 09b)

Bảng dữ liệu để người nghiên cứu rà soát và sửa đổi các thông tin phân loại chủ thể (actor) và lĩnh vực (domain) trước khi chấm điểm:

| Trường | Kiểu | Điền bởi | Mô tả |
| :--- | :---: | :---: | :--- |
| `source_id` | string | Script 09b | ID duy nhất của bản ghi |
| `raw_text` | string | Script 09b | Nội dung điều khoản |
| `final_label` | string | Script 09b | Nhãn tác động 5 lớp đã chốt từ bước 09 |
| `actor_raw` | string | Script 09b | Chủ thể thô trích xuất từ dữ liệu nguồn |
| `actor_group` | string | Script 09b | Nhóm chủ thể do hệ thống gợi ý |
| `actor_needs_review` | bool | Script 09b | `TRUE` nếu hệ thống phát hiện chủ thể có sự mơ hồ |
| `suggested_S_range` | string | Script 09b | Gợi ý khoảng điểm Scope (S) dựa trên nhóm chủ thể |
| `domain_raw` | string | Script 09b | Lĩnh vực môi trường thô trích xuất từ dữ liệu nguồn |
| `domain_primary` | string | Script 09b | Lĩnh vực môi trường chính do hệ thống gợi ý |
| `domain_needs_review` | bool | Script 09b | `TRUE` nếu hệ thống phát hiện lĩnh vực có sự mơ hồ |
| `suggested_R_range` | string | Script 09b | Gợi ý khoảng điểm Risk (R) dựa trên lĩnh vực chính |
| `review_actor_group` | string | 👤 Human | Người nghiên cứu điền đè nhóm chủ thể đúng nếu cần sửa |
| `review_domain_primary` | string | 👤 Human | Người nghiên cứu điền đè lĩnh vực chính đúng nếu cần sửa |
| `review_domain_secondary`| string | 👤 Human | Người nghiên cứu điền đè các lĩnh vực phụ nếu cần |
| `review_note` | string | 👤 Human | Ghi chú lý do điều chỉnh |

### 3.5 `data/processed/actor_domain_dataset.xlsx` (Bước 09c)

Dataset chính thức chứa thông tin actor và domain đã chốt sau khi áp dụng hiệu chỉnh từ người nghiên cứu ở bước 09b:

| Trường | Kiểu | Mô tả |
| :--- | :---: | :--- |
| _[Tất cả trường ở bước 09b]_ | — | — |
| `actor_group_original` | string | Nhóm chủ thể được gợi ý ban đầu |
| `domain_primary_original` | string | Lĩnh vực môi trường chính được gợi ý ban đầu |
| `domain_secondary_original`| string | Các lĩnh vực phụ được gợi ý ban đầu |
| `actor_domain_reviewed` | bool | `True` nếu bản ghi đã được người nghiên cứu hiệu chuẩn hoặc ghi chú |

---

## 4. Schema Tính điểm

### 4.1 `data/interim/scoring_input.xlsx`

Chỉ chứa bản ghi có `final_label` hợp lệ:

| Trường        | Kiểu      | Điền bởi  | Mô tả                          |
| ------------- | --------- | --------- | ------------------------------ |
| `source_id`   | string    | Script 10 | ID bản ghi                     |
| `final_label` | string    | Script 10 | Từ final_labeled_dataset       |
| `raw_text`    | string    | Script 10 | Để tham chiếu khi chấm         |
| `M_i`         | int [1,5] | 👤 Human  | Magnitude — độ lớn tác động    |
| `S_i`         | int [1,5] | 👤 Human  | Scope — phạm vi ảnh hưởng      |
| `D_i`         | int [1,5] | 👤 Human  | Duration — thời gian tác động  |
| `R_i`         | int [1,5] | 👤 Human  | Risk/Reversibility — rủi ro    |
| `W_i`         | float     | 👤 Human  | Object weight (mặc định = 1.0) |

### 4.2 `data/processed/scored_dataset.xlsx`

Output của script 11:

| Trường                          | Kiểu         | Công thức                | Mô tả                             |
| ------------------------------- | ------------ | ------------------------ | --------------------------------- |
| _[Tất cả trường scoring_input]_ | —            | —                        | —                                 |
| `direction_i`                   | int (+1/-1)  | Từ `labels.yaml`         | Hướng tác động theo `final_label` |
| `C_i`                           | float [1,5]  | `0.25*(M+S+D+R)`         | Điểm tổng hợp trước normalize     |
| `C_i_norm`                      | float [0,1]  | `(C_i - 1) / 4`          | Điểm normalize                    |
| `ImpactScore_i`                 | float [-1,1] | `direction * W * C_norm` | Impact Score cuối cùng            |

---

## 5. Luồng dữ liệu tổng hợp

```
JSON raw (N=581)
    │
    ├─[Script 01]─► input_schema_report.xlsx
    │
    ├─[Script 02]─► env_manual_label_template.xlsx ──► [Human gán env_human]
    │
    ├─[Script 03]─► env_llm_labeled_dataset.xlsx
    │
    ├─[Script 04]─► env_filter_metrics.xlsx
    │               env_error_analysis.xlsx
    │               env_review_dataset.xlsx ──► [Human review bất đồng]
    │
    ├─[Script 05]─► env_final_dataset.xlsx (D_env)
    │
    ├─[Script 06]─► class_manual_label_template.xlsx ──► [Human gán class_human]
    │
    ├─[Script 07]─► class_llm_labeled_dataset.xlsx
    │
    ├─[Script 08]─► classification_metrics.xlsx
    │               class_error_analysis.xlsx
    │               class_review_dataset.xlsx ──► [Human review bất đồng]
    │
    ├─[Script 09]─► final_labeled_dataset.xlsx
    │
    ├─[Script 09b]─► actor_domain_review_template.xlsx ──► [Human rà soát actor/domain]
    │
    ├─[Script 09c]─► actor_domain_dataset.xlsx
    │                 actor_domain_validation_report.xlsx
    │
    ├─[Script 10]─► scoring_input.xlsx ──► [Human chấm M,S,D,R,W]
    │
    ├─[Script 11]─► scored_dataset.xlsx
    │               final_impact_report.xlsx
    │
    ├─[Script 12]─► outputs/figures/*.png
    │
    └─[Script 13]─► pipeline_summary_report.xlsx
```
