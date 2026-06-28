# Hướng dẫn gán nhãn 5 nhãn tác động (`class\_human`)

**Dự án:** DTM — Đánh giá tác động chính sách môi trường - khung định lượng: lợi hhh, chi phí, rủi ro  
**Pipeline:** Tầng 2 — Phân loại 5 nhãn tác động  
**Áp dụng cho:** Các bản ghi đã được lọc cuối cùng là `env\_final = 1`  
**Đầu ra cần điền:** `class\_human`, `class\_human\_reason`, `class\_needs\_review`  
**Phiên bản:**2.0

\---

## 1\. Mục tiêu của bước gán 5 nhãn

Bước này dùng để phân loại mỗi bản ghi có tác động môi trường vào đúng **một nhãn chính** trong 5 nhãn:

|Mã|Nhãn đầy đủ|Ý nghĩa|Chiều tác động|
|-|-|-|-|
|`BQ`|`BENEFIT\_QUANTITATIVE`|Lợi ích định lượng|`+1`|
|`BQL`|`BENEFIT\_QUALITATIVE`|Lợi ích định tính|`+1`|
|`CQ`|`COST\_QUANTITATIVE`|Chi phí định lượng|`-1`|
|`CQL`|`COST\_QUALITATIVE`|Chi phí định tính|`-1`|
|`CON`|`CONSTRAINT`|Ràng buộc, điều kiện, lệnh cấm, giới hạn kỹ thuật|`-1`|

Trong hệ thống hiện tại, đây là bài toán **phân loại đa lớp đơn nhãn**. Mỗi bản ghi chỉ được gán **một nhãn cuối cùng trong 5 nhãn**. Nếu bản ghi có nhiều tác động, chọn nhãn thể hiện **tác động chính** của bản ghi đó và đặt `class\_needs\_review = TRUE`.

\---

## 2\. Nguyên tắc chung khi gán nhãn

### 2.1. Không gán nhãn theo cảm tính

Mỗi nhãn phải dựa trên bằng chứng trong `raw\_text`. Khi gán, cần đọc tối thiểu các trường:

source\_id
legal\_citation
raw\_text
actor
legal\_signal
domain
quantitative\_value
condition
```

Không chỉ nhìn vào domain hoặc legal signal để gán nhãn.

### 2.2. Phân biệt ba câu hỏi

Khi đọc một bản ghi, hãy trả lời lần lượt:

1. Bản ghi này tạo **lợi ích**, **chi phí/gánh nặng tuân thủ**, hay **ràng buộc/điều kiện**?
2. Nếu là lợi ích hoặc chi phí, nó có **giá trị định lượng trực tiếp** không?
3. Nếu có số, con số đó có thật sự là giá trị lợi ích/chi phí hay chỉ là thời hạn, số điều/khoản, mã QCVN, điều kiện kỹ thuật?

### 2.3. Có số không đồng nghĩa với nhãn định lượng

Một bản ghi chỉ được gán `BENEFIT\_QUANTITATIVE` hoặc `COST\_QUANTITATIVE` khi con số thể hiện **giá trị lợi ích hoặc chi phí có thể lượng hóa trực tiếp**.

Các loại số **không đủ** để gán nhãn định lượng:

* số điều, khoản, điểm;
* ngày hiệu lực;
* năm ban hành;
* thời hạn hành chính;
* số bộ hồ sơ;
* mã QCVN, TCVN;
* số hiệu văn bản;
* ngưỡng làm điều kiện áp dụng;
* hạn mức kỹ thuật không chuyển trực tiếp thành lợi ích hoặc chi phí.

Ví dụ: “phải đạt quy chuẩn kỹ thuật môi trường” hoặc “QCVN 40:2011/BTNMT” thường là **ràng buộc kỹ thuật** (`CON`), không tự động là `COST\_QUANTITATIVE`.

\---

## 3\. Định nghĩa 5 nhãn

## 3.1. `BENEFIT\_QUANTITATIVE` — Lợi ích định lượng

### Định nghĩa

Gán `BENEFIT\_QUANTITATIVE` khi bản ghi tạo ra lợi ích môi trường, xã hội hoặc kinh tế xanh và lợi ích đó được lượng hóa trực tiếp bằng con số, tỷ lệ, khối lượng, diện tích, mức giảm phát thải, mức hỗ trợ hoặc đại lượng đo được.

### Dấu hiệu thường gặp

* `được hỗ trợ ... đồng`
* `được giảm ... %`
* `giảm ... tấn CO2`
* `tăng ... ha diện tích cây xanh`
* `thu hồi/tái chế ... %`
* `tiết kiệm ... kWh`
* `giảm phát thải ... %`
* `được miễn/giảm một khoản phí cụ thể`

### Điều kiện gán

Gán nhãn này nếu đồng thời có:


Có lợi ích rõ ràng
+ Có giá trị định lượng trực tiếp của lợi ích
```

