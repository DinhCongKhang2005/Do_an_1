# Chương 1: MỞ ĐẦU

## 1.1. Bối cảnh và động cơ nghiên cứu

Trong hệ thống pháp luật của mỗi quốc gia, các văn bản quy phạm pháp luật đóng vai trò là công cụ điều tiết vĩ mô, định hướng hành vi của các chủ thể xã hội và thiết lập các chuẩn mực ứng xử. Đặc biệt, trong các lĩnh vực có tính chất liên ngành cao như bảo vệ môi trường, năng lượng và phát triển bền vững, các văn bản pháp lý thường sở hữu cấu trúc lập pháp vô cùng phức tạp. Một văn bản luật, ví dụ như Luật Bảo vệ môi trường năm 2020 của Việt Nam, chứa đựng hàng trăm điều khoản với nhiều tầng ngữ nghĩa đan xen. Các điều khoản này không chỉ đơn thuần đưa ra các định nghĩa mang tính khái niệm, mà còn áp đặt trực tiếp các nghĩa vụ hành chính, thiết lập các điều kiện kỹ thuật, ràng buộc pháp lý, đồng thời mở ra các chính sách khuyến khích, hỗ trợ. Các tác động này hướng tới nhiều nhóm chủ thể khác nhau trong nền kinh tế, từ các cơ quan quản lý nhà nước, các doanh nghiệp sản xuất, các chủ dự án hạ tầng cho đến cộng đồng dân cư và toàn bộ hệ sinh thái tự nhiên.

Về mặt học thuật và thực tiễn quản lý, việc đánh giá một văn bản quy phạm pháp luật trước và sau khi ban hành đòi hỏi phải áp dụng các phương pháp luận chuẩn hóa. Ba phương pháp phổ biến nhất hiện nay trên thế giới bao gồm: Đánh giá tác động quy định (Regulatory Impact Assessment - RIA) nhằm đo lường tính hiệu quả và gánh nặng hành chính của chính sách; Đánh giá tác động môi trường (Environmental Impact Assessment - EIA) nhằm dự báo các tác động sinh thái và mức độ rủi ro đối với tài nguyên thiên nhiên; và Phân tích chi phí - lợi ích (Cost-Benefit Analysis - CBA) nhằm lượng hóa các giá trị kinh tế và ngoại ứng xã hội của quy định. Sự tích hợp giữa ba phương pháp này tạo nên một khung phân tích toàn diện, giúp các nhà hoạch định chính sách có một cái nhìn định lượng rõ ràng về hiệu quả của các công cụ pháp lý.

Tuy nhiên, quy trình phân tích truyền thống đối mặt với những thách thức rất lớn về mặt nhân lực và thời gian. Việc đọc hiểu, phân loại và bóc tách thủ công hàng ngàn trang văn bản pháp lý đòi hỏi các chuyên gia phải làm việc liên tục trong nhiều tháng, dẫn đến chi phí vận hành rất cao. Quan trọng hơn, quá trình gán nhãn thủ công này thường mang tính chủ quan, phụ thuộc lớn vào kinh nghiệm cá nhân của người nghiên cứu, khiến kết quả đánh giá thiếu tính nhất quán và rất khó tái lập để đối chứng khoa học.

Trong những năm gần đây, sự trỗi dậy của các Mô hình ngôn ngữ lớn (Large Language Models - LLMs) đã mở ra một hướng đi mới cho việc tự động hóa xử lý ngôn ngữ tự nhiên trong miền pháp lý. Với khả năng hiểu ngữ cảnh phức tạp và trích xuất thông tin mạnh mẽ, các mô hình ngôn ngữ lớn có thể hỗ trợ đắc lực cho việc phân tích sơ bộ văn bản luật, rút ngắn đáng kể thời gian xử lý ban đầu. Dù vậy, trong một miền có tính chất nghiêm ngặt và đòi hỏi độ chính xác tuyệt đối như pháp lý và chính sách công, việc tin tưởng hoàn toàn vào một hệ thống trí tuệ nhân tạo tự động là vô cùng nguy hiểm. Các mô hình ngôn ngữ lớn thường gặp phải hiện tượng ảo giác (hallucination) — sinh ra các câu trả lời đọc qua có vẻ hợp lý nhưng thực chất sai lệch về mặt pháp lý. Ngoài ra, AI dễ dàng bỏ sót các điều kiện loại trừ, nhầm lẫn giữa các thuật ngữ kỹ thuật ranh giới hẹp, hoặc không thể suy luận chính xác các mối quan hệ liên kết chéo giữa các điều luật.

