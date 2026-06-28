# Hệ thống đánh giá tác động chính sách môi trường RIA–EIA–CBA

## 0\. Mục tiêu của README này

**Đánh giá tác động chính sách môi trường: Khung định lượng chi phí, lợi ích, rủi ro**

Hệ thống hiện tại có tên thư mục khuyến nghị:

Hệ thống hiện tại tập trung vào pipeline có thể bảo vệ được trong đồ án:
Văn bản pháp lý dạng JSON
→ lọc bản ghi có tác động pháp lý
→ lọc bản ghi có tác động môi trường
→ phân loại 5 nhãn bằng LLM
→ so sánh với nhãn cơ sở do người gán thủ công
→ đánh giá LLM bằng metric
→ chốt nhãn cuối cùng
→ chuyển nhãn thành biến
→ tính Impact Score
→ xuất báo cáo và biểu đồ
```

Phiên bản này **không sử dụng**:

* Multi-Agent Debate.
* Agent A/B.
* Validator phản biện.
* Debate Engine.
* Monte Carlo Simulation nếu chưa có cơ sở phân phối rõ ràng.
* CBA đầy đủ bằng tiền nếu chưa có dữ liệu kinh tế – môi trường đầy đủ.
* Knowledge Graph hoàn chỉnh.
* Multi-label classification ở phiên bản chính.

Mục tiêu của README là cung cấp đầy đủ bối cảnh, pipeline, công thức, cấu trúc thư mục, chức năng script, đầu vào/đầu ra và các quy tắc quan trọng để Agent có thể đọc và tinh chỉnh hệ thống mà không hiểu sai phạm vi đồ án.

\---

## 1\. Bối cảnh hệ thống

Hệ thống phục vụ bài toán đánh giá tác động chính sách môi trường từ văn bản pháp lý đã được tách cấu trúc thành JSON.

Dữ liệu đầu vào hiện tại định hướng là:

data/raw/Luat\_bao\_ve\_moi\_truong\_2020.json
```

File này được tách từ Luật Bảo vệ môi trường năm 2020 hoặc văn bản pháp lý môi trường tương tự. Mỗi record tương ứng với một điều, khoản, điểm hoặc mệnh đề pháp lý có thể xử lý độc lập.

Hệ thống không xử lý trực tiếp văn bản PDF/Word trong pipeline chính. Nếu có văn bản thô, cần có bước tiền xử lý riêng:
PDF/Word/OCR/TXT
→ tách cấu trúc pháp lý
→ chuẩn hóa thành JSON
→ kiểm tra schema
→ đưa vào pipeline chính
```

\---

## 2\. Pipeline tổng thể hiện tại

Pipeline chính:
Bước 0. Chuẩn bị JSON pháp lý đầu vào
Bước 1. Kiểm tra schema và chất lượng dữ liệu
Bước 2. Lọc bản ghi có co\_tac\_dong = true
Bước 3. Lọc bản ghi có tác động tới môi trường
Bước 4. Tạo file gán nhãn thủ công
Bước 5. Người nghiên cứu gán human\_label và human\_reason
Bước 6. Gọi LLM phân loại 5 nhãn
Bước 7. Kiểm tra output LLM
Bước 8. So sánh llm\_label với human\_label
Bước 9. Tính metric đánh giá LLM
Bước 10. Chốt final\_label
Bước 11. Tạo file nhập biến M\_i, S\_i, D\_i, R\_i, W\_i
Bước 12. Tính Impact Score
Bước 13. Tổng hợp theo nhãn, domain, chủ thể
Bước 14. Sinh biểu đồ và báo cáo
Bước 15. Diễn giải kết quả trong báo cáo/slide
```

Biểu diễn ngắn gọn:
Legal JSON
→ Legal Impact Filtering
→ Environmental Impact Filtering
→ Five-label LLM Classification
→ Human-labeled Reference Dataset
→ LLM Evaluation Metrics
→ Final Label
→ Impact Scoring
→ Visualization and Interpretation
```

Nguyên tắc thiết kế:
LLM hỗ trợ phân loại
→ Con người kiểm chứng
→ Metric đánh giá
→ Mô hình toán học lượng hóa
→ Báo cáo có khả năng giải thích
```

\---

## 3\. Dữ liệu đầu vào

### 3.1. File đầu vào chính

