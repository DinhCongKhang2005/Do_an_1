# Chương 3: THIẾT LẬP THỰC NGHIỆM VÀ KẾT QUẢ

## 3.1. Thiết lập thực nghiệm

Thực nghiệm của đồ án được triển khai nhằm kiểm định tính khả thi và hiệu quả của pipeline hai tầng có sự tham gia kiểm chứng của con người (Human-in-the-loop) đối với văn bản quy phạm pháp luật môi trường tại Việt Nam.

* **Đối tượng thực nghiệm:** Luật Bảo vệ môi trường năm 2020. Văn bản được tách cấu trúc và tiền xử lý thành $N = 581$ bản ghi pháp lý dạng JSON. Mọi bản ghi thô đầu vào đều được xác nhận có tác động chính sách (`co_tac_dong = true`).
* **Môi trường và công cụ thực hiện:**
  * Mô hình ngôn ngữ lớn (LLM): Google Gemini 3.5 Flash được gọi thông qua thư viện API chính thức.
  * Tham số cấu hình LLM: $Temperature = 0.0$ nhằm đảm bảo tính nhất quán tối đa và hạn chế tính ngẫu nhiên trong các câu trả lời; độ trễ gọi API (LLM delay) được đặt ở mức $0.5$ giây nhằm tuân thủ giới hạn băng thông (rate limit).
  * Trọng số mặc định cho mô hình toán học: Trọng số của 4 tiêu chí thành phần trong mô hình bán định lượng được phân bổ đều: $\alpha = \beta = \gamma = \delta = 0.25$. Trọng số ưu tiên của chủ thể $W_i = 1.0$ cho toàn bộ các bản ghi nhằm làm điểm mốc cơ sở (baseline) phục vụ phân tích so sánh.

---

## 3.2. Kết quả thực nghiệm Giai đoạn 2: Lọc tác động môi trường (Tầng 1)

Giai đoạn lọc tác động môi trường hoạt động như một bộ phân lớp nhị phân tiên quyết nhằm loại bỏ các điều khoản thuần túy mang tính thủ tục hành chính chung không liên quan đến khía cạnh sinh thái.

Do đối tượng thực nghiệm là Luật Bảo vệ môi trường năm 2020 — một đạo luật chuyên ngành, thực nghiệm ghi nhận toàn bộ $N = 581$ điều khoản thô đầu vào đều chứa đựng các tác động trực tiếp hoặc gián tiếp đến môi trường. Cụ thể:

* Nhãn chuẩn thủ công của người nghiên cứu: $env\_human_i = 1$ cho toàn bộ 581 bản ghi.
* Nhãn dự đoán của mô hình ngôn ngữ lớn: $env\_llm_i = 1$ cho toàn bộ 581 bản ghi.

Hệ thống tính toán các metric hiệu năng của LLM ở Tầng 1 và thu được kết quả:
* Số lượng mẫu khớp nhau (agreement): $581/581$ bản ghi ($100\%$).
* Số lượng mẫu lệch nhau (disagreement): $0/581$ bản ghi ($0\%$).
* Các chỉ số: $Accuracy\_env = 1.0$, $Precision\_env = 1.0$, $Recall\_env = 1.0$, $F1\_env = 1.0$.
* Tỷ lệ hiệu đính thủ công của con người ở Tầng 1: $HCR\_env = 0.0$.

*Ý nghĩa thực nghiệm:* Kết quả này cho thấy mô hình ngôn ngữ lớn hoàn thành tốt nhiệm vụ nhận diện tính chất môi trường ở lớp thô đối với một đạo luật chuyên ngành. Tập dữ liệu môi trường chốt sau giai đoạn này giữ nguyên số lượng $M = 581$ bản ghi để chuyển tiếp sang Tầng 2.

---

## 3.3. Kết quả thực nghiệm Giai đoạn 3: Phân loại tác động 5 nhãn (Tầng 2)

