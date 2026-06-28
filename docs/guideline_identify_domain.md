# Guideline xác định domain cho từng bản ghi pháp lý

**Dự án:** DTM — Đánh giá tác động chính sách môi trường - Khung định lượng: lợi ích, chi phí, rủi ro.
**Mục đích sử dụng:** Chuẩn hóa trường `domain` trước khi chấm điểm `M_i`, `S_i`, `D_i`, `R_i`, `W_i`  
**Áp dụng cho:** Các bản ghi đã có `env_final = 1` và `final_label`  
**Đầu vào chính:** `raw_text`, `legal_citation`, `legal_signal`, `condition`, `domain` hiện có trong file Luat_bao_ve_moi_truong_2020.JSON  
**Đầu ra khuyến nghị:** `domain_primary`, `domain_secondary`, `domain_group`, `domain_reason`, `domain_needs_review`  

---

## 1. Mục tiêu

Domain dùng để xác định bản ghi tác động đến lĩnh vực môi trường nào. Domain không thay thế nhãn tác động `final_label`, nhưng hỗ trợ:

1. Chấm `R_i` vì từng domain có mức rủi ro khác nhau.
2. Chấm `S_i` vì một số domain có phạm vi tác động rộng hơn.
3. Tổng hợp Impact Score theo nhóm lĩnh vực.
4. Phát hiện các bản ghi thiếu domain hoặc domain chưa nhất quán.
5. Giải thích kết quả khi viết báo cáo.

Ví dụ:

Điều khoản về xả nước thải → domain = water + pollution_control_remediation.
Điều khoản về chất thải nguy hại → domain = hazardous_substances + waste.
Điều khoản về ĐTM/giấy phép môi trường → domain = eia_permit_registration.
Điều khoản về khí nhà kính/tầng ô-dôn → domain = climate_carbon.
```

---

## 2. Danh mục domain chuẩn

Trong hệ thống hiện tại, chỉ sử dụng các domain sau. Không tự tạo domain mới nếu chưa cập nhật toàn bộ pipeline.

## 2.1. Nhóm Kiểm soát Ô nhiễm & Quản lý Chất thải  
**Pollution & Waste Control**

| Domain | Tên tiếng Việt | Khi nào gán |
|---|---|---|
| `waste` | Chất thải nói chung | Chất thải rắn, chất thải sinh hoạt, chất thải công nghiệp, thu gom, phân loại, tái chế, tái sử dụng, xử lý chất thải |
| `water` | Môi trường nước | Nước mặt, nước dưới đất, nước biển, nước thải, nguồn nước, lưu vực sông, khả năng chịu tải của môi trường nước |
| `air_noise_radiation` | Không khí, tiếng ồn, độ rung, bức xạ | Khí thải, bụi, mùi, tiếng ồn, độ rung, phóng xạ, chất lượng không khí |
| `hazardous_substances` | Chất thải nguy hại/chất độc hại | Chất thải nguy hại, hóa chất độc hại, chất phóng xạ, chất độc, tác nhân nguy hại, vật liệu chứa yếu tố độc hại |
| `pollution_control_remediation` | Kiểm soát và xử lý ô nhiễm | Phòng ngừa, ứng phó, khắc phục sự cố môi trường, xử lý ô nhiễm, phục hồi môi trường, kiểm soát nguồn thải |

> Lưu ý: Nếu bản ghi có `chất thải nguy hại`, nên gán đồng thời `waste` và `hazardous_substances`. Nếu có hành vi xử lý/khắc phục ô nhiễm, thêm `pollution_control_remediation`.

---

## 2.2. Nhóm Công cụ Quản lý Hành chính & Kỹ thuật  
**Administrative & Technical Tools**

| Domain | Tên tiếng Việt | Khi nào gán |
|---|---|---|
| `eia_permit_registration` | ĐTM, giấy phép môi trường, đăng ký môi trường | Đánh giá tác động môi trường, báo cáo ĐTM, giấy phép môi trường, đăng ký môi trường, thẩm định, phê duyệt, cấp phép |
| `monitoring_reporting` | Quan trắc, giám sát, báo cáo | Quan trắc môi trường, giám sát, kiểm kê, thống kê, báo cáo, công bố thông tin môi trường, cơ sở dữ liệu môi trường |
| `technical_standard_threshold` | Quy chuẩn, tiêu chuẩn, ngưỡng kỹ thuật | Quy chuẩn kỹ thuật môi trường, tiêu chuẩn môi trường, ngưỡng, hạn ngạch, hạn mức, khả năng chịu tải, không vượt quá, đạt quy chuẩn |

> Lưu ý: `technical_standard_threshold` thường đi kèm các domain nội dung như `water`, `air_noise_radiation`, `waste`. Không nên chỉ gán domain kỹ thuật nếu raw_text nêu rõ môi trường nước/không khí/chất thải.

---

## 2.3. Nhóm Quản lý Nhà nước & Quy hoạch Vĩ mô  
**State Administration & Planning**

| Domain | Tên tiếng Việt | Khi nào gán |
|---|---|---|
| `planning_state_management` | Quản lý nhà nước, quy hoạch, kế hoạch | Trách nhiệm của Bộ, Chính phủ, UBND; quy hoạch bảo vệ môi trường; kế hoạch quản lý chất lượng môi trường; phân công quản lý |
| `general_environment` | Bảo vệ môi trường chung | Nội dung bảo vệ môi trường tổng quát, nguyên tắc, trách nhiệm chung, công trình/phương tiện phục vụ bảo vệ môi trường nhưng không chỉ rõ nước/không khí/chất thải/ĐTM |

> Lưu ý: `general_environment` chỉ dùng khi không thể xác định domain chuyên biệt hơn. Nếu raw_text có “nước thải”, “khí thải”, “chất thải”, “ĐTM”, “quan trắc”, nên ưu tiên domain cụ thể thay vì `general_environment`.

---

## 2.4. Nhóm Bảo tồn, Công cụ Kinh tế & Khí hậu  
**Conservation, Economics & Climate**

| Domain | Tên tiếng Việt | Khi nào gán |
|---|---|---|
| `biodiversity_natural_heritage` | Đa dạng sinh học, di sản thiên nhiên | Di sản thiên nhiên, đa dạng sinh học, hệ sinh thái, loài, sinh vật, bảo tồn thiên nhiên, rừng đặc dụng nếu liên quan bảo tồn |
| `environmental_finance` | Công cụ tài chính môi trường | Phí bảo vệ môi trường, quỹ bảo vệ môi trường, ký quỹ cải tạo/phục hồi môi trường, bồi thường thiệt hại môi trường, chi trả dịch vụ môi trường, đóng góp tài chính |
| `climate_carbon` | Khí hậu, các-bon, tầng ô-dôn | Biến đổi khí hậu, khí nhà kính, giảm phát thải, hạn ngạch phát thải, tín chỉ các-bon, thị trường các-bon, tầng ô-dôn |

---

## 3. Cấu trúc domain nên dùng trong file scoring

Để chấm điểm tốt hơn, nên tách domain thành 4 trường:

| Trường | Ý nghĩa |
|---|---|
| `domain_primary` | Domain chính, phản ánh nội dung tác động trung tâm của bản ghi |
| `domain_secondary` | Các domain phụ, nếu bản ghi có nhiều tác động |
| `domain_group` | Nhóm domain lớn theo 4 nhóm ở trên |
| `domain_reason` | Lý do chọn domain, trích tín hiệu chính từ `raw_text` |
| `domain_needs_review` | TRUE nếu domain mơ hồ, nhiều domain ngang nhau hoặc phải suy luận từ ngữ cảnh cha |

Nếu pipeline hiện tại chỉ có cột `domain`, vẫn nên lưu nhiều domain bằng chuỗi phân tách bởi dấu `;`, ví dụ:

water;pollution_control_remediation;technical_standard_threshold
```

---

## 4. Nguyên tắc xác định domain

### 4.1. Ưu tiên bằng chứng trực tiếp trong `raw_text`

Chọn domain dựa trên từ/cụm từ xuất hiện trong `raw_text`, không chỉ dựa vào tiêu đề chương hoặc hiểu biết bên ngoài.

Ví dụ:

"xả nước thải", "môi trường nước mặt", "nguồn nước" → water
"khí thải", "bụi", "tiếng ồn", "độ rung" → air_noise_radiation
"chất thải nguy hại", "hóa chất độc hại" → hazardous_substances
```

### 4.2. Cho phép nhiều domain

Một bản ghi có thể có nhiều domain nếu raw_text chứa nhiều đối tượng tác động.

Ví dụ:
"xả nước thải, xả khí thải chưa được xử lý đạt quy chuẩn kỹ thuật môi trường"
→ water; air_noise_radiation; technical_standard_threshold
```

### 4.3. Domain chính là nội dung tác động trung tâm

Nếu có nhiều domain, chọn domain chính theo nội dung gây tác động trực tiếp nhất.

