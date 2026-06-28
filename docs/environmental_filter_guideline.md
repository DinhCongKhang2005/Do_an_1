# Hướng dẫn `env\_human` — Lọc bản ghi có tác động môi trường

**Dự án:** DTM — Đánh giá tác động chính sách môi trường: Khung định lượng chi phí, lợi ích, rủi ro  
**Pipeline:** Tầng 1 — Lọc tác động môi trường  
**Đầu vào:** Các bản ghi đã có `co\_tac\_dong = true`  
**Đầu ra:** Tập `env\_human` gồm các bản ghi có tác động môi trường do người nghiên cứu lọc thủ công  
**Phiên bản:** 3.1 (Cập nhật lỗi định dạng)

\---

## 1\. Bối cảnh dữ liệu

Dataset đầu vào là **D\_impact** — tập hợp **581 bản ghi** điều khoản từ **Luật Bảo vệ môi trường 2020** (Luật số 72/2020/QH14) đã được xác định là có tác động chính sách (`co\_tac\_dong = true`).

Bước này tiếp tục lọc để xác định trong 581 bản ghi đó, bản ghi nào **có tác động đến môi trường** (`env\_human = 1`) và bản ghi nào **không có tác động môi trường trực tiếp** (`env\_human = 0`).

> ⚠️ \*\*Quan trọng:\*\* Phải hoàn thành gán `env\_human` cho toàn bộ bản ghi \*\*trước khi\*\* xem kết quả LLM. Nếu xem LLM trước rồi mới gán thì metric đánh giá LLM sẽ bị sai (contamination bias).

\---

## 2\. Mục tiêu của bước lọc môi trường

Bước lọc môi trường nhằm xác định trong tập bản ghi đã có tác động chính sách, bản ghi nào thật sự có liên quan đến tác động môi trường.

Với mỗi bản ghi, người nghiên cứu cần điền các trường sau:

|Trường|Ý nghĩa|
|-|-|
|`env\_human`|Nhãn tham chiếu do người nghiên cứu gán. Nhận giá trị `1` hoặc `0`.|
|`env\_domain\_human`|Miền môi trường liên quan nếu `env\_human = 1`.|
|`env\_evidence\_span`|Cụm từ hoặc câu trong `raw\_text` làm căn cứ gán nhãn.|
|`env\_human\_reason`|Lý do ngắn gọn giải thích quyết định gán nhãn.|
|`env\_needs\_review`|Đánh dấu `TRUE` nếu bản ghi mơ hồ, dài, nhiều chủ thể hoặc khó phân loại.|
|`review\_note`|Ghi chú sau khi đọc lại hoặc sau khi đối chiếu với LLM.|

`env\_human` là tập tham chiếu để đánh giá LLM ở bước lọc môi trường. Vì vậy, người nghiên cứu phải thực hiện lọc trước khi xem kết quả lọc của LLM để tránh tính sai lệch metric.

\---

## 3\. Nguyên tắc chung

### 3.1. Không mặc định tất cả điều khoản trong Luật Bảo vệ môi trường đều là `env\_human = 1`

Dù dữ liệu lấy từ Luật Bảo vệ môi trường 2020, không phải mọi bản ghi đều tạo tác động môi trường trực tiếp. Có thể có bản ghi chỉ là tiêu đề, định nghĩa, phạm vi điều chỉnh, hiệu lực thi hành, dẫn chiếu hoặc quy định kỹ thuật về trình tự văn bản.

### 3.2. `co\_tac\_dong = true` không đồng nghĩa với `env\_human = 1`

`co\_tac\_dong = true` chỉ cho biết bản ghi có tác động chính sách hoặc pháp lý hay không. Bước này tiếp tục kiểm tra xem tác động đó có liên quan đến môi trường hay không.

### 3.3. Phải có bằng chứng trực tiếp trong văn bản

