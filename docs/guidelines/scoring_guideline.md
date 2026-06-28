# Rubric chấm điểm M, S, D, R, W — Impact Score

**Dự án:** DTM — Đánh giá tác động chính sách môi trường - Khung định lượng: lợi ich, chi phí, rủi ro.
**Pipeline:** Bài toán 3 — Lượng hóa tác động sau khi đã chốt `final\\\_label`  
**Áp dụng cho:** Tập bản ghi đã chốt nhãn và chuẩn hóa actor/domain trong `actor\\\_domain\\\_dataset.xlsx`  
**Script liên quan:** `src/09b\\\_build\\\_actor\\\_domain\\\_review.py`, `src/09c\\\_validate\\\_actor\\\_domain.py`, `src/10\\\_build\\\_scoring\\\_input.py` và `src/11\\\_calculate\\\_impact\\\_score.py`  
**Phiên bản:** 3.0 — tinh chỉnh tiêu chí chấm điểm, trọng số và quy tắc kiểm soát chất lượng

\---

## 1\. Mục tiêu của bước chấm điểm

Sau khi hệ thống đã chốt nhãn cuối cùng `final\\\_label`, bước này chuyển từng bản ghi có tác động đến môi trường đã được gán nhãn thành một điểm tác động có dấu. Điểm này không phải là giá trị tiền tệ tuyệt đối, mà là **điểm bán định lượng** dùng để so sánh tương đối giữa các nhóm tác động.

Quy trình tổng quát:

final\\\_label
→ xác định chiều tác động direction\\\_i (s\_i)
→ chấm M\\\_i, S\\\_i, D\\\_i, R\\\_i trên thang likert 1–5
→ xác định trọng số alpha, beta, gamma, delta
→ xác định W\\\_i
→ tính ImpactScore\\\_i
→ tổng hợp theo nhãn, domain, chủ thể hoặc nhóm điều khoản
```

Mục tiêu của rubric là giúp người nghiên cứu chấm điểm nhất quán, có căn cứ và có thể giải thích lại khi viết báo cáo.

\---

## 2\. Công thức tính điểm

Với mỗi bản ghi `i`, điểm mức độ tác động chưa chuẩn hóa được tính bằng:


C\\\_i = \\\\alpha M\\\_i + \\\\beta S\\\_i + \\\\gamma D\\\_i + \\\\delta R\\\_i, với i \\in \\mathcal{L}
```

trong đó:


\\\\alpha + \\\\beta + \\\\gamma + \\\\delta = 1
```

Điểm chuẩn hóa:


C\\\_i^{norm} = \\\\frac{C\\\_i - 1}{4}
```

Vì `M\\\_i`, `S\\\_i`, `D\\\_i`, `R\\\_i` nằm trên thang 1–5, nên:


C\\\_i^{norm} \\\\in \\\[0,1]
```

Điểm tác động cuối cùng:


ImpactScore\\\_i = direction\\\_i (s\_i) \\\\times W\\\_i \\\\times C\\\_i^{norm}
```

Trong đó:

|Thành phần|Ý nghĩa|
|-|-|
|`direction\\\_i`|Chiều tác động lấy từ `final\\\_label`|
|`W\\\_i`|Trọng số đối tượng/domain|
|`C\\\_i^{norm}`|Mức độ tác động chuẩn hóa|

Nếu `W\\\_i = 1`, thì `ImpactScore\\\_i` nằm trong khoảng `\\\[-1, +1]`.

\---

## 3\. Chiều tác động theo `final\\\_label`

|`final\\\_label`|Chiều `direction\\\_i`|Ý nghĩa|
|-|-:|-|
|`BENEFIT\\\_QUANTITATIVE`|`+1`|Lợi ích định lượng|
|`BENEFIT\\\_QUALITATIVE`|`+1`|Lợi ích định tính|
|`COST\\\_QUANTITATIVE`|`-1`|Chi phí định lượng|
|`COST\\\_QUALITATIVE`|`-1`|Chi phí định tính/gánh nặng tuân thủ|
|`CONSTRAINT`|`-1`|Ràng buộc, điều kiện, lệnh cấm hoặc giới hạn kỹ thuật|