Từ thực tiễn đó, đồ án này lựa chọn tiếp cận bài toán theo quy trình có con người tham gia kiểm chứng (Human-in-the-loop). Trong quy trình lai này, mô hình ngôn ngữ lớn được sử dụng như một trợ lý phân loại ban đầu, đề xuất các nhãn tác động và trích xuất bằng chứng ngữ cảnh. Chuyên gia nhân văn (người nghiên cứu) đóng vai trò kiểm soát chất lượng tối cao, rà soát các bất đồng, hiệu chỉnh sai sót và phê duyệt bộ nhãn cuối cùng. Bộ dữ liệu sau khi được phê duyệt sẽ được chuyển thành các biến định lượng để tính điểm tác động chính sách theo một mô hình toán học bán định lượng rõ ràng. Động cơ nghiên cứu của đồ án là xây dựng một pipeline (chuỗi xử lý dữ liệu) minh bạch, có khả năng truy vết nguồn gốc (explainable) từ điểm số cuối cùng quay ngược trở lại các điều khoản thô trong văn bản gốc, tạo nên một công cụ hỗ trợ ra quyết định đáng tin cậy cho các nhà phân tích chính sách môi trường tại Việt Nam.

---

## 1.2. Khoảng trống nghiên cứu

Mặc dù các nghiên cứu về đánh giá tác động chính sách và xử lý văn bản pháp luật đã đạt được nhiều thành tựu, việc tổng hợp các phương pháp này vào một hệ thống lượng hóa cụ thể vẫn tồn tại những khoảng trống nghiên cứu rõ rệt sau:

* **Sự thiếu hụt dữ liệu định lượng chi tiết trong phân tích chi phí - lợi ích truyền thống:** Các mô hình CBA truyền thống thường tiếp cận chính sách từ trên xuống (top-down), đòi hỏi các số liệu tài chính vĩ mô rất lớn như dòng tiền doanh nghiệp, chi phí y tế, doanh thu thuế hoặc giá trị tiền tệ hóa của đa dạng sinh học. Tuy nhiên, trong giai đoạn thiết kế hoặc đánh giá ban đầu của một văn bản luật, các dữ liệu tài chính chi tiết này thường không tồn tại hoặc cực kỳ khó tiếp cận ở cấp độ từng điều khoản pháp lý nhỏ nhất. Điều này làm cho các mô hình CBA truyền thống bị vô hiệu hóa hoặc chỉ dừng lại ở mức dự báo mang tính phỏng đoán vĩ mô. Do đó, cần có một phương pháp tiếp cận bán định lượng (semi-quantitative) để lượng hóa tác động trực tiếp từ chính nội dung câu chữ của các điều luật khi thiếu vắng dữ liệu tiền tệ.
* **Sự đứt gãy giữa các nghiên cứu phân loại văn bản bằng học máy và mô hình lượng hóa tác động:** Các nghiên cứu ứng dụng xử lý ngôn ngữ tự nhiên và học máy trong miền pháp lý đa số chỉ tập trung giải quyết bài toán gán nhãn văn bản (phân loại nhiều lớp, nhận diện thực thể pháp lý). Các hệ thống này dừng lại ở việc báo cáo độ chính xác của mô hình phân loại mà chưa xây dựng được cầu nối logic để chuyển các nhãn phân loại định tính đó thành điểm số tác động chính sách có công thức toán học minh bạch. Một hệ thống đánh giá chính sách hoàn chỉnh cần phải chuyển dịch từ kết quả gán nhãn ("điều khoản này là ràng buộc") sang điểm số cụ thể ("mức độ tác động của ràng buộc này lên lĩnh vực nước là bao nhiêu").
* **Sự lẫn lộn giữa tác động chính sách chung và tác động môi trường chuyên biệt:** Trong các nghiên cứu trước đây, quy trình lọc văn bản thường gộp chung bước xác định tác động chính sách pháp lý với tác động môi trường. Việc thiếu phân tách rõ ràng dẫn đến việc dữ liệu đưa vào mô hình bị nhiễu lớn, khi các điều khoản mang tính thủ tục hành chính thuần túy không liên quan đến môi trường vẫn được đưa vào tính toán. Hệ thống cần một cấu trúc pipeline hai tầng rõ rệt: tầng một phân lọc nhị phân để tách biệt các điều khoản thực sự có tác động môi trường, và tầng hai thực hiện phân loại đa lớp chuyên sâu trên tập dữ liệu đã được làm sạch này.