Tại Tầng 2, nhiệm vụ phân loại đa lớp phức tạp hơn nhiều khi mô hình ngôn ngữ lớn bắt buộc phải nhận diện chính xác bản chất chính sách môi trường của từng điều luật trong 5 nhóm nhãn tác động.

### 3.3.1. Đánh giá hiệu năng tổng thể của LLM
So sánh kết quả dự đoán của LLM với nhãn tham chiếu của người nghiên cứu trước khi thực hiện quy trình hiệu chuẩn nhãn, hệ thống ghi nhận các chỉ số hiệu năng tổng hợp như sau:

* **Độ chính xác toàn hệ thống ($Accuracy\_class$):** $69.19\%$ ($402/581$ bản ghi dự đoán đúng).
* **Chỉ số Macro-F1 ($Macro\text{-}F1\_class$):** $25.47\%$.
* **Tỷ lệ sửa lỗi của con người ($HCR\_class$):** $30.81\%$ ($179/581$ bản ghi bắt buộc phải có sự hiệu chỉnh thủ công của người nghiên cứu để sửa các sai lệch của LLM).

### 3.3.2. Hiệu năng phân loại theo từng nhãn tác động
Bảng dưới đây trình bày chi tiết hiệu năng phân loại của LLM trên từng lớp nhãn thuộc không gian nhãn tác động chính sách:

**Bảng 3.1: Chi tiết hiệu năng phân loại của LLM trên từng nhãn tác động**

| Nhãn Tác động | Mã Nhãn | Độ chính xác (Precision) | Độ nhạy (Recall) | F1-Score | Kích thước mẫu (Support) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Lợi ích định lượng** | BQ | 0.00% | 0.00% | 0.00% | 0 |
| **Lợi ích định tính** | BQL | 4.76% | 4.55% | 4.65% | 22 |
| **Chi phí định lượng** | CQ | 0.00% | 0.00% | 0.00% | 0 |
| **Chi phí định tính** | CQL | 84.02% | 76.94% | 80.32% | 451 |
| **Ràng buộc** | CON | 36.73% | 50.00% | 42.35% | 108 |

*Phân tích kết quả:*
* Nhãn **Chi phí định tính (CQL)** chiếm ưu thế vượt trội trong tập mẫu thực tế ($77.6\%$ số điều luật). Nhờ kích thước mẫu lớn, LLM đạt hiệu năng nhận diện rất tốt với Precision đạt $84.02\%$ và F1-score đạt $80.32\%$.
* Ngược lại, đối với nhãn thiểu số như **Lợi ích định tính (BQL)** (chỉ có 22 mẫu), hiệu năng của mô hình sụt giảm nghiêm trọng ($F1 = 4.65\%$), Precision chỉ đạt $4.76\%$. Đây là minh chứng rõ nét cho thấy LLM bị ảnh hưởng tiêu cực bởi sự mất cân bằng dữ liệu cực đoan trong văn bản luật.
* Lớp **Ràng buộc (CON)** có hiệu năng trung bình ($F1 = 42.35\%$), với Recall đạt $50.00\%$, phản ánh việc mô hình ngôn ngữ lớn thường xuyên phân loại nhầm giữa tính chất "ràng buộc kỹ thuật/lệnh cấm" và "nghĩa vụ chi phí thủ tục".

### 3.3.3. Phân tích lỗi phân loại (Error Analysis)
Ma trận nhầm lẫn đa lớp chỉ ra rằng cặp nhầm lẫn phổ biến nhất là việc LLM dự đoán nhầm các điều khoản thuộc nhãn `CONSTRAINT` (ràng buộc) và `BENEFIT_QUALITATIVE` (lợi ích định tính) thành nhãn `COST_QUALITATIVE` (chi phí định tính). Cụ thể:
* Có tới $45.4\%$ ($49/108$) điều khoản ràng buộc thực tế bị mô hình gán nhầm thành chi phí định tính.
* Có tới $68.2\%$ ($15/22$) điều khoản lợi ích định tính thực tế bị mô hình gán nhầm thành chi phí định tính.