Lưu ý: `ImpactScore\\\_i < 0` không có nghĩa là điều khoản “xấu”. Nó chỉ phản ánh rằng điều khoản tạo ra chi phí tuân thủ hoặc ràng buộc đối với chủ thể chịu tác động. Trong chính sách môi trường, nhiều điểm âm là bình thường vì pháp luật môi trường thường đặt ra nghĩa vụ, điều kiện và giới hạn để đạt mục tiêu bảo vệ môi trường.

\---

## 4\. Nguyên tắc chấm điểm chung

### 4.1. Chấm theo tác động của điều khoản, không chấm theo độ dài văn bản

Một bản ghi dài chưa chắc có điểm cao. Một bản ghi ngắn nhưng đặt ra lệnh cấm mạnh, điều kiện nghiêm ngặt hoặc nghĩa vụ đầu tư lớn có thể có điểm cao hơn.

### 4.2. Chấm từng biến độc lập

Không nên cho tất cả biến cùng một điểm chỉ vì cảm giác “quan trọng”. Mỗi biến có ý nghĩa riêng:

|Biến|Câu hỏi cần trả lời|
|-|-|
|`M\\\_i`|Tác động mạnh đến mức nào?|
|`S\\\_i`|Tác động lan rộng đến bao nhiêu chủ thể/khu vực?|
|`D\\\_i`|Tác động kéo dài bao lâu?|
|`R\\\_i`|Nếu không tuân thủ, rủi ro môi trường và khả năng phục hồi ra sao?|
|`W\\\_i`|Domain/chủ thể này có cần trọng số khác mặc định không?|

### 4.3. Nếu thiếu thông tin, dùng mức trung bình có giải thích

Nếu văn bản không nêu rõ phạm vi, thời gian hoặc mức độ kỹ thuật, dùng điểm trung bình hợp lý:


