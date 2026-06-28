# Quy tắc tính điểm Impact Score

> **Cập nhật lần 2:** Nhấn mạnh các ràng buộc học thuật quan trọng.

## ⚠️ Cảnh báo học thuật (Đọc trước khi sử dụng)

| Ràng buộc                                   | Giải thích                                                                                        |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Impact Score chỉ tính sau `final_label`** | Phải hoàn thành Tầng 2 (class_human review) trước. Không dùng `class_llm` trực tiếp để tính điểm. |
| **`final_label` phải qua human review**     | Nhãn cuối phải là `class_human` sau adjudication, không phải nhãn LLM chưa được kiểm chứng.       |
| **W_i = 1.0 nếu chưa có cơ sở chuyên gia**  | Không tự ý đặt W_i ≠ 1.0 nếu không có tài liệu tham chiếu (AHP, khung chính sách).                |
| **Impact Score là bán định lượng**          | Không phải CBA tiền tệ đầy đủ. Không quy đổi sang giá trị tiền tệ.                                |
| **Không gộp với metric LLM**                | Impact Score và Accuracy/F1 là hai loại chỉ số khác nhau, không thể cộng vào nhau.                |

---

## 1. Công thức đầy đủ

```
C_i = alpha*M_i + beta*S_i + gamma*D_i + delta*R_i

C_i_norm = (C_i - scale_min) / (scale_max - scale_min)
         = (C_i - 1) / 4                              [thang 1–5]

ImpactScore_i = direction_i × object_weight_i × C_i_norm
```

## 2. Ý nghĩa từng biến

| Ký hiệu         | Tên đầy đủ         | Thang    | Ý nghĩa                                    |
| --------------- | ------------------ | -------- | ------------------------------------------ |
| M_i             | Magnitude          | 1–5      | Mức độ lớn của tác động                    |
| S_i             | Scope              | 1–5      | Phạm vi tác động (địa lý/đối tượng)        |
| D_i             | Duration           | 1–5      | Thời gian kéo dài của tác động             |
| R_i             | Risk/Reversibility | 1–5      | Mức độ rủi ro và khó khôi phục             |
| direction_i     | Hướng tác động     | {+1, −1} | +1 cho BENEFIT, −1 cho COST/CONSTRAINT     |
| object_weight_i | Trọng số đối tượng | >0       | Tầm quan trọng của đối tượng chịu tác động |

## 3. Trọng số hiện tại

```
alpha = beta = gamma = delta = 0.25
```

**Lưu ý học thuật**: Trọng số bằng nhau là **giả định đơn giản hóa ban đầu**, không phải kết quả thực nghiệm. Phù hợp cho phiên bản pilot study.

## 4. Phạm vi giá trị

| Giá trị                  | Ý nghĩa                       |
| ------------------------ | ----------------------------- |
| C_i ∈ [1, 5]             | Điểm tổng hợp trước chuẩn hóa |
| C_i_norm ∈ [0, 1]        | Điểm đã chuẩn hóa             |
| ImpactScore_i ∈ [-w, +w] | Phụ thuộc vào object_weight   |

Với `object_weight = 1.0` (mặc định): ImpactScore_i ∈ [−1, +1]

## 5. Ví dụ tính

Điều khoản: "Hộ gia đình lắp đặt điện mặt trời mái nhà được ưu đãi giá mua điện"

- Nhãn: BENEFIT → direction = +1
- M_i = 3 (tác động trung bình về lợi ích kinh tế)
- S_i = 4 (phạm vi vùng/quốc gia)
- D_i = 4 (dài hạn)
- R_i = 2 (dễ khôi phục)
- object_weight = 1.0

```
C_i = 0.25×3 + 0.25×4 + 0.25×4 + 0.25×2 = 0.25 × (3+4+4+2) = 3.25
C_i_norm = (3.25 - 1) / 4 = 2.25/4 = 0.5625
ImpactScore_i = (+1) × 1.0 × 0.5625 = +0.5625
```

## 6. Tổng hợp tác động toàn bộ văn bản

```
TotalImpact = Σ ImpactScore_i  (tổng tất cả điều khoản được phân loại)
```

Giải thích:

- TotalImpact > 0: Văn bản có tác động tích cực tổng thể
- TotalImpact < 0: Văn bản có tác động tiêu cực tổng thể
- TotalImpact ≈ 0: Tác động trung lập hoặc cân bằng

## 7. Giới hạn phương pháp

- Không chiết khấu theo thời gian (discount rate) trong phiên bản này
- Không có Monte Carlo để định lượng bất định
- Không có trọng số xã hội (social cost of carbon) do tách biệt khỏi hệ thống đầy đủ
- Thang Likert 1–5 phụ thuộc vào đánh giá chủ quan của nhà nghiên cứu
