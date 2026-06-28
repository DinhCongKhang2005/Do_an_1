# Ví dụ tính toán thủ công — Impact Score

## Mục đích
Ví dụ này giúp nhà nghiên cứu hiểu và kiểm chứng kết quả tính toán từ script `06_calculate_impact_score.py`.

---

## Dữ liệu ví dụ

### Điều khoản 1 — BENEFIT

**Nội dung**: "Hộ gia đình, cá nhân lắp đặt hệ thống điện mặt trời mái nhà tự sản xuất tự tiêu thụ với công suất không quá 100 kW được ưu đãi mức giá mua điện dư phát lên lưới."

**Nhãn**: BENEFIT → direction = **+1**

**Biến đầu vào** (nhà nghiên cứu điền):
- M_i = 4 (lợi ích kinh tế đáng kể cho hộ gia đình)
- S_i = 4 (phạm vi quốc gia — áp dụng cho mọi hộ gia đình)
- D_i = 4 (dài hạn — hợp đồng nhiều năm)
- R_i = 2 (dễ điều chỉnh giá mua)
- object_weight = 1.0
- alpha = beta = gamma = delta = 0.25

**Tính toán**:
```
C_i = 0.25×4 + 0.25×4 + 0.25×4 + 0.25×2
    = 1.0 + 1.0 + 1.0 + 0.5
    = 3.5

C_i_norm = (3.5 - 1) / (5 - 1)
         = 2.5 / 4
         = 0.625

ImpactScore_i = direction × object_weight × C_i_norm
              = (+1) × 1.0 × 0.625
              = +0.625
```

---

### Điều khoản 2 — CONSTRAINT

**Nội dung**: "Hệ thống điện mặt trời mái nhà tự sản xuất tự tiêu thụ phải có công suất lắp đặt không vượt quá 1 MW đối với tổ chức, doanh nghiệp."

**Nhãn**: CONSTRAINT → direction = **−1**

**Biến đầu vào**:
- M_i = 3 (giới hạn trung bình — 1 MW là mức tương đối cao)
- S_i = 3 (phạm vi ngành/doanh nghiệp)
- D_i = 3 (trung hạn — có thể sửa đổi quy định)
- R_i = 2 (có thể điều chỉnh quy định)
- object_weight = 1.0

**Tính toán**:
```
C_i = 0.25×3 + 0.25×3 + 0.25×3 + 0.25×2
    = 0.75 + 0.75 + 0.75 + 0.5
    = 2.75

C_i_norm = (2.75 - 1) / 4
         = 1.75 / 4
         = 0.4375

ImpactScore_i = (-1) × 1.0 × 0.4375
              = -0.4375
```

---

### Điều khoản 3 — COST

**Nội dung**: "Tổ chức, cá nhân khai thác, sử dụng nguồn nước phải nộp tiền cấp quyền khai thác tài nguyên nước theo quy định."

**Nhãn**: COST → direction = **−1**

**Biến đầu vào**:
- M_i = 3 (gánh nặng tài chính trung bình)
- S_i = 3 (vùng/ngành)
- D_i = 4 (dài hạn — nghĩa vụ thường niên)
- R_i = 1 (dễ điều chỉnh mức phí)
- object_weight = 1.0

**Tính toán**:
```
C_i = 0.25×3 + 0.25×3 + 0.25×4 + 0.25×1
    = 0.75 + 0.75 + 1.0 + 0.25
    = 2.75

C_i_norm = (2.75 - 1) / 4 = 1.75 / 4 = 0.4375

ImpactScore_i = (-1) × 1.0 × 0.4375 = -0.4375
```

---

## Tổng hợp 3 điều khoản ví dụ

| STT | Loại | ImpactScore_i |
|-----|------|---------------|
| 1 | BENEFIT | +0.625 |
| 2 | CONSTRAINT | −0.4375 |
| 3 | COST | −0.4375 |
| **Tổng** | | **−0.25** |

**Giải thích**: Tổng Impact Score âm (−0.25) cho thấy tập 3 điều khoản này có tác động tiêu cực tổng thể, chủ yếu do các ràng buộc và chi phí áp đặt nhiều hơn lợi ích tạo ra.

---

## Kiểm tra chéo với script

Chạy lệnh sau để kiểm tra kết quả:
```bash
python src/06_calculate_impact_score.py --input data/interim/scoring_input.xlsx
```

Kết quả trong `data/reports/final_impact_report.xlsx` — Sheet "Chi tiết Impact Score" phải cho cùng giá trị C_i, C_i_norm, ImpactScore_i.

---

## Lưu ý

> Giá trị M_i, S_i, D_i, R_i trong ví dụ này là **giả định minh họa** — nhà nghiên cứu cần tự đánh giá và điền theo thực tế của từng điều khoản.