Chỉ gán `env\_human = 1` khi trong `raw\_text` có căn cứ rõ ràng, ví dụ:

```
môi trường
bảo vệ môi trường
nước thải
khí thải
chất thải
chất thải nguy hại
đánh giá tác động môi trường
giấy phép môi trường
đăng ký môi trường
quan trắc môi trường
ô nhiễm
sự cố môi trường
đa dạng sinh học
di sản thiên nhiên
biến đổi khí hậu
khí nhà kính
tầng ô-dôn
quy chuẩn kỹ thuật môi trường
```

Nếu không tìm được cụm từ chứa bằng chứng trực tiếp thì không nên gán `env\_human = 1` chỉ vì bản ghi nằm trong Luật Bảo vệ môi trường.

### 3.4. Trường hợp mơ hồ phải đánh dấu review

Nếu bản ghi có yếu tố môi trường nhưng chưa rõ có nên giữ lại hay không, gán nhãn theo căn cứ tốt nhất và đặt:

```
env\_needs\_review = TRUE
```

Không được biến một nhãn chưa chắc chắn thành nhãn chắc chắn.

\---

## 4\. Định nghĩa `env\_human = 1`

Gán `env\_human = 1` nếu bản ghi thuộc ít nhất một nhóm sau.

### 4.1. Kiểm soát ô nhiễm, phát thải, xả thải

Gán `env\_human = 1` nếu bản ghi quy định về:

* xả nước thải;
* xả khí thải;
* phát thải bụi, tiếng ồn, độ rung, ánh sáng, bức xạ;
* phát tán chất độc hại;
* kiểm soát ô nhiễm môi trường;
* giới hạn, ngưỡng hoặc quy chuẩn kỹ thuật môi trường;
* xử lý ô nhiễm trước khi thải ra môi trường.

**Lý do ghi:** Bản ghi quy định kiểm soát phát thải/xả thải hoặc giới hạn ô nhiễm, tác động trực tiếp đến chất lượng môi trường.

### 4.2. Quản lý chất thải

Gán `env\_human = 1` nếu bản ghi quy định về:

* chất thải rắn sinh hoạt;
* chất thải rắn công nghiệp;
* chất thải nguy hại;
* thu gom, phân loại, lưu giữ, vận chuyển, xử lý chất thải;
* tái chế, tái sử dụng, thu hồi chất thải;
* nhập khẩu phế liệu hoặc kiểm soát chất thải từ nước ngoài.

**Lý do ghi:** Bản ghi điều chỉnh hoạt động quản lý chất thải, có tác động trực tiếp đến phòng ngừa và kiểm soát ô nhiễm.

### 4.3. Đánh giá tác động môi trường, giấy phép môi trường, đăng ký môi trường

Gán `env\_human = 1` nếu bản ghi quy định về:

* đánh giá môi trường chiến lược;
* đánh giá tác động môi trường;
* giấy phép môi trường;
* đăng ký môi trường;
* thẩm định, phê duyệt, cấp, điều chỉnh, thu hồi giấy phép môi trường;
* miễn giấy phép hoặc miễn đăng ký môi trường.

**Lý do ghi:** Bản ghi quy định thủ tục môi trường bắt buộc hoặc điều kiện pháp lý để kiểm soát tác động môi trường của dự án/cơ sở.

### 4.4. Quan trắc, giám sát, báo cáo và thông tin môi trường

Gán `env\_human = 1` nếu bản ghi quy định về:

* quan trắc môi trường;
* giám sát môi trường;
* báo cáo môi trường;
* hệ thống thông tin, cơ sở dữ liệu môi trường;
* công khai thông tin môi trường;
* kiểm tra, thanh tra về bảo vệ môi trường.

**Lý do ghi:** Bản ghi thiết lập cơ chế theo dõi, giám sát hoặc báo cáo thông tin môi trường, giúp kiểm soát tác động môi trường.

### 4.5. Phòng ngừa, ứng phó, khắc phục và phục hồi môi trường

