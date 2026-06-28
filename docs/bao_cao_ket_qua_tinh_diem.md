# Báo cáo kết quả tính điểm tác động

**Tên file:** `bao\\\\\\\_cao\\\\\\\_ket\\\\\\\_qua\\\\\\\_tinh\\\\\\\_diem.md`  
**Nguồn dữ liệu:** `scored\\\\\\\_dataset.xlsx`, `scoring\\\\\\\_summary.xlsx`, `final\\\\\\\_impact\\\\\\\_report.xlsx`  
**Bước pipeline:** Bước 11 — Validate điểm chấm và tính Impact Score  
**Ngày tổng hợp:** 25/06/2026

\---

## 1\. Mục đích của báo cáo

Báo cáo này diễn giải kết quả sau khi đã chấm các biến `M\\\\\\\_i`, `S\\\\\\\_i`, `D\\\\\\\_i`, `R\\\\\\\_i`, `W\\\\\\\_i` và tính `ImpactScore\\\\\\\_i` cho từng bản ghi đã có nhãn cuối cùng.

Kết quả cần được hiểu là **điểm bán định lượng**, không phải giá trị tiền tệ tuyệt đối của chi phí hoặc lợi ích. Điểm này dùng để trả lời các câu hỏi:

* Điều khoản nào tạo tác động mạnh hơn?
* Tác động chủ yếu nằm ở nhóm nhãn nào?
* Domain môi trường nào chịu mức ràng buộc/chi phí/lợi ích lớn nhất?
* Nhóm chủ thể nào chịu tác động nhiều nhất?
* Kết quả có thể giải thích được bằng `final\\\\\\\_label`, `actor\\\\\\\_group`, `domain\\\\\\\_primary`, `M\\\\\\\_i`, `S\\\\\\\_i`, `D\\\\\\\_i`, `R\\\\\\\_i`, `W\\\\\\\_i` hay không?

\---

## 2\. Công thức

Mỗi bản ghi `i` được tính theo công thức:

`
C\_i = alpha\*M\_i + beta\*S\_i + gamma\*D\_i + delta\*R\_i
C\_i\_norm = (C\_i - 1) / 4
ImpactScore\_i = direction\_i \* W\_i \* C\_i\_norm

```

Trong phạm vi đồ án:


alpha = beta = gamma = delta = 0.25
W\\\\\\\_i = 1.0 cho toàn bộ bản ghi
```

Chiều tác động được xác định theo `final\\\\\\\_label`:

|Nhóm nhãn|direction\_i|Cách hiểu|
|-|-:|-|
|`BENEFIT\\\\\\\_QUANTITATIVE`, `BENEFIT\\\\\\\_QUALITATIVE`|+1|Tạo lợi ích|
|`COST\\\\\\\_QUANTITATIVE`, `COST\\\\\\\_QUALITATIVE`, `CONSTRAINT`|-1|Tạo chi phí tuân thủ, gánh nặng thực hiện hoặc ràng buộc|

Vì vậy, điểm âm **không có nghĩa là điều khoản xấu**. Trong pháp luật về môi trường, nhiều điều khoản được xác định là tiêu cực vì luật thường đặt ra nghĩa vụ, điều kiện và lệnh cấm để kiểm soát ô nhiễm và bảo vệ môi trường.

\---

## 3\. Tổng quan kết quả toàn bộ dataset

|Chỉ số|Giá trị|Diễn giải|
|-|-:|-|
|Số bản ghi|581|Tổng số bản ghi được tính điểm|
|TotalImpact|-362.5000|Tổng điểm tác động của toàn bộ văn bản|
|MeanImpact|-0.6239|Điểm tác động trung bình mỗi bản ghi|
|StdImpact|0.2356|Mức phân tán điểm|
|MaxImpact|0.8125|Điểm lợi ích cao nhất|
|MinImpact|-0.9375|Điểm chi phí/ràng buộc mạnh nhất|

### Diễn giải

Tổng điểm `TotalImpact = -362.5000` và điểm trung bình `MeanImpact = -0.6239` cho thấy tập điều khoản sau khi lọc chủ yếu là các quy định tạo **nghĩa vụ tuân thủ** và **ràng buộc pháp lý/kỹ thuật**. Đây là kết quả hợp lý đối với Luật Bảo vệ môi trường, vì văn bản này chủ yếu điều chỉnh hành vi, phân công trách nhiệm, đặt điều kiện, yêu cầu thủ tục và kiểm soát rủi ro môi trường.

Điểm âm lớn không nên được diễn giải là “tác động xã hội tiêu cực” mà là luật tạo ra mức độ can thiệp quản lý đáng kể lên các chủ thể chịu điều chỉnh, đặc biệt ở các lĩnh vực nước, chất thải, chất thải nguy hại, giấy phép môi trường và kiểm soát ô nhiễm.

\---

## 4\. Phân bố mức độ tác động

|Mức tác động|Số bản ghi|Tỷ lệ (%)|
|-|-:|-:|
|Chi phí/ràng buộc cao `\\\\\\\[-1.0, -0.7]`|188|32.36|
|Chi phí/ràng buộc trung bình `(-0.7, -0.3)`|378|65.06|
|Lợi ích trung bình `(0.3, 0.7)`|12|2.07|
|Lợi ích cao `\\\\\\\[0.7, 1.0]`|3|0.52|

### Diễn giải

Có 566 bản ghi có điểm âm, chiếm 97.42% tổng số bản ghi. Điều này phản ánh cấu trúc của văn bản pháp luật môi trường: đa số điều khoản không trực tiếp trao lợi ích, mà đặt ra trách nhiệm, điều kiện, thủ tục, tiêu chuẩn và nghĩa vụ thực hiện.

Có 15 bản ghi có điểm dương, chiếm 2.58%. Các bản ghi này thuộc nhóm `BENEFIT\\\\\\\_QUALITATIVE`, thường liên quan đến khuyến khích, hỗ trợ, cải thiện quản lý, tái chế, xử lý chất thải hoặc bảo vệ môi trường ở khu vực nông thôn/làng nghề.

\---

## 5\. Kết quả theo nhãn tác động

|Nhãn cuối cùng|Số bản ghi|Tỷ lệ (%)|Điểm TB|Tổng điểm|
|-|-:|-:|-:|-:|
|BENEFIT\_QUALITATIVE|15|2.5800|0.6625|9.9375|
|CONSTRAINT|122|21.0000|-0.7628|-93.0625|
|COST\_QUALITATIVE|444|76.4200|-0.6292|-279.3750|

### Diễn giải theo nhãn

`COST\\\\\\\_QUALITATIVE` là nhóm chiếm ưu thế với 444 bản ghi và tổng điểm -279.3750. Điều này cho thấy phần lớn quy định tạo ra nghĩa vụ thủ tục, nghĩa vụ thực hiện, báo cáo, đăng ký, quan trắc, quản lý chất thải, vận hành công trình hoặc trách nhiệm quản lý.

`CONSTRAINT` có ít bản ghi hơn nhưng điểm trung bình âm mạnh hơn. Đây là nhóm ràng buộc, điều kiện, lệnh cấm, quy chuẩn, hạn ngạch hoặc yêu cầu kỹ thuật. Điểm trung bình của `CONSTRAINT` là -0.7628, thấp hơn `COST\\\\\\\_QUALITATIVE`, phản ánh tính nghiêm ngặt cao hơn trên mỗi điều khoản.

`BENEFIT\\\\\\\_QUALITATIVE` có 15 bản ghi, tổng điểm dương 9.9375. Nhóm này không đủ lớn để đảo chiều tổng điểm, nhưng cho thấy luật vẫn có các cơ chế khuyến khích, hỗ trợ hoặc cải thiện quản lý môi trường.

Không có bản ghi `BENEFIT\\\\\\\_QUANTITATIVE` và `COST\\\\\\\_QUANTITATIVE` trong kết quả cuối. Điều này phù hợp nếu dữ liệu chủ yếu không chứa mức tiền, đơn giá, tỷ lệ hỗ trợ hoặc lợi ích/chi phí định lượng trực tiếp. Các con số như thời hạn hành chính, số điều/khoản hoặc mã quy chuẩn không được xem là chi phí/lợi ích định lượng trực tiếp.

\---

## 6\. Kết quả theo domain môi trường

|Domain chính|Số bản ghi|Tỷ lệ (%)|Điểm TB|Tổng điểm|
|-|-:|-:|-:|-:|
|water|153|26.3300|-0.6520|-99.7500|
|hazardous\_substances|112|19.2800|-0.7193|-80.5625|
|waste|111|19.1000|-0.5755|-63.8750|
|eia\_permit\_registration|93|16.0100|-0.5504|-51.1875|
|air\_noise\_radiation|22|3.7900|-0.6619|-14.5625|
|planning\_state\_management|23|3.9600|-0.5734|-13.1875|
|general\_environment|24|4.1300|-0.4896|-11.7500|
|pollution\_control\_remediation|14|2.4100|-0.6473|-9.0625|
|biodiversity\_natural\_heritage|11|1.8900|-0.7614|-8.3750|
|technical\_standard\_threshold|5|0.8600|-0.7000|-3.5000|
|climate\_carbon|4|0.6900|-0.8438|-3.3750|
|monitoring\_reporting|5|0.8600|-0.4625|-2.3125|
|environmental\_finance|4|0.6900|-0.2500|-1.0000|

### 6.1. Các domain đóng góp tác động lớn nhất

Bốn domain có tổng điểm âm lớn nhất là:

1. `water`: 153 bản ghi, tổng điểm -99.7500.
2. `hazardous\\\\\\\_substances`: 112 bản ghi, tổng điểm -80.5625.
3. `waste`: 111 bản ghi, tổng điểm -63.8750.
4. `eia\\\\\\\_permit\\\\\\\_registration`: 93 bản ghi, tổng điểm -51.1875.

Điều này cho thấy trọng tâm tác động của hệ thống nằm ở kiểm soát môi trường nước, quản lý chất thải/chất thải nguy hại và công cụ hành chính như ĐTM, giấy phép, đăng ký môi trường.

### 6.2. Domain có điểm trung bình mạnh

Một số domain có số lượng bản ghi không lớn nhưng điểm trung bình rất mạnh:

* `climate\\\\\\\_carbon`: mean = -0.8438.
* `biodiversity\\\\\\\_natural\\\\\\\_heritage`: mean = -0.7614.
* `hazardous\\\\\\\_substances`: mean = -0.7193.

Các domain này có rủi ro môi trường cao, phạm vi dài hạn hoặc khả năng phục hồi thấp. Vì vậy, dù số lượng bản ghi ít hơn `water` hoặc `waste`, tác động trung bình trên mỗi bản ghi lại mạnh hơn.

\---

## 7\. Kết quả theo nhóm chủ thể chịu tác động

|Nhóm chủ thể|Số bản ghi|Tỷ lệ (%)|Điểm TB|Tổng điểm|
|-|-:|-:|-:|-:|
|GENERAL\_ORGANIZATION\_INDIVIDUAL|193|33.2200|-0.6580|-127.0000|
|STATE\_AGENCY|179|30.8100|-0.6383|-114.2500|
|PROJECT\_OWNER\_INFRASTRUCTURE|102|17.5600|-0.5778|-58.9375|
|BUSINESS\_FACILITY|87|14.9700|-0.5999|-52.1875|
|COMMUNITY\_CRAFT\_VILLAGE|20|3.4400|-0.5062|-10.1250|

### Diễn giải theo actor

`GENERAL\\\\\\\_ORGANIZATION\\\\\\\_INDIVIDUAL` có tổng điểm âm lớn nhất. Điều này phản ánh nhiều điều khoản áp dụng rộng cho tổ chức, cá nhân, hộ gia đình hoặc nhóm chủ thể chung, ví dụ nghĩa vụ không gây ô nhiễm, quản lý chất thải, không vi phạm quy chuẩn hoặc thực hiện trách nhiệm bảo vệ môi trường.

`STATE\\\\\\\_AGENCY` có tổng điểm âm lớn thứ hai. Đây không phải là “chi phí doanh nghiệp”, mà là gánh nặng quản lý nhà nước: lập quy hoạch, xây dựng kế hoạch, tổ chức quan trắc, thẩm định, cấp phép, công bố thông tin, kiểm tra và xử lý ô nhiễm.

`PROJECT\\\\\\\_OWNER\\\\\\\_INFRASTRUCTURE` và `BUSINESS\\\\\\\_FACILITY` chịu tác động trực tiếp từ các nghĩa vụ tuân thủ như ĐTM, giấy phép môi trường, xử lý chất thải, vận hành công trình bảo vệ môi trường, đáp ứng quy chuẩn và điều kiện kỹ thuật.

`COMMUNITY\\\\\\\_CRAFT\\\\\\\_VILLAGE` có tổng điểm thấp hơn do số lượng bản ghi ít hơn, nhưng vẫn là nhóm quan trọng trong các quy định về bảo vệ môi trường nông thôn, làng nghề, phân loại, thu gom, xử lý chất thải và giữ gìn vệ sinh môi trường.

\---

## 8\. Các bản ghi có tác động dương cao nhất

|Mã|Trích dẫn|Nhãn|Actor|Domain|M\_i|S\_i|D\_i|R\_i|ImpactScore|
|-|-|-|-|-|-:|-:|-:|-:|-:|
|1.58.2.0|Điều 58, Khoản 2|BENEFIT\_QUALITATIVE|STATE\_AGENCY|water|4|5|4|4|0.8125|
|1.75.2.0|Điều 75, Khoản 2|BENEFIT\_QUALITATIVE|STATE\_AGENCY|hazardous\_substances|3|5|4|5|0.8125|
|1.84.3.c|Điều 84, Khoản 3, Điểm c|BENEFIT\_QUALITATIVE|GENERAL\_ORGANIZATION\_INDIVIDUAL|hazardous\_substances|4|4|4|5|0.8125|
|1.58.1.b|Điều 58, Khoản 1, Điểm b|BENEFIT\_QUALITATIVE|GENERAL\_ORGANIZATION\_INDIVIDUAL|water|3|4|4|4|0.6875|
|1.75.4.0|Điều 75, Khoản 4|BENEFIT\_QUALITATIVE|BUSINESS\_FACILITY|hazardous\_substances|3|4|4|4|0.6875|
|1.54.2.b|Điều 54, Khoản 2, Điểm b|BENEFIT\_QUALITATIVE|GENERAL\_ORGANIZATION\_INDIVIDUAL|waste|3|4|3|4|0.6250|
|1.54.2.0|Điều 54, Khoản 2|BENEFIT\_QUALITATIVE|GENERAL\_ORGANIZATION\_INDIVIDUAL|waste|3|4|3|4|0.6250|
|1.58.2.c|Điều 58, Khoản 2, Điểm c|BENEFIT\_QUALITATIVE|STATE\_AGENCY|waste|3|3|4|4|0.6250|

### Diễn giải

Các bản ghi có điểm dương cao chủ yếu thuộc nhóm `BENEFIT\\\\\\\_QUALITATIVE`. Chúng thường liên quan đến:

* chính sách khuyến khích, hỗ trợ;
* cải thiện quản lý môi trường nông thôn;
* phân loại, tái chế, tái sử dụng chất thải;
* áp dụng công nghệ thân thiện môi trường;
* nâng cao hiệu quả quản lý chất thải và chất thải nguy hại.

Điểm dương cao không xuất phát từ giá trị tiền tệ cụ thể, mà từ sự kết hợp của phạm vi tác động rộng (`S\\\\\\\_i` cao), thời gian dài hạn (`D\\\\\\\_i` cao), và domain có rủi ro môi trường đáng kể (`R\\\\\\\_i` cao).

\---

## 9\. Các bản ghi có chi phí/ràng buộc mạnh nhất

|Mã|Trích dẫn|Nhãn|Actor|Domain|M\_i|S\_i|D\_i|R\_i|ImpactScore|
|-|-|-|-|-|-:|-:|-:|-:|-:|
|1.6.11.0|Điều 6, Khoản 11|CONSTRAINT|GENERAL\_ORGANIZATION\_INDIVIDUAL|climate\_carbon|5|5|4|5|-0.9375|
|1.84.3.0|Điều 84, Khoản 3|CONSTRAINT|GENERAL\_ORGANIZATION\_INDIVIDUAL|hazardous\_substances|4|5|4|5|-0.8750|
|1.27.2.0|Điều 27, Khoản 2|COST\_QUALITATIVE|GENERAL\_ORGANIZATION\_INDIVIDUAL|climate\_carbon|4|5|4|5|-0.8750|
|1.84.3.a|Điều 84, Khoản 3, Điểm a|CONSTRAINT|GENERAL\_ORGANIZATION\_INDIVIDUAL|hazardous\_substances|4|5|4|5|-0.8750|
|1.28.7.0|Điều 28, Khoản 7|CONSTRAINT|STATE\_AGENCY|water|4|5|4|5|-0.8750|
|1.47.2.c|Điều 47, Khoản 2, Điểm c|CONSTRAINT|STATE\_AGENCY|hazardous\_substances|4|5|4|5|-0.8750|
|1.53.1.0|Điều 53, Khoản 1|CONSTRAINT|PROJECT\_OWNER\_INFRASTRUCTURE|hazardous\_substances|4|5|4|5|-0.8750|
|1.62.2.0|Điều 62, Khoản 2|CONSTRAINT|GENERAL\_ORGANIZATION\_INDIVIDUAL|hazardous\_substances|5|4|4|5|-0.8750|
|1.47.2.0|Điều 47, Khoản 2|CONSTRAINT|STATE\_AGENCY|hazardous\_substances|4|5|4|5|-0.8750|
|1.41.3.0|Điều 41, Khoản 3|CONSTRAINT|STATE\_AGENCY|hazardous\_substances|4|5|4|5|-0.8750|

### Diễn giải

Các bản ghi có điểm âm mạnh nhất thường có một hoặc nhiều đặc điểm sau:

* thuộc `CONSTRAINT` hoặc `COST\\\\\\\_QUALITATIVE`;
* có domain rủi ro cao như `climate\\\\\\\_carbon`, `hazardous\\\\\\\_substances`, `water`;
* có phạm vi rộng hoặc cấp quốc gia;
* đặt ra lệnh cấm, điều kiện kỹ thuật hoặc nghĩa vụ tuân thủ dài hạn;
* nếu không tuân thủ có thể gây rủi ro môi trường nghiêm trọng hoặc khó phục hồi.

Ví dụ, bản ghi `1.6.11.0` về hành vi liên quan chất làm suy giảm tầng ô-dôn có `ImpactScore\\\\\\\_i = -0.9375`. Điểm này hợp lý vì bản ghi có tính ràng buộc mạnh, phạm vi rộng, tác động dài hạn và rủi ro cao trong domain `climate\\\\\\\_carbon`.

Một lưu ý chất lượng dữ liệu: bản ghi `1.28.7.0` có đoạn `raw\\\\\\\_text` chứa phần tiêu đề/công báo/ký số lẫn nội dung luật. Bản ghi này vẫn được tính điểm, nhưng nên được kiểm tra lại ở bước làm sạch dữ liệu để bảo đảm phần văn bản pháp lý chính không bị nhiễu bởi metadata của tài liệu.

\---

## 10\. Kết quả phản ánh điều gì?

### 10.1. Về bản chất chính sách

Kết quả cho thấy Luật Bảo vệ môi trường 2020 trong tập bản ghi được xử lý có thiên hướng mạnh về:



nghĩa vụ tuân thủ
ràng buộc kỹ thuật
điều kiện cấp phép
kiểm soát nguồn thải
quan trắc, báo cáo, thẩm định
quản lý chất thải và ô nhiễm

```

