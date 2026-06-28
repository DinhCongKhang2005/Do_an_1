# Định nghĩa biến — DTM_Khong_debate

## 1. Biến đầu vào từ dữ liệu JSON

| Tên cột | Kiểu | Mô tả |
|---------|------|-------|
| `source_id` | str | Mã định danh duy nhất của điều khoản (tự sinh) |
| `legal_citation` | str | Số hiệu điều khoản (ví dụ: "Điều 5, Khoản 2") |
| `noi_dung_dieu_khoan` | str | Nội dung đầy đủ của điều khoản pháp lý |
| `co_tac_dong` | bool | Cờ boolean: True nếu điều khoản có tác động chính sách |
| `chu_the` | str | Chủ thể pháp lý chịu ảnh hưởng |
| `loai_phap_ly` | str | Loại điều khoản pháp lý |
| `tin_hieu_phap_ly` | str | Tín hiệu pháp lý (phải, được phép, cấm,...) |
| `doi_tuong` | str | Đối tượng điều chỉnh |
| `dieu_kien` | str | Điều kiện áp dụng |
| `gia_tri_dinh_luong` | str | Giá trị số nếu có (kW, %, ngày,...) |

---

## 2. Biến gán nhãn

| Tên cột | Kiểu | Mô tả | Ai điền |
|---------|------|-------|---------|
| `human_label` | str | Nhãn thủ công: BENEFIT/COST/CONSTRAINT | Nhà nghiên cứu |
| `human_reason` | str | Lý do gán nhãn của nhà nghiên cứu | Nhà nghiên cứu |
| `labeler_name` | str | Tên người gán nhãn | Nhà nghiên cứu |
| `labeled_at` | str | Ngày gán nhãn | Nhà nghiên cứu |
| `llm_label` | str | Nhãn do LLM phân loại | Tự động (LLM) |
| `llm_reason` | str | Lý do của LLM | Tự động (LLM) |
| `llm_evidence_span` | str | Bằng chứng trích dẫn từ văn bản | Tự động (LLM) |
| `llm_confidence` | float | Độ tự tin của LLM [0.0–1.0] | Tự động (LLM) |
| `final_label` | str | Nhãn cuối: human_label nếu có, ngược lại llm_label | Tự động |
| `final_label_source` | str | Nguồn nhãn cuối: "human" hoặc "llm" | Tự động |

---

## 3. Biến tính điểm (Likert 1–5)

| Tên cột | Ký hiệu | Thang | Ý nghĩa | Ai điền |
|---------|---------|-------|---------|---------|
| `M_i` | Magnitude | 1–5 | Độ lớn của tác động môi trường/kinh tế | Nhà nghiên cứu |
| `S_i` | Scope | 1–5 | Phạm vi địa lý hoặc số đối tượng bị ảnh hưởng | Nhà nghiên cứu |
| `D_i` | Duration | 1–5 | Thời gian kéo dài của tác động | Nhà nghiên cứu |
| `R_i` | Risk/Reversibility | 1–5 | Mức độ rủi ro và khó khôi phục | Nhà nghiên cứu |
| `object_weight` | w | >0 | Trọng số tầm quan trọng của đối tượng | Nhà nghiên cứu |
| `affected_object` | — | str | Tên đối tượng chịu tác động | Nhà nghiên cứu |

### Hướng dẫn điền thang Likert

**M_i — Magnitude (Độ lớn)**
| Điểm | Ý nghĩa |
|------|---------|
| 1 | Không đáng kể / Rất nhỏ |
| 2 | Nhỏ / Hạn chế |
| 3 | Trung bình |
| 4 | Lớn / Đáng kể |
| 5 | Rất lớn / Căn bản |

**S_i — Scope (Phạm vi)**
| Điểm | Ý nghĩa |
|------|---------|
| 1 | Cá nhân / Hộ gia đình |
| 2 | Địa phương / Doanh nghiệp nhỏ |
| 3 | Vùng / Ngành |
| 4 | Quốc gia |
| 5 | Toàn cầu |

**D_i — Duration (Thời gian)**
| Điểm | Ý nghĩa |
|------|---------|
| 1 | Tức thời / Một lần |
| 2 | Ngắn hạn (< 1 năm) |
| 3 | Trung hạn (1–5 năm) |
| 4 | Dài hạn (> 5 năm) |
| 5 | Vĩnh viễn / Không thể đảo ngược về thời gian |

**R_i — Risk/Reversibility**
| Điểm | Ý nghĩa |
|------|---------|
| 1 | Dễ khôi phục hoàn toàn |
| 2 | Có thể khôi phục một phần |
| 3 | Khôi phục khó khăn / Trung bình |
| 4 | Khó khôi phục |
| 5 | Không thể khôi phục / Không thể đảo ngược |

---

## 4. Biến kết quả tính toán

| Tên cột | Kiểu | Công thức | Ý nghĩa |
|---------|------|----------|---------|
| `direction` | int | BENEFIT=+1, COST/CONSTRAINT=−1 | Hướng tác động |
| `C_i` | float | alpha×M + beta×S + gamma×D + delta×R | Điểm tổng hợp trước chuẩn hóa |
| `C_i_norm` | float | (C_i − 1) / 4 | Điểm đã chuẩn hóa về [0, 1] |
| `ImpactScore_i` | float | direction × object_weight × C_i_norm | Điểm tác động cuối cùng |

---

## 5. Cấu hình trọng số (config/project_config.yaml)

```yaml
scoring:
  alpha: 0.25   # Trọng số M_i
  beta:  0.25   # Trọng số S_i
  gamma: 0.25   # Trọng số D_i
  delta: 0.25   # Trọng số R_i
  scale_min: 1
  scale_max: 5
  default_object_weight: 1.0
```

> **Giả định**: alpha = beta = gamma = delta = 0.25 là giả định trọng số bằng nhau. Đây là điểm khởi đầu để được thay thế bằng trọng số thực nghiệm khi có dữ liệu.