File đầu vào:
data/raw/Luat\_bao\_ve\_moi\_truong\_2020.json
```

### 3.2. Yêu cầu với JSON đầu vào

File JSON phải đáp ứng ba yêu cầu:

1. **Giữ cấu trúc pháp lý**: có thể truy vết điều, khoản, điểm, mệnh đề.
2. **Trung thành với văn bản gốc**: không tự tóm tắt làm mất nghĩa pháp lý.
3. **Đủ thông tin cho phân loại và tính điểm**.

### 3.3. Trường dữ liệu khuyến nghị

Mỗi record nên có các trường sau:

|Trường|Bắt buộc|Vai trò|
|-|-:|-|
|`source\_id`|Có|Mã định danh duy nhất của record.|
|`legal\_citation`|Có|Trích dẫn pháp lý, ví dụ Điều 4, Khoản 6.|
|`raw\_text`|Có|Nội dung gốc hoặc gần nguyên văn của điều khoản.|
|`co\_tac\_dong`|Có|Cho biết record có tác động pháp lý/chính sách hay không.|
|`chu\_the`| có|Chủ thể chịu tác động hoặc chủ thể có quyền/nghĩa vụ.|
|`tin\_hieu\_tac\_dong`| có|Tín hiệu như “phải”, “được”, “không được”, “nghiêm cấm”.|
|`domain`| có|Miền môi trường: nước, không khí, chất thải, khí hậu, giấy phép, quan trắc...|
|`gia\_tri\_dinh\_luong`| có|Giá trị định lượng nếu có: tiền, %, thời hạn, ngưỡng kỹ thuật, hạn ngạch...|
|`dieu\_kien\_ap\_dung`| có|Điều kiện, thời hạn, ngưỡng, tiêu chuẩn, quy chuẩn hoặc điều kiện áp dụng.|
|`ly\_do`| có|Lý do sơ bộ vì sao record được xem là có/không có tác động.|
|`muc\_do\_ro\_rang`| có|Mức rõ ràng của tác động, dùng để ưu tiên kiểm tra thủ công.|

Trường `co\_tac\_dong` là bắt buộc vì pipeline bắt đầu từ bước:
lọc co\_tac\_dong = true
```

Nếu thiếu `co\_tac\_dong`, hệ thống không thể thực hiện bước lọc tác động pháp lý.

\---

## 4\. Bộ nhãn phân loại 5 lớp

Hệ thống hiện tại dùng 5 nhãn:
BENEFIT\_QUANTITATIVE
BENEFIT\_QUALITATIVE
COST\_QUANTITATIVE
COST\_QUALITATIVE
CONSTRAINT

|Nhãn|Ý nghĩa|Hướng tác động|
|-|-|-:|
|`BENEFIT\_QUANTITATIVE`|Lợi ích có thể lượng hóa trực tiếp bằng số, tiền, tỷ lệ, lượng phát thải giảm, mức hỗ trợ...|`+1`|
|`BENEFIT\_QUALITATIVE`|Lợi ích môi trường/xã hội/quản lý nhưng chưa có số cụ thể.|`+1`|
|`COST\_QUANTITATIVE`|Chi phí hoặc nghĩa vụ tài chính có số tiền, tỷ lệ, công thức hoặc đại lượng định lượng trực tiếp.|`-1`|
|`COST\_QUALITATIVE`|Chi phí, nghĩa vụ, thủ tục, gánh nặng tuân thủ chưa có số cụ thể.|`-1`|
|`CONSTRAINT`|Điều kiện, lệnh cấm, giới hạn, ngưỡng kỹ thuật, quy chuẩn, thời hạn hoặc ràng buộc pháp lý/kỹ thuật.|`-1`|

### 4.1. Quy tắc quan trọng

Không phải cứ có số là nhãn định lượng.

Ví dụ:
“Kế hoạch được lập theo thời kỳ 05 năm”
```

Con số `05 năm` là thời hạn/ràng buộc thời gian, không phải lợi ích hoặc chi phí định lượng. Trường hợp này thường nghiêng về:CONSTRAINT
```

### 4.2. Các cặp nhãn dễ nhầm

|Cặp nhãn|Quy tắc phân biệt|
|-|-|
|`COST\_QUALITATIVE` vs `CONSTRAINT`|Nếu trọng tâm là phải thực hiện thủ tục/nghĩa vụ → `COST\_QUALITATIVE`. Nếu trọng tâm là điều kiện, cấm đoán, giới hạn, quy chuẩn → `CONSTRAINT`.|
|`BENEFIT\_QUANTITATIVE` vs `BENEFIT\_QUALITATIVE`|Chỉ chọn định lượng nếu giá trị số gắn trực tiếp với lợi ích.|
|`COST\_QUANTITATIVE` vs `COST\_QUALITATIVE`|Chỉ chọn định lượng nếu có số tiền, tỷ lệ, công thức hoặc mức chi phí cụ thể.|
|`BENEFIT\_QUALITATIVE` vs `CONSTRAINT`|Nếu mục tiêu tốt cho môi trường nhưng hình thức là lệnh cấm/điều kiện → `CONSTRAINT`.|

\---

## 5\. Prompt LLM phân loại

Prompt phân loại chính đặt tại:


prompts/classify\_system\_prompt.txt


Prompt phải yêu cầu LLM:

1. Chỉ chọn đúng một trong 5 nhãn.
2. Không tạo nhãn mới.
3. Không suy diễn ngoài `raw\_text`.
4. Không tự ước lượng chi phí/lợi ích.
5. Trích `evidence\_span` trực tiếp từ `raw\_text`.
6. Trả về JSON hợp lệ.
7. Ghi `needs\_human\_review = true` nếu record mơ hồ.
8. Ghi `quantity\_interpretation` nếu record có giá trị định lượng.
9. Ghi `rule\_applied` để phục vụ phân tích lỗi.