*Nguyên nhân khoa học:* Sự nhập nhằng về mặt ngữ nghĩa trong hành văn pháp lý là nguyên nhân chính. Ví dụ, một điều khoản bắt buộc doanh nghiệp "phải xây dựng công trình xử lý chất thải đạt quy chuẩn kỹ thuật" vừa mang tính chất ràng buộc kỹ thuật (`CONSTRAINT`), vừa tạo ra chi phí tuân thủ vận hành (`COST_QUALITATIVE`). LLM có xu hướng chọn nhãn phổ biến nhất (CQL) khi ngữ cảnh mang tính lưỡng tính. Việc gán nhầm từ CONSTRAINT sang CQL không làm thay đổi hướng tác động ($s_i = -1$) nhưng làm giảm độ nghiêm trọng vật lý khi tính điểm. Tuy nhiên, việc gán nhầm từ BQL sang CQL làm đảo ngược hoàn toàn vector hướng tác động từ dương sang âm, gây sai số nghiêm trọng cho mô hình lượng hóa nếu không có bước hiệu chỉnh thủ công của con người.

---

## 3.4. Kết quả thực nghiệm Giai đoạn 3b: Chuẩn hóa và Kiểm định Actor/Domain

Quy trình chuẩn hóa Actor/Domain tự động quét dựa trên từ khóa pháp lý đã phát hiện các vấn đề và kết xuất báo cáo kiểm định:

* Tổng số bản ghi thực hiện kiểm định: 581 bản ghi.
* Số lượng lỗi nghiêm trọng (`ERROR`): 0 lỗi.
* Số lượng cảnh báo rà soát (`WARNING`): 160 cảnh báo.
* Trạng thái kiểm định: Đạt yêu cầu để chuyển tiếp sang bước chấm điểm.

*Phân tích cảnh báo:* 160 cảnh báo chủ yếu thuộc về trường hợp một điều luật được gán vào nhóm chủ thể chung `GENERAL_ORGANIZATION_INDIVIDUAL` nhưng chứa đựng các từ khóa liên quan đến khối kinh tế hoặc cơ quan công quyền, hoặc các điều khoản thuộc lĩnh vực rủi ro cao nhưng thang điểm đề xuất cần được người nghiên cứu hiệu chuẩn lại thủ công để phản ánh chính xác phạm vi ảnh hưởng thực tế. Sau khi người nghiên cứu hiệu chỉnh các cảnh báo này, tập dữ liệu đạt tính nhất quán logic tuyệt đối trước khi bước vào chấm điểm.

---

## 3.5. Kết quả thực nghiệm Giai đoạn 4: Lượng hóa điểm tác động (Impact Score)

### 3.5.1. Thống kê mô tả điểm tác động toàn dataset
Sau khi chạy thuật toán tính điểm tích lũy trên tập dữ liệu đã hiệu chuẩn cuối cùng ($N = 581$), hệ thống thu được các thông số thống kê mô tả tổng quan:

**Bảng 3.2: Thống kê mô tả điểm tác động tích lũy toàn bộ văn bản**

| Chỉ số lượng hóa | Giá trị điểm số | Diễn giải ý nghĩa học thuật |
| :--- | :---: | :--- |
| **Tổng điểm tác động ($TotalImpact$)** | -362.5000 | Điểm tác động tích lũy của toàn bộ văn bản luật. |
| **Điểm trung bình ($MeanImpact$)** | -0.6239 | Điểm tác động trung bình trên mỗi điều khoản. |
| **Độ lệch chuẩn ($StdImpact$)** | 0.2356 | Mức độ phân tán điểm số xung quanh giá trị trung bình. |
| **Điểm tác động dương cao nhất ($MaxImpact$)** | +0.8125 | Giá trị ưu đãi/khuyến khích lớn nhất ghi nhận được. |
| **Điểm tác động âm thấp nhất ($MinImpact$)** | -0.9375 | Mức độ ràng buộc/chi phí tuân thủ nghiêm ngặt nhất. |
| **Số điều khoản mang tác động tiêu cực** | 566 | Chiếm $97.42\%$ tổng số điều luật điều chỉnh. |
| **Số điều khoản mang tác động tích cực** | 15 | Chiếm $2.58\%$ tổng số điều luật điều chỉnh. |