Gán `env\_human = 1` nếu bản ghi quy định về:

* phòng ngừa sự cố môi trường;
* ứng phó sự cố môi trường;
* khắc phục ô nhiễm;
* phục hồi môi trường;
* cải tạo phục hồi môi trường sau khai thác;
* bồi thường thiệt hại môi trường;
* xử lý khu vực ô nhiễm.

**Lý do ghi:** Bản ghi quy định trách nhiệm phòng ngừa, khắc phục hoặc phục hồi môi trường sau ô nhiễm/sự cố.

### 4.6. Tài nguyên nước, đất, không khí, biển và tài nguyên thiên nhiên

Gán `env\_human = 1` nếu bản ghi quy định về:

* bảo vệ nguồn nước;
* chất lượng nước;
* môi trường đất;
* môi trường không khí;
* môi trường biển;
* khai thác tài nguyên gắn với yêu cầu bảo vệ môi trường;
* bảo vệ cảnh quan, hệ sinh thái tự nhiên.

**Lý do ghi:** Bản ghi liên quan đến bảo vệ hoặc kiểm soát tác động lên tài nguyên và thành phần môi trường.

### 4.7. Đa dạng sinh học, di sản thiên nhiên, hệ sinh thái

Gán `env\_human = 1` nếu bản ghi quy định về:

* đa dạng sinh học;
* loài nguy cấp, quý, hiếm;
* hệ sinh thái tự nhiên;
* di sản thiên nhiên;
* khu bảo tồn;
* hành vi phá hoại hoặc xâm chiếm di sản thiên nhiên.

**Lý do ghi:** Bản ghi chứa nội dung có tác động đến đa dạng sinh học, hệ sinh thái hoặc di sản thiên nhiên.

### 4.8. Biến đổi khí hậu, khí nhà kính, tầng ô-dôn

Gán `env\_human = 1` nếu bản ghi quy định về:

* phát thải khí nhà kính;
* kiểm kê khí nhà kính;
* hạn ngạch phát thải;
* tín chỉ các-bon;
* thích ứng với biến đổi khí hậu;
* giảm nhẹ biến đổi khí hậu;
* bảo vệ tầng ô-dôn;
* kiểm soát chất làm suy giảm tầng ô-dôn.

**Lý do ghi:** Bản ghi liên quan đến biến đổi khí hậu, phát thải khí nhà kính hoặc bảo vệ tầng ô-dôn.

### 4.9. Công cụ kinh tế, tài chính môi trường

Gán `env\_human = 1` nếu bản ghi quy định về:

* phí bảo vệ môi trường;
* ký quỹ cải tạo, phục hồi môi trường;
* bồi thường thiệt hại môi trường;
* quỹ bảo vệ môi trường;
* chi trả dịch vụ hệ sinh thái;
* ưu đãi, hỗ trợ cho hoạt động bảo vệ môi trường;
* trách nhiệm tài chính gắn trực tiếp với ô nhiễm hoặc bảo vệ môi trường.

**Lý do ghi:** Bản ghi thiết lập công cụ tài chính hoặc nghĩa vụ tài chính nhằm bảo vệ, khắc phục hoặc cải thiện môi trường.

### 4.10. Quản lý nhà nước về bảo vệ môi trường

Gán `env\_human = 1` nếu bản ghi phân công nhiệm vụ cụ thể liên quan đến:

* bảo vệ môi trường;
* quản lý chất thải;
* kiểm soát ô nhiễm;
* cấp phép môi trường;
* quan trắc môi trường;
* thanh tra, kiểm tra môi trường;
* xây dựng hạ tầng môi trường;
* tổ chức thực hiện chính sách bảo vệ môi trường.

**Lý do ghi:** Bản ghi phân công trách nhiệm quản lý nhà nước cụ thể trong lĩnh vực bảo vệ môi trường.