M\\\_i = 3 nếu có tác động rõ nhưng chưa thấy mức rất cao.
S\\\_i = 3 nếu áp dụng cho nhóm ngành, cấp tỉnh hoặc nhóm chủ thể rộng.
D\\\_i = 3 nếu không nêu thời gian cụ thể.
R\\\_i = 3 nếu có rủi ro môi trường rõ nhưng chưa thấy nguy cơ nghiêm trọng/khó phục hồi.
W\\\_i = 1.0 nếu không có cơ sở chuyên gia để phân biệt trọng số.
```

Cần ghi lý do trong `scoring\\\_note`.

\---

## 5\. Rubric chấm `M\\\_i` — Magnitude / Cường độ tác động

### 5.1. Định nghĩa

`M\\\_i` đo mức độ lớn/mạnh của thay đổi mà điều khoản tạo ra. Biến này tập trung vào **mức thay đổi hành vi, quy trình, công nghệ, tài chính hoặc vận hành** mà chủ thể phải thực hiện hoặc được hưởng lợi.

### 5.2. Thang điểm

|Điểm|Mức độ|Mô tả|Ví dụ|
|-:|-|-|-|
|1|Không đáng kể|Thay đổi rất nhỏ, chủ yếu là ghi nhận, cung cấp thông tin hoặc yêu cầu hành chính nhẹ|Ghi nhận thông tin môi trường trong hồ sơ|
|2|Thấp|Có yêu cầu thực hiện nhưng đơn giản, ít làm thay đổi vận hành chính|Dán nhãn, phân loại thông tin, báo cáo đơn giản|
|3|Trung bình|Tác động rõ đến quy trình quản lý hoặc vận hành|Lập báo cáo, đăng ký môi trường, quan trắc định kỳ|
|4|Cao|Buộc thay đổi đáng kể về công nghệ, hạ tầng, quy trình sản xuất hoặc quản lý|Lắp đặt hệ thống xử lý nước thải, tổ chức thu gom/xử lý chất thải|
|5|Rất cao|Tác động mang tính chuyển đổi, thay đổi mô hình hoạt động hoặc ảnh hưởng lớn đến toàn ngành|Cấm hoàn toàn một hoạt động gây ô nhiễm nghiêm trọng, bắt buộc chuyển đổi công nghệ lớn|

### 5.3. Quy tắc chấm nhanh

* `BENEFIT\\\_QUALITATIVE`: thường `M\\\_i = 2–4`, tùy lợi ích là khuyến khích chung hay cải thiện lớn.
* `COST\\\_QUALITATIVE`: thường `M\\\_i = 3–4`, vì thường tạo nghĩa vụ thủ tục hoặc vận hành.
* `CONSTRAINT`: thường `M\\\_i = 3–5`, nếu là lệnh cấm/điều kiện mạnh.
* Không chấm `M\\\_i = 5` chỉ vì điều khoản quan trọng về mặt pháp lý; phải có thay đổi lớn về hành vi, công nghệ, chi phí hoặc phạm vi quản lý.

\---

## 6\. Rubric chấm `S\\\_i` — Scope / Phạm vi ảnh hưởng

### 6.1. Định nghĩa

`S\\\_i` đo phạm vi chủ thể, ngành, địa phương hoặc không gian môi trường chịu ảnh hưởng bởi điều khoản.

### 6.2. Thang điểm

|Điểm|Phạm vi|Mô tả|Ví dụ|
|-:|-|-|-|
|1|Cá nhân/cơ sở đơn lẻ|Tác động đến một chủ thể hoặc một dự án cụ thể|Một dự án/cơ sở riêng lẻ|
|2|Nhóm nhỏ/địa phương hẹp|Tác động đến một nhóm chủ thể hoặc một khu vực nhỏ|Một cụm dân cư, một xã/huyện|
|3|Ngành, tỉnh hoặc nhóm chủ thể rộng|Tác động đến một ngành, một cấp tỉnh hoặc nhóm doanh nghiệp/cơ sở rộng|Chủ dự án, cơ sở sản xuất kinh doanh, UBND cấp tỉnh|
|4|Liên tỉnh, vùng hoặc đa ngành|Tác động đến nhiều địa phương, nhiều ngành hoặc lưu vực lớn|Sông hồ liên tỉnh, khu vực liên vùng|
|5|Quốc gia hoặc xuyên biên giới|Tác động toàn quốc, toàn nền kinh tế hoặc có yếu tố toàn cầu|Khí nhà kính, tầng ô-dôn, chính sách chất thải toàn quốc|

### 6.3. Quy tắc chấm nhanh

* Nếu chủ thể là `Bộ`, `Chính phủ`, `Thủ tướng`, quy hoạch quốc gia: thường `S\\\_i = 4–5`.
* Nếu chủ thể là `UBND cấp tỉnh`: thường `S\\\_i = 3`.
* Nếu liên quan sông, hồ liên tỉnh hoặc vùng liên tỉnh: thường `S\\\_i = 4`.
* Nếu liên quan khí nhà kính, tầng ô-dôn hoặc chính sách toàn quốc: thường `S\\\_i = 5`.
* Nếu chỉ áp dụng cho một cơ sở hoặc một dự án: `S\\\_i = 1–2`.

\---

## 7\. Rubric chấm `D\\\_i` — Duration / Thời gian tác động

### 7.1. Định nghĩa

`D\\\_i` đo thời gian tác động của điều khoản kéo dài trong thực tế. Đây không chỉ là thời hạn xử lý hồ sơ, mà là thời gian nghĩa vụ, lợi ích hoặc ràng buộc tồn tại.

### 7.2. Thang điểm

|Điểm|Thời gian|Mô tả|Ví dụ|
|-:|-|-|-|
|1|Ngắn hạn, một lần|Tác động dưới 1 năm hoặc phát sinh một lần|Báo cáo sự cố một lần|
|2|Ngắn hạn|1–5 năm hoặc trong giai đoạn chuyển tiếp ngắn|Thời hạn khắc phục ngắn|
|3|Trung hạn|5–20 năm hoặc theo chu kỳ kế hoạch/quản lý thông thường|Kế hoạch, quy hoạch, nghĩa vụ vận hành chưa xác định dài hạn|
|4|Dài hạn|Trên 20 năm hoặc kéo dài theo vòng đời dự án/cơ sở|Hạ tầng xử lý nước thải, quản lý chất thải lâu dài|
|5|Rất dài hạn/khó đảo ngược|Tác động gần như vĩnh viễn hoặc gắn với hệ sinh thái khó phục hồi|Đa dạng sinh học, di sản thiên nhiên, ô nhiễm lâu dài|

### 7.3. Quy tắc chấm nhanh

* Nếu văn bản không nêu thời gian cụ thể: dùng `D\\\_i = 3`.
* Nếu nghĩa vụ tồn tại trong suốt quá trình vận hành cơ sở/dự án: dùng `D\\\_i = 4`.
* Nếu tác động liên quan đa dạng sinh học, di sản thiên nhiên, khí hậu, ô nhiễm lâu dài: cân nhắc `D\\\_i = 4–5`.
* Không dùng thời hạn hành chính như “20 ngày”, “45 ngày” để tự động chấm `D\\\_i` thấp; cần xem tác động thực chất kéo dài bao lâu.

\---

## 8\. Rubric chấm `R\\\_i` — Risk/Reversibility / Rủi ro và khả năng phục hồi

### 8.1. Định nghĩa

`R\\\_i` đo mức độ rủi ro môi trường nếu điều khoản không được tuân thủ, đồng thời xét khả năng phục hồi khi tác động xảy ra.

### 8.2. Thang điểm

|Điểm|Rủi ro/khả năng phục hồi|Mô tả|Ví dụ|
|-:|-|-|-|
|1|Rủi ro thấp|Hậu quả chủ yếu là chậm thủ tục, ít tác động trực tiếp đến môi trường|Chậm nộp báo cáo ít nghiêm trọng|
|2|Rủi ro thấp–trung bình|Có thể gây tác động môi trường nhỏ, dễ khắc phục|Thiếu phân loại hoặc lưu giữ tạm thời ở mức nhẹ|
|3|Rủi ro trung bình|Có nguy cơ ô nhiễm hoặc suy giảm môi trường rõ, cần chi phí khắc phục|Ô nhiễm cục bộ, quan trắc không đầy đủ|
|4|Rủi ro cao|Có thể gây ô nhiễm nghiêm trọng hoặc khó phục hồi hoàn toàn|Ô nhiễm nước ngầm, chất thải nguy hại, sự cố môi trường lớn|
|5|Rủi ro rất cao|Tác động khó đảo ngược, lâu dài hoặc có quy mô lớn|Mất đa dạng sinh học, suy giảm tầng ô-dôn, phát thải khí nhà kính lớn, ô nhiễm độc hại kéo dài|

### 8.3. Quy tắc chấm nhanh theo domain

|Domain|Gợi ý `R\\\_i` thường gặp|Lưu ý|
|-|-:|-|
|`monitoring\\\_reporting`|1–3|Rủi ro gián tiếp, trừ khi liên quan cảnh báo sự cố nghiêm trọng|
|`eia\\\_permit\\\_registration`|2–4|Rủi ro phụ thuộc quy mô dự án và điều kiện cấp phép|
|`waste`|3–4|Chất thải thông thường thường trung bình–cao|
|`hazardous\\\_waste`|4–5|Chất thải nguy hại thường rủi ro cao|
|`water`|3–4|Nước mặt/nước ngầm có thể khó phục hồi|
|`air\\\_noise\\\_radiation`|3–4|Tùy mức độ khí thải, bụi, tiếng ồn, phóng xạ|
|`biodiversity\\\_natural\\\_heritage`|4–5|Khó phục hồi, có thể bất thuận nghịch|
|`climate\\\_ozone\\\_carbon`|4–5|Tác động dài hạn và quy mô rộng|
|`pollution\\\_control\\\_remediation`|3–5|Phụ thuộc loại ô nhiễm và khả năng khắc phục|
|`circular\\\_economy`|2–4|Rủi ro thường gián tiếp, trừ khi liên quan chất thải lớn|

\---

## 9\. Xác định trọng số `alpha`, `beta`, `gamma`, `delta`

### 9.1. Phương án mặc định cho đồ án hiện tại

Trong phiên bản cơ sở, sử dụng:


\\\\alpha = \\\\beta = \\\\gamma = \\\\delta = 0.25
```