Đây là đặc điểm phù hợp với văn bản pháp luật môi trường, vì luật môi trường thường không chỉ “khuyến khích” mà còn đặt ra điều kiện và trách nhiệm bắt buộc để phòng ngừa thiệt hại môi trường.

### 10.2. Về nhóm chịu ảnh hưởng

Nhóm chịu ảnh hưởng lớn nhất là:

1. \*\*Tổ chức, cá nhân chung\*\*: chịu ràng buộc rộng về hành vi, chất thải, ô nhiễm và nghĩa vụ bảo vệ môi trường.
2. \*\*Cơ quan nhà nước\*\*: chịu trách nhiệm quản lý, kiểm tra, cấp phép, quy hoạch, quan trắc, công bố thông tin và xử lý ô nhiễm.
3. \*\*Chủ dự án đầu tư/chủ đầu tư hạ tầng\*\*: chịu nghĩa vụ ĐTM, giấy phép, điều kiện môi trường và công trình bảo vệ môi trường.
4. \*\*Doanh nghiệp/cơ sở sản xuất kinh doanh\*\*: chịu nghĩa vụ xử lý chất thải, nước thải, khí thải, chất thải nguy hại, vận hành hệ thống xử lý.
5. \*\*Cộng đồng dân cư/làng nghề\*\*: chịu tác động ở cấp địa phương, đặc biệt về chất thải sinh hoạt, môi trường nông thôn và vệ sinh môi trường.