### Không gán BQ nếu

* con số chỉ là thời hạn, số điều/khoản, số bộ hồ sơ;
* con số là ngưỡng điều kiện để được cấp phép;
* bản ghi là nghĩa vụ tuân thủ của doanh nghiệp, không phải cơ chế lợi ích;
* bản ghi chỉ nói “khuyến khích”, “hỗ trợ” nhưng không có mức định lượng.

### Mẫu lý do


Bản ghi tạo lợi ích môi trường có thể lượng hóa trực tiếp thông qua \[giá trị định lượng], nên được gán BENEFIT\_QUANTITATIVE.
```

### Ví dụ


Tổ chức thực hiện hoạt động tái chế được hỗ trợ 50% kinh phí đầu tư thiết bị xử lý chất thải.
```

→ `BENEFIT\_QUANTITATIVE`  
→ Lý do: có lợi ích hỗ trợ tài chính và mức hỗ trợ định lượng là `50%`.

\---

## 3.2. `BENEFIT\_QUALITATIVE` — Lợi ích định tính

### Định nghĩa

Gán `BENEFIT\_QUALITATIVE` khi bản ghi tạo ra lợi ích môi trường hoặc lợi ích quản lý môi trường nhưng chưa có con số đo lường trực tiếp.

### Dấu hiệu thường gặp

* `khuyến khích`
* `hỗ trợ`
* `ưu đãi`
* `tạo điều kiện`
* `bảo vệ`
* `cải thiện`
* `phục hồi`
* `phát triển kinh tế tuần hoàn`
* `thúc đẩy công nghệ sạch`
* `nâng cao hiệu quả quản lý môi trường`

### Điều kiện gán

Gán nhãn này nếu:


Có lợi ích môi trường hoặc lợi ích quản lý môi trường rõ ràng
+ Không có giá trị định lượng trực tiếp
+ Không phải lệnh cấm hay điều kiện kỹ thuật là trọng tâm chính
```

### Không gán BQL nếu

* bản ghi chủ yếu là lệnh cấm, giới hạn, điều kiện, tiêu chuẩn;
* bản ghi đặt ra nghĩa vụ lập hồ sơ, báo cáo, quan trắc, xin phép;
* bản ghi tạo nghĩa vụ tài chính hoặc chi phí tuân thủ.

### Mẫu lý do


Bản ghi tạo lợi ích định tính cho bảo vệ/quản lý môi trường nhưng không có giá trị định lượng trực tiếp, nên được gán BENEFIT\_QUALITATIVE.
```

### Ví dụ