Tức là:


M\\\_i, S\\\_i, D\\\_i, R\\\_i có vai trò ngang nhau.
```

Đây là lựa chọn phù hợp cho đồ án hiện tại vì:

* chưa có hội đồng chuyên gia độc lập để xác định trọng số;
* chưa có dữ liệu thực nghiệm đủ lớn để học trọng số;
* tránh làm mô hình phức tạp quá mức;
* dễ giải thích, dễ tái lập và phù hợp với nghiên cứu ban đầu.

### 9.2. Khi nào được điều chỉnh trọng số

Chỉ điều chỉnh `alpha`, `beta`, `gamma`, `delta` nếu có một trong các cơ sở sau:

1. Ý kiến chuyên gia môi trường/pháp lý.
2. Ma trận AHP có kiểm tra nhất quán.
3. Tài liệu chính sách hoặc khoa học chỉ ra tiêu chí nào quan trọng hơn.
4. Phân tích độ nhạy để chứng minh kết quả không bị phụ thuộc quá mức vào một trọng số tùy ý.

Nếu không có cơ sở trên, không nên tự đặt ví dụ như:


R\\\_i = 0.4, M\\\_i = 0.3, S\\\_i = 0.2, D\\\_i = 0.1
```

vì có thể làm kết quả thiếu khách quan.

