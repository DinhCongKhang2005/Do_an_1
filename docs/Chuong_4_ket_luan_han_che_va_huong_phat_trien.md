# Chương 4: KẾT LUẬN, HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN

## 4.1. Kết luận

Đồ án đã nghiên cứu và xây dựng thành công hệ thống DTM — Đánh giá tác động chính sách môi trường theo hướng RIA–EIA–CBA kết hợp Mô hình ngôn ngữ lớn (LLM) và quy trình có con người tham gia kiểm chứng (Human-in-the-loop). Đối tượng thực nghiệm là Luật Bảo vệ môi trường năm 2020 ($N = 581$ bản ghi) đã chứng minh tính khả thi và độ tin cậy khoa học của toàn bộ pipeline đề xuất. Từ các kết quả định lượng và phân tích chuyên sâu, đồ án rút ra các kết luận quan trọng sau:

* **Tính khả thi của chuỗi xử lý (pipeline) dữ liệu pháp lý hai tầng:** Đồ án đã hiện thực hóa thành công một quy trình chuyển đổi văn bản quy phạm pháp luật dạng phi cấu trúc sang dữ liệu JSON có cấu trúc, tách bạch rõ ràng hai giai đoạn lọc: lọc nhị phân xác định tác động môi trường (Tầng 1) và phân loại đa lớp xác định tính chất chính sách (Tầng 2). Quy trình này đảm bảo tính minh bạch khoa học thông qua khả năng truy vết hai chiều (explainable AI) từ điểm tác động cuối cùng quay ngược trở lại các đoạn văn bản gốc (`raw_text`) và nguồn trích dẫn pháp lý (`legal_citation`).
* **Vai trò của quy trình kiểm chứng Human-in-the-loop:** Kết quả thực nghiệm tại Tầng 2 với độ chính xác phân loại của LLM đạt $69.19\%$ và chỉ số Macro-F1 đạt $25.47\%$ chỉ ra rằng các mô hình ngôn ngữ lớn hiện tại chưa thể tự động hóa hoàn toàn trong miền pháp lý. Tỷ lệ hiệu đính của con người $HCR = 30.81\%$ khẳng định vai trò kiểm soát chất lượng tối cao của chuyên gia để sửa đổi các nhầm lẫn nghiêm trọng của AI (đặc biệt là lỗi gán nhầm từ nhãn lợi ích sang nhãn chi phí gây đảo ngược hướng tác động $s_i$), bảo đảm độ tin cậy tuyệt đối của dữ liệu trước khi chấm điểm.
* **Ý nghĩa thực tiễn của mô hình lượng hóa bán định lượng:** Mô hình toán học bán định lượng dựa trên Khung tiêu chí MSDR (Cường độ, Không gian, Thời gian, Rủi ro) kết hợp vector hướng tác động đã lượng hóa thành công nội dung định tính của văn bản luật thành các giá trị số có thể so sánh trực tiếp. Điểm tác động tích lũy toàn bộ văn bản $TotalImpact = -362.5000$ và trung bình mỗi điều khoản $MeanImpact = -0.6239$ cho thấy Luật Bảo vệ môi trường năm 2020 chủ yếu thiết lập các nghĩa vụ hành chính, quy chuẩn kỹ thuật và điều kiện bắt buộc nhằm chủ động phòng ngừa rủi ro sinh thái. Điều này chứng minh vai trò điều tiết và kiểm soát nguồn thải của nhà nước, không mang ý nghĩa tiêu cực đối với sự phát triển kinh tế vĩ mô.

---

## 4.2. Hạn chế của đồ án

Mặc dù hệ thống đã vận hành ổn định và đạt được các mục tiêu đề ra, nghiên cứu vẫn tồn tại một số hạn chế kỹ thuật cần được thẳng thắn nhìn nhận:

* **Sự phụ thuộc vào chất lượng bóc tách cấu trúc dữ liệu đầu vào:** Pipeline hoạt động dựa trên giả định tệp dữ liệu JSON đầu vào đã được phân mảnh chuẩn hóa thành các đơn vị pháp lý độc lập có nghĩa nghĩa phân tích độc lập. Nếu quá trình tiền xử lý văn bản thô (như chuyển từ tệp PDF/Word gốc sang JSON) bị lỗi cấu trúc, thiếu trường nội dung hoặc gộp quá nhiều nghĩa vụ phức tạp vào một bản ghi, độ chính xác phân loại của LLM và tính chính xác của điểm chấm thành phần sẽ bị ảnh hưởng lớn.
* **Tính chủ quan của bộ nhãn chuẩn tham chiếu (Ground Truth):** Trong phạm vi thực hiện đồ án, tập nhãn chuẩn tham chiếu (Human-labeled Reference Dataset) hoàn toàn do một người nghiên cứu gán nhãn và chấm điểm dựa trên hướng dẫn. Điều này có thể dẫn đến sai số chủ quan hệ thống do thiên kiến cá nhân, thiếu sự đánh giá đồng đồng thuận đa chủ thể để kiểm chứng độ tin cậy liên chủ thể (Inter-Annotator Agreement).
* **Hiệu năng phân loại kém của LLM trên các nhãn thiểu số:** Mô hình ngôn ngữ lớn gặp khó khăn nghiêm trọng khi phân loại các lớp nhãn có kích thước mẫu quá nhỏ như `BENEFIT_QUALITATIVE` ($F1 = 4.65\%$) do hiện tượng mất cân bằng dữ liệu tự nhiên của văn bản luật bảo vệ môi trường (đa số điều khoản là chi phí và ràng buộc). Prompt hiện tại chưa tối ưu hóa để khắc phục triệt để hiện tượng thiên lệch này của AI.
* **Giả định đơn giản hóa trong mô hình tính điểm:** Mô hình tính điểm hiện tại đang sử dụng các giả định đơn giản hóa như gán trọng số thành phần bằng nhau ($\alpha = \beta = \gamma = \delta = 0.25$) và trọng số chủ thể bằng nhau ($W_i = 1.0$) cho toàn bộ điều luật. Điều này chưa phản ánh được sự ưu tiên chính sách khác nhau đối với từng lĩnh vực cụ thể hoặc mức độ nhạy cảm sinh thái của từng nhóm đối tượng chịu ảnh hưởng.