> \*\*Lưu ý:\*\* Nếu điều khoản chỉ nói chung "cơ quan có thẩm quyền thực hiện theo quy định của pháp luật" mà không có nội dung môi trường cụ thể thì nên gán `env\_human = 0` hoặc đánh dấu `env\_needs\_review = TRUE`.

\---

## 5\. Định nghĩa `env\_human = 0`

Gán `env\_human = 0` nếu bản ghi không chứa tác động môi trường trực tiếp hoặc không đủ bằng chứng để giữ lại.

### 5.1. Tiêu đề, tên chương, tên mục, tên điều

Ví dụ:

```
Chương I. Quy định chung
Điều 1. Phạm vi điều chỉnh
Mục 2. Giấy phép môi trường
```

**Lý do ghi:** Bản ghi là tiêu đề hoặc nhãn cấu trúc, không tạo tác động môi trường độc lập.

### 5.2. Phạm vi điều chỉnh, đối tượng áp dụng, giải thích từ ngữ

Gán `env\_human = 0` nếu bản ghi chỉ định nghĩa thuật ngữ hoặc mô tả phạm vi chung mà không tạo nghĩa vụ, quyền, điều kiện hoặc công cụ môi trường cụ thể.

**Lý do ghi:** Bản ghi chỉ nêu phạm vi/định nghĩa chung, chưa tạo tác động môi trường cụ thể.

> \*\*Lưu ý:\*\* Nếu định nghĩa chứa ngưỡng kỹ thuật, tiêu chuẩn, thành phần môi trường hoặc cơ chế môi trường có thể ảnh hưởng đến bước sau, đánh dấu `env\_needs\_review = TRUE`.

### 5.3. Dẫn chiếu thuần túy

Ví dụ:

```
Thực hiện theo quy định tại khoản 2 Điều này.
Chính phủ quy định chi tiết điều này.
```

**Lý do ghi:** Bản ghi chỉ dẫn chiếu hoặc giao quy định chi tiết, không chứa nội dung môi trường cụ thể.

### 5.4. Hiệu lực thi hành, điều khoản chuyển tiếp, kỹ thuật văn bản

Ví dụ:

```
Luật này có hiệu lực thi hành từ ngày...
Các văn bản trước đây hết hiệu lực kể từ ngày...
```

**Lý do ghi:** Bản ghi thuộc nhóm hiệu lực/chuyển tiếp/kỹ thuật văn bản, không tạo tác động môi trường trực tiếp.

### 5.5. Thẩm quyền hoặc thủ tục hành chính chung không gắn với nội dung môi trường cụ thể

Gán `env\_human = 0` nếu điều khoản chỉ nói về thẩm quyền, trình tự, hồ sơ, thời hạn hoặc cơ quan xử lý nhưng không nêu rõ đối tượng môi trường, giấy phép môi trường, báo cáo môi trường, chất thải, phát thải hoặc yêu cầu bảo vệ môi trường.

**Lý do ghi:** Bản ghi chỉ quy định thủ tục/thẩm quyền chung, không có nội dung môi trường cụ thể.

### 5.6. Quy định kinh tế - xã hội chung không có yếu tố môi trường rõ ràng

Ví dụ:

* phát triển kinh tế chung;
* hỗ trợ doanh nghiệp chung;
* đầu tư công chung;
* quản lý ngân sách chung;
* đào tạo, tuyên truyền chung không gắn với bảo vệ môi trường.

**Lý do ghi:** Bản ghi có tác động chính sách nhưng không có căn cứ trực tiếp về tác động môi trường.

\---

## 6\. Danh mục domain môi trường nên dùng

Khi `env\_human = 1`, chọn một hoặc nhiều domain sau:

|Domain|Khi nào dùng|
|-|-|
|`water`|Nước thải, tài nguyên nước, chất lượng nước, nguồn tiếp nhận|
|`air\_noise\_radiation`|Khí thải, bụi, tiếng ồn, độ rung, ánh sáng, bức xạ, mùi|
|`soil`|Ô nhiễm đất, phục hồi đất, cải tạo môi trường đất|
|`waste`|Chất thải rắn, thu gom, phân loại, xử lý, tái chế|
|`hazardous\_waste`|Chất thải nguy hại, hóa chất độc hại, chất ô nhiễm khó phân hủy|
|`biodiversity\_natural\_heritage`|Đa dạng sinh học, hệ sinh thái, di sản thiên nhiên|
|`climate\_ozone\_carbon`|Khí nhà kính, biến đổi khí hậu, tầng ô-dôn, tín chỉ các-bon|
|`eia\_permit\_registration`|ĐTM, giấy phép môi trường, đăng ký môi trường|
|`monitoring\_reporting`|Quan trắc, giám sát, báo cáo, cơ sở dữ liệu môi trường|
|`pollution\_control\_remediation`|Kiểm soát ô nhiễm, sự cố môi trường, khắc phục, phục hồi|
|`environmental\_finance`|Phí, ký quỹ, quỹ BVMT, bồi thường, ưu đãi/hỗ trợ môi trường|
|`circular\_economy`|Kinh tế tuần hoàn, tái sử dụng, tái chế, giảm chất thải|
|`planning\_state\_management`|Quy hoạch, phân công trách nhiệm, quản lý nhà nước về BVMT|
|`technical\_standard\_threshold`|Quy chuẩn, tiêu chuẩn, ngưỡng kỹ thuật, giới hạn môi trường|
|`other`|Có tác động môi trường nhưng chưa thuộc nhóm trên|

Không dùng domain quá dài hoặc trích nguyên câu làm domain. Domain phải là nhóm phân tích ổn định để phục vụ trực quan hóa sau này.

\---

## 7\. Quy trình gán nhãn cho từng bản ghi

Với mỗi bản ghi, thực hiện theo 6 bước:

1. Đọc `legal\_citation` và `raw\_text`.
2. Tìm bằng chứng môi trường trong nội dung bản ghi.
3. Xác định bản ghi thuộc nhóm tác động nào: chất thải, phát thải, giấy phép, quan trắc, phục hồi, khí hậu, tài chính môi trường, quản lý nhà nước về môi trường.
4. Gán `env\_human`.
5. Điền `env\_domain\_human`.
6. Ghi `env\_evidence\_span` và `env\_human\_reason`.

Không để trống `env\_evidence\_span` nếu `env\_human = 1`. Nếu `env\_human = 0`, phải ghi lý do vì sao bản ghi không được giữ lại.

\---

## 8\. Các lý do thường gặp khi gán `env\_human = 1`

Có thể dùng các lý do sau, tùy chỉnh theo từng bản ghi:

|Nhóm|Lý do|
|-|-|
|Nước thải/nước|Bản ghi quy định về thu gom, xử lý hoặc xả nước thải, tác động trực tiếp đến chất lượng nước.|
|Khí thải/không khí|Bản ghi quy định về kiểm soát khí thải, bụi, tiếng ồn hoặc các yếu tố ảnh hưởng đến môi trường không khí.|
|Chất thải|Bản ghi quy định phân loại, thu gom, vận chuyển, xử lý hoặc tái chế chất thải.|
|Chất thải nguy hại|Bản ghi điều chỉnh chất thải nguy hại/chất độc hại, có rủi ro môi trường cao.|
|ĐTM/giấy phép/đăng ký|Bản ghi quy định thủ tục pháp lý nhằm kiểm soát tác động môi trường của dự án/cơ sở.|
|Quan trắc/báo cáo|Bản ghi quy định quan trắc, giám sát, báo cáo hoặc công khai thông tin môi trường.|
|Ô nhiễm/sự cố|Bản ghi quy định phòng ngừa, ứng phó, khắc phục ô nhiễm hoặc sự cố môi trường.|
|Tài chính môi trường|Bản ghi quy định phí, ký quỹ, bồi thường, hỗ trợ hoặc công cụ tài chính gắn với bảo vệ môi trường.|
|Đa dạng sinh học|Bản ghi liên quan đến bảo vệ hệ sinh thái, loài, khu bảo tồn hoặc di sản thiên nhiên.|
|Khí hậu/tầng ô-dôn|Bản ghi liên quan đến khí nhà kính, biến đổi khí hậu, tín chỉ các-bon hoặc tầng ô-dôn.|
|Quy chuẩn/ngưỡng|Bản ghi đặt ra quy chuẩn, tiêu chuẩn hoặc giới hạn kỹ thuật môi trường.|
|Quản lý nhà nước|Bản ghi phân công trách nhiệm cụ thể trong quản lý, kiểm tra hoặc tổ chức thực hiện bảo vệ môi trường.|