### 9.3. Gợi ý kịch bản phân tích độ nhạy

Có thể báo cáo thêm các kịch bản phụ, nhưng không thay thế kịch bản mặc định:

|Kịch bản|alpha|beta|gamma|delta|Ý nghĩa|
|-|-:|-:|-:|-:|-|
|Equal weight|0.25|0.25|0.25|0.25|Kịch bản chính|
|Risk-oriented|0.20|0.20|0.20|0.40|Nhấn mạnh rủi ro/khó phục hồi|
|Scope-oriented|0.20|0.40|0.20|0.20|Nhấn mạnh phạm vi tác động|
|Magnitude-oriented|0.40|0.20|0.20|0.20|Nhấn mạnh cường độ tác động|

Nếu dùng các kịch bản này, phải ghi rõ là **phân tích độ nhạy**, không phải kết quả chính.

\---

## 10\. Xác định `W\\\_i` — trọng số đối tượng/domain

### 10.1. Trong phạm vi đồ án hiện tại

Sử dụng:


W\\\_i = 1.0
```

cho tất cả bản ghi.

Đây là lựa chọn khuyến nghị trong phiên bản hiện tại vì chưa có cơ sở chuyên gia để khẳng định domain nào quan trọng hơn domain nào trong bối cảnh định lượng của đồ án.

### 10.2. Khi nào được dùng `W\\\_i ≠ 1.0`

Chỉ dùng `W\\\_i` khác 1 nếu có căn cứ rõ ràng, ví dụ:

* chuyên gia xác nhận mức ưu tiên domain;
* có tài liệu khoa học/chính sách hỗ trợ;
* có phương pháp AHP hoặc so sánh cặp;
* có phân tích độ nhạy riêng cho trọng số domain.

### 10.3. Gợi ý trọng số tham khảo, không dùng làm mặc định

|Nhóm domain|W tham khảo|Giải thích|
|-|-:|-|
|`climate\\\_ozone\\\_carbon`|1.3–1.5|Tác động dài hạn, phạm vi rộng|
|`biodiversity\\\_natural\\\_heritage`|1.3–1.5|Khó phục hồi, có thể bất thuận nghịch|
|`hazardous\\\_waste`|1.2–1.4|Rủi ro cao với sức khỏe và môi trường|
|`water`|1.1–1.3|Liên quan tài nguyên thiết yếu và sức khỏe cộng đồng|
|`air\\\_noise\\\_radiation`|1.0–1.2|Tùy mức độ ô nhiễm và dân cư chịu ảnh hưởng|
|`waste`|1.0–1.2|Tác động phổ biến, có thể quản lý bằng hệ thống xử lý|
|`eia\\\_permit\\\_registration`|0.9–1.1|Tác động gián tiếp qua công cụ quản lý|
|`monitoring\\\_reporting`|0.8–1.0|Tác động gián tiếp, hỗ trợ phát hiện và quản lý|
|`planning\\\_state\\\_management`|0.9–1.1|Tác động rộng nhưng thường gián tiếp|
|`circular\\\_economy`|1.0–1.2|Có lợi ích môi trường, phụ thuộc mức thực thi|

Trong báo cáo chính, nên giữ `W\\\_i = 1.0`. Bảng trên chỉ nên dùng trong phần hạn chế hoặc hướng phát triển.

\---

## 11\. Gợi ý chấm điểm theo `final\\\_label`

### 11.1. `BENEFIT\\\_QUALITATIVE`

Thường là các cơ chế khuyến khích, hỗ trợ, ưu đãi, cải thiện quản lý môi trường.

Gợi ý:

M\\\_i = 2–4
S\\\_i = 3–5 nếu chính sách áp dụng rộng
D\\\_i = 3–4 nếu chính sách có tính dài hạn
R\\\_i = 2–4 tùy domain
W\\\_i = 1.0
```

### 11.2. `COST\\\_QUALITATIVE`

Thường là nghĩa vụ lập hồ sơ, báo cáo, quan trắc, đăng ký, xử lý, chuyển giao, vận hành.