Schema đầu ra của LLM:

```json
{
  "label": "BENEFIT\_QUANTITATIVE | BENEFIT\_QUALITATIVE | COST\_QUANTITATIVE | COST\_QUALITATIVE | CONSTRAINT",
  "reason": "Giải thích ngắn gọn bằng tiếng Việt.",
  "evidence\_span": "Cụm từ hoặc câu xuất hiện trực tiếp trong raw\_text.",
  "confidence": 0.0,
  "needs\_human\_review": false,
  "rule\_applied": "DIRECT\_CONSTRAINT | DIRECT\_COMPLIANCE\_COST | DIRECT\_BENEFIT | QUANTITATIVE\_CHECK | COST\_QUALITATIVE\_vs\_CONSTRAINT",
  "quantity\_interpretation": "none hoặc giải thích loại giá trị định lượng"
}
```

Khuyến nghị cấu hình Gemini:

```env
LLM\_MODEL\_NAME=gemini-2.5-flash
LLM\_TEMPERATURE=0.0
LLM\_DELAY\_SECONDS=0.5
```

Có thể thử nghiệm thêm các model khác nếu API hỗ trợ, nhưng khi báo cáo cần ghi rõ model, prompt version và cấu hình.

\---

## 6\. Human-labeled Reference Dataset

### 6.1. Khái niệm

`human\_label` là nhãn cơ sở do người nghiên cứu gán thủ công. Đây là nhãn tham chiếu để đánh giá LLM.

Với mỗi record:
llm\_label   = nhãn do LLM dự đoán
human\_label = nhãn do người nghiên cứu gán
final\_label = nhãn cuối cùng sau review


Trong phiên bản hiện tại:

Quy tắc mặc định:
final\_label = human\_label
```

trừ khi người nghiên cứu xem lại và chỉnh trong bước review.

### 6.2. Vì sao cần human\_label?

Nếu không có `human\_label`, hệ thống không thể tính:

* Accuracy.
* Precision.
* Recall.
* F1-score.
* Macro-F1.
* Confusion Matrix.
* Human Correction Rate.

Vì vậy, bước gán nhãn thủ công là bắt buộc.

### 6.3. Cột dữ liệu nên có trong file human label

File:
data/interim/human\_labeled\_dataset.xlsx
```

Nên có các cột:

|Cột|Ý nghĩa|
|-|-|
|`source\_id`|Khóa để merge với kết quả LLM.|
|`legal\_citation`|Trích dẫn pháp lý.|
|`raw\_text`|Nội dung điều khoản.|
|`domain`|Miền môi trường.|
|`llm\_label`|Có thể để trống trước khi merge.|
|`human\_label`|Nhãn người nghiên cứu gán.|
|`human\_reason`|Lý do gán nhãn.|
|`review\_note`|Ghi chú khi record khó/mơ hồ.|
|`needs\_second\_review`|true/false nếu cần xem lại.|

\---

## 7\. Công thức metric đánh giá LLM

Đây là phần bắt buộc vì hệ thống cần đánh giá LLM so với `human\_label`.

Gọi:
L = {l\_1, l\_2, l\_3, l\_4, l\_5}
```

trong đó:
l\_1 = BENEFIT\_QUANTITATIVE
l\_2 = BENEFIT\_QUALITATIVE
l\_3 = COST\_QUANTITATIVE
l\_4 = COST\_QUALITATIVE
l\_5 = CONSTRAINT
```

Với mỗi record `i`:
y\_i      = human\_label\_i
y\_hat\_i  = llm\_label\_i
```

Tập dữ liệu đánh giá gồm `M\_eval` record có cả `human\_label` và `llm\_label` hợp lệ.

\---

### 7.1. Confusion Matrix

Ma trận nhầm lẫn là ma trận 5x5:
C ∈ N^(5x5)
```

Phần tử `C\[k]\[j]` được định nghĩa:
C\[k]\[j] = số record có human\_label = l\_k và llm\_label = l\_j
```

Diễn giải:
Hàng = nhãn đúng theo human\_label
Cột  = nhãn dự đoán theo llm\_label
```

Bảng cấu trúc:

|Human \\ LLM|BQ|BQL|CQ|CQL|CON|
|-|-:|-:|-:|-:|-:|
|BQ|C11|C12|C13|C14|C15|
|BQL|C21|C22|C23|C24|C25|
|CQ|C31|C32|C33|C34|C35|
|CQL|C41|C42|C43|C44|C45|
|CON|C51|C52|C53|C54|C55|

Trong đó:
BQ  = BENEFIT\_QUANTITATIVE
BQL = BENEFIT\_QUALITATIVE
CQ  = COST\_QUANTITATIVE
CQL = COST\_QUALITATIVE
CON = CONSTRAINT
```

Các phần tử đường chéo `C\[k]\[k]` là số dự đoán đúng.

\---

### 7.2. Accuracy

Công thức:


Accuracy = (tổng số dự đoán đúng) / (tổng số record đánh giá)
```

Theo ma trận nhầm lẫn:


Accuracy = (Σ\_k C\[k]\[k]) / (Σ\_k Σ\_j C\[k]\[j])
```

Theo từng record:


Accuracy = |{i : y\_i = y\_hat\_i}| / M\_eval
```

Ý nghĩa:


Accuracy cho biết tỷ lệ nhãn LLM trùng với nhãn con người trên toàn bộ tập đánh giá.
```

\---

### 7.3. Precision theo từng nhãn

Với nhãn `l\_k`:


TP\_k = C\[k]\[k]
FP\_k = Σ\_{r≠k} C\[r]\[k]
```

Trong đó:

* `TP\_k`: số record thuộc nhãn `l\_k` và được LLM dự đoán đúng.
* `FP\_k`: số record không thuộc nhãn `l\_k` nhưng bị LLM dự đoán thành `l\_k`.

Công thức:
Precision\_k = TP\_k / (TP\_k + FP\_k)
```

Nếu mẫu số bằng 0:

Precision\_k = 0
```

Quy ước này giúp code chạy ổn định khi LLM không dự đoán nhãn nào đó.

Ý nghĩa:
Trong tất cả record mà LLM dự đoán là nhãn l\_k, Precision\_k cho biết có bao nhiêu record thật sự thuộc nhãn đó theo human\_label.
```

\---

### 7.4. Recall theo từng nhãn

Với nhãn `l\_k`:


TP\_k = C\[k]\[k]
FN\_k = Σ\_{c≠k} C\[k]\[c]
```

Trong đó:

* `FN\_k`: số record thật sự thuộc nhãn `l\_k` nhưng LLM dự đoán sang nhãn khác.

Công thức:


Recall\_k = TP\_k / (TP\_k + FN\_k)
```

Nếu mẫu số bằng 0:


Recall\_k = 0
```

Ý nghĩa:
Trong tất cả record thật sự thuộc nhãn l\_k theo human\_label, Recall\_k cho biết LLM tìm đúng được bao nhiêu record.
```

\---

### 7.5. F1-score theo từng nhãn

Công thức:


F1\_k = 2 \* Precision\_k \* Recall\_k / (Precision\_k + Recall\_k)
```

Nếu:


Precision\_k + Recall\_k = 0
```

thì:


F1\_k = 0
```

Ý nghĩa:
F1-score cân bằng giữa Precision và Recall.
```

\---

### 7.6. Macro-F1

Công thức:
Macro-F1 = (1/5) \* Σ\_k F1\_k
```

Vì hệ thống có 5 nhãn nên:


Macro-F1 = (F1\_BQ + F1\_BQL + F1\_CQ + F1\_CQL + F1\_CON) / 5
```

Ý nghĩa:


Macro-F1 đánh giá hiệu năng trung bình trên 5 nhãn, không để nhãn có nhiều mẫu lấn át các nhãn ít mẫu.
```

Metric này rất quan trọng vì dữ liệu pháp lý môi trường có thể lệch nhãn, ví dụ `CONSTRAINT` và `COST\_QUALITATIVE` thường nhiều hơn các nhãn định lượng.

\---

### 7.7. Support theo từng nhãn

Support của nhãn `l\_k`:


Support\_k = Σ\_j C\[k]\[j]
```

Ý nghĩa:


Support\_k là số record thật sự thuộc nhãn l\_k theo human\_label.
```

Support cần được báo cáo cùng Precision/Recall/F1 để tránh diễn giải sai khi một nhãn có quá ít mẫu.

\---

### 7.8. Human Correction Rate

Công thức:


HumanCorrectionRate = |{i : y\_i ≠ y\_hat\_i}| / M\_eval
```

Nếu mọi record đều có nhãn hợp lệ:


HumanCorrectionRate = 1 - Accuracy
```

Ý nghĩa:


Human Correction Rate cho biết tỷ lệ nhãn LLM cần con người sửa lại.
```

Đây là metric rất quan trọng đối với pipeline Human-in-the-loop.

\---

### 7.9. Label Match

Với từng record:


label\_match\_i = true  nếu y\_i = y\_hat\_i
label\_match\_i = false nếu y\_i ≠ y\_hat\_i
```

Cột này nên được lưu trong:


data/processed/final\_labeled\_dataset.xlsx
```

\---

### 7.10. Error Analysis

Các record (bản ghi) có:


label\_match = false
```

cần được xuất ra sheet riêng hoặc file riêng để phân tích lỗi.

Các cặp lỗi cần ưu tiên phân tích:

|Lỗi|Ý nghĩa|
|-|-|
|`COST\_QUALITATIVE → CONSTRAINT`|LLM nhầm nghĩa vụ tuân thủ thành ràng buộc.|
|`CONSTRAINT → COST\_QUALITATIVE`|LLM nhầm ràng buộc thành nghĩa vụ tuân thủ.|
|`BENEFIT\_QUALITATIVE → CONSTRAINT`|LLM nhầm lợi ích định tính với điều kiện/ràng buộc.|
|`CONSTRAINT → BENEFIT\_QUALITATIVE`|LLM suy diễn lợi ích môi trường từ lệnh cấm/điều kiện.|
|`COST\_QUANTITATIVE → COST\_QUALITATIVE`|LLM bỏ sót yếu tố định lượng của chi phí.|
|`COST\_QUALITATIVE → COST\_QUANTITATIVE`|LLM nhầm nghĩa vụ chưa có số thành chi phí định lượng.|
|`BENEFIT\_QUANTITATIVE → BENEFIT\_QUALITATIVE`|LLM bỏ sót yếu tố định lượng của lợi ích.|
|`BENEFIT\_QUALITATIVE → BENEFIT\_QUANTITATIVE`|LLM nhầm lợi ích chưa có số thành lợi ích định lượng.|

\---

## 8\. Mô hình toán học Impact Score

Sau khi có `final\_label`, hệ thống chuyển nhãn thành hướng tác động.

8.1. Direction
BENEFIT\_QUANTITATIVE → +1
BENEFIT\_QUALITATIVE  → +1
COST\_QUANTITATIVE    → -1
COST\_QUALITATIVE     → -1
CONSTRAINT           → -1
```

Ký hiệu:
direction\_i = s\_i
```

### 8.2. Các biến điểm

|Biến|Ý nghĩa|Thang điểm|
|-|-|-|
|`M\_i`|Magnitude — cường độ tác động|1–5|
|`S\_i`|Scope — phạm vi tác động|1–5|
|`D\_i`|Duration — thời gian tác động|1–5|
|`R\_i`|Risk/Reversibility — rủi ro hoặc khả năng đảo ngược|1–5|
|`W\_i`|Object/domain weight — trọng số đối tượng hoặc domain|mặc định 1.0|

### 8.3. Công thức tính điểm thành phần


C\_i = alpha\*M\_i + beta\*S\_i + gamma\*D\_i + delta\*R\_i
```

Trong phiên bản cơ sở:


alpha = beta = gamma = delta = 0.25
```

Do đó:


C\_i = 0.25\*M\_i + 0.25\*S\_i + 0.25\*D\_i + 0.25\*R\_i
```

Vì:


M\_i, S\_i, D\_i, R\_i ∈ \[1,5]
```

nên:


C\_i ∈ \[1,5]
```

### 8.4. Chuẩn hóa điểm

C\_i\_norm = (C\_i - 1) / 4
```

Do đó:


C\_i\_norm ∈ \[0,1]
```

### 8.5. Công thức Impact Score


ImpactScore\_i = direction\_i \* W\_i \* C\_i\_norm
```

Nếu:

`
W\_i = 1.0
```

thì:


ImpactScore\_i ∈ \[-1,1]
```

### 8.6. Tổng hợp điểm

Tổng điểm toàn bộ:
TotalImpact = Σ\_i ImpactScore\_i
```

Tổng điểm theo nhãn:


TotalImpact(label = l\_k) = Σ\_{i: final\_label\_i = l\_k} ImpactScore\_i
```

Tổng điểm theo domain:


TotalImpact(domain = d) = Σ\_{i: domain\_i = d} ImpactScore\_i
```

Tổng điểm theo chủ thể:


TotalImpact(actor = a) = Σ\_{i: chu\_the\_i = a} ImpactScore\_i
```

### 8.7. Diễn giải

|Giá trị|Ý nghĩa|
|-|-|
|`ImpactScore\_i > 0`|Điều khoản tạo lợi ích theo mô hình.|
|`ImpactScore\_i < 0`|Điều khoản tạo chi phí, gánh nặng hoặc ràng buộc theo mô hình.|
|`|ImpactScore\_i|

Lưu ý:


Impact Score là điểm bán định lượng, không phải giá trị tiền tệ tuyệt đối và chưa thay thế CBA đầy đủ.
```

\---

## 9\. Cấu trúc thư mục khuyến nghị


DTM\_Khong\_debate/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── config/
│   └── project\_config.yaml
│
├── prompts/
│   └── classify\_system\_prompt.txt
│
├── data/
│   ├── raw/
│   │   └── Luat\_bao\_ve\_moi\_truong\_2020.json
│   ├── interim/
│   ├── processed/
│   └── reports/
│
├── src/
│   ├── 01\_validate\_input\_schema.py
│   ├── 02\_filter\_legal\_impact.py
│   ├── 03\_filter\_environmental\_impact.py
│   ├── 04\_build\_manual\_label\_file.py
│   ├── 05\_llm\_classify\_5\_labels.py
│   ├── 06\_compare\_llm\_vs\_human.py
│   ├── 07\_build\_scoring\_input.py
│   ├── 08\_calculate\_impact\_score.py
│   └── 09\_generate\_figures.py
│
├── docs/
│   ├── methodology.md
│   ├── label\_guideline.md
│   ├── metric\_definition.md
│   ├── variable\_definition.md
│   ├── scoring\_rule.md
│   ├── example\_manual\_calculation.md
│   ├── limitations\_and\_future\_work.md
│   └── literature\_justification.md
│
├── outputs/
│   └── figures/
│
└── references/
    └── README.md
```