Nhà nước khuyến khích phát triển mô hình kinh tế tuần hoàn, sản xuất sạch hơn và tiêu dùng bền vững.
```

→ `BENEFIT\_QUALITATIVE`  
→ Lý do: tạo lợi ích định tính cho môi trường, chưa có số đo cụ thể.

\---

## 3.3. `COST\_QUANTITATIVE` — Chi phí định lượng

### Định nghĩa

Gán `COST\_QUANTITATIVE` khi bản ghi tạo nghĩa vụ tài chính hoặc chi phí tuân thủ có giá trị định lượng trực tiếp.

### Dấu hiệu thường gặp

* `phải nộp ... đồng`
* `phí bảo vệ môi trường ...`
* `thuế ...`
* `ký quỹ ...`
* `bồi thường ...`
* `chi trả ...`
* `mức đóng góp ...`
* `mức phạt ...`
* `đơn giá ... đồng/tấn`, `đồng/m3`, `đồng/kg`

### Điều kiện gán

Gán nhãn này nếu đồng thời có:
Có nghĩa vụ tài chính/chi phí tuân thủ
+ Có số tiền, tỷ lệ tiền, đơn giá hoặc mức chi trả cụ thể
```

### Không gán CQ nếu

* chỉ có nghĩa vụ “đóng góp tài chính”, “chi trả”, “bồi thường” nhưng không nêu số tiền;
* chỉ có thời hạn, mã QCVN, số điều/khoản;
* con số chỉ là ngưỡng kỹ thuật hoặc điều kiện cấp phép;
* chỉ là nghĩa vụ lập hồ sơ, báo cáo, quan trắc nhưng chưa có số tiền.

Những trường hợp trên thường là `COST\_QUALITATIVE` hoặc `CONSTRAINT`.

### Mẫu lý do


Bản ghi tạo nghĩa vụ tài chính có giá trị định lượng trực tiếp là \[giá trị, con số], nên được gán COST\_QUANTITATIVE.
```

### Ví dụ

Cơ sở xả nước thải phải nộp phí bảo vệ môi trường là 40.000 đồng/m3 nước thải.
```

→ `COST\_QUANTITATIVE`  
→ Lý do: có nghĩa vụ tài chính và mức phí cụ thể.

\---

## 3.4. `COST\_QUALITATIVE` — Chi phí định tính

### Định nghĩa

Gán `COST\_QUALITATIVE` khi bản ghi đặt ra nghĩa vụ tuân thủ, thủ tục, hồ sơ, báo cáo, vận hành, quan trắc, đăng ký hoặc xin phép, làm phát sinh chi phí thời gian, nhân lực, tổ chức thực hiện nhưng chưa có giá trị tiền tệ cụ thể.

### Dấu hiệu thường gặp

* `phải lập`
* `phải trình`
* `phải nộp`
* `phải báo cáo`
* `phải đăng ký`
* `phải quan trắc`
* `phải giám sát`
* `phải phân loại`
* `phải thu gom`
* `phải xử lý`
* `phải chuyển giao`
* `phải có giấy phép môi trường`
* `có trách nhiệm thực hiện`
* `xây dựng kế hoạch`
* `tổ chức thực hiện`

### Điều kiện gán

Gán nhãn này nếu:

Có nghĩa vụ tuân thủ hoặc thủ tục cụ thể
+ Chưa có số tiền/chi phí định lượng trực tiếp
+ Trọng tâm không phải là lệnh cấm hoặc giới hạn kỹ thuật
```

### Không gán CQL nếu

* trọng tâm chính là “nghiêm cấm”, “không được”, “chỉ được”, “không phê duyệt”, “không cấp phép”;
* trọng tâm chính là ngưỡng, điều kiện, quy chuẩn, giới hạn kỹ thuật;
* có số tiền hoặc mức phí cụ thể.

### Mẫu lý do

Bản ghi đặt ra nghĩa vụ thủ tục/tuân thủ làm phát sinh gánh nặng thực hiện nhưng không nêu chi phí định lượng trực tiếp, nên được gán COST\_QUALITATIVE.
```

### Ví dụ