Gợi ý:


M\\\_i = 3–4
S\\\_i = 2–4 tùy chủ thể áp dụng
D\\\_i = 3–4 nếu nghĩa vụ lặp lại hoặc kéo dài
R\\\_i = 2–4 tùy rủi ro nếu không tuân thủ
W\\\_i = 1.0
```

### 11.3. `CONSTRAINT`

Thường là cấm, không được, chỉ được, điều kiện, quy chuẩn, ngưỡng, hạn ngạch.

Gợi ý:


M\\\_i = 3–5
S\\\_i = 2–5 tùy phạm vi áp dụng
D\\\_i = 3–5 nếu ràng buộc dài hạn
R\\\_i = 3–5 nếu hành vi bị cấm có rủi ro lớn
W\\\_i = 1.0
```

### 11.4. `BENEFIT\\\_QUANTITATIVE` và `COST\\\_QUANTITATIVE`

Nếu dữ liệu có nhãn này, cần đọc kỹ `quantitative\\\_value`.

* Với `BENEFIT\\\_QUANTITATIVE`, con số phải thể hiện lợi ích định lượng.
* Với `COST\\\_QUANTITATIVE`, con số phải thể hiện chi phí, phí, ký quỹ, thuế, bồi thường hoặc mức chi trả cụ thể.

Không dùng thời hạn, mã QCVN hoặc số điều/khoản làm cơ sở chấm định lượng.

\---

## 12\. Mẫu ghi `scoring\\\_note`

Nên ghi chú ngắn gọn theo mẫu:

M=4 vì điều khoản yêu cầu thay đổi vận hành chính; S=3 vì áp dụng cho nhóm cơ sở/doanh nghiệp; D=4 vì nghĩa vụ kéo dài trong quá trình vận hành; R=4 vì không tuân thủ có thể gây ô nhiễm khó phục hồi; W=1.0 theo cấu hình mặc định.
```

Mẫu cho `CONSTRAINT`:

`
M=4 vì bản ghi đặt điều kiện/cấm hành vi có tác động lớn; S=3 vì áp dụng cho nhóm chủ thể trong lĩnh vực liên quan; D=4 vì ràng buộc có tính dài hạn; R=4 vì vi phạm có thể gây rủi ro môi trường cao; W=1.0 mặc định.
```

Mẫu cho `BENEFIT\\\_QUALITATIVE`:


M=3 vì chính sách tạo lợi ích quản lý môi trường rõ nhưng chưa có định lượng; S=4 vì áp dụng phạm vi rộng; D=4 vì lợi ích có tính dài hạn; R=3 vì domain có rủi ro trung bình nếu không thực thi; W=1.0 mặc định.
```

\---

## 13\. Ví dụ tính điểm minh họa

### Ví dụ 1 — `COST\\\_QUALITATIVE`

Bản ghi:


Chủ dự án đầu tư phải lập báo cáo đánh giá tác động môi trường và trình cơ quan có thẩm quyền thẩm định.
```

Chấm điểm:

|Biến|Điểm|Lý do|
|-|-:|-|
|`M\\\_i`|3|Tạo nghĩa vụ thủ tục rõ ràng|
|`S\\\_i`|3|Áp dụng cho nhóm chủ dự án thuộc diện phải thực hiện ĐTM|
|`D\\\_i`|3|Tác động theo chu kỳ dự án/quy trình phê duyệt|
|`R\\\_i`|3|Nếu không thực hiện có thể bỏ sót rủi ro môi trường|
|`W\\\_i`|1.0|Mặc định|


C\\\_i = 0.25(3) + 0.25(3) + 0.25(3) + 0.25(3) = 3
C\\\_i^{norm} = \\\\frac{3 - 1}{4} = 0.5
ImpactScore\\\_i = -1 \\\\times 1.0 \\\\times 0.5 = -0.5


### Ví dụ 2 — `CONSTRAINT`

Bản ghi:


Nghiêm cấm xả nước thải, khí thải chưa được xử lý đạt quy chuẩn kỹ thuật môi trường ra môi trường.
```

Chấm điểm:

|Biến|Điểm|Lý do|
|-|-:|-|
|`M\\\_i`|4|Lệnh cấm mạnh đối với hành vi xả thải chưa xử lý|
|`S\\\_i`|4|Áp dụng rộng cho nhiều chủ thể có phát sinh xả thải|
|`D\\\_i`|4|Ràng buộc có tính dài hạn|
|`R\\\_i`|4|Vi phạm có thể gây ô nhiễm nước/không khí nghiêm trọng|
|`W\\\_i`|1.0|Mặc định|


