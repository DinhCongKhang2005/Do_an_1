# Cơ sở lý thuyết và tài liệu tham khảo

> **Lưu ý**: Các mục đánh dấu `[TODO: Verify citation]` cần được nhà nghiên cứu kiểm tra và bổ sung thông tin trích dẫn đầy đủ trước khi nộp báo cáo.

---

## 1. Khung đánh giá tác động quy định (RIA)

### 1.1 Phương pháp phân tích chi phí-lợi ích (CBA)

Phân tích chi phí-lợi ích là công cụ chuẩn trong đánh giá tác động quy định, được áp dụng rộng rãi trong chính sách môi trường.

**Tài liệu tham khảo:**
- `[TODO: Verify citation]` OECD (2020). *Regulatory Impact Assessment*. OECD Publishing. https://doi.org/10.1787/7a9638cb-en
- `[TODO: Verify citation]` European Commission (2021). *Better Regulation Guidelines*. SWD(2021) 305 final.
- `[TODO: Verify citation]` World Bank (2010). *Cost-Benefit Analysis in World Bank Projects*. World Bank Publications.

### 1.2 RIA trong chính sách môi trường Việt Nam

- `[TODO: Verify citation]` Luật Ban hành văn bản quy phạm pháp luật 2015 (sửa đổi 2020) — quy định về đánh giá tác động chính sách.
- `[TODO: Verify citation]` Nghị định số 34/2016/NĐ-CP về hướng dẫn Luật BHVBQPPL — quy trình RIA.

---

## 2. Phân loại văn bản pháp luật bằng LLM

### 2.1 Ứng dụng LLM trong phân tích văn bản pháp luật

Các nghiên cứu gần đây đã áp dụng LLM (Large Language Models) để phân loại và phân tích văn bản pháp lý với kết quả khả quan.

**Tài liệu tham khảo:**
- `[TODO: Verify citation]` Chalkidis, I., et al. (2022). *LexGLUE: A Benchmark Dataset for Legal Language Understanding in English*. ACL 2022.
- `[TODO: Verify citation]` Bommarito, M., & Katz, D. M. (2022). *GPT Takes the Bar Exam*. arXiv:2212.14402.
- `[TODO: Verify citation]` Nay, J. J. (2023). *Large Language Models as Corporate Lobbyists*. arXiv:2301.01181.

### 2.2 Zero-shot và Few-shot classification

Hệ thống này sử dụng zero-shot classification — LLM phân loại dựa trên system prompt mà không cần fine-tuning.

- `[TODO: Verify citation]` Brown, T., et al. (2020). *Language Models are Few-Shot Learners*. NeurIPS 2020.
- `[TODO: Verify citation]` Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. NeurIPS 2022.

---

## 3. Mô hình tính điểm tác động (Impact Scoring)

### 3.1 Thang đo Likert trong đánh giá tác động

Sử dụng thang điểm Likert 1–5 để định lượng hóa các tiêu chí định tính trong đánh giá tác động chính sách.

**Tài liệu tham khảo:**
- `[TODO: Verify citation]` Likert, R. (1932). *A technique for the measurement of attitudes*. Archives of Psychology, 22(140), 5–55.
- `[TODO: Verify citation]` Morrison, M. (2009). *Using and interpreting Likert scales*. RMIT University.

### 3.2 Tiêu chí đánh giá tác động môi trường

Các tiêu chí Magnitude (M), Scope (S), Duration (D), Risk/Reversibility (R) tham chiếu từ:

- `[TODO: Verify citation]` Canter, L. W. (1996). *Environmental Impact Assessment* (2nd ed.). McGraw-Hill.
- `[TODO: Verify citation]` Glasson, J., Therivel, R., & Chadwick, A. (2012). *Introduction to Environmental Impact Assessment* (4th ed.). Routledge.
- `[TODO: Verify citation]` European Commission (2001). *Guidance on EIA — Environmental Statement*. Luxembourg: Office for Official Publications.

### 3.3 Giả định trọng số bằng nhau

Việc gán trọng số bằng nhau (equal weighting) cho các tiêu chí là phổ biến trong các nghiên cứu pilot khi chưa có dữ liệu calibrate.

- `[TODO: Verify citation]` Dawes, R. M. (1979). *The robust beauty of improper linear models in decision making*. American Psychologist, 34(7), 571–582.

---

## 4. Đánh giá mô hình phân loại

### 4.1 Chỉ số Precision, Recall, F1

- `[TODO: Verify citation]` Powers, D. M. W. (2011). *Evaluation: From Precision, Recall and F-Measure to ROC, Informedness, Markedness and Correlation*. JMLR.

### 4.2 Macro F1 cho phân loại đa nhãn không cân bằng

- `[TODO: Verify citation]` Sokolova, M., & Lapalme, G. (2009). *A systematic analysis of performance measures for classification tasks*. Information Processing & Management, 45(4), 427–437.

---

## 5. Văn bản pháp luật Việt Nam được phân tích

- Nghị định số 135/2024/NĐ-CP — `[TODO: Điền tên đầy đủ và URL nguồn chính thức]`
- `[TODO: Bổ sung các văn bản pháp lý khác trong dataset]`

---

## 6. Hướng dẫn hoàn thiện tài liệu

Trước khi nộp báo cáo cuối:
1. Tìm kiếm DOI chính xác cho mỗi mục `[TODO: Verify citation]`
2. Kiểm tra năm xuất bản và số trang
3. Xác nhận các tài liệu OECD/World Bank có thể truy cập công khai
4. Bổ sung tài liệu tham khảo tiếng Việt liên quan
5. Định dạng theo chuẩn APA 7th edition hoặc chuẩn của trường
