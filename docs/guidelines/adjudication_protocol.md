# Giao thức xử lý bất đồng (Adjudication Protocol)

**Dự án:** DTM — Đánh giá tác động chính sách môi trường - Khung định lượng: lợi ich , chi phí, rủi ro
**Áp dụng cho:**

* Tầng 1: `env\_human` so với `env\_llm`
* Tầng 2: `class\_human` so với `class\_llm`

**Phiên bản:** 2.0

\---

## 1\. Mục tiêu của giao thức

Giao thức này hướng dẫn người nghiên cứu xử lý các trường hợp bất đồng giữa nhãn do con người gán và nhãn do LLM dự đoán.

Mục tiêu không phải là “chọn theo LLM” hoặc “luôn giữ nhãn con người”, mà là:


đọc lại raw\_text
→ đối chiếu guideline
→ kiểm tra evidence và reason
→ xác định nhãn hợp lý nhất
→ ghi lại quyết định review
→ chốt nhãn cuối cùng dùng cho pipeline sau
```

Trong hệ thống hiện tại:
Tổng số bản ghi tầng 2: 581
Số bản ghi class\_human = class\_llm: 402
Số bản ghi class\_human ≠ class\_llm: 179
```

402 bản ghi đồng thuận không mặc nhiên đúng tuyệt đối, nhưng có rủi ro thấp hơn.  
179 bản ghi bất đồng là nhóm cần review bắt buộc trước khi chốt `final\_label`.

\---

## 2\. Nguyên tắc cốt lõi

## 2.1. Metric phải được tính trước adjudication

Metric ban đầu của LLM phải được tính bằng:


env\_llm   vs env\_human
class\_llm vs class\_human
```

Không dùng:


env\_llm   vs env\_final
class\_llm vs final\_label
```

Lý do: `env\_final` và `final\_label` là nhãn đã được review và có thể đã bị sửa sau khi xem kết quả LLM. Nếu dùng chúng để tính metric ban đầu, kết quả đánh giá LLM sẽ bị phóng đại.

\---

## 2.2. Phân biệt rõ 4 loại nhãn

Ở tầng 1:

|Trường|Ý nghĩa|
|-|-|
|`env\_human`|Nhãn do người nghiên cứu gán trước khi xem LLM|
|`env\_llm`|Nhãn do LLM dự đoán|
|`env\_final`|Nhãn cuối cùng sau review|
|`env\_needs\_review`|Cờ đánh dấu bản ghi cần kiểm tra lại|

Ở tầng 2:

|Trường|Ý nghĩa|
|-|-|
|`class\_human`|Nhãn 5 lớp do người nghiên cứu gán trước khi xem LLM|
|`class\_llm`|Nhãn 5 lớp do LLM dự đoán|
|`final\_label`|Nhãn cuối cùng sau review|
|`class\_needs\_review`|Cờ đánh dấu bản ghi cần kiểm tra lại|

\---

## 2.3. Human label là nhãn tham chiếu, không phải chân lý tuyệt đối

`env\_human` và `class\_human` là **Human-labeled Reference Dataset**.  
Không nên gọi là Gold Dataset nếu chưa có nhiều annotator, đo đồng thuận và chuyên gia xác nhận.

Trong quá trình adjudication, nếu phát hiện nhãn human ban đầu sai rõ ràng theo guideline, được phép sửa trong nhãn cuối cùng, nhưng phải ghi lại lý do.

\---

## 2.4. Không sửa âm thầm

Mọi thay đổi sau review phải có dấu vết.

Nên có các cột sau trong file review hoặc file final:


review\_decision
final\_label
final\_reason
review\_note
error\_type
reviewer
reviewed\_at
```

Nếu chưa có đủ các cột này, nên bổ sung trước khi chốt dataset cuối cùng.

\---

## 3\. Quy trình tổng quát

## 3.1. Bước 1 — Tính metric ban đầu

Trước khi review, chạy script so sánh để có metric ban đầu.

Tầng 1:


env\_llm vs env\_human
```

Tầng 2:


class\_llm vs class\_human
```

Với tầng 2 hiện tại:
Agreement = 402 / 581 ≈ 69.19%
Disagreement = 179 / 581 ≈ 30.81%
```