*Diễn giải kết quả:* Tổng điểm tác động tích lũy đạt giá trị âm lớn ($-362.5000$) phản ánh đúng bản chất đặc thù của Luật Bảo vệ môi trường năm 2020. Văn bản lập pháp này tập trung thiết lập các hành lang pháp lý bắt buộc, phân định trách nhiệm kiểm soát ô nhiễm, quy chuẩn xả thải và nghĩa vụ báo cáo hành chính. Điểm số âm này đại diện cho **gánh nặng tuân thủ pháp luật tương đối** mà xã hội phải thực hiện để đổi lấy lợi ích bảo vệ môi trường dài hạn, không nên diễn giải đây là tác động tiêu cực của chính sách đối với sự phát triển kinh tế.

### 3.5.2. Phân tích điểm tác động theo Nhãn, Lĩnh vực và Nhóm chủ thể

#### A. Phân tích theo nhóm nhãn tác động chốt cuối cùng (final_label)
Tập nhãn cuối cùng sau khi con người hiệu chuẩn ghi nhận sự phân bổ điểm như sau:

**Bảng 3.3: Thống kê điểm tác động phân bổ theo nhãn cuối cùng**

| Nhãn Tác động Cuối cùng | Số lượng điều khoản | Tỷ lệ (%) | Điểm tác động TB ($MeanImpact$) | Tổng điểm tác động |
| :--- | :---: | :---: | :---: | :---: |
| **Lợi ích định tính (BQL)** | 15 | 2.58% | +0.6625 | +9.9375 |
| **Ràng buộc (CON)** | 122 | 21.00% | -0.7628 | -93.0625 |
| **Chi phí định tính (CQL)** | 444 | 76.42% | -0.6292 | -279.3750 |

*Nhận xét:* Lớp nhãn `COST_QUALITATIVE` (chi phí định tính) chiếm đa số tuyệt đối và đóng góp lớn nhất vào tổng điểm âm. Tuy nhiên, nhãn `CONSTRAINT` (ràng buộc) có điểm trung bình âm mạnh hơn ($-0.7628$ so với $-0.6292$). Điều này phản ánh tính nghiêm ngặt vượt trội của các điều khoản thiết lập tiêu chuẩn kỹ thuật, hạn ngạch hoặc lệnh cấm so với các nghĩa vụ mang tính thủ tục hành chính hoặc báo cáo định kỳ.

#### B. Phân tích theo lĩnh vực môi trường chính (domain_primary)
Phân tích điểm tác động theo lĩnh vực giúp xác định các trọng tâm điều chỉnh của văn bản luật:

**Bảng 3.4: Điểm tác động phân bổ theo lĩnh vực môi trường**

| Lĩnh vực môi trường chính | Số lượng điều khoản | Điểm tác động TB | Tổng điểm tác động |
| :--- | :---: | :---: | :---: |
| **Tài nguyên nước** (`water`) | 153 | -0.6520 | -99.7500 |
| **Chất độc hại & Hóa chất** (`hazardous_substances`) | 112 | -0.7193 | -80.5625 |
| **Chất thải** (`waste`) | 111 | -0.5755 | -63.8750 |
| **ĐTM, Cấp phép & Đăng ký** (`eia_permit_registration`) | 93 | -0.5504 | -51.1875 |
| **Biến đổi khí hậu & Cacbon** (`climate_carbon`) | 4 | -0.8438 | -3.3750 |
| **Đa dạng sinh học** (`biodiversity_natural_heritage`) | 11 | -0.7614 | -8.3750 |