Đồ án này được thực hiện nhằm lấp đầy các khoảng trống nghiên cứu trên bằng cách đề xuất một pipeline hai tầng kết hợp mô hình bán định lượng dựa trên bốn biến đo lường: Cường độ (Magnitude), Không gian (Scope), Thời gian (Duration), và Rủi ro (Risk) để lượng hóa tác động của Luật Bảo vệ môi trường năm 2020.

---

## 1.3. Phát biểu bài toán nghiên cứu

Bài toán nghiên cứu của đồ án được phát biểu dưới dạng toán học hóa quy trình xử lý dữ liệu pháp lý đầu vào như sau:

Giả sử một văn bản quy phạm pháp luật về môi trường được cấu trúc hóa dưới định dạng JSON thành một tập hợp hữu hạn gồm $N$ bản ghi:
$$D = \{d_1, d_2, d_3, \dots, d_N\}$$
Trong đó, mỗi bản ghi $d_i$ đại diện cho một đơn vị pháp lý nhỏ nhất (ví dụ: một khoản hoặc một điểm trong luật) độc lập và có tác động chính sách. Mỗi bản ghi $d_i$ được biểu diễn bằng bộ thông tin cấu trúc:
$$d_i = (source\_id_i, legal\_citation_i, raw\_text_i, co\_tac\_dong_i)$$
Với:
* $source\_id_i$: Mã định danh duy nhất của bản ghi.
* $legal\_citation_i$: Nguồn trích dẫn pháp lý tương ứng (ví dụ: "Điều 6, Khoản 11").
* $raw\_text_i$: Nội dung văn bản gốc của điều khoản.
* $co\_tac\_dong_i$: Biến logic nhận giá trị `true` khẳng định điều khoản có chứa tác động chính sách.

Quy trình nghiên cứu giải quyết tuần tự ba bài toán con:

### Bài toán 1: Lọc tác động môi trường (Tầng 1 - Phân lớp nhị phân)
Xây dựng hàm lọc tác động môi trường $f_{env}$ đi từ tập dữ liệu ban đầu $D$ vào tập nhãn nhị phân $\{0, 1\}$:
$$f_{env} : D \rightarrow \{0, 1\}$$
Thỏa mãn với mỗi $d_i \in D$:
$$f_{env}(d_i) = \begin{cases} 
1, & \text{nếu } d_i \text{ có tác động trực tiếp hoặc gián tiếp đến môi trường} \\ 
0, & \text{nếu } d_i \text{ không có tác động đến môi trường} 
\end{cases}$$
Mục tiêu là trích xuất tập con các điều khoản môi trường $D_{env}$:
$$D_{env} = \{d_i \in D \mid f_{env}(d_i) = 1\}$$
Với kích thước tập con là $M$ ($M \le N$). Trong thực nghiệm của đồ án đối với Luật Bảo vệ môi trường năm 2020, toàn bộ $N = 581$ điều khoản đầu vào đều được xác định thuộc tập $D_{env}$ ($M = 581$).