Chủ dự án đầu tư phải lập báo cáo đánh giá tác động môi trường và trình cơ quan có thẩm quyền thẩm định.
```

→ `COST\_QUALITATIVE`  
→ Lý do: nghĩa vụ lập và trình hồ sơ ĐTM tạo gánh nặng tuân thủ, chưa có chi phí định lượng.

\---

## 3.5. `CONSTRAINT` — Ràng buộc

### Định nghĩa

Gán `CONSTRAINT` khi bản ghi đặt ra lệnh cấm, điều kiện, giới hạn, ngưỡng kỹ thuật, quy chuẩn, tiêu chuẩn, điều kiện cấp phép hoặc điều kiện vận hành. Đây là nhãn cho các bản ghi làm hạn chế hoặc định khung hành vi của chủ thể.

### Dấu hiệu thường gặp

* `nghiêm cấm`
* `cấm`
* `không được`
* `không phê duyệt`
* `không cấp giấy phép`
* `chỉ được`
* `trừ trường hợp`
* `không vượt quá`
* `phải đáp ứng`
* `phải bảo đảm`
* `đạt quy chuẩn kỹ thuật môi trường`
* `theo quy chuẩn`
* `theo tiêu chuẩn`
* `hạn ngạch`
* `hạn mức`
* `ngưỡng`
* `khả năng chịu tải`
* `điều kiện`

### Điều kiện gán

Gán nhãn này nếu:
Trọng tâm bản ghi là cấm, hạn chế, điều kiện, ngưỡng, tiêu chuẩn, quy chuẩn hoặc điều kiện cấp phép/vận hành
```

### Không gán CONSTRAIN nếu

* bản ghi chủ yếu là nghĩa vụ lập hồ sơ, báo cáo, quan trắc, đăng ký, xin phép;
* bản ghi chủ yếu là cơ chế khuyến khích, hỗ trợ, ưu đãi;
* bản ghi chủ yếu là nghĩa vụ tài chính có số tiền cụ thể.

### Mẫu lý do


Bản ghi đặt ra lệnh cấm/điều kiện/quy chuẩn giới hạn hành vi môi trường, nên được gán CONSTRAINT.
```

### Ví dụ

Nghiêm cấm xả nước thải, khí thải chưa được xử lý đạt quy chuẩn kỹ thuật môi trường ra môi trường.
```

→ `CONSTRAINT`  
→ Lý do: bản ghi là lệnh cấm và đặt điều kiện quy chuẩn kỹ thuật môi trường.

\---

## 4\. Quy tắc ưu tiên khi một bản ghi có nhiều dấu hiệu

Do hệ thống hiện tại dùng một nhãn duy nhất, cần áp dụng quy tắc ưu tiên sau.

### 4.1. Ưu tiên theo bản chất tác động chính

|Nếu trọng tâm bản ghi là|Nhãn ưu tiên|
|-|-|
|Hỗ trợ, ưu đãi, khuyến khích, cải thiện môi trường có số cụ thể|`BENEFIT\_QUANTITATIVE`|
|Hỗ trợ, ưu đãi, khuyến khích, cải thiện môi trường không có số cụ thể|`BENEFIT\_QUALITATIVE`|
|Phí, thuế, ký quỹ, bồi thường, chi trả có số tiền cụ thể|`COST\_QUANTITATIVE`|
|Nghĩa vụ lập hồ sơ, báo cáo, quan trắc, đăng ký, xin phép, tổ chức thực hiện|`COST\_QUALITATIVE`|
|Cấm, không được, chỉ được, không phê duyệt, điều kiện, quy chuẩn, ngưỡng, hạn ngạch|`CONSTRAINT`|

### 4.2. Nếu vừa có thủ tục vừa có điều kiện

* Nếu câu chính là “phải lập”, “phải nộp”, “phải báo cáo”, “phải quan trắc”, “phải đăng ký”, “phải có giấy phép” → thường chọn `COST\_QUALITATIVE`.
* Nếu câu chính là “không được”, “không phê duyệt”, “không cấp”, “chỉ được”, “trừ trường hợp”, “đạt quy chuẩn”, “không vượt quá” → thường chọn `CONSTRAINT`.

### 4.3. Nếu vừa có lợi ích vừa có nghĩa vụ