Ví dụ:

"không cấp giấy phép môi trường cho dự án xả nước thải vào môi trường nước mặt không còn khả năng chịu tải"
domain_primary = water
domain_secondary = eia_permit_registration; technical_standard_threshold
```

### 4.4. Domain công cụ không thay thế domain nội dung

`eia_permit_registration`, `monitoring_reporting`, `technical_standard_threshold` là công cụ quản lý. Nếu raw_text nêu rõ nước, khí, chất thải, khí hậu, đa dạng sinh học, cần giữ domain nội dung tương ứng.

Ví dụ:


"quan trắc chất lượng môi trường không khí"
→ air_noise_radiation; monitoring_reporting
```

Không chỉ gán:

monitoring_reporting
```

### 4.5. Không gán quá nhiều domain nếu chỉ là dẫn chiếu

Nếu bản ghi chỉ dẫn chiếu đến điều/khoản khác, không tự mở rộng domain quá mức. Dùng domain từ điều khoản được dẫn chiếu chỉ khi nội dung dẫn chiếu đã được chèn rõ trong raw_text.

---

## 5. Cơ chế suy luận domain khi `domain = null` hoặc rỗng

Nếu domain bị thiếu, thực hiện theo thứ tự sau:

### Bước 1. Đọc `raw_text`

Tìm từ khóa trực tiếp:

| Từ khóa/cụm từ trong `raw_text` | Domain đề xuất |
|---|---|
| nước thải, nước mặt, nước dưới đất, nước biển, nguồn nước, lưu vực, khả năng chịu tải của nước | `water` |
| khí thải, bụi, không khí, tiếng ồn, độ rung, mùi, bức xạ | `air_noise_radiation` |
| chất thải, rác thải, phế liệu, tái chế, tái sử dụng, thu gom, xử lý chất thải | `waste` |
| chất thải nguy hại, hóa chất độc hại, chất phóng xạ, chất độc hại | `hazardous_substances` |
| ô nhiễm, khắc phục, xử lý ô nhiễm, sự cố môi trường, phục hồi môi trường | `pollution_control_remediation` |
| ĐTM, đánh giá tác động môi trường, giấy phép môi trường, đăng ký môi trường, thẩm định, phê duyệt | `eia_permit_registration` |
| quan trắc, giám sát, kiểm kê, báo cáo, công bố thông tin, dữ liệu môi trường | `monitoring_reporting` |
| quy chuẩn, tiêu chuẩn, ngưỡng, hạn ngạch, hạn mức, không vượt quá, đạt quy chuẩn | `technical_standard_threshold` |
| quy hoạch, kế hoạch, chương trình, trách nhiệm quản lý nhà nước, Bộ, UBND, Chính phủ | `planning_state_management` |
| bảo vệ môi trường chung, nguyên tắc bảo vệ môi trường, công trình bảo vệ môi trường | `general_environment` |
| đa dạng sinh học, di sản thiên nhiên, hệ sinh thái, loài, sinh vật | `biodiversity_natural_heritage` |
| phí, quỹ, ký quỹ, bồi thường, chi trả, đóng góp tài chính | `environmental_finance` |
| biến đổi khí hậu, khí nhà kính, các-bon, tín chỉ các-bon, tầng ô-dôn | `climate_carbon` |

### Bước 2. Đọc `legal_citation`

Nếu raw_text ngắn hoặc là điểm/khoản tách rời, dùng tên điều/mục trong `raw_text` hoặc `legal_citation` để bổ sung ngữ cảnh.

Ví dụ:

Điều 8. Hoạt động bảo vệ môi trường nước mặt
→ nếu điểm con không nhắc lại "nước", vẫn có thể gán water.
```

### Bước 3. Đọc `legal_signal` và `condition`

Nếu raw_text thiếu từ khóa nhưng `legal_signal` hoặc `condition` có cụm như “quan trắc”, “xử lý”, “giấy phép môi trường”, có thể dùng để suy luận domain.

### Bước 4. Nếu vẫn không rõ

Gán:

domain_primary = general_environment
domain_needs_review = TRUE
domain_reason = "Không có tín hiệu domain chuyên biệt rõ ràng trong raw_text; tạm gán general_environment."
```

---

## 6. Quy tắc ưu tiên khi có nhiều domain

| Tình huống | Domain ưu tiên |
|---|---|
| Có chất thải nguy hại | `hazardous_substances` là domain chính; thêm `waste` |
| Có nước thải/xả vào nước | `water` là domain chính |
| Có khí thải/bụi/tiếng ồn | `air_noise_radiation` là domain chính |
| Có ĐTM/giấy phép và một đối tượng môi trường cụ thể | domain đối tượng là chính; `eia_permit_registration` là phụ |
| Có quan trắc và một đối tượng môi trường cụ thể | domain đối tượng là chính; `monitoring_reporting` là phụ |
| Có quy chuẩn/ngưỡng và một đối tượng môi trường cụ thể | domain đối tượng là chính; `technical_standard_threshold` là phụ |
| Có phí/ký quỹ/bồi thường do ô nhiễm | `environmental_finance` là chính hoặc phụ tùy trọng tâm; thêm domain ô nhiễm/chất thải nếu có |
| Có trách nhiệm của cơ quan nhà nước về một domain cụ thể | domain cụ thể là chính; `planning_state_management` là phụ |
| Chỉ nói bảo vệ môi trường chung | `general_environment` |

---

## 7. Gợi ý domain theo nhóm điều khoản thường gặp trong Luật Bảo vệ môi trường 2020

| Nhóm nội dung | Domain thường dùng |
|---|---|
| Hành vi bị nghiêm cấm liên quan xả thải | `water`; `air_noise_radiation`; `waste`; `technical_standard_threshold` |
| Nhập khẩu chất thải/phế liệu | `waste`; `technical_standard_threshold` |
| Chất thải nguy hại | `hazardous_substances`; `waste` |
| Bảo vệ môi trường nước mặt/nước dưới đất/nước biển | `water`; có thể thêm `monitoring_reporting`, `pollution_control_remediation`, `technical_standard_threshold` |
| Bảo vệ môi trường không khí | `air_noise_radiation`; có thể thêm `monitoring_reporting`, `pollution_control_remediation` |
| Đánh giá tác động môi trường | `eia_permit_registration` |
| Giấy phép môi trường/đăng ký môi trường | `eia_permit_registration`; có thể thêm `technical_standard_threshold` |
| Quan trắc và báo cáo môi trường | `monitoring_reporting`; thêm domain nội dung nếu rõ |
| Kinh tế tuần hoàn, tái chế, EPR | `circular_economy`; `waste`; có thể thêm `environmental_finance` |
| Phí, ký quỹ, quỹ bảo vệ môi trường, bồi thường | `environmental_finance` |
| Khí nhà kính, các-bon, tầng ô-dôn | `climate_carbon` |
| Di sản thiên nhiên, đa dạng sinh học | `biodiversity_natural_heritage` |
| Quy hoạch/kế hoạch/trách nhiệm quản lý | `planning_state_management`; thêm domain nội dung nếu rõ |

---

## 8. Kiểm tra chất lượng domain

Trước khi dùng domain để tổng hợp Impact Score, cần kiểm tra:

Không có domain rỗng nếu env_final = 1.
Mỗi domain nằm trong danh mục chuẩn.
Nếu có nhiều domain, domain_primary phải phản ánh tác động trung tâm.
Không dùng general_environment khi raw_text có domain cụ thể hơn.
Không dùng technical_standard_threshold đơn độc nếu raw_text có nước/khí/chất thải.
Các bản ghi có hazardous_substances nên được kiểm tra R_i cẩn thận.
Các bản ghi có climate_carbon hoặc biodiversity_natural_heritage không nên có R_i quá thấp nếu tác động rõ.
```

---

## 9. Mẫu ghi chú domain


domain_primary=water vì raw_text đề cập xả nước thải vào môi trường nước mặt; domain_secondary=eia_permit_registration;technical_standard_threshold vì điều khoản gắn với giấy phép môi trường và khả năng chịu tải.

domain_primary=waste vì raw_text quy định thu gom, phân loại và xử lý chất thải; domain_secondary=circular_economy nếu có tái chế/tái sử dụng.

domain_primary=planning_state_management vì raw_text quy định trách nhiệm của UBND cấp tỉnh trong tổ chức thực hiện kế hoạch quản lý môi trường; domain_secondary=water vì kế hoạch liên quan chất lượng môi trường nước mặt.
```

---

## 10. Khuyến nghị áp dụng cho hệ thống hiện tại

Trong file scoring, nên bổ sung hoặc chuẩn hóa các cột:

domain_primary
domain_secondary
domain_group
domain_reason
domain_needs_review
```

Nếu chưa muốn sửa cấu trúc Excel, có thể tạm giữ cột `domain`, nhưng cần bảo đảm domain được ghi nhất quán theo danh mục chuẩn và phân tách bằng dấu `;`.