Lưu ý: đây là tỷ lệ đồng thuận nếu mỗi bản ghi chỉ có một nhãn. Các metric đầy đủ như Precision, Recall, F1-score, Macro-F1 phải tính từ confusion matrix 5 lớp.

\---

## 3.2. Bước 2 — Tạo tập review

Tầng 1:


env\_review\_dataset.xlsx = các dòng env\_human ≠ env\_llm
```

Tầng 2:


class\_review\_dataset.xlsx = các dòng class\_human ≠ class\_llm
```

Ngoài các dòng bất đồng, nên kiểm tra thêm:


class\_needs\_review = TRUE
LLM needs\_human\_review = TRUE
LLM confidence thấp
nhãn BQ hoặc CQ
bản ghi quá dài
bản ghi có nhiều chủ thể
bản ghi có nhiều tác động trong cùng raw\_text
```

\---

## 3.3. Bước 3 — Review từng bản ghi

Với mỗi bản ghi bất đồng, đọc theo thứ tự:

`
1. source\_id
2. legal\_citation
3. raw\_text
4. class\_human hoặc env\_human
5. class\_human\_reason hoặc env\_human\_reason
6. class\_llm hoặc env\_llm
7. class\_llm\_reason hoặc env\_llm\_reason
8. evidence\_span
9. rule\_applied
10. quantity\_interpretation
```

Không quyết định chỉ dựa vào tên nhãn. Phải đọc `raw\_text`.

\---

## 3.4. Bước 4 — Ra quyết định review

Mỗi bản ghi cần được gán một `review\_decision`.

|`review\_decision`|Khi nào dùng|Kết quả|
|-|-|-|
|`KEEP\_HUMAN`|Human đúng, LLM sai|`final\_label = class\_human`|
|`ACCEPT\_LLM`|LLM đúng, human ban đầu sai|`final\_label = class\_llm`|
|`NEW\_LABEL`|Cả human và LLM đều chưa phù hợp|`final\_label = nhãn mới do reviewer chọn`|
|`AMBIGUOUS\_KEEP\_HUMAN`|Còn mơ hồ, chưa đủ cơ sở đổi nhãn|`final\_label = class\_human`, giữ `needs\_review = TRUE`|
|`NEED\_EXPERT\_REVIEW`|Bản ghi vượt quá khả năng xác quyết của người nghiên cứu|tạm giữ nhãn tốt nhất, đánh dấu cần chuyên gia|

\---

## 4\. Giao thức tầng 1 — Lọc tác động môi trường

Tầng 1 xử lý bài toán nhị phân:


env\_label ∈ {0, 1}
```

## 4.1. Khi giữ nhãn human

Giữ `env\_human` nếu:

* `raw\_text` không có bằng chứng môi trường trực tiếp;
* LLM gán `true` chỉ vì văn bản thuộc Luật Bảo vệ môi trường;
* LLM suy diễn ngoài văn bản;
* LLM không chỉ ra được `evidence\_span` thuyết phục.

`review\_decision = KEEP\_HUMAN`

\---

## 4.2. Khi chấp nhận nhãn LLM

Chấp nhận `env\_llm` nếu:

* LLM chỉ ra cụm bằng chứng môi trường rõ ràng trong `raw\_text`;
* human ban đầu bỏ sót yếu tố như chất thải, nước thải, khí thải, ĐTM, giấy phép môi trường, quan trắc, ô nhiễm, khí nhà kính, đa dạng sinh học;
* nhãn human ban đầu vi phạm guideline lọc môi trường.

`review\_decision = ACCEPT\_LLM`

\---

## 4.3. Khi cần chuyên gia hoặc review tiếp

Đánh dấu cần review nếu:

* bản ghi chỉ dẫn chiếu nhưng điều được dẫn chiếu có thể chứa nội dung môi trường;
* bản ghi là định nghĩa nhưng có ảnh hưởng đến phạm vi áp dụng;
* bản ghi quá dài, chứa nhiều nội dung;
* không xác định được bản ghi có tác động môi trường trực tiếp hay chỉ là thủ tục chung.

`review\_decision = NEED\_EXPERT\_REVIEW`

\---

## 5\. Giao thức tầng 2 — Gán 5 nhãn tác động