* Nếu bản ghi trao quyền, hỗ trợ, ưu đãi cho chủ thể → ưu tiên nhãn lợi ích.
* Nếu bản ghi bắt buộc chủ thể thực hiện việc gây chi phí → ưu tiên nhãn chi phí hoặc ràng buộc.
* Nếu không rõ tác động chính, gán theo phần có tín hiệu pháp lý mạnh hơn và đặt `class\_needs\_review = TRUE`.

\---

## 5\. Phân biệt các cặp nhãn dễ nhầm

## 5.1. `COST\_QUALITATIVE` và `CONSTRAINT`

|Tiêu chí|`COST\_QUALITATIVE`|`CONSTRAINT`|
|-|-|-|
|Trọng tâm|Nghĩa vụ thực hiện/thủ tục|Điều kiện, cấm, giới hạn|
|Cụm từ điển hình|phải lập, báo cáo, đăng ký, quan trắc, chuyển giao|nghiêm cấm, không được, chỉ được, không cấp, đạt quy chuẩn|
|Bản chất|Gánh nặng tuân thủ|Ràng buộc hành vi hoặc điều kiện pháp lý/kỹ thuật|
|Ví dụ|Phải lập báo cáo ĐTM|Không cấp phép nếu môi trường không còn khả năng chịu tải|

**Quy tắc ngắn:**  
Nếu phải làm thêm một công việc/hồ sơ → `COST\_QUALITATIVE`.  
Nếu bị giới hạn/cấm/điều kiện hóa hành vi → `CONSTRAINT`.

\---

## 5.2. `COST\_QUANTITATIVE` và `COST\_QUALITATIVE`

|Tiêu chí|`COST\_QUANTITATIVE`|`COST\_QUALITATIVE`|
|-|-|-|
|Có số tiền/đơn giá/mức chi trả cụ thể|Có|Không|
|Ví dụ|Nộp phí 40.000 đồng/m3|Phải nộp báo cáo môi trường|
|Bản chất|Chi phí đo được trực tiếp|Gánh nặng tuân thủ chưa lượng hóa|

**Quy tắc ngắn:**  
Có nghĩa vụ tài chính nhưng không có số tiền → `COST\_QUALITATIVE`, không phải `COST\_QUANTITATIVE`.

\---

## 5.3. `BENEFIT\_QUANTITATIVE` và `BENEFIT\_QUALITATIVE`

|Tiêu chí|`BENEFIT\_QUANTITATIVE`|`BENEFIT\_QUALITATIVE`|
|-|-|-|
|Có số đo lợi ích trực tiếp|Có|Không|
|Ví dụ|Hỗ trợ 50% kinh phí xử lý chất thải|Khuyến khích công nghệ sạch|
|Bản chất|Lợi ích đo được|Lợi ích chưa lượng hóa|

\---

## 5.4. `BENEFIT\_QUALITATIVE` và `CONSTRAINT`

|Tiêu chí|`BENEFIT\_QUALITATIVE`|`CONSTRAINT`|
|-|-|-|
|Trọng tâm|Tạo lợi ích/hỗ trợ/cải thiện|Hạn chế hoặc cấm hành vi|
|Cụm từ điển hình|khuyến khích, hỗ trợ, ưu đãi, bảo vệ, phát triển|cấm, không được, không cấp, chỉ được|
|Ví dụ|Khuyến khích kinh tế tuần hoàn|Cấm nhập khẩu chất thải|

**Quy tắc ngắn:**  
Nếu điều khoản dùng cơ chế hỗ trợ/khuyến khích → `BENEFIT\_QUALITATIVE`.  
Nếu điều khoản dùng lệnh cấm/điều kiện → `CONSTRAINT`.

\---

## 6\. Mẫu lý do nên dùng khi điền `class\_human\_reason`

### 6.1. Mẫu cho `BENEFIT\_QUANTITATIVE`


