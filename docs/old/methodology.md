# Phương pháp luận — DTM_Khong_debate

## 1. Tổng quan

Hệ thống này triển khai một quy trình đánh giá tác động chính sách môi trường (Regulatory Impact Assessment — RIA) dựa trên:
1. Lọc điều khoản có tác động từ văn bản pháp luật JSON
2. Gán nhãn thủ công bởi nhà nghiên cứu (Human-in-the-loop)
3. Phân loại tự động bằng một LLM duy nhất
4. So sánh nhãn LLM với nhãn người để đánh giá độ tin cậy
5. Tính điểm tác động tất định theo mô hình toán học

---

## 2. Hệ thống nhãn

### 2.1 Ba nhãn phân loại

| Nhãn | Định nghĩa | direction |
|------|-----------|-----------|
| **BENEFIT** | Điều khoản tạo ra tác động tích cực đối với môi trường, xã hội hoặc kinh tế. Ví dụ: ưu đãi đầu tư năng lượng tái tạo, cơ chế bán điện mặt trời. | +1 |
| **COST** | Điều khoản áp đặt chi phí, nghĩa vụ tài chính, gánh nặng tuân thủ, yêu cầu đầu tư hoặc vận hành. Ví dụ: phí môi trường, nghĩa vụ lập báo cáo, chi phí nghiệm thu. | −1 |
| **CONSTRAINT** | Điều khoản đặt ra ngưỡng kỹ thuật, giới hạn, điều kiện kỹ thuật hoặc ràng buộc bắt buộc. Ví dụ: giới hạn công suất (kW/MW), ngưỡng điện áp (kV), điều kiện đấu nối. | −1 |

### 2.2 Quy tắc phân loại ưu tiên

> **Quy tắc quan trọng**: Nếu giá trị số trong điều khoản thể hiện ngưỡng/giới hạn/điều kiện kỹ thuật → **ưu tiên CONSTRAINT**, ngay cả khi điều khoản đó có thể được hiểu theo nhiều cách.

### 2.3 Lý do rút gọn từ hệ thống nguồn

Hệ thống nguồn (`my-ria-project`) dùng 6 nhãn chi tiết:
- `Loi_ich_dinh_luong`, `Loi_ich_khong_dinh_luong`
- `Chi_phi_dinh_luong`, `Chi_phi_khong_dinh_luong`
- `Rang_buoc`, `Khong_lien_quan`

Hệ thống con này đơn giản hóa thành 3 nhãn để:
- Phù hợp phạm vi bảo vệ đề tài
- Giảm độ phức tạp phân loại
- Tập trung vào hướng tác động (dương/âm)

---

## 3. Quy trình Human-in-the-loop

Hệ thống yêu cầu sự tham gia thủ công của nhà nghiên cứu ở **hai thời điểm**:

### Thời điểm 1: Gán nhãn (sau Bước 2)
- Nhà nghiên cứu đọc từng điều khoản và gán nhãn `BENEFIT/COST/CONSTRAINT`
- Ghi lại lý do bằng `human_reason`
- Đây là **nhãn vàng (gold label)** dùng để đánh giá LLM

### Thời điểm 2: Điền biến tính điểm (sau Bước 5)
- Nhà nghiên cứu điền giá trị Likert 1–5 cho M, S, D, R
- Điều chỉnh `object_weight` nếu cần
- Dữ liệu này quyết định trực tiếp Impact Score

---

## 4. Phân loại LLM

### 4.1 Mô hình sử dụng
- Mặc định: `gemini-2.5-flash`
- Nhiệt độ (temperature): 0.0 (đảm bảo tính lặp lại)
- Đầu ra bắt buộc: JSON hợp lệ

### 4.2 Đầu ra yêu cầu
```json
{
  "label": "BENEFIT|COST|CONSTRAINT",
  "reason": "Giải thích ngắn gọn",
  "evidence_span": "Trích dẫn từ văn bản gốc",
  "confidence": 0.85
}
```

### 4.3 Kiểm soát chất lượng
- LLM chỉ phân loại — **không có phản biện, không có debate**
- Nhãn cuối (`final_label`) = `human_label` nếu có, ngược lại = `llm_label`
- Các bản ghi có `llm_confidence < 0.7` được ghi nhận để nhà nghiên cứu chú ý

---

## 5. Công thức Impact Score

### 5.1 Biến số

| Biến | Tên | Thang | Ý nghĩa |
|------|-----|-------|---------|
| M_i | Magnitude | 1–5 | Độ lớn của tác động |
| S_i | Scope | 1–5 | Phạm vi địa lý/đối tượng |
| D_i | Duration | 1–5 | Thời gian tác động |
| R_i | Risk/Reversibility | 1–5 | Mức độ khó khôi phục |

### 5.2 Công thức

**Bước 1: Tính C_i (điểm tổng hợp)**
```
C_i = alpha * M_i + beta * S_i + gamma * D_i + delta * R_i
```

**Bước 2: Chuẩn hóa về [0, 1]**
```
C_i_norm = (C_i - 1) / 4
```
*(khi thang điểm 1–5: scale_min=1, scale_max=5)*

**Bước 3: Tính Impact Score từng điều khoản**
```
ImpactScore_i = direction_i * object_weight_i * C_i_norm
```

### 5.3 Giả định trọng số bằng nhau

Hiện tại:
```
alpha = beta = gamma = delta = 0.25
```

**Đây là giả định đơn giản hóa ban đầu (initial simplifying assumption).**

Lý do:
- Không có dữ liệu thực nghiệm đủ lớn để ước lượng trọng số
- Chuyên gia trong lĩnh vực chưa thực hiện khảo sát AHP
- Phù hợp với nguyên tắc Occam's razor cho phiên bản pilot

Hạn chế và đề xuất:
- Trọng số có thể được hiệu chỉnh qua khảo sát chuyên gia (AHP)
- Dữ liệu lịch sử tác động chính sách có thể dùng để học trọng số

### 5.4 Phương pháp: Tất định (Deterministic)

Hệ thống hiện tại tính điểm **tất định** — một bộ đầu vào cho một kết quả duy nhất.

**Monte Carlo là hướng nghiên cứu tương lai** — xem `docs/limitations_and_future_work.md`.

---

## 6. Chỉ số đánh giá phân loại

Sau khi có nhãn người và nhãn LLM:
- **Accuracy**: Tỷ lệ phân loại đúng tổng thể
- **Precision** (macro, weighted, per-class): Độ chính xác
- **Recall** (macro, weighted, per-class): Độ bao phủ
- **F1-score** (macro, weighted, per-class): Trung bình điều hòa P và R
- **Macro F1**: Trung bình F1 không tính tần suất nhãn
- **Confusion Matrix**: Ma trận nhầm lẫn 3×3

---

## 7. Minh bạch học thuật

- Không có tuyên bố sai về Gold Dataset hoàn chỉnh
- Không có kết quả Monte Carlo giả (chỉ tính điểm tất định)
- Trọng số bằng nhau được ghi nhận là giả định, không phải kết quả thực nghiệm
- Các hạn chế được liệt kê rõ ràng trong `docs/limitations_and_future_work.md`