Tầng 2 xử lý bài toán 5 nhãn:


BENEFIT\_QUANTITATIVE
BENEFIT\_QUALITATIVE
COST\_QUANTITATIVE
COST\_QUALITATIVE
CONSTRAINT
```

## 5.1. Thứ tự đọc khi review 179 bất đồng

Với 179 dòng bất đồng trong `class\_review\_dataset.xlsx`, thực hiện lần lượt:


1. Đọc raw\_text.
2. Xác định tín hiệu pháp lý chính.
3. Xác định bản chất tác động: lợi ích, chi phí tuân thủ hay ràng buộc.
4. Kiểm tra có giá trị định lượng thật hay không.
5. So sánh class\_human\_reason với class\_llm\_reason.
6. Kiểm tra evidence\_span của LLM có nằm trong raw\_text không.
7. Chọn review\_decision.
8. Chốt final\_label và final\_reason.
```

\---

## 5.2. Quy tắc xử lý theo từng kiểu bất đồng

### A. `COST\_QUALITATIVE` vs `CONSTRAINT`

Đây thường là nhóm bất đồng lớn nhất.

Chọn `COST\_QUALITATIVE` nếu trọng tâm là:


phải lập
phải nộp
phải báo cáo
phải đăng ký
phải quan trắc
phải xử lý
phải thu gom
phải chuyển giao
phải có giấy phép môi trường
tổ chức thực hiện
xây dựng kế hoạch
```

Chọn `CONSTRAINT` nếu trọng tâm là:

`
nghiêm cấm
không được
không cấp
không phê duyệt
chỉ được
trừ trường hợp
phải đáp ứng
đạt quy chuẩn kỹ thuật môi trường
không vượt quá
hạn ngạch
khả năng chịu tải
điều kiện
```

Mẫu `final\_reason`:


Chọn COST\_QUALITATIVE vì trọng tâm bản ghi là nghĩa vụ thực hiện/thủ tục, không phải lệnh cấm hoặc điều kiện kỹ thuật.
```

hoặc:


Chọn CONSTRAINT vì trọng tâm bản ghi là điều kiện/quy chuẩn giới hạn hành vi, không phải nghĩa vụ thủ tục.
```

\---

### B. `COST\_QUANTITATIVE` vs `COST\_QUALITATIVE`

Chọn `COST\_QUANTITATIVE` chỉ khi có:


số tiền
đơn giá
mức phí
mức thuế
mức ký quỹ
mức bồi thường
tỷ lệ chi trả tài chính
```

Chọn `COST\_QUALITATIVE` nếu chỉ có:


thời hạn
mã QCVN
số điều/khoản
ngưỡng kỹ thuật
số bộ hồ sơ
nghĩa vụ tài chính nhưng chưa có mức tiền
```

Mẫu `final\_reason`:


Chọn COST\_QUALITATIVE vì bản ghi có nghĩa vụ tuân thủ nhưng không nêu số tiền, đơn giá hoặc mức chi trả cụ thể.
```

\---

### C. `BENEFIT\_QUALITATIVE` vs `CONSTRAINT`

Chọn `BENEFIT\_QUALITATIVE` nếu điều khoản dùng cơ chế:


khuyến khích
hỗ trợ
ưu đãi
tạo điều kiện
phát triển
cải thiện
phục hồi
```

Chọn `CONSTRAINT` nếu điều khoản dùng cơ chế:

```text

không được
không cấp
chỉ được
điều kiện
quy chuẩn
ngưỡng
hạn chế hành vi
```

Mẫu `final\_reason`:


Chọn BENEFIT\_QUALITATIVE vì bản ghi tạo cơ chế khuyến khích/hỗ trợ có lợi cho môi trường.
```

hoặc:


Chọn CONSTRAINT vì bản ghi không trao lợi ích trực tiếp mà đặt ra giới hạn hoặc điều kiện pháp lý.
```

\---

### D. `BENEFIT\_QUANTITATIVE` vs `BENEFIT\_QUALITATIVE`

Chọn `BENEFIT\_QUANTITATIVE` chỉ khi lợi ích được lượng hóa bằng:

`
số tiền hỗ trợ
tỷ lệ hỗ trợ
tỷ lệ giảm phát thải
khối lượng chất thải giảm/tái chế
diện tích phục hồi
lượng tài nguyên tiết kiệm
```

Chọn `BENEFIT\_QUALITATIVE` nếu chỉ có:


khuyến khích
hỗ trợ
ưu đãi
cải thiện
bảo vệ
phát triển
```