### Bài toán 2: Phân loại tác động chính sách (Tầng 2 - Phân loại đa lớp đơn nhãn)
Định nghĩa không gian nhãn tác động chính sách gồm 5 phần tử rời rạc đại diện cho các khía cạnh kinh tế - xã hội của chính sách:
$$L = \{BQ, BQL, CQ, CQL, CON\}$$
Trong đó:
* $BQ$ (Benefit Quantitative): Lợi ích định lượng được bằng số tiền hoặc chỉ số vật lý trực tiếp.
* $BQL$ (Benefit Qualitative): Lợi ích định tính về mặt môi trường, xã hội hoặc quản lý.
* $CQ$ (Cost Quantitative): Chi phí hoặc nghĩa vụ tài chính định lượng được trực tiếp.
* $CQL$ (Cost Qualitative): Chi phí định tính hoặc gánh nặng tuân thủ thủ tục hành chính.
* $CON$ (Constraint): Ràng buộc kỹ thuật, lệnh cấm, quy chuẩn hoặc hạn ngạch bắt buộc.

Bài toán đặt ra là tìm hàm ánh xạ phân loại $f_{class}$ đưa mỗi bản ghi $x_i \in D_{env}$ vào duy nhất một nhãn thuộc không gian $L$:
$$f_{class} : D_{env} \rightarrow L$$
Bộ nhãn dự đoán thu được từ mô hình ngôn ngữ lớn ký hiệu là $\hat{Y} = \{\hat{y}_1, \hat{y}_2, \dots, \hat{y}_M\}$, bộ nhãn chuẩn do người nghiên cứu gán làm mốc đối chứng ký hiệu là $Y = \{y_1, y_2, \dots, y_M\}$. Sau quy trình rà soát bất đồng nhãn, tập nhãn cuối cùng được chốt ký hiệu là $Y^{final} = \{y^{final}_1, y^{final}_2, \dots, y^{final}_M\}$.

### Bài toán 3: Mô hình hóa toán học lượng hóa điểm tác động (Impact Score)
Với mỗi bản ghi $x_i \in D_{env}$ đã có nhãn cuối cùng $y^{final}_i \in L$, ánh xạ nhãn này sang hướng tác động $s_i \in \{-1, +1\}$:
$$s_i = \begin{cases} 
+1, & \text{nếu } y^{final}_i \in \{BQ, BQL\} \\ 
-1, & \text{nếu } y^{final}_i \in \{CQ, CQL, CON\} 
\end{cases}$$
Người nghiên cứu thực hiện chấm điểm bán định lượng cho 4 biến thành phần trên thang đo Likert $[1, 5]$ gồm: Cường độ ($M_i$), Không gian ($S_i$), Thời gian ($D_i$), và Rủi ro môi trường ($R_i$). 

Điểm tác động tổng hợp chưa chuẩn hóa $C_i$ được tính bằng phương pháp cộng tuyến tính có trọng số thành phần:
$$C_i = \alpha M_i + \beta S_i + \gamma D_i + \delta R_i$$
Với các trọng số thỏa mãn điều kiện ràng buộc: $\alpha + \beta + \gamma + \delta = 1$ (mặc định chọn $\alpha = \beta = \gamma = \delta = 0.25$).
Chuẩn hóa điểm số về khoảng giá trị $[0, 1]$:
$$C_{norm\_i} = \frac{C_i - 1}{4}$$
Tính toán điểm tác động cuối cùng $ImpactScore_i$ của từng bản ghi bằng cách kết hợp hướng tác động $s_i$ và trọng số ưu tiên chủ thể $W_i$ (mặc định $W_i = 1.0$):
$$ImpactScore_i = s_i \times W_i \times C_{norm\_i}$$
Tổng điểm tác động tích lũy của toàn bộ văn bản chính sách ($TotalImpact$) được xác định bởi hàm mục tiêu:
$$TotalImpact = \sum_{i=1}^{M} ImpactScore_i$$

