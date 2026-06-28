# Guideline xác định actor cho từng bản ghi pháp lý

**Dự án:** DTM — Đánh giá tác động chính sách môi trường - Khung định lượng: lợi ích, chi phí, rủi ro.
**Mục đích sử dụng:** Chuẩn hóa trường `actor` trước khi chấm điểm tác động và tổng hợp Impact Score theo chủ thể  
**Áp dụng cho:** Các bản ghi đã có `env_final = 1` và `final_label`  
**Đầu vào chính:** `raw_text`, `chu_the`/`actor` hiện có, `legal_signal`, `condition`, `legal_citation`  
**Đầu ra khuyến nghị:** `actor_raw`, `actor_group`, `actor_primary`, `actor_reason`, `actor_needs_review`  

---

## 1. Mục tiêu

Actor là chủ thể chịu tác động hoặc chủ thể phải thực hiện hành động pháp lý trong bản ghi. Việc xác định actor giúp:

1. Tổng hợp Impact Score theo nhóm chủ thể.
2. Chấm `S_i` chính xác hơn.
3. Phân biệt tác động lên doanh nghiệp, cơ quan nhà nước, cộng đồng dân cư hay chủ dự án.
4. Xử lý các bản ghi có `actor = null`.
5. Giải thích kết quả khi báo cáo.

---

## 2. Chuẩn hóa nhóm actor

Đề xuất ban đầu có lặp nhóm “Tổ chức, cá nhân (Chung)”. Để dùng trong hệ thống, nên chuẩn hóa thành 5 nhóm chính sau:

| Mã nhóm | Tên nhóm actor | Khi nào dùng |
|---|---|---|
| `BUSINESS_FACILITY` | Doanh nghiệp / Cơ sở sản xuất, kinh doanh, dịch vụ | Doanh nghiệp, cơ sở sản xuất, cơ sở kinh doanh, cơ sở dịch vụ, khu sản xuất, khu công nghiệp, cụm công nghiệp, chủ nguồn thải, đơn vị xử lý chất thải |
| `PROJECT_OWNER_INFRASTRUCTURE` | Chủ dự án đầu tư / Chủ đầu tư hạ tầng | Chủ dự án đầu tư, chủ đầu tư, nhà đầu tư, chủ đầu tư xây dựng và kinh doanh hạ tầng, dự án đầu tư, ban quản lý dự án |
| `STATE_AGENCY` | Cơ quan nhà nước | Chính phủ, Thủ tướng, Bộ, Bộ Tài nguyên và Môi trường, UBND các cấp, cơ quan cấp phép, cơ quan thẩm định, cơ quan quản lý nhà nước |
| `GENERAL_ORGANIZATION_INDIVIDUAL` | Tổ chức, cá nhân chung | Tổ chức, cá nhân; hộ gia đình, cá nhân; cơ quan, tổ chức, cá nhân khi điều khoản áp dụng chung và không xác định nhóm chuyên biệt hơn |
| `COMMUNITY_CRAFT_VILLAGE` | Cộng đồng dân cư / Làng nghề | Cộng đồng dân cư, khu dân cư, làng nghề, cơ sở/hộ sản xuất trong làng nghề, hộ gia đình tại khu dân cư |

Nếu cần mở rộng về sau, có thể thêm nhóm riêng như `HOUSEHOLD_INDIVIDUAL`, `WASTE_SERVICE_PROVIDER`, `IMPORTER`, nhưng trong đồ án hiện tại nên giữ 5 nhóm để dễ tổng hợp.

---

## 3. Nguyên tắc xác định actor

### 3.1. Actor chính là chủ thể chịu nghĩa vụ/quyền/ràng buộc trực tiếp

Đọc câu hỏi:


Ai phải làm?
Ai bị cấm?
Ai được hỗ trợ/ưu đãi?
Ai phải chịu trách nhiệm?
Ai được cấp phép hoặc không được cấp phép?
```

Chủ thể trả lời cho các câu hỏi này là actor chính.

### 3.2. Ưu tiên actor xuất hiện trực tiếp trong `raw_text`

Nếu raw_text có:

Bộ Tài nguyên và Môi trường có trách nhiệm...
Ủy ban nhân dân cấp tỉnh có trách nhiệm...
Chủ dự án đầu tư phải...
Cơ sở sản xuất, kinh doanh, dịch vụ phải...
Tổ chức, cá nhân không được...
Cộng đồng dân cư có trách nhiệm...
```

thì dùng chính cụm đó làm `actor_raw` và gán nhóm tương ứng.

### 3.3. Không nhầm actor với đối tượng môi trường

Các cụm như sau không phải actor:

môi trường nước mặt
chất thải nguy hại
khí thải
đa dạng sinh học
di sản thiên nhiên
nguồn nước
```

Đó là đối tượng/domain môi trường. Actor phải là cơ quan, tổ chức, cá nhân, doanh nghiệp, cộng đồng hoặc chủ dự án.

### 3.4. Một bản ghi có thể có nhiều actor

Nếu raw_text có nhiều chủ thể với nghĩa vụ khác nhau, nên ghi:

actor_primary = chủ thể chịu tác động chính
actor_secondary = các chủ thể còn lại
actor_needs_review = TRUE
```

Nếu pipeline chỉ có một cột `actor`, ghi theo dạng:

Cơ quan nhà nước; Chủ dự án đầu tư
```

---

## 4. Cơ chế suy luận actor khi `actor = null`

Nếu actor bị thiếu, thực hiện theo thứ tự sau.

### Bước 1. Tìm chủ ngữ trong `raw_text`

Tìm các cụm đứng trước tín hiệu pháp lý:

có trách nhiệm
phải
không được
nghiêm cấm
được
được hỗ trợ
phải lập
phải nộp
phải báo cáo
phải xử lý
```

Ví dụ:


"Ủy ban nhân dân cấp tỉnh có trách nhiệm..."
→ actor = Ủy ban nhân dân cấp tỉnh
→ actor_group = STATE_AGENCY
```

### Bước 2. Nếu là điểm/khoản con, đọc ngữ cảnh cha trong raw_text

Một số bản ghi điểm a, b, c không lặp lại actor vì actor đã nằm ở đầu khoản.

Ví dụ:

"Khoản 3. Ủy ban nhân dân cấp tỉnh có trách nhiệm sau đây: ... Điểm đ. Ban hành, tổ chức thực hiện kế hoạch..."
```

Nếu bản ghi điểm đ chỉ còn:

"Ban hành, tổ chức thực hiện kế hoạch..."
```

thì suy luận actor từ khoản cha là:


actor = Ủy ban nhân dân cấp tỉnh
actor_group = STATE_AGENCY
```

Nếu file không chứa ngữ cảnh cha, đặt `actor_needs_review = TRUE`.

### Bước 3. Dựa vào loại thủ tục

Nếu raw_text nói:

| Cụm nội dung | Actor hợp lý |
|---|---|
| phải lập báo cáo ĐTM | Chủ dự án đầu tư |
| phải có giấy phép môi trường | Chủ dự án đầu tư/cơ sở |
| phải đăng ký môi trường | Chủ dự án đầu tư/cơ sở/hộ kinh doanh tùy raw_text |
| phải quan trắc, vận hành công trình xử lý | Cơ sở sản xuất, kinh doanh, dịch vụ hoặc chủ dự án/cơ sở |
| phải phân loại, thu gom, chuyển giao chất thải | Chủ nguồn thải, cơ sở, tổ chức/cá nhân phát sinh chất thải |
| cơ quan thẩm định/cấp phép | Cơ quan nhà nước |

### Bước 4. Nếu vẫn không rõ

Gán:


actor_raw = "Chủ thể liên quan theo quy định của điều khoản"
actor_group = GENERAL_ORGANIZATION_INDIVIDUAL
actor_needs_review = TRUE
actor_reason = "Không xác định được chủ thể trực tiếp trong raw_text; tạm gán nhóm chung."
```

Không tự đoán tên cơ quan hoặc nhóm doanh nghiệp cụ thể nếu văn bản không có căn cứ.

---

## 5. Bảng quy tắc ánh xạ actor

| Cụm trong raw_text/actor | actor_group |
|---|---|
| Chính phủ, Thủ tướng Chính phủ | `STATE_AGENCY` |
| Bộ Tài nguyên và Môi trường, Bộ, cơ quan ngang Bộ | `STATE_AGENCY` |
| Ủy ban nhân dân cấp tỉnh/huyện/xã | `STATE_AGENCY` |
| cơ quan quản lý nhà nước, cơ quan cấp phép, cơ quan thẩm định | `STATE_AGENCY` |
| chủ dự án đầu tư, chủ đầu tư, nhà đầu tư, dự án đầu tư | `PROJECT_OWNER_INFRASTRUCTURE` |
| chủ đầu tư xây dựng và kinh doanh hạ tầng | `PROJECT_OWNER_INFRASTRUCTURE` |
| doanh nghiệp, cơ sở sản xuất, kinh doanh, dịch vụ | `BUSINESS_FACILITY` |
| khu sản xuất, kinh doanh, dịch vụ tập trung; khu công nghiệp; cụm công nghiệp | `BUSINESS_FACILITY` |
| chủ nguồn thải, cơ sở phát sinh chất thải | `BUSINESS_FACILITY` |
| đơn vị thu gom, vận chuyển, xử lý chất thải | `BUSINESS_FACILITY` |
| tổ chức, cá nhân | `GENERAL_ORGANIZATION_INDIVIDUAL` |
| hộ gia đình, cá nhân | `GENERAL_ORGANIZATION_INDIVIDUAL` hoặc `COMMUNITY_CRAFT_VILLAGE` nếu trong ngữ cảnh cộng đồng/làng nghề |
| cộng đồng dân cư, khu dân cư | `COMMUNITY_CRAFT_VILLAGE` |
| làng nghề, cơ sở trong làng nghề | `COMMUNITY_CRAFT_VILLAGE` |

---

## 6. Quy tắc ưu tiên khi có nhiều actor

| Tình huống | Actor chính nên chọn |
|---|---|
| Cơ quan nhà nước cấp phép, chủ dự án chịu điều kiện | Nếu bản ghi nói “không cấp phép/không phê duyệt” → `STATE_AGENCY`; nếu trọng tâm là nghĩa vụ của chủ dự án → `PROJECT_OWNER_INFRASTRUCTURE` |
| Chủ dự án và cơ sở cùng xuất hiện | Chọn nhóm được nêu trực tiếp với nghĩa vụ chính; nếu cả hai cùng chịu nghĩa vụ, ghi cả hai và đặt review |
| Tổ chức, cá nhân gây ô nhiễm | `GENERAL_ORGANIZATION_INDIVIDUAL`, trừ khi raw_text nêu rõ cơ sở/doanh nghiệp |
| Cơ sở sản xuất, kinh doanh, dịch vụ | `BUSINESS_FACILITY` |
| UBND cấp tỉnh tổ chức thực hiện kế hoạch | `STATE_AGENCY` |
| Cộng đồng dân cư/hộ gia đình trong làng nghề | `COMMUNITY_CRAFT_VILLAGE` |

---

## 7. Actor và ảnh hưởng đến chấm `S_i`

Actor không quyết định trực tiếp `ImpactScore`, nhưng giúp chấm `S_i`.

| actor_group | Gợi ý `S_i` thường gặp | Lý do |
|---|---:|---|
| `STATE_AGENCY` | 3–5 | Phạm vi thường cấp tỉnh, liên tỉnh hoặc quốc gia |
| `PROJECT_OWNER_INFRASTRUCTURE` | 2–4 | Phụ thuộc quy mô dự án |
| `BUSINESS_FACILITY` | 2–4 | Có thể tác động đến nhiều cơ sở/ngành |
| `GENERAL_ORGANIZATION_INDIVIDUAL` | 3–5 | Quy định chung có thể áp dụng rộng |
| `COMMUNITY_CRAFT_VILLAGE` | 2–3 | Phạm vi cộng đồng/làng nghề, thường cục bộ nhưng có tác động trực tiếp |

Không chấm `S_i` chỉ theo tên actor; cần kết hợp với phạm vi trong `raw_text` và `legal_citation`.

---

## 8. Mẫu ghi chú actor


actor_group=STATE_AGENCY vì raw_text nêu "Ủy ban nhân dân cấp tỉnh có trách nhiệm".
```


actor_group=PROJECT_OWNER_INFRASTRUCTURE vì raw_text quy định "chủ dự án đầu tư phải lập báo cáo đánh giá tác động môi trường".
```


actor_group=BUSINESS_FACILITY vì raw_text áp dụng cho "cơ sở sản xuất, kinh doanh, dịch vụ có phát thải bụi, khí thải".
```

actor_group=COMMUNITY_CRAFT_VILLAGE vì raw_text quy định trách nhiệm của cộng đồng dân cư/làng nghề trong bảo vệ môi trường.
```

actor_group=GENERAL_ORGANIZATION_INDIVIDUAL vì raw_text chỉ nêu "tổ chức, cá nhân" và không có căn cứ để xác định nhóm chuyên biệt hơn.
```

---

## 9. Kiểm tra chất lượng actor

Trước khi dùng actor để tổng hợp Impact Score, cần kiểm tra:

Không có actor rỗng nếu có thể suy luận từ raw_text.
Không nhầm domain môi trường thành actor.
Các điểm/khoản con thiếu actor đã được đối chiếu với ngữ cảnh cha.
Actor_group chỉ thuộc 5 nhóm chuẩn.
Các bản ghi có nhiều actor phải có actor_needs_review = TRUE.
Không gán STATE_AGENCY chỉ vì có cụm "theo quy định của pháp luật".
Không gán BUSINESS_FACILITY nếu raw_text chỉ nói chung "tổ chức, cá nhân".
```

---

## 10. Khuyến nghị áp dụng cho hệ thống hiện tại

Trong file scoring, nên bổ sung hoặc chuẩn hóa các cột:

actor_raw
actor_primary
actor_group
actor_reason
actor_needs_review
```

Nếu chưa sửa cấu trúc Excel, có thể dùng cột `actor` hiện có, nhưng nên tạo thêm bảng ánh xạ actor để tổng hợp theo 5 nhóm chuẩn.