\---

## 9\. Các lý do thường gặp khi gán `env\_human = 0`

Có thể dùng các mẫu lý do sau:

|Nhóm lý do|Mẫu lý do|
|-|-|
|Tiêu đề/cấu trúc|Bản ghi chỉ là tiêu đề hoặc thành phần cấu trúc, không tạo tác động môi trường độc lập.|
|Định nghĩa chung|Bản ghi chỉ giải thích thuật ngữ, chưa tạo nghĩa vụ, quyền, điều kiện hoặc công cụ môi trường cụ thể.|
|Phạm vi/đối tượng chung|Bản ghi chỉ nêu phạm vi hoặc đối tượng áp dụng, chưa có nội dung môi trường cụ thể cần xử lý.|
|Dẫn chiếu|Bản ghi chỉ dẫn chiếu sang điều/khoản khác, không có nội dung môi trường độc lập.|
|Hiệu lực/chuyển tiếp|Bản ghi chỉ quy định hiệu lực, chuyển tiếp hoặc kỹ thuật văn bản.|
|Thủ tục hành chính chung|Bản ghi chỉ nêu trình tự, thẩm quyền hoặc hồ sơ chung, không gắn với yêu cầu môi trường cụ thể.|
|Chính sách chung|Bản ghi nêu định hướng phát triển hoặc quản lý chung nhưng không có bằng chứng trực tiếp về môi trường.|
|Không đủ căn cứ|Không tìm thấy bằng chứng trực tiếp trong `raw\_text` để xác định tác động môi trường.|

\---

## 10\. Quy tắc xử lý trường hợp dễ nhầm

### 10.1. Có từ "bền vững"

* Nếu chỉ nói "phát triển bền vững" chung chung: `env\_human = 0` hoặc `env\_needs\_review = TRUE`.
* Nếu có thêm bảo vệ môi trường, giảm phát thải, tài nguyên, chất thải: `env\_human = 1`.

### 10.2. Có từ "đầu tư"

* Đầu tư chung: `env\_human = 0`.
* Đầu tư công trình xử lý nước thải, chất thải, hạ tầng bảo vệ môi trường: `env\_human = 1`.

### 10.3. Có từ "quy hoạch"

* Quy hoạch chung không có nội dung môi trường: `env\_human = 0`.
* Quy hoạch bảo vệ môi trường, phân vùng môi trường, hạ tầng xử lý môi trường: `env\_human = 1`.

### 10.4. Có từ "báo cáo"

* Báo cáo hành chính chung: `env\_human = 0`.
* Báo cáo môi trường, báo cáo quan trắc, báo cáo ĐTM, báo cáo chất thải: `env\_human = 1`.

### 10.5. Có từ "giấy phép"

* Giấy phép chung không liên quan môi trường: `env\_human = 0`.
* Giấy phép môi trường: `env\_human = 1`.

### 10.6. Có số liệu

Có số không tự động làm bản ghi có tác động môi trường.