*Nhận xét:* Lĩnh vực **Tài nguyên nước** gánh chịu tổng điểm tác động âm lớn nhất ($-99.75$), thể hiện đây là lĩnh vực có mức độ điều tiết dày đặc nhất. Trái lại, lĩnh vực **Biến đổi khí hậu & Cacbon** dù có số lượng điều khoản rất ít ($N=4$) nhưng có điểm trung bình âm mạnh nhất ($-0.8438$). Điều này chứng minh rằng các nghĩa vụ liên quan đến giảm phát thải và bảo vệ tầng ô-dôn có tính chất ràng buộc kỹ thuật đặc biệt nghiêm ngặt và rủi ro sinh thái dài hạn rất cao.

#### C. Phân tích theo nhóm chủ thể chịu điều chỉnh (actor_group)
Phân bổ điểm tác động theo các nhóm chủ thể xã hội chịu điều chỉnh:

**Bảng 3.5: Điểm tác động phân bổ theo nhóm chủ thể**

| Nhóm chủ thể chịu tác động | Số lượng điều khoản | Điểm tác động TB | Tổng điểm tác động |
| :--- | :---: | :---: | :---: |
| **Tổ chức, cá nhân chung** (`GENERAL_ORGANIZATION_INDIVIDUAL`) | 193 | -0.6580 | -127.0000 |
| **Cơ quan quản lý Nhà nước** (`STATE_AGENCY`) | 179 | -0.6383 | -114.2500 |
| **Chủ dự án đầu tư, hạ tầng** (`PROJECT_OWNER_INFRASTRUCTURE`) | 102 | -0.5778 | -58.9375 |
| **Doanh nghiệp, cơ sở SXKD** (`BUSINESS_FACILITY`) | 87 | -0.5999 | -52.1875 |
| **Cộng đồng dân cư, làng nghề** (`COMMUNITY_CRAFT_VILLAGE`) | 20 | -0.5062 | -10.1250 |

*Nhận xét:* Điểm tác động âm tập trung lớn nhất ở nhóm **Tổ chức, cá nhân chung** và **Cơ quan quản lý Nhà nước**. Kết quả này làm nổi bật luận điểm: Luật Bảo vệ môi trường năm 2020 không chỉ định hướng điều tiết khối doanh nghiệp sản xuất trực tiếp, mà còn phân bổ một phần trách nhiệm hành chính và nghĩa vụ vệ sinh môi trường khổng lồ lên hệ thống cơ quan công quyền và đời sống dân sinh xã hội.

### 3.5.3. Phân tích định tính các trường hợp tác động cực đoan điển hình (Outliers)

Để làm rõ tính giải thích được (explainability) của mô hình toán học, ta tiến hành phân tích sâu hai trường hợp điển hình đại diện cho hai đầu điểm số tác động:

#### A. Trường hợp tác động âm mạnh nhất: Bản ghi `1.6.11.0` (Điều 6, Khoản 11)
* **Nội dung pháp lý gốc:** *"Cấm các hành vi sản xuất, nhập khẩu, tạm nhập, tái xuất, tiêu thụ chất làm suy giảm tầng ô-dôn trái quy định của điều ước quốc tế..."*
* **Tham số lượng hóa:** Nhãn chốt: `CONSTRAINT` $\rightarrow$ hướng tác động $s_i = -1$; Cường độ $M_i = 5$ (lệnh cấm tuyệt đối); Không gian $S_i = 5$ (phạm vi toàn quốc và liên quan quốc tế); Thời gian $D_i = 4$ (tác động dài hạn); Mức rủi ro lĩnh vực $R_i = 5$ (suy giảm tầng ô-dôn có rủi ro sinh thái toàn cầu và không thể phục hồi).
* **Kết quả tính điểm:** Điểm thô chưa chuẩn hóa $C_i = 0.25 \times (5 + 5 + 4 + 5) = 4.75$. Điểm chuẩn hóa $C_{norm\_i} = (4.75 - 1)/4 = 0.9375$. Điểm tác động cuối cùng $ImpactScore = -1 \times 1.0 \times 0.9375 = -0.9375$.
* **Diễn giải học thuật:** Đây là điểm số tiệm cận mức tối đa của thang đo. Kết quả này phản ánh chính xác tính chất nghiêm ngặt bậc nhất của luật pháp đối với các hành vi gây suy hại sinh thái nghiêm trọng và vi phạm cam kết quốc tế.

