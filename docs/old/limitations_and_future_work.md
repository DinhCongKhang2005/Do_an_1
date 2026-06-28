# Hạn chế và Hướng nghiên cứu tương lai

## 1. Hạn chế hiện tại của hệ thống

### 1.1 Về tập dữ liệu

- **Quy mô nhỏ (pilot study)**: Tập nhãn người hiện tại là nghiên cứu thử nghiệm, không phải Gold Dataset hoàn chỉnh. Chưa đủ để rút ra kết luận thống kê mạnh.
- **Một người gán nhãn**: Việc gán nhãn thủ công chỉ do một nhà nghiên cứu thực hiện, thiếu Inter-Annotator Agreement (IAA).
- **Không có nhãn đối chiếu chuyên gia**: Chưa có xác nhận từ chuyên gia luật hoặc chính sách môi trường.

### 1.2 Về phân loại LLM

- **Một LLM duy nhất**: Phiên bản này chỉ dùng một LLM để phân loại, không có cơ chế phản biện. Kết quả phụ thuộc vào chất lượng của model được chọn.
- **Không có Validator Engine**: Bằng chứng (`evidence_span`) không được kiểm tra tự động xem có xuất hiện thực sự trong văn bản gốc hay không.
- **Hallucination chưa được kiểm soát đầy đủ**: LLM có thể suy diễn vượt nội dung văn bản.
- **Một phiên chạy**: Kết quả chưa được kiểm tra tính ổn định (run-to-run consistency) dù temperature=0.

### 1.3 Về tính điểm

- **Trọng số bằng nhau**: alpha = beta = gamma = delta = 0.25 là **giả định đơn giản hóa ban đầu**, không có cơ sở thực nghiệm. Các trọng số này có thể không phản ánh đúng tầm quan trọng tương đối của từng tiêu chí.
- **Thang Likert chủ quan**: Giá trị M, S, D, R phụ thuộc vào đánh giá chủ quan của người điền. Không có hướng dẫn định lượng chặt chẽ cho từng mức điểm.
- **Không có chiết khấu thời gian**: Khác với NPV đầy đủ, hệ thống không áp dụng Social Discount Rate.
- **Không có Social Cost of Carbon (SCC)**: Tác động về phát thải CO₂ không được định lượng bằng tiền tương đương.

### 1.4 Không có Monte Carlo

**Đây là hệ thống tính điểm TẤT ĐỊNH (deterministic).** Monte Carlo Simulation không được thực thi trong phiên bản này.

Hệ quả:
- Không có khoảng tin cậy (confidence interval) cho Impact Score
- Không định lượng được bất định (uncertainty) của kết quả
- Không có phân tích độ nhạy (sensitivity analysis)

---

## 2. Hướng nghiên cứu tương lai

### 2.1 Monte Carlo Simulation *(Ưu tiên cao)*

**Đây là bước mở rộng quan trọng nhất.**

Triển khai mô phỏng Monte Carlo với N = 10,000 lần lặp cho phép:
- Định lượng bất định của Impact Score
- Tính khoảng tin cậy 90% (p5, p95)
- Tính xác suất tác động tích cực P(IS > 0)
- Phân tích độ nhạy với Tornado Chart

**Biến bất định có thể mô phỏng**:
- M, S, D, R ~ Normal(giá_trị_trung_tâm, σ)
- object_weight ~ Uniform(0.8, 1.2)
- Trọng số alpha, beta, gamma, delta ~ Dirichlet(uniform)

### 2.2 Cải thiện hệ thống phân loại

- **Multi-annotator agreement**: Có ≥2 người gán nhãn độc lập, tính Cohen's Kappa
- **Active Learning**: Ưu tiên gán nhãn các bản ghi mà LLM có độ tự tin thấp
- **Evidence Validation**: Tự động kiểm tra evidence_span có xuất hiện trong văn bản gốc
- **Cross-model validation**: So sánh kết quả giữa nhiều LLM khác nhau

### 2.3 Hiệu chỉnh trọng số

- **AHP (Analytic Hierarchy Process)**: Khảo sát chuyên gia để xác định trọng số tương đối của M, S, D, R
- **Dữ liệu lịch sử**: Học trọng số từ các đánh giá tác động chính sách thực tế trong quá khứ
- **Regression-based weights**: Hồi quy OLS/Ridge để ước lượng trọng số từ điểm chuyên gia

### 2.4 Mở rộng phạm vi

- Áp dụng cho nhiều văn bản pháp luật khác nhau (luật môi trường, luật năng lượng, quy hoạch...)
- So sánh giữa các văn bản để xếp hạng tác động
- Tích hợp dữ liệu kinh tế-xã hội thực tế để calibrate thang điểm

### 2.5 Multi-Agent Debate *(Nghiên cứu dài hạn)*

Hệ thống nguồn (`my-ria-project`) đã triển khai Multi-Agent Debate (Agent A + Agent B + Debate Engine). Phân tích so sánh giữa:
- Single-LLM (hệ thống hiện tại)
- Multi-Agent với Debate

Sẽ giúp trả lời câu hỏi: Debate có cải thiện đáng kể chất lượng phân loại không?

---

## 3. Rủi ro hiện tại

| Rủi ro | Mức độ | Ghi chú |
|--------|--------|---------|
| Tập nhãn nhỏ → kết quả metrics không đại diện | Cao | Cần mở rộng dataset |
| Trọng số bằng nhau không tối ưu | Trung bình | Cần AHP hoặc dữ liệu thực nghiệm |
| LLM hallucination chưa được kiểm soát | Trung bình | Cần Evidence Validation |
| Phụ thuộc vào một model LLM | Thấp-Trung bình | Có thể đổi model qua .env |
| Biến số Likert chủ quan | Cao | Cần hướng dẫn chi tiết hơn |

---

## 4. Tuyên bố minh bạch (Transparency Statement)

> Phiên bản này là **pilot study** với quy mô nhỏ. Kết quả chỉ có giá trị minh họa và khám phá, không đủ để đưa ra kết luận chính sách. Các phát hiện cần được xác nhận với dữ liệu lớn hơn và phương pháp kiểm chứng nghiêm ngặt hơn trước khi ứng dụng thực tế.