Bản ghi tạo lợi ích môi trường có thể lượng hóa trực tiếp bằng \[giá trị định lượng], nên được gán BENEFIT\_QUANTITATIVE.
```

### 6.2. Mẫu cho `BENEFIT\_QUALITATIVE`


Bản ghi tạo lợi ích định tính cho bảo vệ/quản lý môi trường thông qua \[cơ chế lợi ích], nhưng không có giá trị định lượng trực tiếp, nên được gán BENEFIT\_QUALITATIVE.
```

### 6.3. Mẫu cho `COST\_QUANTITATIVE`


Bản ghi tạo nghĩa vụ tài chính/chi phí tuân thủ có giá trị định lượng trực tiếp là \[giá trị], nên được gán COST\_QUANTITATIVE.
```

### 6.4. Mẫu cho `COST\_QUALITATIVE`

`
Bản ghi đặt ra nghĩa vụ thủ tục/tuân thủ như \[hành động phải thực hiện], làm phát sinh gánh nặng thực hiện nhưng không nêu chi phí định lượng, nên được gán COST\_QUALITATIVE.
```

### 6.5. Mẫu cho `CONSTRAINT`


Bản ghi đặt ra lệnh cấm/điều kiện/quy chuẩn/hạn chế đối với \[hành vi hoặc chủ thể], nên được gán CONSTRAINT.
```

\---

## 7\. Ví dụ minh họa theo từng nhãn

### 7.1. `BENEFIT\_QUANTITATIVE`


Cơ sở tái chế chất thải được hỗ trợ 50% kinh phí đầu tư thiết bị xử lý chất thải.
```

→ `BENEFIT\_QUANTITATIVE`  
→ Lý do: lợi ích hỗ trợ tài chính được lượng hóa bằng tỷ lệ 50%.


Chương trình giảm phát thải khí nhà kính đặt mục tiêu giảm 20% lượng phát thải vào năm 2030.
```

→ `BENEFIT\_QUANTITATIVE`  
→ Lý do: lợi ích giảm phát thải được lượng hóa bằng tỷ lệ 20%.

\---

### 7.2. `BENEFIT\_QUALITATIVE`

Nhà nước khuyến khích tổ chức, cá nhân tham gia hoạt động phân loại, tái chế và tái sử dụng chất thải.
```

→ `BENEFIT\_QUALITATIVE`  
→ Lý do: tạo cơ chế khuyến khích có lợi cho môi trường nhưng chưa có mức hỗ trợ hoặc kết quả định lượng.


Nhà nước ưu tiên phát triển công nghệ thân thiện với môi trường.
```

→ `BENEFIT\_QUALITATIVE`  
→ Lý do: tạo lợi ích định tính thông qua ưu tiên công nghệ sạch.

\---

### 7.3. `COST\_QUANTITATIVE`


Cơ sở xả nước thải phải nộp phí bảo vệ môi trường là 40.000 đồng/m3 nước thải.
```

→ `COST\_QUANTITATIVE`  
→ Lý do: nghĩa vụ tài chính có mức phí cụ thể.


Chủ dự án khai thác khoáng sản phải ký quỹ cải tạo, phục hồi môi trường với mức tối thiểu 500 triệu đồng.
```

→ `COST\_QUANTITATIVE`  
→ Lý do: nghĩa vụ ký quỹ có số tiền cụ thể.

\---

### 7.4. `COST\_QUALITATIVE`


Chủ dự án đầu tư phải lập báo cáo đánh giá tác động môi trường và trình cơ quan có thẩm quyền thẩm định.
```

→ `COST\_QUALITATIVE`  
→ Lý do: nghĩa vụ lập và trình hồ sơ ĐTM tạo gánh nặng tuân thủ, chưa có chi phí định lượng.


Cơ sở sản xuất, kinh doanh, dịch vụ phải thực hiện quan trắc môi trường định kỳ và gửi báo cáo cho cơ quan có thẩm quyền.
```

→ `COST\_QUALITATIVE`  
→ Lý do: nghĩa vụ quan trắc và báo cáo môi trường làm phát sinh chi phí thực hiện, chưa có số tiền cụ thể.