C\\\_i = 0.25(4) + 0.25(4) + 0.25(4) + 0.25(4) = 4
C\\\_i^{norm} = \\\\frac{4 - 1}{4} = 0.75
ImpactScore\\\_i = -1 \\\\times 1.0 \\\\times 0.75 = -0.75
```

### Ví dụ 3 — `BENEFIT\\\_QUALITATIVE`

Bản ghi:


Nhà nước khuyến khích phát triển kinh tế tuần hoàn, tái chế và tái sử dụng chất thải.
```

Chấm điểm:

|Biến|Điểm|Lý do|
|-|-:|-|
|`M\\\_i`|3|Tạo lợi ích quản lý môi trường rõ nhưng chưa lượng hóa|
|`S\\\_i`|4|Có thể áp dụng cho nhiều nhóm chủ thể|
|`D\\\_i`|4|Chính sách có tính dài hạn|
|`R\\\_i`|3|Nếu không thực hiện, rủi ro môi trường ở mức trung bình|
|`W\\\_i`|1.0|Mặc định|


C\\\_i = 0.25(3) + 0.25(4) + 0.25(4) + 0.25(3) = 3.5
C\\\_i^{norm} = \\\\frac{3.5 - 1}{4} = 0.625
ImpactScore\\\_i = +1 \\\\times 1.0 \\\\times 0.625 = 0.625
```

\---

## 14\. Kiểm tra chất lượng trước khi chạy script tính điểm

Trước khi chạy script tính Impact Score, cần kiểm tra:


Không có dòng thiếu M\\\_i, S\\\_i, D\\\_i, R\\\_i.
M\\\_i, S\\\_i, D\\\_i, R\\\_i chỉ nằm trong {1,2,3,4,5}.
W\\\_i > 0.
Nếu W\\\_i khác 1.0, phải có scoring\\\_note giải thích.
Không dùng thời hạn hành chính để tự động chấm D\\\_i thấp.
Không dùng mã QCVN hoặc số điều/khoản để coi là chi phí/lợi ích định lượng.
Các bản ghi CONSTRAINT có R\\\_i thấp phải được kiểm tra lại.
Các bản ghi liên quan biodiversity, climate, hazardous\\\_waste có R\\\_i thấp phải được kiểm tra lại.
Các bản ghi có M\\\_i = 5 hoặc R\\\_i = 5 phải có lý do rõ trong scoring\\\_note.
```

\---

## 15\. Khuyến nghị sử dụng trong đồ án hiện tại

Để bảo đảm tính khách quan và dễ bảo vệ khi thuyết trình, nên dùng cấu hình chính:


alpha = 0.25
beta  = 0.25
gamma = 0.25
delta = 0.25
W\\\_i   = 1.0 cho toàn bộ bản ghi
```

Nếu muốn mở rộng, có thể trình bày AHP, trọng số domain hoặc phân tích độ nhạy ở phần **hạn chế và hướng phát triển**, không nên coi đó là kết quả chính nếu chưa có chuyên gia hoặc dữ liệu thực nghiệm.

\---

## 16\. Tham chiếu nội bộ

* `config/scoring\\\_config.yaml` — cấu hình `alpha`, `beta`, `gamma`, `delta`, `default\\\_W\\\_i`.
* `src/09b\\\_build\\\_actor\\\_domain\\\_review.py` — gợi ý và rà soát chuẩn hóa actor/domain.
* `src/09c\\\_validate\\\_actor\\\_domain.py` — validate và chốt actor/domain trước khi scoring.
* `src/10\\\_build\\\_scoring\\\_input.py` — tạo file `scoring\\\_input.xlsx` với các cột `M\\\_i`, `S\\\_i`, `D\\\_i`, `R\\\_i`, `W\\\_i`, `scoring\\\_note`.
* `src/11\\\_calculate\\\_impact\\\_score.py` — tính `ImpactScore\\\_i`.
* `docs/label\\\_guideline\\\_5-labels.md` — xác định `final\\\_label` và chiều tác động.
* `docs/adjudication\\\_protocol.md` — quy trình chốt nhãn cuối cùng trước khi lượng hóa.

