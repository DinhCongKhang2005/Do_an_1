## 0\. Mục đích của tài liệu

Tài liệu này tổng hợp lần cập nhật thứ hai cho hệ thống đồ án **DTM — Đánh giá tác động chính sách môi trường theo hướng RIA–EIA–CBA: Khung định lượng, lợi ích, chi phí, rủi ro kết hợp LLM và Human-in-the-loop**.

Mục tiêu của lần cập nhật này là tinh chỉnh lại cấu trúc thư mục, pipeline xử lý dữ liệu, hệ thống file hướng dẫn, prompt, script và báo cáo đầu ra để phù hợp với pipeline mới:
Dữ liệu đầu vào là một văn bản quy phạm pháp luật (VBQPPL), test study ở đây là luật bảo vệ môi trường năm 2020 đã được tách cấu trúc thành các bản ghi định dạng JSON có tác động chính sách (gồm các bản ghi có trường "co\_tac\_dong" = true), sau đó:
→ Human/LLM lọc tác động môi trường
→ tính metric\_env
→ chốt env\_final
→ Human/LLM phân loại 5 nhãn
→ tính metric\_class
→ chốt final\_label
→ chấm M\_i, S\_i, D\_i, R\_i, W\_i
→ tính Impact Score
→ trực quan hóa và báo cáo

Điểm quan trọng của lần cập nhật này là tách rõ hai bài toán đánh giá:

1. **Bài toán lọc tác động môi trường**: phân lớp nhị phân (binary classification), một ánh xạ đi từ tập các bản ghi có tác động chính sách vào tập nhãn thuộc `{0, 1}, 0 tức là các bản ghi không có tác động đến môi trường, 1 là các bản ghi có tác động đến môi trường.
2. **Bài toán phân loại 5 nhãn tác động**: phân loại đa lớp đơn nhãn (multi-class single-label classification), nhãn thuộc 5 lớp:

   * `BENEFIT\\\_QUANTITATIVE`(lợi ích định lượng)
   * `BENEFIT\\\_QUALITATIVE` (lợi ích định tính)
   * `COST\\\_QUANTITATIVE` (chi phí định lượng)
   * `COST\\\_QUALITATIVE` (chi phí định tính)
   * `CONSTRAINT` (ràng buộc)

Hai bài toán này phải có dữ liệu, prompt, metric, file lỗi và báo cáo riêng. Không gộp chúng vào một bước chung chung vì sẽ làm sai logic đánh giá LLM.

## 1\. Cấu trúc thư mục hệ thống hiện tại

Cấu trúc hiện tại đã có nền tảng tương đối tốt:

DTM/
├── config/
├── prompts/
├── data/
├── docs/
├── outputs/
├── references/
└── src/

```

Các thành phần hiện tại đã đáp ứng được phiên bản pipeline cũ:

\* Có file JSON đầu vào.
\* Có bước lọc `co\\\_tac\\\_dong = true`(bây giờ không cần nữa bởi vì đầu vào của hệ thống đã được thay đổi là toàn bộ bản ghi có tác động chính sách, tức là toàn bộ bản ghi ban đầu đều có trường "co\\\_tac\\\_dong"  = true.
\* Có bước lọc môi trường.
\* Có bước tạo file gán nhãn thủ công.
\* Có bước gọi LLM phân loại 5 nhãn.
\* Có bước so sánh LLM với human label.
\* Có bước tính Impact Score.
\* Có thư mục `docs/`, `outputs/`, `references/`.

Tuy nhiên, so với pipeline mới, cấu trúc hiện tại còn thiếu hoặc chưa rõ các điểm sau.

### 1.1. Chưa tách riêng bài toán lọc môi trường và bài toán phân loại 5 nhãn

Hiện tại trong `src/` mới có:

03\\\_filter\\\_environmental\\\_impact.py
04\\\_build\\\_manual\\\_label\\\_file.py
05\\\_llm\\\_classify\\\_5\\\_labels.py
06\\\_compare\\\_llm\\\_vs\\\_human.py
```

Cách đặt này dễ hiểu sai hiểu rằng bước lọc môi trường chỉ là lọc keyword, còn bước đánh giá LLM chỉ áp dụng cho phân loại 5 nhãn. Trong pipeline mới, bước lọc môi trường cũng cần có:



env\_human
env\_llm
env\_final
metric\_env
env\_error\_analysis

```

Vì vậy, cần tách riêng các script và file dữ liệu cho bước lọc môi trường.

### 1.2. Chỉ có một prompt `classify\\\_system\\\_prompt.txt`

Pipeline mới cần ít nhất hai prompt:


prompts/env\\\_filter\\\_system\\\_prompt.txt
prompts/classify\\\_5\\\_labels\\\_system\\\_prompt.txt
```

Lý do:

* `env\\\_filter\\\_system\\\_prompt.txt` dùng cho bài toán nhị phân: bản ghi có tác động môi trường hay không.
* `classify\\\_5\\\_labels\\\_system\\\_prompt.txt` dùng cho bài toán phân loại 5 nhãn: lợi ích, chi phí, ràng buộc.

Nếu dùng chung một prompt, LLM dễ lẫn giữa “có tác động môi trường” và “thuộc nhãn nào trong 5 nhãn”.

### 1.3. Chưa có bản hướng dẫn (guideline) riêng cho lọc môi trường

Hiện tại đã có `label\\\_guideline.md`, nhưng chưa có file hướng dẫn riêng cho việc gán `env\\\_human`.

Cần bổ sung:

docs/environmental\_filter\_guideline.md

```

File này định nghĩa rõ:


env\\\_human = 1 khi nào?
env\\\_human = 0 khi nào?
Trường hợp mơ hồ xử lý ra sao?
Ví dụ đúng/sai cụ thể là gì?


Nếu không có guideline, `env\\\_human` sẽ bị xem là gán nhãn chủ quan.

### 1.4. Chưa có giao thức xử lý bất đồng

Pipeline mới có hai nơi xảy ra bất đồng:


env\\\_human ≠ env\\\_llm
class\\\_human ≠ class\\\_llm
```

Do đó cần có file:



docs/adjudication\_protocol.md

```

File này quy định:

\* Khi human và LLM bất đồng thì xử lý thế nào.
\* Ai có quyền chốt nhãn.
\* Khi nào đặt `needs\\\_review = true`.
\* Khi nào giữ nhãn human.
\* Khi nào sửa lại human label sau khi đọc lại văn bản.
\* Vì sao không dùng `final\\\_label` để tính metric LLM.

### 1.5. Cách gọi “Gold Dataset” cần thận trọng

Trong cấu trúc hiện tại, `human\\\_labeled\\\_dataset.xlsx` được mô tả là `Gold Dataset`.

Với đồ án hiện tại, nếu chỉ có một người nghiên cứu gán nhãn, nên gọi là:


Human-labeled Reference Dataset
```

Không nên gọi là Gold Dataset theo nghĩa mạnh, vì Gold Dataset thường cần nhiều annotator, đo đồng thuận liên chủ thể và có chuyên gia xác nhận.

### 1.6. `gcp\\\_key.json` không nên nằm trực tiếp trong `data/`

Hiện tại:



data/gcp\_key.json

```

Đây là rủi ro bảo mật. File khóa dịch vụ Google Cloud không nên đặt trong vùng dữ liệu dễ bị commit.

Nên đổi thành:


secrets/gcp\\\_key.json
```

hoặc để ngoài repository, sau đó khai báo đường dẫn trong `.env`.

`.gitignore` phải chắc chắn có:



.env
secrets/
data/gcp\_key.json
\*.json.key

```

### 1.7. Biểu đồ hiện tại còn thiếu metric plot

Hiện tại `outputs/figures/` có:


confusion\\\_matrix.png
impact\\\_score\\\_by\\\_actor.png
impact\\\_score\\\_by\\\_domain.png
impact\\\_score\\\_by\\\_label.png
label\\\_distribution.png
```

Cần bổ sung:



env\_confusion\_matrix.png
env\_metric\_summary.png
classification\_metric\_by\_label.png
normalized\_confusion\_matrix.png
top\_error\_pairs.png
impact\_score\_histogram.png
score\_component\_distribution.png

```

Đặc biệt nên có `classification\\\_metric\\\_by\\\_label.png` để trực quan hóa Precision, Recall, F1-score theo từng nhãn.

\\---

## 2\\. Pipeline hệ thống sau cập nhật

### 2.1. Pipeline logic

Pipeline mới được đề xuất như sau:


Bước 0. Chuẩn bị dữ liệu: VBQPPL được tách cấu trúc thành các bản ghi có tác động chính sách
Bước 1. Kiểm tra schema đầu vào
Bước 2. Tạo file human annotation cho lọc môi trường
Bước 3. Người nghiên cứu gán env\\\_human
Bước 4. LLM dự đoán env\\\_llm
Bước 5. So sánh env\\\_llm với env\\\_human và tính metric\\\_env
Bước 6. Chốt env\\\_final và tạo tập D\\\_env
Bước 7. Tạo file human annotation cho 5 nhãn
Bước 8. Người nghiên cứu gán class\\\_human
Bước 9. LLM dự đoán class\\\_llm
Bước 10. So sánh class\\\_llm với class\\\_human và tính metric\\\_class
Bước 11. Chốt final\\\_label
Bước 12. Tạo file scoring\\\_input để chấm M\\\_i, S\\\_i, D\\\_i, R\\\_i, W\\\_i
Bước 13. Người nghiên cứu chấm điểm thành phần
Bước 14. Tính ImpactScore\\\_i
Bước 15. Tổng hợp theo nhãn, domain, chủ thể
Bước 16. Sinh biểu đồ và báo cáo


(Ngoài ra,nếu cần hệ thống chèn thêm vào vị trí hợp lý bước tính thêm Accuracy\\\_end-to-end để đo hiệu quả toàn pipeline, trong đó một bản ghi chỉ được xem là đúng nếu LLM lọc đúng môi trường và, với các bản ghi có tác động môi trường, tiếp tục gán đúng nhãn 5 lớp để xem độ chính xác tổng thể là bao nhiêu)

### 2.2. Biểu diễn toán học ngắn gọn

Gọi tập bản ghi có tác động chính sách ban đầu là:


D\\\_impact = {d\\\_1, d\\\_2, ..., d\\\_N}


Trong thực nghiệm hiện tại, với test study là luật bảo vệ môi trường năm 2020 có N = 581



#### Bài toán 1 — lọc tác động môi trường

Human label:


env\\\_human\\\_i ∈ {0,1}
```

LLM prediction:



env\_llm\_i ∈ {0,1}

```

Sau đánh giá và review:


env\\\_final\\\_i ∈ {0,1}
```

Tập bản ghi có tác động môi trường cuối cùng:



D\_env = {d\_i ∈ D\_impact | env\_final\_i = 1}

```

#### Bài toán 2 — phân loại 5 nhãn

Không gian nhãn:


L = {BQ, BQL, CQ, CQL, CON}
```

Trong đó:



BQ  = BENEFIT\_QUANTITATIVE (lợi ích định lượng)
BQL = BENEFIT\_QUALITATIVE (lợi ích định tính)
CQ  = COST\_QUANTITATIVE (chi phí định lượng)
CQL = COST\_QUALITATIVE (chi phí định tính)
CON = CONSTRAINT (ràng buộc)

```

Human label:


class\\\_human\\\_i ∈ L


LLM prediction:


class\\\_llm\\\_i ∈ L


Final label:


final\\\_label\\\_i ∈ L
```

#### Bài toán 3 — tính Impact Score

Ánh xạ hướng tác động:



BQ, BQL → +1 (lợi ích là tác động tích cực nên được có chiều là +1)
CQ, CQL, CON → -1 (chi phí và ràng buộc là những tác động tiêu cực (có thể xem xét bổ sung, vì nếu nhìn theo khía cạnh khác thì chi phí có thể là tác động tích cực, chẳng hạn đối với môi trường) nên có chiều là -1)

```

Công thức:


C\\\_i = alpha\\\*M\\\_i + beta\\\*S\\\_i + gamma\\\*D\\\_i + delta\\\*R\\\_i (với alpha + beta + gamma + delta = 1) 
C\\\_i\\\_norm = (C\\\_i - 1) / 4
ImpactScore\\\_i = s\\\_i \\\* W\\\_i \\\* C\\\_i\\\_norm
```

Trong phiên bản cơ sở:



alpha = beta = gamma = delta = 0.25
W\_i = 1.0



(giải thích rõ ràng từng chỉ số, nó dùng để làm gì và được tính như thế nào, có nguồn gốc uy tín, hay được trích dẫn trong bài báo khoa học nào,...)



## 3\. Cấu trúc thư mục đề xuất sau cập nhật

Cấu trúc mới nên là:



DTM/
├── README.md
├── README\_3\_updated.md
├── Cap\_nhat\_he\_thong\_lan\_2.md
├── Cac\_buoc\_chay\_he\_thong.md
├── requirements.txt
├── .env.example
├── .env                         # không commit
├── .gitignore
│
├── config/
│   ├── project\_config.yaml
│   ├── labels.yaml
│   ├── env\_filter\_keywords.yaml
│   └── scoring\_config.yaml
│
├── prompts/
│   ├── env\_filter\_system\_prompt.txt
│   ├── classify\_5\_labels\_system\_prompt.txt
│   └── \_archive/
│       └── classify\_system\_prompt\_old.txt
│
├── data/
│   ├── raw/
│   │   ├── Luat\_bao\_ve\_moi\_truong\_2020.json
│   │   └── .gitkeep
│   │
│   ├── interim/
│   │   |
│   │   │
│   │   ├── env\_manual\_label\_template.xlsx
│   │   ├── env\_human\_labeled\_dataset.xlsx
│   │   ├── env\_llm\_labeled\_dataset.xlsx
│   │   ├── env\_review\_dataset.xlsx
│   │   ├── environmental\_impact\_records\_final.xlsx
│   │   │
│   │   ├── class\_manual\_label\_template.xlsx
│   │   ├── class\_human\_labeled\_dataset.xlsx
│   │   ├── class\_llm\_labeled\_dataset.xlsx
│   │   ├── class\_review\_dataset.xlsx
│   │   │
│   │   ├── scoring\_input.xlsx
│   │   └── \_archive/
│   │       ├── human\_labeled\_dataset\_3labels\_backup.xlsx
│   │       └── old\_manual\_label\_template.xlsx
│   │
│   ├── processed/
│   │   ├── env\_final\_dataset.xlsx
│   │   ├── final\_labeled\_dataset.xlsx
│   │   ├── scored\_dataset.xlsx
│   │   └── pipeline\_master\_dataset.xlsx
│   │
│   └── reports/
│       ├── input\_schema\_report.xlsx
│       ├── env\_filter\_metrics.xlsx
│       ├── env\_error\_analysis.xlsx
│       ├── classification\_metrics.xlsx
│       ├── class\_error\_analysis.xlsx
│       ├── scoring\_summary.xlsx
│       ├── final\_impact\_report.xlsx
│       └── pipeline\_summary\_report.xlsx
│
├── docs/
│   ├── methodology.md
│   ├── data\_schema.md
│   ├── environmental\_filter\_guideline.md
│   ├── label\_guideline\_5\_labels.md
│   ├── adjudication\_protocol.md
│   ├── metric\_definition.md
│   ├── variable\_definition.md
│   ├── scoring\_rubric\_MSDR.md
│   ├── scoring\_rule.md
│   ├── example\_manual\_calculation.md
│   ├── literature\_justification.md
│   └── limitations\_and\_future\_work.md
│
├── src/
│   ├── 00\_common/
│   │   ├── io\_utils.py
│   │   ├── config\_loader.py
│   │   ├── label\_utils.py
│   │   ├── metric\_utils.py
│   │   └── llm\_client.py
│   │
│   ├── 01\_validate\_input\_schema.py
│   ├
│   │
│   ├── 02\_build\_env\_manual\_label\_file.py
│   ├── 03\_llm\_filter\_environmental\_impact.py
│   ├── 04\_compare\_env\_human\_vs\_llm.py
│   ├── 05\_build\_env\_final\_dataset.py
│   │
│   ├── 06\_build\_5label\_manual\_file.py
│   ├── 07\_llm\_classify\_5\_labels.py
│   ├── 08\_compare\_5label\_human\_vs\_llm.py
│   ├── 09\_build\_final\_labeled\_dataset.py
│   │
│   ├── 10\_build\_scoring\_input.py
│   ├── 11\_calculate\_impact\_score.py
│   ├── 12\_generate\_figures.py
│   ├── 13\_generate\_pipeline\_summary.py
│   └── \_archive/
│       ├── 03\_filter\_environmental\_impact\_old.py
│       ├── 04\_build\_manual\_label\_file\_old.py
│       ├── 05\_llm\_classify\_5\_labels\_old.py
│       └── 06\_compare\_llm\_vs\_human\_old.py
│
├── outputs/
│   ├── figures/
│   │   ├── data\_funnel.png
│   │   ├── env\_confusion\_matrix.png
│   │   ├── env\_metric\_summary.png
│   │   ├── label\_distribution.png
│   │   ├── classification\_metric\_by\_label.png
│   │   ├── confusion\_matrix.png
│   │   ├── normalized\_confusion\_matrix.png
│   │   ├── top\_error\_pairs.png
│   │   ├── impact\_score\_histogram.png
│   │   ├── impact\_score\_by\_label.png
│   │   ├── impact\_score\_by\_actor.png
│   │   ├── impact\_score\_by\_domain.png
│   │   ├── score\_component\_distribution.png
│   │   └── Old\_figure/
│   │
│   └── logs/
│       ├── env\_filter.log
│       ├── classification.log
│       ├── scoring.log
│       └── figures.log
│
├── references/
│   ├── README.md
│   └── ... các tài liệu tham khảo
│
└── secrets/
└── gcp\_key.json              # không commit

```

\\---

## 4\\. Chức năng chi tiết các file mới cần bổ sung

### 4.1. `config/labels.yaml`

Chứa danh sách nhãn và mapping hướng tác động.

```yaml
labels:
  BQ: BENEFIT\\\_QUANTITATIVE
  BQL: BENEFIT\\\_QUALITATIVE
  CQ: COST\\\_QUANTITATIVE
  CQL: COST\\\_QUALITATIVE
  CON: CONSTRAINT

impact\\\_direction:
  BENEFIT\\\_QUANTITATIVE: 1
  BENEFIT\\\_QUALITATIVE: 1
  COST\\\_QUANTITATIVE: -1
  COST\\\_QUALITATIVE: -1
  CONSTRAINT: -1
```

### 4.2. `config/env\\\_filter\\\_keywords.yaml`

Chứa nhóm từ khóa/dấu hiệu phục vụ lọc môi trường.

```yaml
environment\\\_domains:
  water:
    - nước thải
    - nước mặt
    - tài nguyên nước
  waste:
    - chất thải
    - chất thải nguy hại
    - thu gom
    - xử lý
  air:
    - khí thải
    - không khí
    - tiếng ồn
  climate:
    - khí nhà kính
    - biến đổi khí hậu
    - tầng ô-dôn
  eia\\\_permit:
    - đánh giá tác động môi trường
    - giấy phép môi trường
    - đăng ký môi trường
  monitoring:
    - quan trắc
    - giám sát
    - báo cáo môi trường
```

Keyword chỉ là công cụ hỗ trợ, không thay thế human label.

### 4.3. `config/scoring\\\_config.yaml`

Chứa trọng số và thang điểm.

```yaml
score\\\_range:
  min: 1
  max: 5

weights:

với phạm vi hiện tại:
  alpha: 0.25
  beta: 0.25
  gamma: 0.25
  delta: 0.25

default\\\_W\\\_i: 1.0

normalize:
  formula: "(C\\\_i - 1) / 4"
```

### 4.4. `prompts/env\\\_filter\\\_system\\\_prompt.txt`

Dùng cho LLM lọc tác động môi trường.

Output bắt buộc:

```json
{
  "env\\\_label": true,
  "reason": "...",
  "evidence\\\_span": "...",
  "confidence": 0.0,
  "needs\\\_human\\\_review": false
}
```

### 4.5. `prompts/classify\\\_5\\\_labels\\\_system\\\_prompt.txt`

Thay thế `classify\\\_system\\\_prompt.txt` hiện tại.

Output bắt buộc:

```json
{
  "label": "BENEFIT\\\_QUANTITATIVE | BENEFIT\\\_QUALITATIVE | COST\\\_QUANTITATIVE | COST\\\_QUALITATIVE | CONSTRAINT",
  "reason": "...",
  "evidence\\\_span": "...",
  "confidence": 0.0,
  "needs\\\_human\\\_review": false,
  "rule\\\_applied": "...",
  "quantity\\\_interpretation": "..."
}
```

### 4.6. `docs/environmental\\\_filter\\\_guideline.md`

Hướng dẫn người nghiên cứu gán `env\\\_human`.

Cấu trúc nên có:



1. Mục tiêu
2. Định nghĩa env\_human = 1
3. Định nghĩa env\_human = 0
4. Các domain môi trường
5. Trường hợp mơ hồ
6. Ví dụ gán đúng
7. Ví dụ gán sai
8. Quy tắc review

```

### 4.7. `docs/label\\\_guideline\\\_5\\\_labels.md`

Thay thế hoặc mở rộng `label\\\_guideline.md`.

Cần có:

1\\. Định nghĩa 5 nhãn
2. Quy tắc “có số không đồng nghĩa với định lượng”
3. Phân biệt CQL và CON
4. Phân biệt BQL và CON
5. Phân biệt CQ và CQL
6. Phân biệt BQ và BQL
7. Ví dụ minh họa từng nhãn
8. Trường hợp cần second review
```

### 4.8. `docs/adjudication\\\_protocol.md`

Quy tắc xử lý bất đồng.

Cần ghi rõ:



Metric được tính trước khi adjudication.
env\_final/final\_label chỉ dùng cho pipeline sau.
Không dùng final\_label để đánh giá LLM nếu final\_label đã được sửa sau review.
Human label là nhãn tham chiếu.
LLM label là nhãn dự đoán.
Nếu human label sai rõ ràng sau khi đọc lại, phải sửa human label và ghi review\_note.

```

### 4.9. `docs/metric\\\_definition.md`

Cần mở rộng thành hai nhóm metric:


Metric cho env filtering:
- Confusion Matrix 2x2
- Accuracy\\\_env
- Precision\\\_env
- Recall\\\_env
- F1\\\_env
- HumanCorrectionRate\\\_env

Metric cho 5-label classification:
- Confusion Matrix 5x5
- Accuracy\\\_class
- Precision\\\_k
- Recall\\\_k
- F1\\\_k
- Macro-F1
- HumanCorrectionRate\\\_class
```

### 4.10. `docs/scoring\\\_rubric\\\_MSDR.md`

Tách rõ hướng dẫn chấm:



M\_i: Magnitude
S\_i: Scope
D\_i: Duration
R\_i: Risk/Reversibility
W\_i: Object/domain weight

```

Mỗi biến phải có thang điểm 1–5 và ví dụ.

\\---

## 5\\. Cập nhật nội dung các file cũ

### 5.1. `README\\\_3\\\_updated.md`

Cần cập nhật thành README chính thức hoặc đổi tên:


README.md
```

Nội dung cần bổ sung:

* Pipeline 2 tầng: env filtering và 5-label classification.
* Phân biệt `env\\\_human`, `env\\\_llm`, `env\\\_final`.
* Phân biệt `class\\\_human`, `class\\\_llm`, `final\\\_label`.
* Metric riêng cho từng tầng.
* Cấu trúc file mới.
* Cách chạy pipeline từ script 01 đến 14.
* Cảnh báo không dùng `final\\\_label` để tính metric LLM.
* Cảnh báo không gọi `human\\\_labeled\\\_dataset.xlsx` là Gold Dataset nếu chỉ có một người gán.

### 5.2. `Cac\\\_buoc\\\_chay\\\_he\\\_thong.md`

Cần đổi thứ tự chạy từ 01–09 sang 01–14.

Phiên bản mới:



01\_validate\_input\_schema.py
02\_build\_env\_manual\_label\_file.py
03\_llm\_filter\_environmental\_impact.py
04\_compare\_env\_human\_vs\_llm.py
05\_build\_env\_final\_dataset.py
06\_build\_5label\_manual\_file.py
07\_llm\_classify\_5\_labels.py
08\_compare\_5label\_human\_vs\_llm.py
09\_build\_final\_labeled\_dataset.py
10\_build\_scoring\_input.py
11\_calculate\_impact\_score.py
12\_generate\_figures.py
13\_generate\_pipeline\_summary.py

```

### 5.3. `config/project\\\_config.yaml`

Cần thêm các khối:

```yaml
env\\\_filter:
  human\\\_label\\\_column: env\\\_human
  llm\\\_label\\\_column: env\\\_llm
  final\\\_label\\\_column: env\\\_final

classification:
  human\\\_label\\\_column: class\\\_human
  llm\\\_label\\\_column: class\\\_llm
  final\\\_label\\\_column: final\\\_label

metrics:
  zero\\\_division: 0
  average: macro

prompts:
  env\\\_filter: prompts/env\\\_filter\\\_system\\\_prompt.txt
  classify\\\_5\\\_labels: prompts/classify\\\_5\\\_labels\\\_system\\\_prompt.txt
```

### 5.4. `prompts/classify\\\_system\\\_prompt.txt`

Không nên xóa ngay. Nên đổi thành:



prompts/\_archive/classify\_system\_prompt\_old.txt

```

Sau đó tạo file mới:


prompts/classify\\\_5\\\_labels\\\_system\\\_prompt.txt
```

### 5.5. `docs/label\\\_guideline.md`

Có thể đổi tên thành:



docs/label\_guideline\_5\_labels.md

```

và bổ sung nhiều ví dụ hơn.

### 5.6. `docs/metric\\\_definition.md`

Cần cập nhật từ metric 5 nhãn sang cả hai nhóm:


env metrics
class metrics
end-to-end summary
```

### 5.7. `docs/scoring\\\_rule.md`

Cần nhấn mạnh:



Impact Score chỉ được tính sau khi có final\_label.
final\_label phải được human review.
W\_i mặc định = 1 nếu chưa có cơ sở chuyên gia.
Impact Score là bán định lượng, không phải CBA tiền tệ đầy đủ.

```

### 5.8. `src/03\\\_filter\\\_environmental\\\_impact.py`

Nếu script này đang lọc bằng keyword, nên đổi tên thành:


03\\\_rule\\\_based\\\_env\\\_filter\\\_baseline.py
```

hoặc đưa vào `\\\_archive`.

Pipeline mới cần script:



03\_build\_env\_manual\_label\_file.py
04\_llm\_filter\_environmental\_impact.py
05\_compare\_env\_human\_vs\_llm.py
06\_build\_env\_final\_dataset.py

```

### 5.9. `src/04\\\_build\\\_manual\\\_label\\\_file.py`

Đổi thành:


07\\\_build\\\_5label\\\_manual\\\_file.py
```

vì đây là file tạo template gán 5 nhãn, không phải template cho toàn bộ pipeline.

### 5.10. `src/05\\\_llm\\\_classify\\\_5\\\_labels.py`

Đổi thành:



08\_llm\_classify\_5\_labels.py

```

Đầu vào phải là:


data/processed/env\\\_final\\\_dataset.xlsx
```

hoặc:



data/interim/environmental\_impact\_records\_final.xlsx

```



### 5.11. `src/06\\\_compare\\\_llm\\\_vs\\\_human.py`

Đổi thành:


09\\\_compare\\\_5label\\\_human\\\_vs\\\_llm.py
```

Để tránh nhầm với bước so sánh env.

### 5.12. `outputs/figures/impact\\\_score\\\_by\\\_domain.png`

Cần kiểm tra lại dữ liệu trục tung. Nếu trục tung đang chứa `tin\\\_hieu\\\_tac\\\_dong` hoặc chuỗi danh sách quá dài, không nên gọi là domain.

Nên tách thành hai hình:



impact\_score\_by\_domain.png
impact\_score\_by\_legal\_signal.png

```

Domain phải là nhóm chuẩn như:

water
waste
air
climate
eia\\\_permit
monitoring
pollution\\\_control
biodiversity
environmental\\\_finance
planning\\\_state\\\_management
```

\---

## 6\. File dữ liệu đề xuất sau cập nhật

### 6.1. Dữ liệu đầu vào



data/raw/Luat\_bao\_ve\_moi\_truong\_2020.json

```

### 6.2. Mỗi bản ghi gồm:

```

Gồm:



source\_id
legal\_citation
raw\_text
co\_tac\_dong
actor
legal\_signal
domain
quantitative\_value
condition
source\_document

```

### 6.3. Bước lọc môi trường

Template human:


data/interim/env\\\_manual\\\_label\\\_template.xlsx
```

Sau human gán:



data/interim/env\_human\_labeled\_dataset.xlsx

```

Sau LLM dự đoán:


data/interim/env\\\_llm\\\_labeled\\\_dataset.xlsx
```

Sau so sánh:



data/reports/env\_filter\_metrics.xlsx
data/reports/env\_error\_analysis.xlsx

```

Sau chốt:

data/processed/env\\\_final\\\_dataset.xlsx
```

### 6.4. Bước phân loại 5 nhãn

Template human:



data/interim/class\_manual\_label\_template.xlsx

```

Sau human gán:


data/interim/class\\\_human\\\_labeled\\\_dataset.xlsx
```

Sau LLM dự đoán:



data/interim/class\_llm\_labeled\_dataset.xlsx

```

Sau so sánh:


data/reports/classification\\\_metrics.xlsx
data/reports/class\\\_error\\\_analysis.xlsx
```

Sau chốt:



data/processed/final\_labeled\_dataset.xlsx

```

### 6.5. Bước tính điểm

Template chấm điểm:


data/interim/scoring\\\_input.xlsx
```

Sau tính điểm:

data/processed/scored\_dataset.xlsx
data/reports/final\_impact\_report.xlsx
data/reports/scoring\_summary.xlsx

```

### 6.6. Báo cáo tổng pipeline


data/reports/pipeline\\\_summary\\\_report.xlsx
```

Nên gồm các sheet:



Overview
Data\_Funnel
Env\_Metrics
Class\_Metrics
Error\_Summary
Impact\_By\_Label
Impact\_By\_Domain
Impact\_By\_Actor
Top\_Positive\_Records
Top\_Negative\_Records

```

\\---

## 7\\. Script pipeline đề xuất sau cập nhật

### 7.1. `01\\\_validate\\\_input\\\_schema.py`

Kiểm tra:

\* File JSON tồn tại.
\* Mỗi record có `source\\\_id`.
\* Không trùng `source\\\_id`.
\* Không thiếu `raw\\\_text`.
\* Có `co\\\_tac\\\_dong` = true.
\* Có trường `legal\\\_citation`.
\* Báo cáo số bản ghi true.

Output:


data/reports/input\\\_schema\\\_report.xlsx
```

### 7.2. `02\\\_build\\\_env\\\_manual\\\_label\\\_file.py`

Tạo file để người nghiên cứu gán:



env\_human
env\_human\_reason
env\_needs\_review

```

Output:


data/interim/env\\\_manual\\\_label\\\_template.xlsx
```

### 7.3. `03\\\_llm\\\_filter\\\_environmental\\\_impact.py`

LLM dự đoán:



env\_llm
env\_llm\_reason
env\_evidence\_span
env\_confidence
env\_needs\_human\_review

```

Output:


data/interim/env\\\_llm\\\_labeled\\\_dataset.xlsx
```

### 7.4. `04\\\_compare\\\_env\\\_human\\\_vs\\\_llm.py`

Tính:



Confusion Matrix 2x2
Accuracy\_env
Precision\_env
Recall\_env
F1\_env
HumanCorrectionRate\_env

```

Output:


data/reports/env\\\_filter\\\_metrics.xlsx
data/reports/env\\\_error\\\_analysis.xlsx
data/interim/env\\\_review\\\_dataset.xlsx
```

### 7.5. `05\\\_build\\\_env\\\_final\\\_dataset.py`

Chốt:



env\_final

```

Output:


data/processed/env\\\_final\\\_dataset.xlsx
```

### 7.6. `06\\\_build\\\_5label\\\_manual\\\_file.py`

Tạo file gán 5 nhãn:



class\_human
class\_human\_reason
class\_needs\_review

```

Output:


data/interim/class\\\_manual\\\_label\\\_template.xlsx
```

### 7.7. `07\\\_llm\\\_classify\\\_5\\\_labels.py`

LLM dự đoán 5 nhãn:



class\_llm
class\_llm\_reason
class\_evidence\_span
class\_confidence
class\_needs\_human\_review
rule\_applied
quantity\_interpretation

```

Output:


data/interim/class\\\_llm\\\_labeled\\\_dataset.xlsx
```

### 7.8. `08\\\_compare\\\_5label\\\_human\\\_vs\\\_llm.py`

Tính:



Confusion Matrix 5x5
Accuracy\_class
Precision\_k
Recall\_k
F1\_k
MacroF1
HumanCorrectionRate\_class
Support\_k

```

Output:


data/reports/classification\\\_metrics.xlsx
data/reports/class\\\_error\\\_analysis.xlsx
data/interim/class\\\_review\\\_dataset.xlsx
```

### 7.9. `09\\\_build\\\_final\\\_labeled\\\_dataset.py`

Chốt:



final\_label

```

Output:


data/processed/final\\\_labeled\\\_dataset.xlsx
```

### 7.10. `10\\\_build\\\_scoring\\\_input.py`

Tạo file chấm:



M\_i
S\_i
D\_i
R\_i
W\_i

```

Output:


data/interim/scoring\\\_input.xlsx
```

### 7.11. `11\\\_calculate\\\_impact\\\_score.py`

Tính:

```text
direction\\\_i
C\\\_i
C\\\_i\\\_norm
ImpactScore\\\_i
```

Output:



data/processed/scored\_dataset.xlsx
data/reports/final\_impact\_report.xlsx

```

### 7.12. `12\\\_generate\\\_figures.py`

Sinh biểu đồ rõ ràng và chính xác:


data\\\_funnel.png
env\\\_confusion\\\_matrix.png
env\\\_metric\\\_summary.png
label\\\_distribution.png
classification\\\_metric\\\_by\\\_label.png
confusion\\\_matrix.png
normalized\\\_confusion\\\_matrix.png
top\\\_error\\\_pairs.png
impact\\\_score\\\_histogram.png
impact\\\_score\\\_by\\\_label.png
impact\\\_score\\\_by\\\_actor.png
impact\\\_score\\\_by\\\_domain.png
score\\\_component\\\_distribution.png
```

### 7.13. `13\\\_generate\\\_pipeline\\\_summary.py`

Tạo báo cáo tổng hợp:



pipeline\_summary\_report.xlsx

```

và có thể xuất:


pipeline\\\_summary.md
```

## 8\. Checklist thực hiện cập nhật hệ thống

### 8.1. Việc cần làm ngay



\[ ] Sao lưu toàn bộ hệ thống hiện tại.
\[ ] Tạo branch hoặc thư mục backup trước khi sửa.
\[ ] Cập nhật README theo pipeline 2 tầng.
\[ ] Tạo environmental\_filter\_guideline.md.
\[ ] Tạo env\_filter\_system\_prompt.txt.
\[ ] Đổi classify\_system\_prompt.txt thành classify\_5\_labels\_system\_prompt.txt.
\[ ] Bổ sung adjudication\_protocol.md.
\[ ] Cập nhật metric\_definition.md.
\[ ] Bổ sung scoring\_rubric\_MSDR.md.
\[ ] Cập nhật project\_config.yaml.
\[ ] Tạo labels.yaml, env\_filter\_keywords.yaml, scoring\_config.yaml.
\[ ] Tách script env filtering thành 4 bước: build human, LLM, compare, final.
\[ ] Tách script 5-label classification thành 4 bước: build human, LLM, compare, final.
\[ ] Cập nhật script generate figures để thêm metric plots.
\[ ] Di chuyển gcp\_key.json ra secrets/ hoặc đảm bảo không commit.

```

### 8.2. Việc cần kiểm tra sau khi cập nhật


\\\[ ] JSON đầu vào không thiếu source\\\_id/raw\\\_text/co\\\_tac\\\_dong.
\\\[ ] Số bản ghi co\\\_tac\\\_dong=true ở test study đúng bằng 581.
\\\[ ] env\\\_human và env\\\_llm được lưu riêng.
\\\[ ] metric\\\_env được tính trước env\\\_final.
\\\[ ] class\\\_human và class\\\_llm được lưu riêng.
\\\[ ] metric\\\_class được tính trước final\\\_label.
\\\[ ] final\\\_label được dùng cho Impact Score.
\\\[ ] Impact Score không dùng llm\\\_label trực tiếp.
\\\[ ] Có error\\\_analysis cho cả env và class.
\\\[ ] Có biểu đồ metric cho cả env và class.
\\\[ ] Có pipeline\\\_summary\\\_report.xlsx.
```

\---

## 9\. Những lỗi cần tránh

### 9.1. Không dùng `final\\\_label` để đánh giá LLM

Sai:



llm\_label vs final\_label

```

Đúng:


llm\\\_label vs human\\\_label
```

Metric phải đo chất lượng LLM trước khi con người sửa/chốt.

### 9.2. Không gọi human label là Gold Dataset nếu chưa đủ điều kiện

Nên dùng:



Human-labeled Reference Dataset

```

Chỉ dùng Gold Dataset nếu có:


nhiều annotator
đo đồng thuận
quy trình xử lý bất đồng
chuyên gia xác nhận
```

### 9.3. Không gộp metric env và metric class thành một chỉ số duy nhất

Nên báo cáo riêng:



Accuracy\_env
F1\_env
Accuracy\_class
MacroF1\_class

```

Nếu cần end-to-end summary thì chỉ dùng như chỉ số bổ sung.

### 9.4. Không gọi LLM là “học từ prompt”

Nên viết:


LLM được điều kiện hóa bởi prompt để dự đoán theo tiêu chí đã định nghĩa.
```

Không nên viết:



LLM học từ prompt.

```

### 9.5. Không đưa Monte Carlo, AHP, NPV vào pipeline chính nếu chưa triển khai

Các phần này chỉ nên nằm ở:


Chương 5 — Hướng phát triển
```

\---

## 10\. Kết luận

Cấu trúc hiện tại đã đủ nền tảng để phát triển, nhưng cần cập nhật để phản ánh đúng pipeline mới. Sự thay đổi quan trọng nhất là tách pipeline thành hai tầng đánh giá độc lập:



Tầng 1: lọc tác động môi trường
Tầng 2: phân loại 5 nhãn tác động

```

Mỗi tầng cần có:

`
human reference
LLM prediction
metric
error analysis
adjudication/final label
```

Sau hai tầng này mới chuyển sang:



Impact Score
visualization
report

```

Cấu trúc mới sẽ giúp hệ thống rõ ràng hơn, dễ code hơn, dễ kiểm tra hơn và dễ bảo vệ hơn. Đồng thời, nó giải quyết được các câu hỏi quan trọng trong hội đồng:


Metric này đo cái gì?
Human label nằm ở đâu?
LLM có được đánh giá thật không?
Nhãn cuối cùng lấy từ đâu?
Impact Score có dùng nhãn đã kiểm chứng không?
Kết quả có thể giải thích được không?
```

