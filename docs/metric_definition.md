# Định Nghĩa Các Metrics Đánh Giá — Pipeline 2 Tầng

> **Cập nhật lần 2:** Bổ sung metric Tầng 1 (env filtering) và End-to-end Accuracy.

## Mục đích

File này định nghĩa toàn bộ các metric sử dụng trong pipeline 2 tầng:

- **Tầng 1:** Đánh giá LLM lọc tác động môi trường (binary classification: `env_llm` vs `env_human`)
- **Tầng 2:** Đánh giá LLM phân loại 5 nhãn (multi-class: `class_llm` vs `class_human`)
- **Tổng hợp:** End-to-end Accuracy (cả 2 tầng)

> ⚠️ **Nguyên tắc bất di bất dịch:** Tất cả metric đều được tính dựa trên `llm_label vs human_label` — **KHÔNG BAO GIờ** dùng `final_label` để đánh giá LLM.

---

## PHẦN A — Metric Tầng 1: Lọc Tác Động Môi Trường

> Script tính: `src/04_compare_env_human_vs_llm.py`  
> Dữ liệu: `env_human` (reference) vs `env_llm` (LLM prediction)  
> Tập đánh giá: toàn bộ D_impact (N = 581)

### Ký hiệu cho Tầng 1

| Ký hiệu | Nghĩa                                             |
| ------- | ------------------------------------------------- |
| N       | Tổng số bản ghi (= 581)                           |
| TP_env  | LLM dự đoán = 1, human = 1                        |
| TN_env  | LLM dự đoán = 0, human = 0                        |
| FP_env  | LLM dự đoán = 1, human = 0 (dương tính giả)       |
| FN_env  | LLM dự đoán = 0, human = 1 (không phát hiện được) |

### A.1 — Confusion Matrix 2×2

Ma trận 2×2, hàng = `env_human`, cột = `env_llm`:

|              | Pred = 0 | Pred = 1 |
| ------------ | -------- | -------- |
| **True = 0** | TN_env   | FP_env   |
| **True = 1** | FN_env   | TP_env   |

### A.2 — Accuracy_env

$$\text{Accuracy}_{env} = \frac{TP_{env} + TN_{env}}{N}$$

- **Ý nghĩa:** Tỷ lệ bản ghi LLM lọc đúng (cả có và không có tác động môi trường)
- **Phạm vi:** [0, 1]

### A.3 — Precision_env

$$\text{Precision}_{env} = \frac{TP_{env}}{TP_{env} + FP_{env}}$$

- **Ý nghĩa:** Trong số bản ghi LLM nói "có tác động môi trường", có bao nhiêu % thực sự đúng?

### A.4 — Recall_env

$$\text{Recall}_{env} = \frac{TP_{env}}{TP_{env} + FN_{env}}$$

- **Ý nghĩa:** Trong số bản ghi thực sự có tác động môi trường (env_human=1), LLM phát hiện được bao nhiêu %?
- **Quan trọng hơn Precision** trong ngữ cảnh này: bỏ sót bản ghi có tác động môi trường (FN) nguy hiểm hơn là lấy nhầm (FP).

### A.5 — F1_env

$$F1_{env} = \frac{2 \times \text{Precision}_{env} \times \text{Recall}_{env}}{\text{Precision}_{env} + \text{Recall}_{env}}$$

### A.6 — HumanCorrectionRate_env

$$\text{HCR}_{env} = 1 - \text{Accuracy}_{env}$$

- **Ý nghĩa:** Tỷ lệ bản ghi người nghiên cứu phải review lại sau khi LLM dự đoán sai
- **Nguồn:** Tham khảo khái niệm "labeling effort" trong active learning literature

---

## PHẦN B — Metric Tầng 2: Phân Loại 5 Nhãn

> Script tính: `src/08_compare_5label_human_vs_llm.py`  
> Dữ liệu: `class_human` (reference) vs `class_llm` (LLM prediction)  
> Tập đánh giá: D_env (các bản ghi có env_human = 1)

## Ký Hiệu

| Ký hiệu | Nghĩa                                                                 |
| ------- | --------------------------------------------------------------------- |
| M       | Tổng số bản ghi trong D_env có cả `class_human` và `class_llm` hợp lệ |
| K = 5   | Số lớp phân loại                                                      |
| TP_k    | True Positive của lớp k                                               |
| FP_k    | False Positive của lớp k                                              |
| FN_k    | False Negative của lớp k                                              |
| y_i     | Nhãn thực tế (class_human) của bản ghi i                              |
| ỹ_i     | Nhãn dự đoán (class_llm) của bản ghi i                                |

---

## 8 Metrics Bắt Buộc