### 10.3. Về domain môi trường

Các domain có tác động lớn nhất là:


water
hazardous\\\\\\\_substances
waste
eia\\\\\\\_permit\\\\\\\_registration
```

Điều này phản ánh hệ thống pháp luật tập trung vào các vấn đề có tính thực tiễn cao: nước, chất thải, chất thải nguy hại và công cụ quản lý hành chính/kỹ thuật như ĐTM, giấy phép, quan trắc, quy chuẩn.

\---

## 11\. Mức độ explainable của kết quả

Kết quả có thể giải thích được vì mỗi `ImpactScore\\\\\\\_i` truy vết được qua chuỗi sau:



raw\\\_text
→ final\\\_label
→ direction\\\_i
→ actor\\\_group
→ domain\\\_primary
→ M\\\_i, S\\\_i, D\\\_i, R\\\_i
→ W\\\_i
→ C\\\_i, C\\\_i\\\_norm
→ ImpactScore\\\_i

```

Ví dụ cách đọc một bản ghi:


final\\\\\\\_label = CONSTRAINT
direction\\\\\\\_i = -1
M\\\\\\\_i = 4 vì ràng buộc/cấm/điều kiện có tác động lớn đến hành vi
S\\\\\\\_i = 5 vì phạm vi quốc gia/rất rộng
D\\\\\\\_i = 4 vì ràng buộc có tính dài hạn
R\\\\\\\_i = 5 vì domain có rủi ro rất cao
W\\\\\\\_i = 1.0
C\\\\\\\_i = 4.5
C\\\\\\\_i\\\\\\\_norm = 0.875
ImpactScore\\\\\\\_i = -0.875
```

Như vậy, điểm không phải là kết quả “hộp đen”; nó được tạo từ các biến có ý nghĩa rõ ràng và có `scoring\\\\\\\_note` giải thích.

\---

## 12\. Đánh giá độ hợp lý của kết quả

### 12.1. Điểm hợp lý

Kết quả hiện tại có logic nội tại tốt:

* Nhóm `COST\\\\\\\_QUALITATIVE` nhiều nhất, phù hợp với bản chất của luật môi trường.
* Nhóm `CONSTRAINT` ít hơn nhưng có điểm trung bình âm mạnh hơn, phù hợp vì ràng buộc/lệnh cấm thường nghiêm ngặt hơn nghĩa vụ thủ tục.
* Domain `water`, `waste`, `hazardous\\\\\\\_substances` có tổng điểm lớn, phù hợp với trọng tâm của Luật Bảo vệ môi trường.
* `climate\\\\\\\_carbon` và `biodiversity\\\\\\\_natural\\\\\\\_heritage` có điểm trung bình mạnh, phù hợp vì đây là các domain dài hạn và khó phục hồi.
* `W\\\\\\\_i = 1.0` giúp tránh việc kết quả bị thiên lệch bởi trọng số chủ quan khi chưa có AHP hoặc chuyên gia.

### 12.2. Điểm cần lưu ý

Một số kết quả cần được diễn giải thận trọng:

1. **TotalImpact âm không phải kết luận chính sách có hại.** Đây là điểm gánh nặng/ràng buộc tương đối, không phải CBA tiền tệ.
2. **Số lượng lợi ích dương còn ít.** Điều này có thể do nhãn cuối cùng chỉ có 15 bản ghi `BENEFIT\\\\\\\_QUALITATIVE`, không có nhãn lợi ích/chi phí định lượng.
3. **Một số bản ghi có raw\_text nhiễu metadata.** Cần kiểm tra thêm nếu dùng để trích dẫn trong báo cáo chính.
4. **Kết quả phụ thuộc vào rubric chấm M/S/D/R.** Vì vậy nên trình bày đây là mô hình bán định lượng có kiểm chứng, không phải đo lường kinh tế tuyệt đối.
5. **W\_i đang bằng nhau cho tất cả bản ghi.** Đây là lựa chọn an toàn, nhưng trong nghiên cứu mở rộng có thể dùng AHP hoặc chuyên gia để xác định trọng số domain/chủ thể.

\---

## 13\. Khuyến nghị sử dụng kết quả trong báo cáo đồ án

Khi viết báo cáo, nên trình bày kết quả theo hướng sau:



Kết quả tính điểm cho thấy hệ thống pháp luật môi trường tạo ra tổng điểm tác động âm, chủ yếu do các nghĩa vụ tuân thủ và ràng buộc pháp lý/kỹ thuật. Điều này phản ánh vai trò điều tiết của Luật Bảo vệ môi trường, không phải tác động tiêu cực tuyệt đối. Các domain có mức tác động lớn nhất là water, hazardous\\\_substances, waste và eia\\\_permit\\\_registration. Các nhóm chịu ảnh hưởng chính là tổ chức/cá nhân chung, cơ quan nhà nước, chủ dự án đầu tư và cơ sở sản xuất kinh doanh. Kết quả có thể giải thích thông qua final\\\_label, domain, actor và bốn biến M, S, D, R.

```