* Số là thời hạn, số điều, số khoản, ngày hiệu lực: thường `env\_human = 0`, trừ khi gắn với nghĩa vụ môi trường.
* Số là ngưỡng phát thải, tỷ lệ thu gom, mức phí bảo vệ môi trường, hạn ngạch phát thải: thường `env\_human = 1`.

\---

## 11\. Ví dụ `env\_human = 1`

### Ví dụ 1 — Nước thải

```text
Cơ sở sản xuất, kinh doanh, dịch vụ phải xử lý nước thải đạt quy chuẩn kỹ thuật môi trường trước khi xả vào nguồn tiếp nhận.
```

* `env\_human = 1`
* `env\_domain\_human = water; technical\_standard\_threshold`
* `env\_evidence\_span = xử lý nước thải đạt quy chuẩn kỹ thuật môi trường`
* `env\_human\_reason = Bản ghi quy định nghĩa vụ xử lý nước thải, tác động trực tiếp đến chất lượng nước.`

### Ví dụ 2 — Chất thải nguy hại

```text
Chủ nguồn thải chất thải nguy hại có trách nhiệm phân định, phân loại, lưu giữ và chuyển giao chất thải nguy hại theo quy định.
```

* `env\_human = 1`
* `env\_domain\_human = hazardous\_waste; waste`
* `env\_evidence\_span = phân loại, lưu giữ và chuyển giao chất thải nguy hại`
* `env\_human\_reason = Bản ghi điều chỉnh quản lý chất thải nguy hại, có rủi ro môi trường cao.`

### Ví dụ 3 — Giấy phép môi trường

```text
Dự án đầu tư có phát sinh nước thải, bụi, khí thải xả ra môi trường phải có giấy phép môi trường.
```

* `env\_human = 1`
* `env\_domain\_human = eia\_permit\_registration; water; air\_noise\_radiation`
* `env\_evidence\_span = phát sinh nước thải, bụi, khí thải xả ra môi trường; phải có giấy phép môi trường`
* `env\_human\_reason = Bản ghi quy định thủ tục giấy phép môi trường để kiểm soát tác động của dự án.`

### Ví dụ 4 — Quan trắc

```text
Cơ sở sản xuất, kinh doanh, dịch vụ phải thực hiện quan trắc môi trường định kỳ và gửi báo cáo cho cơ quan có thẩm quyền.
```

* `env\_human = 1`
* `env\_domain\_human = monitoring\_reporting`
* `env\_evidence\_span = quan trắc môi trường định kỳ`
* `env\_human\_reason = Bản ghi quy định hoạt động quan trắc và báo cáo môi trường.`

### Ví dụ 5 — Khí hậu

```text
Cơ sở thuộc danh mục phải kiểm kê khí nhà kính có trách nhiệm thực hiện kiểm kê khí nhà kính theo quy định.
```

* `env\_human = 1`
* `env\_domain\_human = climate\_ozone\_carbon`
* `env\_evidence\_span = kiểm kê khí nhà kính`
* `env\_human\_reason = Bản ghi liên quan đến quản lý phát thải khí nhà kính.`

\---

## 12\. Ví dụ `env\_human = 0`

### Ví dụ 1 — Hiệu lực

```text
Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2022.
```

* `env\_human = 0`
* `env\_domain\_human =`
* `env\_evidence\_span =`
* `env\_human\_reason = Bản ghi chỉ quy định hiệu lực thi hành, không tạo tác động môi trường trực tiếp.`

### Ví dụ 2 — Dẫn chiếu

```text
Chính phủ quy định chi tiết khoản này.
```

* `env\_human = 0`
* `env\_human\_reason = Bản ghi chỉ giao quy định chi tiết, không chứa nội dung môi trường độc lập.`

### Ví dụ 3 — Tiêu đề

```text
Điều 39. Đối tượng phải có giấy phép môi trường.
```