### Metric 1: Confusion Matrix (5×5)

Ma trận nhầm lẫn M\_{ij} trong đó:

- **Hàng i** = nhãn thực tế (human_label)
- **Cột j** = nhãn dự đoán (llm_label)
- M\_{ij} = số lượng bản ghi có human_label = nhãn_i và llm_label = nhãn_j
- **Ô đường chéo** M\_{ii} = phân loại đúng
- **Ô ngoài đường chéo** = phân loại sai

Thứ tự nhãn trong ma trận:

| Hàng/Cột | 1   | 2   | 3   | 4   | 5   |
| -------- | --- | --- | --- | --- | --- |
| **Nhãn** | BQ  | BQL | CQ  | CQL | CON |

_(BQ=BENEFIT_QUANTITATIVE, BQL=BENEFIT_QUALITATIVE, CQ=COST_QUANTITATIVE, CQL=COST_QUALITATIVE, CON=CONSTRAINT)_

---

### Metric 2: Accuracy (Độ chính xác tổng thể)

$$\text{Accuracy} = \frac{\sum_{i=1}^{M} \mathbf{1}[y_i = \hat{y}_i]}{M}$$

- **Ý nghĩa**: Tỷ lệ bản ghi LLM phân loại đúng trên tổng số bản ghi có nhãn người
- **Phạm vi**: [0, 1] — càng cao càng tốt
- **Hạn chế**: Có thể bị misleading nếu phân bố nhãn mất cân bằng → cần kết hợp Macro-F1

---

### Metric 3: Precision per-class (Độ chính xác theo lớp)

$$\text{Precision}_k = \frac{TP_k}{TP_k + FP_k}$$

- **Ý nghĩa**: Trong số các bản ghi LLM dự đoán là lớp k, có bao nhiêu % thực sự là lớp k?
- **Phạm vi**: [0, 1] — càng cao càng tốt
- **Quy ước**: zero_division = 0 (nếu LLM không bao giờ dự đoán lớp k → Precision_k = 0)

---

### Metric 4: Recall per-class (Độ phủ theo lớp)

$$\text{Recall}_k = \frac{TP_k}{TP_k + FN_k}$$

- **Ý nghĩa**: Trong số các bản ghi thực sự là lớp k (theo human_label), LLM phát hiện được bao nhiêu %?
- **Phạm vi**: [0, 1] — càng cao càng tốt
- **Quy ước**: zero_division = 0 (nếu không có bản ghi nào thuộc lớp k → Recall_k = 0)

---

### Metric 5: F1-score per-class

$$F1_k = \frac{2 \times \text{Precision}_k \times \text{Recall}_k}{\text{Precision}_k + \text{Recall}_k}$$

- **Ý nghĩa**: Trung bình điều hòa giữa Precision và Recall — cân bằng cả hai
- **Phạm vi**: [0, 1] — càng cao càng tốt
- **Quy ước**: zero_division = 0 (nếu cả P và R đều = 0 → F1 = 0)

---

### Metric 6: Macro-F1

$$\text{Macro-F1} = \frac{1}{K} \sum_{k=1}^{K} F1_k = \frac{F1_{\text{BQ}} + F1_{\text{BQL}} + F1_{\text{CQ}} + F1_{\text{CQL}} + F1_{\text{CON}}}{5}$$

- **Ý nghĩa**: Trung bình F1 trên 5 nhãn — **không** tính trọng số theo số lượng mỗi lớp
- **Lý do dùng Macro**: Mỗi nhãn được coi trọng như nhau, đặc biệt quan trọng khi phân bố nhãn mất cân bằng
- **Phạm vi**: [0, 1] — càng cao càng tốt
- **Ngưỡng tham khảo**: Macro-F1 > 0.70 là tốt cho bài toán 5 lớp bất cân bằng

---

### Metric 7: Support per-class

$$\text{Support}_k = \sum_{i=1}^{M} \mathbf{1}[y_i = k]$$

- **Ý nghĩa**: Số lượng bản ghi thực sự thuộc lớp k (theo human_label)
- **Dùng để**: Giải thích Precision/Recall/F1 — nhãn có Support thấp thường có F1 không ổn định
- **Phạm vi**: [0, M]

---

### Metric 8: Human Correction Rate

$$\text{Human Correction Rate} = 1 - \text{Accuracy} = \frac{\sum_{i=1}^{M} \mathbf{1}[y_i \neq \hat{y}_i]}{M}$$