Nên tránh viết:


Luật có tổng tác động tiêu cực.
```

Nên viết:



Theo mô hình bán định lượng đã chọn, phần lớn điều khoản tạo chi phí tuân thủ hoặc ràng buộc pháp lý/kỹ thuật, trong khi lợi ích định tính xuất hiện ít hơn nhưng vẫn đóng vai trò tích cực trong một số nhóm chính sách.

```

\\---

## 14\\. Kết luận

Kết quả tính điểm cho thấy pipeline đã chuyển được văn bản pháp lý từ dạng bản ghi có nhãn thành dữ liệu định lượng có thể giải thích. `ImpactScore\\\\\\\_i` giúp nhận diện các điều khoản, domain và nhóm chủ thể có mức tác động lớn, đồng thời vẫn giữ được khả năng truy vết về `raw\\\\\\\_text`, `final\\\\\\\_label`, `actor\\\\\\\_group`, `domain\\\\\\\_primary` và `scoring\\\\\\\_note`.

Trong phạm vi đồ án hiện tại, kết quả đủ cơ sở để sử dụng cho:

\* tổng hợp tác động theo nhãn;
\* tổng hợp tác động theo domain;
\* tổng hợp tác động theo actor;
\* chọn top bản ghi có tác động lớn để phân tích định tính;
\* viết phần kết quả, thảo luận, hạn chế và hướng phát triển.

Tuy nhiên, cần nhấn mạnh rằng đây là \*\*mô hình bán định lượng\*\*, không thay thế phân tích CBA đầy đủ bằng tiền và không nên diễn giải `TotalImpact` như thặng dư xã hội tuyệt đối.