* `env\_human = 0`
* `env\_human\_reason = Bản ghi chỉ là tiêu đề điều, không tạo tác động môi trường độc lập.`

> \*\*Lưu ý:\*\* Nếu bản ghi chứa nội dung cụ thể bên dưới tiêu đề về giấy phép môi trường, bản ghi đó có thể là `env\_human = 1`.

### Ví dụ 4 — Định nghĩa chung

```text
Trong Luật này, các từ ngữ dưới đây được hiểu như sau...
```

* `env\_human = 0`
* `env\_needs\_review = TRUE` nếu định nghĩa chứa thuật ngữ môi trường quan trọng
* `env\_human\_reason = Bản ghi chỉ mở đầu phần giải thích từ ngữ, chưa tạo tác động môi trường cụ thể.`

### Ví dụ 5 — Thủ tục chung

```text
Hồ sơ được gửi đến cơ quan có thẩm quyền theo hình thức trực tiếp hoặc trực tuyến.
```

* `env\_human = 0`
* `env\_human\_reason = Bản ghi chỉ quy định cách thức nộp hồ sơ, không có nội dung môi trường cụ thể.`

\---

## 13\. Quy tắc review sau khi gán

Cần review lại các bản ghi có một trong các điều kiện sau:

```
env\_needs\_review = TRUE
env\_human ≠ env\_llm
LLM confidence thấp
không có evidence\_span
domain không rõ
bản ghi quá dài, chứa nhiều nghĩa vụ
bản ghi có nhiều chủ thể
```

> \*\*Lưu ý về dẫn chiếu:\*\* Mục 5.3 quy định bản ghi chỉ dẫn chiếu thuần túy → `env\_human = 0`. Trường hợp ngoại lệ: nếu bản ghi dẫn chiếu đến một điều khoản môi trường và bản thân nó đặt thêm nghĩa vụ/điều kiện môi trường mới, không chỉ lặp lại dẫn chiếu, thì có thể xem xét `env\_human = 1` và đặt `env\_needs\_review = TRUE` để kiểm tra lại.

Khi review:

1. Đọc lại `raw\_text`.
2. Kiểm tra `env\_evidence\_span`.
3. So với định nghĩa trong guideline.
4. Nếu sửa nhãn, ghi rõ lý do trong `review\_note`.
5. Không dùng nhãn đã sửa sau review để tính lại metric LLM ban đầu, trừ khi bạn tuyên bố rõ rằng đang tạo lại phiên bản human reference mới.

\---

## 14\. Quy tắc chất lượng dữ liệu

Trước khi dùng `env\_human` để tính metric hoặc tạo `env\_final`, kiểm tra:

```
Không có bản ghi thiếu env\_human.
Nếu env\_human = 1 thì nên có env\_domain\_human.
Nếu env\_human = 1 thì bắt buộc có env\_evidence\_span.
Nếu env\_human = 0 thì phải có env\_human\_reason.
Các bản ghi needs\_review phải được đọc lại trước khi chốt env\_final.
Không trộn domain với evidence\_span.
Không dùng câu quá dài làm domain.
```

\---

## 15\. Kết luận — Quy tắc quyết định ngắn gọn

> \*\*Gán `env\_human = 1`\*\* nếu bản ghi có bằng chứng trực tiếp về môi trường, chất thải, phát thải, ô nhiễm, ĐTM, giấy phép môi trường, quan trắc, phục hồi, đa dạng sinh học, khí hậu hoặc tài chính môi trường.
>
> \*\*Gán `env\_human = 0`\*\* nếu bản ghi chỉ là tiêu đề, định nghĩa, phạm vi chung, dẫn chiếu, hiệu lực, thủ tục chung hoặc không có căn cứ trực tiếp về tác động môi trường.
>
> \*\*Nếu mơ hồ:\*\* gán theo căn cứ tốt nhất, ghi evidence, ghi reason và đặt `env\_needs\_review = TRUE`.