- **Ý nghĩa**: Tỷ lệ bản ghi mà người nghiên cứu sẽ phải sửa lại nhãn LLM — **thước đo gánh nặng kiểm tra thủ công**
- **Phạm vi**: [0, 1] — càng thấp càng tốt
- **Ví dụ**: Nếu Accuracy = 0.72 → Human Correction Rate = 0.28 → người nghiên cứu phải review lại 28% records
- **Ngưỡng tham khảo**: HCR < 0.20 là tốt (ít hơn 1/5 record cần sửa)

---

## Bảng Tóm Tắt

| Metric                | Phạm vi | Mục tiêu | Công thức tóm tắt               |
| --------------------- | :-----: | :------: | ------------------------------- |
| Confusion Matrix 5×5  |    —    |    —     | M\_{ij} = count(true=i, pred=j) |
| Accuracy              |  [0,1]  |  ↑ Max   | Σ(y==ŷ) / M                     |
| Precision_k           |  [0,1]  |  ↑ Max   | TP_k / (TP_k + FP_k)            |
| Recall_k              |  [0,1]  |  ↑ Max   | TP_k / (TP_k + FN_k)            |
| F1_k                  |  [0,1]  |  ↑ Max   | 2·P·R / (P+R)                   |
| Macro-F1              |  [0,1]  |  ↑ Max   | mean(F1_k) over K=5 classes     |
| Support_k             |  [0,M]  |    —     | count(human_label = k)          |
| Human Correction Rate |  [0,1]  |  ↓ Min   | 1 − Accuracy                    |

---

## Nguồn Tham Khảo

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). _Introduction to Information Retrieval_. Cambridge University Press. (Chapter 8: Evaluation in Information Retrieval)
- Sokolova, M., & Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. _Information Processing & Management_, 45(4), 427-437.
- Björkelund, A., & Plank, B. (2022). Inter-annotator Agreement and Named Entity Recognition. — (về vấn đề đo lường HumanCorrectionRate)
- `docs/adjudication_protocol.md` — Giải thích tại sao metric phải tính trước adjudication

---

## PHẦN C — End-to-End Accuracy

> Script tính: `src/08_compare_5label_human_vs_llm.py` (thêm chức năng)

### Định nghĩa

Một bản ghi được xem là **đúng end-to-end** khi:

$$\text{correct}_{e2e}(i) = \begin{cases} \mathbf{1}[env\_llm_i = env\_human_i] & \text{nếu } env\_human_i = 0 \\ \mathbf{1}[env\_llm_i = env\_human_i] \wedge \mathbf{1}[class\_llm_i = class\_human_i] & \text{nếu } env\_human_i = 1 \end{cases}$$

$$\text{Accuracy}_{e2e} = \frac{\sum_{i=1}^{N} \text{correct}_{e2e}(i)}{N}$$

- **Ý nghĩa:** LLM chỉ được xem là đúng toàn pipeline khi:
  - Bản ghi không có tác động môi trường: LLM phải lọc đúng (env_llm = 0)
  - Bản ghi có tác động môi trường: LLM phải lọc đúng (env_llm = 1) VÀ phân loại đúng nhãn (class_llm = class_human)
- **Phạm vi:** [0, 1]
- **Chú ý:** Đây là metric bổ sung, nghị hơn Accuracy_env và Accuracy_class riêng lế. Dùng để báo cáo tổng quan pipeline.

---

## Bảng Tóm Tắt Toàn Bộ Metrics

| Metric                    | Tầng | Phạm vi | Mục tiêu | Script |
| ------------------------- | ---- | :-----: | :------: | ------ |
| Confusion Matrix 2×2      | 1    |    —    |    —     | 04     |
| Accuracy_env              | 1    |  [0,1]  |    ↑     | 04     |
| Precision_env             | 1    |  [0,1]  |    ↑     | 04     |
| Recall_env                | 1    |  [0,1]  |    ↑     | 04     |
| F1_env                    | 1    |  [0,1]  |    ↑     | 04     |
| HumanCorrectionRate_env   | 1    |  [0,1]  |    ↓     | 04     |
| Confusion Matrix 5×5      | 2    |    —    |    —     | 08     |
| Accuracy_class            | 2    |  [0,1]  |    ↑     | 08     |
| Precision_k               | 2    |  [0,1]  |    ↑     | 08     |
| Recall_k                  | 2    |  [0,1]  |    ↑     | 08     |
| F1_k                      | 2    |  [0,1]  |    ↑     | 08     |
| Macro-F1_class            | 2    |  [0,1]  |    ↑     | 08     |
| Support_k                 | 2    |  [0,M]  |    —     | 08     |
| HumanCorrectionRate_class | 2    |  [0,1]  |    ↓     | 08     |
| Accuracy_e2e              | Tổng |  [0,1]  |    ↑     | 08     |