---

## 4.3. Hướng phát triển trong tương lai

Từ các hạn chế nêu trên, đồ án định hướng các bước phát triển và nghiên cứu mở rộng trong tương lai như sau:

* **Mở rộng quy mô thực nghiệm dữ liệu pháp lý:** Tiếp tục thử nghiệm và đánh giá pipeline trên các văn bản quy phạm pháp luật dưới luật (như Nghị định, Thông tư hướng dẫn thi hành Luật Bảo vệ môi trường) và các văn bản quy chuẩn kỹ thuật quốc gia về môi trường. Điều này giúp kiểm chứng khả năng tổng quát hóa và độ ổn định của hệ thống trên các định dạng văn bản pháp lý khác nhau.
* **Tự động hóa toàn diện quy trình tiền xử lý đầu vào:** Nghiên cứu tích hợp các mô hình nhận diện cấu trúc tài liệu (Document Layout Analysis) và nhận dạng ký tự quang học (OCR) để tự động hóa hoàn toàn bước chuyển đổi văn bản luật gốc từ tệp PDF/Word sang JSON có cấu trúc theo đúng chương, mục, điều, khoản, điểm.
* **Nâng cấp tập dữ liệu tham chiếu thành Gold Dataset:** Tổ chức quy trình gán nhãn song song bởi ít nhất 3 chuyên gia luật hoặc chuyên gia chính sách công độc lập, tính toán chỉ số đồng thuận Cohen's Kappa hoặc Fleiss' Kappa, thiết lập cơ chế hòa giải bất đồng để xây dựng bộ dữ liệu chuẩn đạt độ tin cậy khoa học cao nhất.
* **Tối ưu hóa Prompt và thử nghiệm đa mô hình:** Ứng dụng kỹ thuật Prompt vài lượt mẫu (few-shot prompting) kèm theo các ví dụ minh họa trực quan cho các nhãn thiểu số (lợi ích) để cải thiện độ nhạy của LLM. Đồng thời, thực hiện đánh giá so sánh hiệu năng phân loại giữa nhiều mô hình ngôn ngữ lớn khác nhau (như GPT, Claude, DeepSeek, Llama) trên cùng một tập dữ liệu đối chứng.
* **Hiệu chuẩn trọng số và mô hình tính điểm nâng cao:** 
  * Áp dụng phương pháp Phân tích phân cấp (AHP) để khảo sát ý kiến chuyên gia, thiết lập ma trận so sánh cặp để tính toán bộ trọng số thành phần $(\alpha, \beta, \gamma, \delta)$ có cơ sở khoa học.
  * Tích hợp trọng số ưu tiên chủ thể $W_i$ và trọng số lĩnh vực dựa trên mức độ nhạy cảm sinh thái của từng địa phương.
  * Nghiên cứu triển khai hàm phạt phi tuyến (Non-linear Penalty) cho nhãn `CONSTRAINT` để đánh giá sát hơn các tác động nghiêm trọng của lệnh cấm.
* **Tiến tới Phân tích Chi phí - Lợi ích bằng tiền mặt đầy đủ (Full CBA):** Khi hệ thống dữ liệu kinh tế vĩ mô được tích lũy đầy đủ (các chỉ số phát thải, dòng chi phí tuân thủ của doanh nghiệp, chi phí y tế cộng đồng), nghiên cứu có thể tích hợp các hàm quy đổi giá trị phi tiền tệ sang tiền mặt để thực hiện các phân tích CBA tài chính hoàn chỉnh theo dòng thời gian.
* **Xây dựng Dashboard trực quan hóa và Knowledge Graph:** Phát triển ứng dụng giao diện web cho phép người dùng tải lên tệp JSON văn bản luật, theo dõi pipeline chạy tự động, thực hiện hiệu chỉnh nhãn trực quan, chấm điểm trực tiếp và xuất báo cáo PDF tự động. Xây dựng Đồ thị tri thức (Knowledge Graph) biểu diễn mối liên kết đa chiều giữa điều khoản luật, chủ thể, nghĩa vụ, lĩnh vực môi trường và điểm tác động để hỗ trợ truy vấn thông minh.