nhưng không nêu giá trị định lượng trực tiếp.

\---

### E. `BENEFIT\_\*` vs `COST\_\*`

Chọn nhãn lợi ích nếu bản ghi chủ yếu trao quyền, ưu đãi, hỗ trợ hoặc khuyến khích.

Chọn nhãn chi phí nếu bản ghi chủ yếu bắt buộc chủ thể thực hiện một nghĩa vụ, thủ tục, báo cáo, quan trắc, xử lý, đầu tư, vận hành hoặc chi trả.

Nếu bản ghi vừa có lợi ích vừa có nghĩa vụ:

`
chọn nhãn theo mệnh đề chính;
nếu không chắc, đặt class\_needs\_review = TRUE.
```

\---

## 6\. Nhóm lỗi thường gặp của LLM

Khi review, nên phân loại lỗi để phục vụ phân tích sau này.

|`error\_type`|Ý nghĩa|
|-|-|
|`LLM\_CQL\_CON\_CONFUSION`|LLM nhầm giữa chi phí định tính và ràng buộc|
|`LLM\_QUANTITATIVE\_OVERDETECTION`|LLM thấy số/mã QCVN/thời hạn và gán nhãn định lượng sai|
|`LLM\_BENEFIT\_OVERDETECTION`|LLM diễn giải nghĩa vụ/ràng buộc thành lợi ích|
|`LLM\_MISREAD\_LEGAL\_SIGNAL`|LLM đọc sai tín hiệu pháp lý chính|
|`LLM\_WEAK\_EVIDENCE`|LLM chọn nhãn nhưng evidence không đủ|
|`HUMAN\_INITIAL\_ERROR`|Nhãn human ban đầu sai rõ theo guideline|
|`AMBIGUOUS\_MULTI\_IMPACT`|Bản ghi có nhiều tác động, khó chọn một nhãn|
|`SEGMENTATION\_ISSUE`|Bản ghi quá dài hoặc gộp nhiều mệnh đề|
|`REFERENCE\_OR\_CROSS\_REFERENCE`|Bản ghi dẫn chiếu, cần đọc điều/khoản liên quan|
|`NO\_ERROR\_AGREEMENT`|Không có lỗi, human và LLM đồng thuận|

\---

## 7\. Review đối với 402 bản ghi đồng thuận

402 bản ghi đồng thuận có thể được chấp nhận nhanh hơn, nhưng không nên bỏ qua hoàn toàn.

Nên kiểm tra chọn mẫu:


10%–20% bản ghi đồng thuận
toàn bộ bản ghi có confidence thấp
toàn bộ bản ghi có class\_needs\_review = TRUE
toàn bộ bản ghi có nhãn BQ hoặc CQ
một số bản ghi dài, nhiều chủ thể, nhiều domain
```

Nếu phát hiện tỷ lệ lỗi cao trong nhóm đồng thuận, cần mở rộng review.

\---

## 8\. Cách chốt `final\_label`

## 8.1. Quy tắc mặc định

Sau review:


final\_label = nhãn được reviewer xác nhận là hợp lý nhất
```

Không mặc định `final\_label = class\_human` trong mọi trường hợp.

Các khả năng:


KEEP\_HUMAN       → final\_label = class\_human
ACCEPT\_LLM       → final\_label = class\_llm
NEW\_LABEL        → final\_label = nhãn mới
AMBIGUOUS\_KEEP\_HUMAN → final\_label = class\_human, vẫn giữ needs\_review = TRUE
NEED\_EXPERT\_REVIEW  → final\_label = nhãn tạm thời, review\_note ghi cần chuyên gia
```

## 8.2. Cột cần có trong file final

File final nên có tối thiểu:


source\_id
legal\_citation
raw\_text
class\_human
class\_llm
final\_label
final\_reason
review\_decision
error\_type
class\_needs\_review
review\_note
```

\---