Chủ nguồn thải chất thải nguy hại phải phân loại, lưu giữ và chuyển giao chất thải nguy hại cho đơn vị có chức năng xử lý.
```

→ `COST\_QUALITATIVE`  
→ Lý do: nghĩa vụ phân loại, lưu giữ và chuyển giao chất thải tạo gánh nặng tuân thủ.

\---

### 7.5. `CONSTRAINT`


Nghiêm cấm xả nước thải, khí thải chưa được xử lý đạt quy chuẩn kỹ thuật môi trường ra môi trường.
```

→ `CONSTRAINT`  
→ Lý do: bản ghi đặt ra lệnh cấm và điều kiện quy chuẩn kỹ thuật môi trường.


Không phê duyệt báo cáo đánh giá tác động môi trường hoặc không cấp giấy phép môi trường cho dự án xả nước thải vào nguồn nước không còn khả năng chịu tải.
```

→ `CONSTRAINT`  
→ Lý do: bản ghi đặt ra điều kiện hạn chế phê duyệt/cấp phép.


Chỉ được nhập khẩu phế liệu làm nguyên liệu sản xuất khi đáp ứng quy chuẩn kỹ thuật môi trường.
```

→ `CONSTRAINT`  
→ Lý do: bản ghi đặt ra điều kiện kỹ thuật cho hoạt động nhập khẩu phế liệu.

\---

## 8\. Trường hợp cần `class\_needs\_review = TRUE`

Đánh dấu `class\_needs\_review = TRUE` nếu gặp một trong các trường hợp sau:

1. Bản ghi vừa có nghĩa vụ thủ tục vừa có điều kiện/quy chuẩn.
2. Bản ghi vừa có hỗ trợ/lợi ích vừa có nghĩa vụ tuân thủ.
3. Bản ghi có nhiều chủ thể, mỗi chủ thể chịu tác động khác nhau.
4. Bản ghi có số nhưng không rõ đó là chi phí/lợi ích định lượng hay chỉ là điều kiện kỹ thuật.
5. Bản ghi chỉ dẫn chiếu sang điều/khoản khác.
6. Bản ghi quá dài, chứa nhiều hành động pháp lý khác nhau.
7. Người gán không chắc giữa `COST\_QUALITATIVE` và `CONSTRAINT`.
8. Người gán không chắc giữa nhãn định lượng và định tính.

Khi đặt `class\_needs\_review = TRUE`, vẫn cần điền `class\_human` theo phán đoán tốt nhất và ghi rõ lý do mơ hồ trong `class\_human\_reason`.

\---

## 9\. Quy trình gán nhãn cho từng bản ghi

### Bước 1. Đọc toàn bộ `raw\_text`

Không gán nhãn chỉ dựa vào tiêu đề hoặc domain.

### Bước 2. Xác định tín hiệu pháp lý chính

Tìm các cụm như:


được hỗ trợ
được ưu đãi
khuyến khích
phải lập
phải báo cáo
phải đăng ký
phải quan trắc
phải xử lý
phải nộp
phải chi trả
nghiêm cấm
không được
không cấp
không phê duyệt
chỉ được
đạt quy chuẩn
không vượt quá
```

### Bước 3. Xác định bản chất tác động

* Lợi ích → BQ/BQL
* Chi phí/gánh nặng tuân thủ → CQ/CQL
* Điều kiện/ràng buộc/cấm đoán → CON

### Bước 4. Kiểm tra yếu tố định lượng

Chỉ coi là định lượng nếu con số thể hiện trực tiếp:


số tiền
tỷ lệ hỗ trợ
tỷ lệ giảm phát thải
khối lượng chất thải
diện tích môi trường được cải thiện
lượng tài nguyên tiết kiệm
đơn giá phí/thuế/ký quỹ/bồi thường
```

Không coi là định lượng nếu con số chỉ là:


số điều/khoản
ngày hiệu lực
thời hạn thủ tục
mã QCVN
số lượng hồ sơ
ngưỡng điều kiện áp dụng
```

### Bước 5. Gán `class\_human`

Chỉ dùng một trong 5 giá trị:


BENEFIT\_QUANTITATIVE
BENEFIT\_QUALITATIVE
COST\_QUANTITATIVE
COST\_QUALITATIVE
CONSTRAINT
```

Không viết tắt trong file Excel.

### Bước 6. Ghi `class\_human\_reason`

Lý do phải ngắn, rõ, có căn cứ trong văn bản.

### Bước 7. Đánh dấu `class\_needs\_review`

* `FALSE` nếu nhãn rõ.
* `TRUE` nếu nhãn còn mơ hồ hoặc có nhiều tác động.

\---

## 10\. Kiểm tra chất lượng trước khi chốt nhãn

Trước khi lưu thành `class\_human\_labeled\_dataset.xlsx`, cần kiểm tra:


Không có bản ghi thiếu class\_human.
class\_human chỉ thuộc 5 nhãn hợp lệ.
Không dùng BQ/CQ chỉ vì có số điều, thời hạn hoặc mã QCVN.
Các bản ghi class\_needs\_review = TRUE đã có lý do.
Các bản ghi CQL/CON dễ nhầm đã được đọc lại.
Các bản ghi có nhiều tác động đã chọn nhãn chính và ghi rõ trong reason.
```

\---

## 11\. Gợi ý cập nhật `labels\_reference` trong script tạo template

Trong sheet `labels\_reference`, nên dùng mô tả ngắn sau để tránh người gán hiểu nhầm:

|Nhãn|Mã ngắn|Mô tả đề xuất|direction|
|-|-|-|-|
|`BENEFIT\_QUANTITATIVE`|`BQ`|Lợi ích môi trường/xã hội được lượng hóa trực tiếp bằng số tiền, tỷ lệ, khối lượng, lượng giảm phát thải hoặc đại lượng đo được|`+1`|
|`BENEFIT\_QUALITATIVE`|`BQL`|Lợi ích môi trường/xã hội hoặc lợi ích quản lý môi trường chưa có giá trị định lượng trực tiếp|`+1`|
|`COST\_QUANTITATIVE`|`CQ`|Nghĩa vụ tài chính hoặc chi phí tuân thủ có số tiền, đơn giá, tỷ lệ chi trả, ký quỹ, phí, thuế hoặc bồi thường cụ thể|`-1`|
|`COST\_QUALITATIVE`|`CQL`|Nghĩa vụ thủ tục, hồ sơ, báo cáo, đăng ký, quan trắc, vận hành, xử lý hoặc tổ chức thực hiện chưa có chi phí định lượng|`-1`|
|`CONSTRAINT`|`CON`|Lệnh cấm, điều kiện, giới hạn, tiêu chuẩn, quy chuẩn, hạn ngạch hoặc ràng buộc kỹ thuật/pháp lý đối với hành vi|`-1`|

\---

## 12\. Kết luận sử dụng

Quy tắc ngắn nhất:


Có hỗ trợ/lợi ích + có số đo trực tiếp → BENEFIT\_QUANTITATIVE.
Có hỗ trợ/lợi ích nhưng chưa có số đo → BENEFIT\_QUALITATIVE.
Có phí/thuế/ký quỹ/bồi thường/chi trả với số tiền cụ thể → COST\_QUANTITATIVE.
Có nghĩa vụ lập, nộp, báo cáo, quan trắc, đăng ký, xin phép, xử lý, chuyển giao nhưng chưa có số tiền → COST\_QUALITATIVE.
Có cấm, không được, chỉ được, không cấp, không phê duyệt, điều kiện, quy chuẩn, ngưỡng, hạn ngạch → CONSTRAINT.
```

Nếu không chắc, vẫn gán nhãn theo phán đoán tốt nhất, đặt `class\_needs\_review = TRUE` và ghi rõ lý do trong `class\_human\_reason`.