---

## 1.4. Mục tiêu nghiên cứu

Để giải quyết trọn vẹn bài toán nghiên cứu đã phát biểu, đồ án thiết lập 4 mục tiêu cụ thể sau:

1. **Xây dựng chuỗi xử lý (pipeline) dữ liệu pháp lý chuẩn hóa:** Thiết kế và triển khai quy trình kỹ thuật chuyển đổi văn bản quy phạm pháp luật từ định dạng thô sang JSON có cấu trúc, đảm bảo khả năng truy vết thông tin hai chiều giữa kết quả lượng hóa cuối cùng và nội dung điều khoản gốc.
2. **Triển khai phân loại tác động bằng mô hình ngôn ngữ lớn:** Thiết kế các bộ prompt chuyên biệt cho bài toán lọc môi trường (Tầng 1) và phân loại 5 nhãn tác động (Tầng 2). Sử dụng mô hình ngôn ngữ lớn để tự động hóa việc gán nhãn, trích xuất lý do lập luận và bằng chứng ngữ cảnh nhằm giảm thiểu công sức đọc hiểu thủ công.
3. **Thiết lập quy trình kiểm chứng Human-in-the-loop và đo lường hiệu năng:** Xây dựng giao thức xử lý bất đồng nhãn (Adjudication Protocol) để người nghiên cứu đối chiếu và hiệu chuẩn dữ liệu. Tính toán các metric học máy tiêu chuẩn như Accuracy, Precision, Recall, F1-score, Macro-F1 để đánh giá khách quan năng lực phân tích pháp lý của AI so với chuyên gia con người.
4. **Hiện thực hóa mô hình toán học lượng hóa và trực quan hóa tác động:** Áp dụng mô hình bán định lượng để tính điểm tác động chính sách ($ImpactScore_i$). Thực hiện phân tích thống kê mô tả, tổng hợp điểm số theo lĩnh vực môi trường và nhóm chủ thể chịu điều chỉnh, từ đó sinh các biểu đồ trực quan hóa chuyên nghiệp phục vụ phân tích chính sách.

---

## 1.5. Cấu trúc đồ án

Báo cáo đồ án được cấu trúc thành 4 chương chính như sau:

* **Chương 1: Mở đầu:** Giới thiệu bối cảnh, động cơ nghiên cứu, chỉ ra các khoảng trống khoa học hiện tại, phát biểu bài toán nghiên cứu dưới dạng toán học, xác định mục tiêu và cấu trúc tổng thể của đồ án.
* **Chương 2: Cơ sở Phương pháp và Kiến trúc Hệ thống:** Trình bày chi tiết cơ sở lý thuyết của RIA, EIA, CBA và vai trò của mô hình ngôn ngữ lớn. Mô tả chi tiết kiến trúc hệ thống, quy trình Human-in-the-loop, ma trận nhầm lẫn, các quy tắc chuẩn hóa đối tượng/lĩnh vực và xây dựng mô hình toán học bán định lượng tính điểm tác động.
* **Chương 3: Thực nghiệm và Đánh giá kết quả:** Mô tả thiết lập thực nghiệm trên đối tượng Luật Bảo vệ môi trường năm 2020. Trình bày và phân tích các kết quả định lượng thu được qua từng bước chạy pipeline: hiệu năng phân loại của LLM, kết quả rà soát Actor/Domain, thống kê mô tả điểm tác động chính sách tổng hợp và chi tiết theo nhóm đối tượng/lĩnh vực. Phân tích định tính các điều khoản tác động điển hình.
* **Chương 4: Kết luận và Hướng phát triển:** Tổng kết lại các đóng góp chính của đồ án, trả lời các câu hỏi nghiên cứu, thẳng thắn nhìn nhận những hạn chế kỹ thuật hiện tại và đề xuất các hướng nghiên cứu mở rộng khả thi trong tương lai.