#### B. Trường hợp tác động dương cao nhất: Bản ghi `1.58.2.0` (Điều 58, Khoản 2)
* **Nội dung pháp lý gốc:** *"Nhà nước khuyến khích và có chính sách ưu đãi, hỗ trợ cho tổ chức, cá nhân tham gia thực hiện các hoạt động tuần hoàn nước, xử lý và tái sử dụng nước thải đạt chuẩn..."*
* **Tham số lượng hóa:** Nhãn chốt: `BENEFIT_QUALITATIVE` $\rightarrow$ hướng tác động $s_i = +1$; Cường độ $M_i = 4$ (chính sách ưu đãi hỗ trợ lớn); Không gian $S_i = 5$ (áp dụng rộng rãi toàn quốc); Thời gian $D_i = 4$ (có tính dài hạn); Mức rủi ro lĩnh vực $R_i = 4$ (lĩnh vực an ninh nguồn nước có rủi ro cao nếu không bảo vệ).
* **Kết quả tính điểm:** Điểm thô chưa chuẩn hóa $C_i = 0.25 \times (4 + 5 + 4 + 4) = 4.25$. Điểm chuẩn hóa $C_{norm\_i} = (4.25 - 1)/4 = 0.8125$. Điểm tác động cuối cùng $ImpactScore = +1 \times 1.0 \times 0.8125 = +0.8125$.
* **Diễn giải học thuật:** Điểm tác động dương cao phản ánh vai trò kiến tạo và thúc đẩy của luật pháp. Quy định này tạo động lực tài chính và kỹ thuật mạnh mẽ khuyến khích khối tư nhân đầu tư vào các công nghệ kinh tế tuần hoàn nước.

---

## 3.6. Thảo luận và Nhận xét kết quả thực nghiệm

Kết quả thực nghiệm đã chứng minh tính đúng đắn và khả thi của hệ thống DTM, đồng thời mở ra các nhận định khoa học quan trọng:

1. **AI không thể thay thế con người trong miền pháp lý:** Với tỷ lệ sửa lỗi $HCR = 30.81\%$ ở Tầng 2, thực nghiệm chứng minh rằng các mô hình ngôn ngữ lớn hiện tại chỉ nên đóng vai trò là công cụ lọc và gợi ý nhãn sơ bộ. Việc thiếu vắng bước kiểm chứng của chuyên gia con người sẽ dẫn tới sai lệch cực kỳ nghiêm trọng trong việc xác định hướng tác động ($s_i$) của chính sách, từ đó làm vô hiệu hóa giá trị của mô hình lượng hóa phía sau.
2. **Hiện tượng thiên lệch của AI đối với lớp dữ liệu lớn:** Sự sụt giảm F1-score nghiêm trọng ở lớp BQL ($4.65\%$) so với lớp CQL ($80.32\%$) khẳng định thách thức lớn của LLM khi xử lý dữ liệu bị mất cân bằng. Điều này đặt ra yêu cầu kỹ thuật cho các nghiên cứu tiếp theo: cần tối ưu hóa prompt bằng kỹ thuật vài lượt mẫu (few-shot prompting) hoặc tinh chỉnh mô hình chuyên biệt để nâng cao độ nhạy đối với các điều khoản mang tính khuyến khích/lợi ích.
3. **Mô hình toán học bán định lượng có tính giải thích tốt:** Khung tính điểm MSDR đã lượng hóa thành công các điều khoản văn bản phi cấu trúc thành dữ liệu số có khả năng so sánh trực tiếp. Việc điểm số cuối cùng được xây dựng từ các tiêu chí vật lý có định nghĩa rõ ràng ($M, S, D, R$) giúp kết quả chấm điểm đạt tính minh bạch cao, dễ dàng giải thích và truy vết nguồn gốc pháp lý cho từng điều khoản cụ thể.