\---

## 10\. Chức năng từng script

|Script|Chức năng|
|-|-|
|`01\_validate\_input\_schema.py`|Kiểm tra file JSON đầu vào có đủ trường bắt buộc, không trùng `source\_id`, không thiếu `raw\_text`, tạo báo cáo schema.|
|`02\_filter\_legal\_impact.py`|Lọc các bản ghi có `co\_tac\_dong = true`.|
|`03\_filter\_environmental\_impact.py`|Lọc tiếp các bản ghi có tác động môi trường dựa trên `domain`, keyword, tín hiệu pháp lý và review thủ công nếu cần.|
|`04\_build\_manual\_label\_file.py`|Tạo file Excel để người nghiên cứu gán `human\_label`, `human\_reason`.|
|`05\_llm\_classify\_5\_labels.py`|Gọi Gemini để phân loại 5 nhãn, trả về JSON gồm label, reason, evidence, confidence.|
|`06\_compare\_llm\_vs\_human.py`|So sánh `llm\_label` với `human\_label`, tính đầy đủ metric và tạo `final\_label`.|
|`07\_build\_scoring\_input.py`|Tạo file nhập điểm `M\_i`, `S\_i`, `D\_i`, `R\_i`, `W\_i`.|
|`08\_calculate\_impact\_score.py`|Tính `C\_i`, `C\_i\_norm`, `ImpactScore\_i`, tổng hợp theo nhãn/domain/chủ thể.|
|`09\_generate\_figures.py`|Sinh biểu đồ phân bố nhãn, confusion matrix, Impact Score.|

\---

## 11\. File đầu ra chính

|File|Nội dung|
|-|-|
|`data/reports/input\_schema\_report.xlsx`|Báo cáo kiểm tra schema JSON đầu vào.|
|`data/interim/legal\_impact\_records.xlsx`|Các record có `co\_tac\_dong = true`.|
|`data/interim/environmental\_impact\_records.xlsx`|Các record có tác động môi trường.|
|`data/interim/manual\_label\_template.xlsx`|File để người nghiên cứu gán nhãn thủ công.|
|`data/interim/human\_labeled\_dataset.xlsx`|Tập dữ liệu đã có `human\_label`.|
|`data/processed/llm\_labeled\_dataset.xlsx`|Tập dữ liệu đã có `llm\_label`.|
|`data/reports/classification\_metrics.xlsx`|Accuracy, Precision, Recall, F1, Macro-F1, Confusion Matrix, Human Correction Rate.|
|`data/reports/error\_analysis.xlsx`|Các record LLM phân loại khác human label.|
|`data/processed/final\_labeled\_dataset.xlsx`|Tập dữ liệu có `final\_label`.|
|`data/interim/scoring\_input.xlsx`|File nhập biến `M\_i`, `S\_i`, `D\_i`, `R\_i`, `W\_i`.|
|`data/reports/final\_impact\_report.xlsx`|Báo cáo Impact Score cuối cùng.|
|`outputs/figures/label\_distribution.png`|Biểu đồ phân bố nhãn.|
|`outputs/figures/confusion\_matrix.png`|Biểu đồ ma trận nhầm lẫn.|
|`outputs/figures/impact\_score\_by\_label.png`|Biểu đồ Impact Score theo nhãn.|
|`outputs/figures/impact\_score\_by\_domain.png`|Biểu đồ Impact Score theo domain.|
|`outputs/figures/impact\_score\_by\_actor.png`|Biểu đồ Impact Score theo chủ thể.|

\---

## 12\. Cách chạy pipeline

Chạy từ thư mục gốc của repository.

### Bước 0. Cài đặt

```powershell
py -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Điền API key hoặc cấu hình Vertex AI vào `.env`.

\---

### Bước 1. Kiểm tra schema JSON

```powershell
py src/01\_validate\_input\_schema.py
```

Kết quả:


data/reports/input\_schema\_report.xlsx
```

\---

### Bước 2. Lọc bản ghi có tác động pháp lý

```powershell
py src/02\_filter\_legal\_impact.py
```

Kết quả:


data/interim/legal\_impact\_records.xlsx
```

\---

### Bước 3. Lọc bản ghi có tác động môi trường

```powershell
py src/03\_filter\_environmental\_impact.py
```

Kết quả:


data/interim/environmental\_impact\_records.xlsx
```

\---

### Bước 4. Tạo file gán nhãn thủ công

```powershell
py src/04\_build\_manual\_label\_file.py
```

Kết quả:


data/interim/manual\_label\_template.xlsx
```

\---

### Bước 5. Người nghiên cứu gán nhãn thủ công

Mở:
data/interim/manual\_label\_template.xlsx
```

Điền:
human\_label
human\_reason
review\_note
needs\_second\_review
```

Lưu thành:


data/interim/human\_labeled\_dataset.xlsx
```

`human\_label` phải là một trong 5 nhãn:


BENEFIT\_QUANTITATIVE
BENEFIT\_QUALITATIVE
COST\_QUANTITATIVE
COST\_QUALITATIVE
CONSTRAINT
```

\---

### Bước 6. LLM phân loại 5 nhãn

```powershell
py src/05\_llm\_classify\_5\_labels.py
```

Kết quả:


data/processed/llm\_labeled\_dataset.xlsx
```

Có thể chạy thử không gọi API:

```powershell
py src/05\_llm\_classify\_5\_labels.py --dry-run
```

\---

### Bước 7. So sánh LLM với nhãn con người

```powershell
py src/06\_compare\_llm\_vs\_human.py
```

Kết quả:


data/reports/classification\_metrics.xlsx
data/reports/error\_analysis.xlsx
data/processed/final\_labeled\_dataset.xlsx
```

Script này bắt buộc phải tính:

Confusion Matrix
Accuracy
Precision từng nhãn
Recall từng nhãn
F1-score từng nhãn
Macro-F1
Support từng nhãn
Human Correction Rate
Label Match
```

\---

### Bước 8. Tạo bảng nhập biến tính điểm

```powershell
py src/07\_build\_scoring\_input.py
```

Kết quả:
data/interim/scoring\_input.xlsx
```

Điền thủ công:
M\_i
S\_i
D\_i
R\_i
W\_i
```

\---

### Bước 9. Tính Impact Score

```powershell
py src/08\_calculate\_impact\_score.py
```

Kết quả:


data/reports/final\_impact\_report.xlsx
```

\---

### Bước 10. Sinh biểu đồ

```powershell
py src/09\_generate\_figures.py
```

Kết quả:


outputs/figures/label\_distribution.png
outputs/figures/confusion\_matrix.png
outputs/figures/impact\_score\_by\_label.png
outputs/figures/impact\_score\_by\_domain.png
outputs/figures/impact\_score\_by\_actor.png
```

\---

## 13\. Cấu hình `.env`

### Google AI Studio

```env
LLM\_PROVIDER=google\_ai\_studio
GOOGLE\_API\_KEY=your\_google\_api\_key\_here
LLM\_MODEL\_NAME=gemini-2.5-flash
LLM\_TEMPERATURE=0.0
LLM\_DELAY\_SECONDS=0.5
```

### Vertex AI

```env
LLM\_PROVIDER=vertex\_ai
GOOGLE\_CLOUD\_PROJECT=your-project-id
GOOGLE\_CLOUD\_LOCATION=us-central1
GOOGLE\_APPLICATION\_CREDENTIALS=data/gcp\_key.json
LLM\_MODEL\_NAME=gemini-2.5-flash
LLM\_TEMPERATURE=0.0
LLM\_DELAY\_SECONDS=0.5
```

Không commit:

.env
data/gcp\_key.json
\*.json.key
```

\---

## 14\. Cấu hình `project\_config.yaml`

File:


config/project\_config.yaml
```

Nội dung khuyến nghị:

```yaml
project:
  name: DTM\_Khong\_debate
  input\_file: data/raw/Luat\_bao\_ve\_moi\_truong\_2020.json

labels:
  - BENEFIT\_QUANTITATIVE
  - BENEFIT\_QUALITATIVE
  - COST\_QUANTITATIVE
  - COST\_QUALITATIVE
  - CONSTRAINT

scoring:
  alpha: 0.25
  beta: 0.25
  gamma: 0.25
  delta: 0.25
  default\_object\_weight: 1.0
  score\_min: 1
  score\_max: 5

metrics:
  zero\_division: 0
  average: macro
  confusion\_matrix\_order:
    - BENEFIT\_QUANTITATIVE
    - BENEFIT\_QUALITATIVE
    - COST\_QUANTITATIVE
    - COST\_QUALITATIVE
    - CONSTRAINT

llm:
  model\_name: gemini-2.5-flash
  temperature: 0.0
  delay\_seconds: 0.5
  prompt\_path: prompts/classify\_system\_prompt.txt

paths:
  raw\_data: data/raw
  interim: data/interim
  processed: data/processed
  reports: data/reports
  figures: outputs/figures
```

\---

## 15\. Ví dụ tính metric thủ công

Giả sử có 10 record đánh giá và LLM dự đoán đúng 7 record:


Accuracy = 7 / 10 = 0.70
HumanCorrectionRate = 3 / 10 = 0.30
```

Với nhãn `CONSTRAINT`, giả sử:

TP\_CON = 4
FP\_CON = 1
FN\_CON = 2
```

Khi đó:


Precision\_CON = 4 / (4 + 1) = 0.80
Recall\_CON = 4 / (4 + 2) = 0.6667
F1\_CON = 2 \* 0.80 \* 0.6667 / (0.80 + 0.6667) ≈ 0.7273
```

Macro-F1:


Macro-F1 = (F1\_BQ + F1\_BQL + F1\_CQ + F1\_CQL + F1\_CON) / 5
```

\---

## 16\. Ví dụ tính Impact Score

Giả sử một điều khoản có:


final\_label = COST\_QUALITATIVE
M\_i = 3
S\_i = 3
D\_i = 4
R\_i = 2
W\_i = 1
```

Khi đó:

```text
direction\_i = -1
C\_i = 0.25\*3 + 0.25\*3 + 0.25\*4 + 0.25\*2 = 3.0
C\_i\_norm = (3.0 - 1) / 4 = 0.5
ImpactScore\_i = -1 \* 1 \* 0.5 = -0.5
```

Diễn giải:


Điều khoản tạo gánh nặng tuân thủ ở mức trung bình.
Điểm âm không có nghĩa điều khoản xấu về chính sách, mà phản ánh chi phí/ràng buộc đối với chủ thể chịu tác động trong mô hình hiện tại.
```

\---

## 17\. Checklist cho Agent khi tinh chỉnh hệ thống

Agent phải đảm bảo:

* Không khôi phục Multi-Agent Debate nếu chưa có sự đồng ý của người nghiên cứu.
* Không thêm Agent A/B hoặc Validator phản biện nếu chưa có sự đồng ý của người nghiên cứu.
* Không thêm Monte Carlo nếu chưa có cơ sở phân phối.
* Không đổi bài toán 5 nhãn thành 3 nhãn.
* Không dùng trực tiếp `llm\_label` để tính Impact Score nếu chưa có `final\_label`.
* Không bỏ bước `human\_label`.
* Không bỏ metric đánh giá LLM.
* Không bỏ `Confusion Matrix`.
* Không bỏ công thức Precision/Recall/F1/Macro-F1.
* Không hard-code đường dẫn tuyệt đối.
* Không ghi đè dữ liệu thô trong `data/raw`.
* Không commit `.env` hoặc khóa API.
* Mọi output phải lưu vào `data/interim`, `data/processed`, `data/reports` hoặc `outputs/figures`.

\---

## 18\. Phạm vi hiện tại

Phiên bản này tập trung vào:

* JSON pháp lý đã tách cấu trúc.
* Lọc `co\_tac\_dong = true`.
* Lọc tác động môi trường.
* Phân loại 5 nhãn bằng một LLM.
* Kiểm chứng bằng `human\_label`.
* Đánh giá bằng metric phân loại đầy đủ.
* Tính Impact Score tất định.
* Xuất báo cáo Excel và biểu đồ.

Phiên bản này không bao gồm:

* Multi-Agent Debate.
* Agent A/B.
* Validator phản biện.
* Debate Engine.
* Monte Carlo Simulation nếu chưa có cơ sở phân phối.
* CBA đầy đủ bằng tiền.
* Knowledge Graph hoàn chỉnh.
* Multi-label classification.

\---

## 19\. Hạn chế

1. Phụ thuộc vào chất lượng file JSON đầu vào.
2. `human\_label` có thể còn chủ quan nếu chỉ do một người gán.
3. Một điều khoản có thể có nhiều tác động nhưng hệ thống hiện tại chỉ gán một nhãn chính.
4. LLM có thể nhầm giữa `COST\_QUALITATIVE` và `CONSTRAINT`.
5. Các nhãn định lượng có thể ít dữ liệu.
6. Impact Score là bán định lượng, chưa phải CBA đầy đủ.
7. Trọng số `alpha`, `beta`, `gamma`, `delta`, `W\_i` hiện là giả định cơ sở.
8. Chưa có phân tích độ nhạy trong phiên bản chính.
9. Chưa đánh giá trên nhiều văn bản pháp lý khác nhau.

\---

## 20\. Hướng phát triển

1. Mở rộng dữ liệu sang nghị định, thông tư, quy chuẩn kỹ thuật môi trường.
2. Hoàn thiện quy trình chuyển PDF/Word/OCR sang JSON pháp lý.
3. Nâng Human-labeled Reference Dataset thành Gold Dataset có nhiều người gán nhãn.
4. So sánh nhiều LLM: Gemini, GPT, Claude, DeepSeek.
5. Cải thiện prompt theo Confusion Matrix và Error Analysis.
6. Phát triển phân loại đa nhãn nếu một điều khoản có nhiều tác động.
7. Bổ sung phân tích độ nhạy cho trọng số và điểm thành phần.
8. Mở rộng sang CBA đầy đủ khi có dữ liệu kinh tế/môi trường.
9. Xây dựng dashboard trực quan hóa.
10. Phát triển Knowledge Graph pháp lý – môi trường.

\---

## 21\. Ghi chú bảo mật

Không đưa khóa API hoặc service account lên GitHub.

Cần đưa vào `.gitignore`:
.env
data/gcp\_key.json
\*.json.key
data/interim/
data/processed/
data/reports/
outputs/logs/
```

Nếu private key từng bị lộ, cần thu hồi key trong Google Cloud IAM và tạo key mới.

\---

## 22\. Mục đích sử dụng

Dự án phục vụ nghiên cứu học thuật và báo cáo học phần **MI3380 — Đồ án 1**.

Hệ thống không thay thế chuyên gia pháp lý, chuyên gia môi trường hoặc cơ quan quản lý nhà nước. Kết quả của hệ thống là công cụ hỗ trợ phân tích, cần được diễn giải trong phạm vi mô hình, dữ liệu và giả định đã nêu.