## 9\. Cách ghi `final\_reason`

`final\_reason` nên ngắn, rõ, dựa vào guideline.

Ví dụ:


Chọn COST\_QUALITATIVE vì bản ghi yêu cầu chủ thể lập và gửi báo cáo môi trường, tạo gánh nặng tuân thủ nhưng không nêu chi phí định lượng.
```


Chọn CONSTRAINT vì bản ghi đặt điều kiện không cấp phép nếu nguồn nước không còn khả năng chịu tải.
```


Chọn BENEFIT\_QUALITATIVE vì bản ghi quy định cơ chế khuyến khích tái chế, có lợi cho môi trường nhưng không nêu mức hỗ trợ cụ thể.
```


Chọn COST\_QUANTITATIVE vì bản ghi quy định mức ký quỹ cụ thể bằng tiền.
```

\---

## 10\. Quy tắc về metric sau adjudication

## 10.1. Metric ban đầu

Báo cáo chính nên dùng metric ban đầu:

class\_llm vs class\_human
```

Đây là kết quả phản ánh LLM khi so với nhãn tham chiếu ban đầu.

## 10.2. Metric sau khi sửa reference, nếu có

Nếu trong adjudication phát hiện nhiều lỗi human ban đầu và bạn tạo thêm cột:


class\_reference\_corrected
```

thì có thể tính thêm metric phụ:

class\_llm vs class\_reference\_corrected
```

Nhưng phải gọi rõ là:


Metric against corrected human reference
```

Không gọi là metric ban đầu.

## 10.3. Không dùng `final\_label` để thổi phồng kết quả

Không báo cáo:


class\_llm vs final\_label
```

như metric chính nếu `final\_label` đã được chọn sau khi xem cả human và LLM.

\---

## 11\. Kiểm tra chất lượng trước khi xuất file cuối

Trước khi xuất `final\_labeled\_dataset.xlsx`, kiểm tra:


Không có dòng thiếu final\_label.
final\_label chỉ thuộc 5 nhãn hợp lệ.
Mọi dòng bất đồng đều có review\_decision.
Mọi dòng bất đồng đều có final\_reason.
Mọi dòng ACCEPT\_LLM đều có lý do vì sao human ban đầu sai.
Mọi dòng NEW\_LABEL đều ghi rõ vì sao cả human và LLM chưa phù hợp.
Mọi dòng NEED\_EXPERT\_REVIEW vẫn có nhãn tạm thời và review\_note.
Không còn bản ghi BQ/CQ chỉ vì có số điều, thời hạn hoặc mã QCVN.
Các lỗi CQL/CON đã được rà soát theo guideline.
```

\---

## 12\. Checklist thao tác với 179 bản ghi bất đồng


\[ ] Mở class\_review\_dataset.xlsx.
\[ ] Đọc lại raw\_text của từng dòng bất đồng.
\[ ] Mở label\_guideline\_5-labels.md để đối chiếu.
\[ ] So sánh class\_human\_reason với class\_llm\_reason.
\[ ] Kiểm tra evidence\_span có đúng là trích từ raw\_text không.
\[ ] Xác định nhãn hợp lý nhất.
\[ ] Điền review\_decision.
\[ ] Điền final\_label.
\[ ] Điền final\_reason.
\[ ] Điền error\_type.
\[ ] Điền review\_note nếu cần.
\[ ] Đánh dấu class\_needs\_review nếu vẫn mơ hồ.
\[ ] Sau khi xong 179 dòng, kiểm tra lại các nhãn BQ/CQ và các dòng confidence thấp.
```

\---

## 13\. Kết luận ngắn gọn

Quy tắc quyết định cuối cùng:


Metric đo LLM phải tính trước review.
Adjudication dùng để chốt nhãn cuối cùng, không dùng để làm đẹp metric.
Bất đồng phải được giải quyết bằng raw\_text + guideline + evidence, không chọn theo cảm tính.
Nếu LLM đúng và human ban đầu sai, được chấp nhận LLM nhưng phải ghi lý do.
Nếu cả hai chưa đúng, chọn nhãn mới và ghi rõ.
Nếu vẫn mơ hồ, giữ nhãn tốt nhất và đánh dấu cần review/chuyên gia.
```

