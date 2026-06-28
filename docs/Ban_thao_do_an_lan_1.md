ĐẠI HỌC BÁCH KHOA HÀ NỘI
KHOA TOÁN - TIN
–o0o–
ĐÁNH GIÁ TÁC ĐỘNG CHÍNH SÁCH
MÔI TRƯỜNG: KHUNG ĐỊNH LƯỢNG
CHI PHÍ - LỢI ÍCH - RÀNG BUỘC
ĐỒ ÁN I
Chuyên ngành:TOÁN TIN
Giảng viên hướng dẫn: PGS. TS. Nguyễn Thị Ngọc Anh
Sinh viên thực hiện: Đinh Công Khang
Mã số sinh viên: 20237351
Lớp: Toán-Tin 02-K68
Hà Nội, 2026

NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN

1. Mục tiêu và nội dung của đồ án
(a) Mục tiêu: Ứng dụng được phương pháp suy luận nhân quả và mô hình hồi
quy tuyến tính cho bài toán dự báo nhu cầu.
(b) Nội dung: Nghiên cứu tổng quan và trình bày cơ sở lý thuyết suy luận nhân
quả và mô hình hồi quy tuyến tính. Tiến hành thực nghiệm đối với bài toán
hồi quy đa biến, đánh giá và so sánh.
2. Kết quả đạt được
...............................................................................
...............................................................................
...............................................................................
...............................................................................
...............................................................................
3. Ý thức làm việc của sinh viên:
...............................................................................
...............................................................................
...............................................................................
...............................................................................
...............................................................................
Hà Nội, ngày tháng năm 2025
Giảng viên hướng dẫn
PGS. TS. Nguyễn Thị Ngọc Anh
i

LỜI CẢM ƠN
Trước tiên, em xin gửi lời cảm ơn chân thành đến các thầy cô trong khoa Toán - Tin,
Đại học Bách khoa Hà Nội, những người đã truyền đạt cho em những kiến thức quý
báu trong suốt quá trình học tập và nghiên cứu. Sự tận tâm giảng dạy của thầy cô là
nền tảng vững chắc giúp em thực hiện đồ án này.
Em xin bày tỏ lòng biết ơn sâu sắc đến giảng viên hướng dẫn - PGS. TS. Nguyễn Thị
Ngọc Anh, người đã tận tình chỉ bảo, định hướng và đóng góp nhiều ý kiến quý giá,
giúp em hoàn thiện nội dung và nâng cao chất lượng đồ án.
Bên cạnh đó, em cũng muốn gửi lời cảm ơn chân thành đến các anh chị khóa trên,
những người đã nhiệt tình chia sẻ kinh nghiệm, hướng dẫn em trong quá trình thực
hiện đồ án. Sự hỗ trợ và những lời khuyên quý báu từ anh chị đã giúp em vượt qua
nhiều khó khăn và hoàn thiện đồ án của mình.
Mặc dù đã cố gắng hết sức, nhưng đồ án chắc chắn không thể tránh khỏi những thiếu
sót. Em rất mong nhận được những nhận xét, góp ý quý báu từ phía thầy cô để có thể
hoàn thiện hơn trong tương lai.
ii

Tóm tắt
Báo cáo trình bày về hệ thống hỗ trợ “Đánh giá tác động chính sách môi trường” với
đầu vào là một văn bản quy phạm pháp luật. Trọng tâm của hệ thống là một quy trình
xử lý (pipeline) có kiểm chứng : văn bản pháp luật đã được tách cấu trúc thành tập
các bản ghi (điều, khoản , điểm,...) có tác động chính sách, từ đó lọc các bản ghi có
tác động tới môi trường, quá trình này được thực hiện thủ công bởi người nghiên cứu
trước, sau đó, dùng LLM để lọc và tính toán các metric lần 1. Sau khi đã tiến hành
đánh giá mức độ đồng thuận, người nghiên cứu tiếp tục gán nhãn thủ công, vào 5 nhãn:
lợi ích định lượng, lợi ích định tính, chi phí định lượng, lợi ích định tính, ràng buộc và
thu được bộ nhãn cơ sở.Tiếp theo, sử dụng LLM để gán nhãn tương tự, thu được bộ
nhãn dự đoán, tại đây, Kết quả nhãn dự đoán được so sánh với nhãn cơ sở và đánh giá
bằng các metric lần 2. Sau khi đã đồng thuận các kết quả và thu được bộ nhãn cuối
cùng, tiến hành lượng hóa và chuyển thành biến định lượng để tính điểm tác động.
Khác với cách tiếp cận một hệ thống tự động hoàn toàn, nhãn LLM không được
xem là kết quả cuối cùng, LLM chỉ đóng vai trò hỗ trợ phân loại ban đầu, nhãn cơ sở
do người nghiên cứu gán được dùng làm mốc tham chiều để đánh giá và làm cơ sở hình
thành bộ nhãn cuối cùng (final\_label). Mô hình toán học được xây dựng theo hướng
bán định lượng, sử dụng các biếnMi, Si, Di, Ri, trọng sốWi và hướng tác độngsi để
tính điểm tác động (ImpactScore). Quy trình Human Verification Workflow được sử
dụng để có cơ sở kiểm chứng trong từng bước, đồng thời tạo tập dữ liệu tham chiếu
phục vụ đánh giá bằng Accuracy, Precision, Recall, F1-score, Macro F1 và Confusion
Matrix.
Từ khóa:RIA, EIA, CBA, LLM, Human in the loop, Impact Score.
iii

Mục lục
Tóm tắt iii
Danh sách hình vẽ vi
Danh sách bảng vii
Bảng ký hiệu và chữ viết tắt viii
1 Mở đầu 1
1.1 Bối cảnh và động cơ nghiên cứu . . . . . . . . . . . . . . . . . . . . . . . 1
1.2 Khoảng trống nghiên cứu . . . . . . . . . . . . . . . . . . . . . . . . . . 2
1.3 Phát biểu bài toán nghiên cứu . . . . . . . . . . . . . . . . . . . . . . . 3
1.4 Mục tiêu nghiên cứu . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
1.5 Cấu trúc đồ án . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
2 Phương pháp nghiên cứu 9
2.1 RIA, EIA và CBA . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
2.2 Vai trò của mô hình ngôn ngữ lớn . . . . . . . . . . . . . . . . . . . . . . 10
2.3 Human Verification Workflow trong đánh giá kết quả AI . . . . . . . . . 10
2.4 Các chỉ số đánh giá phân loại . . . . . . . . . . . . . . . . . . . . . . . . 11
2.5 Thang điểm 1–5 và mô hình bán định lượng trong EIA . . . . . . . . . . 12
2.6 Tổng quan quy trình nghiên cứu . . . . . . . . . . . . . . . . . . . . . . 14
2.7 Dữ liệu đầu vào và tiền xử lý . . . . . . . . . . . . . . . . . . . . . . . . 14
2.8 Bộ nhãn phân loại tác động . . . . . . . . . . . . . . . . . . . . . . . . . 15
2.9 Thiết kế prompt LLM . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
2.10Xây dựng Human-labeled Reference Dataset . . . . . . . . . . . . . . . . 16
2.11Đánh giá LLM so với nhãn con người . . . . . . . . . . . . . . . . . . . . 17
2.12Mô hình toán học lượng hóa tác động . . . . . . . . . . . . . . . . . . . 17
2.12.1Biến đầu vào . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
2.12.2Điểm tổng hợp chưa chuẩn hóa . . . . . . . . . . . . . . . . . . . . 18
2.12.3Chuẩn hóa điểm . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
iv

2.12.4Điểm tác động của điều khoản . . . . . . . . . . . . . . . . . . . . 18
2.12.5Điểm tác động tổng hợp . . . . . . . . . . . . . . . . . . . . . . . 18
2.12.6Giả định trọng số . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
3 Kết quả và đánh giá thực nghiệm 20
3.1 Thiết lập thực nghiệm . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
3.2 Thống kê dữ liệu . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
3.3 Kết quả phân loại của LLM . . . . . . . . . . . . . . . . . . . . . . . . . 21
3.4 Phân tích ma trận nhầm lẫn . . . . . . . . . . . . . . . . . . . . . . . . 22
3.5 Kết quả tính điểm tác động . . . . . . . . . . . . . . . . . . . . . . . . . 23
3.6 Nhận xét kết quả . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
4 Kết luận, hạn chế và hướng phát triển 26
4.1 Kết luận . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26
4.2 Hạn chế . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
4.3 Hướng phát triển . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
A Mẫu JSON đầu vào 29
B Prompt LLM 30
C Hướng dẫn gán nhãn thủ công 31
D Hướng dẫn chấm điểm 1–5 32
E Mapping tài liệu tham khảo với thành phần hệ thống 33
Tài liệu tham khảo 35
v

Danh sách hình vẽ
vi

Danh sách bảng
2.1 Bảng mô tả mức độ đánh giá cho thang điểm 1–5. . . . . . . . . . . . . 13
2.2 Bộ nhãn phân loại tác động . . . . . . . . . . . . . . . . . . . . . . . . . 15
2.3 Các biến trong mô hình điểm tác động. . . . . . . . . . . . . . . . . . . 18
3.1 Thống kê tổng quan dữ liệu qua các bước xử lý . . . . . . . . . . . . . . 21
3.2 Phân bố nhãn do LLM dự đoán . . . . . . . . . . . . . . . . . . . . . . . 21
3.3 Bảng kết quả đánh giá phân loại tổng hợp. . . . . . . . . . . . . . . . . 22
3.4 Bảng metric theo từng nhãn. . . . . . . . . . . . . . . . . . . . . . . . . 22
3.5 Mẫu bảng phân tích các trường hợp LLM phân loại sai. . . . . . . . . . 22
3.6 Mẫu ma trận nhầm lẫn giữa human label và LLM label . . . . . . . . . . 23
3.7 Bảng kết quả tính Impact Score cho từng điều khoản . . . . . . . . . . . 23
3.8 Bảng kết quả tổng hợp điểm tác động. . . . . . . . . . . . . . . . . . . . 24
3.9 Bảng tổng hợp Impact Score theo nhãn. . . . . . . . . . . . . . . . . . . 24
C.1 Hướng dẫn gán nhãn thủ công. . . . . . . . . . . . . . . . . . . . . . . . 31
D.1 Gợi ý rubric chấm điểm mức độ tác động. . . . . . . . . . . . . . . . . . 32
E.1 Bảng mapping tài liệu tham khảo với quyết định thiết kế. . . . . . . . . 33
vii

Bảng ký hiệu và chữ viết tắt
Ký hiệu / Viết
tắt
Ý nghĩa
RIA Regulatory Impact Assessment – Đánh giá tác động quy
định/chính sách.
EIA Environmental Impact Assessment – Đánh giá tác động môi
trường.
CBA Cost-Benefit Analysis – Phân tích chi phí – lợi ích.
SCBA Social Cost-Benefit Analysis – Phân tích chi phí – lợi ích
xã hội.
LLM Large Language Model – Mô hình ngôn ngữ lớn.
HITL Human-in-the-loop – Quy trình có con người tham gia kiểm
chứng.
VBQPPL Văn bản quy phạm pháp luật
Dco\_tac\_dong Tập chứa các bản ghi có tác động chính sách
Dmoi\_truong Tập bản ghi có tác động chính sách môi trường
LKhông gian chứa 5 nhãn tác động
yi Nhãn cơ sở do người nghiên cứu gán cho bản ghi thứi
ˆyi Nhãn do LLM dự đoán / gán cho bản ghii
Mi Magnitude – cường độ tác động của điều khoảni.
Si Scope – phạm vi ảnh hưởng của điều khoảni.
Di Duration – thời gian tác động của điều khoảni.
Ri Risk/Reversibility – rủi ro hoặc khả năng phục hồi của tác
động.
viii

Wi Trọng số theo đối tượng, lĩnh vực hoặc mức ưu tiên chính
sách.
si Hướng tác động:+1với lợi ích, −1với chi phí hoặc ràng
buộc.
Ci Điểm tổng hợp chưa chuẩn hóa.
C norm
i Điểm tổng hợp đã chuẩn hóa về khoảng\[0,1].
ImpactScorei Điểm tác động của điều khoảni.
TotalImpactTổng điểm tác động của toàn bộ tập điều khoản.
ix

Chương 1
Mở đầu
1.1 Bối cảnh và động cơ nghiên cứu
Các văn bản pháp luật trong lĩnh vực môi trường, năng lượng,phát triển bền
vững,..vv.. thường có cấu trúc phức tạp, nhiều điều khoản, nhiều chủ thể và chứa nhiều
tầng ngữ nghĩa. Một điều khoản có thể đồng thời tạo ra nghĩa vụ tuân thủ, điều kiện
kỹ thuật, chi phí thực hiện, lợi ích môi trường hoặc ràng buộc pháp lý đối với các nhóm
chủ thể khác nhau như cơ quan quản lý, doanh nghiệp, chủ dự án, cộng đồng dân cư và
môi trường tự nhiên. Trong bối cảnh chuyển đối xanh, phát triển bền vững và gia tăng
yêu cầu quản trị môi trường, việc đánh giá tác động chính sách môi trường trở thành
một yếu tố quan trọng.
Về mặt phương pháp, đánh giá tác động chính sách môi trường không chỉ là đọc hiểu
các văn bản quy phạm pháp luật, mà là sự kết hợp giữa Regulatory Impact Assessment
(RIA), Environment Impact Assessment (EIA), Cost-Benefit Analysis (CBA), xử lý
ngôn ngữ pháp lý và mô hình hóa định lượng.RIA giúp xác dịnh các quy định tạo ra
tác động chính sách, nâng cao chất lượng và tăng tính minh bạch trong quá trình ra
quyết định; EIA giúp xác định các tác động đó liên quan đến môi trường ra sao bằng
cách mô tả, diễn giải các tác động môi trường trước khi chính sách hoặc dự án được
triển khai.Bên cạnh đó, CBA giúp lượng hóa tác động, so sánh lợi ích, chi phí và các
ngoại ứng môi trường trong một khung phân tích thống nhất.
Tuy nhiên, trong thực tế, việc đọc và phân loại thủ công các điều khoản pháp lý
thường tốn nhiều thời gian, khó tái lập và dễ phụ thuộc vào nhận định chủ quan, dẫn
tới thiếu tính nhất quán. Các mô hình ngôn ngữ lớn (Large Language Models – LLMs)
có thể hỗ trợ phân tích văn bản phức tạp, trích xuất thông tin từ văn bản pháp lý. Dù
vậy, trong miền pháp lý và chính sách, LLM không nên được xem là công cụ tự động
quyết định cuối cùng vì có thể suy diễn sai, hiểu sai điều kiện áp dụng, bỏ sót ngoại lệ
1

2
hoặc nhầm lẫn giữa nghĩa vụ pháp lý và tác động thực tế. Nhiều nghiên cứu đã chỉ ra
rằng, LLM có thể bị ảo giác (hallucination) khi thực hiện các tác vụ phức tạp, dữ liệu
mà LLM sinh ra đọc có vẻ hợp lý nhưng thực tế không có bằng chứng xác thực.
Từ bối cảnh đó, đồ án lựa chọn hướng tiếp cận có kiểm chứng bằng phương pháp
Human in the loop : LLM được sử dụng như một công cụ hỗ trợ phân loại ban đầu,
sau đó con người đóng vai trò tạo nhãn tham chiếu, kiểm chứng và chốt kết quả. Các
nhãn cuối cùng sau kiểm chứng được chuyển thành biến định lượng để tính điểm tác
động chính sách theo mô hình toán học bán định lượng, có thang điểm, trọng số và quy
tắc chuẩn hóa rõ ràng.Động cơ nghiên cứu của đồ án là xây dựng một hệ thống có cấu
trúc rõ ràng, có khả năng truy vết, có thể tính độ chính xác của LLM và chuyển kết
quả phân loại thành điểm tác động phục vụ cho việc phân tích chính sách môi trường.
1.2 Khoảng trống nghiên cứu
Các công trình nghiên cứu liên quan.
Các nghiên cứu và hệ thống hiện tại thường tiếp cận bài toán theo một trong hai
hướng.Thứ nhất,tập trung vào việc phân tích chính sách và CBA nhưng đòi hỏi nhiều
dữ liệu định lượng như chi phí, lợi ích, dòng tiền, tỷ lệ chiết khấu, dữ liệu phát thải
hoặc dữ liệu sức khỏe,..etc..Thứ hai, tập trung vào xử lý ngôn ngữ tự nhiên và phân
loại văn bản, nhưng đa số chỉ dừng ở mức gán nhãn mà chưa kết hợp giữa kết quả phân
loại với mô hình đánh giá tác động có công thức rõ ràng.
Đối với văn bản pháp luật về môi trường ở Việt Nam,thường thiếu một quy trình
có khả năng biến các điều khoản pháp lý dạng JSON thành dữ liệu có nhãn, có kiểm
chứng và có điểm tác động bán định lượng. Nếu chỉ dùng LLM để gán nhãn, hệ thống
sẽ thiếu cơ chế đánh giá độ chính xác. Nếu chỉ dùng CBA truyền thống, hệ thống lại
thiếu dữ liệu định lượng cần thiết ở cấp độ từng đơn vị pháp lý nhỏ nhất là các điều
khoản. Do đó, cần có một khung tiếp cận phù hợp hơn với dữ liệu pháp lý: bắt đầu từ
file JSOn, lọc tác động, phân loại, kiểm chứng, đánh giá metric, tính điểm tác động
bằng mô hình bán định lượng.
Bên cạnh đó, một điều khoản có thể có tác động pháp lý nhưng không nhất thiết
phải có tác động đến môi trường, do đó, cần tách bạch hai bước lọcco\_tac\_dong =
true và tác động môi trường. Nếu bị gộp lại, dữ liệu đưa vào LLM có thể gây nhiễu và
làm giảm chất lượng phân loại.

3
1.3 Phát biểu bài toán nghiên cứu
Một văn bản quy phạm pháp luật đã được tách cấu trúc thành một tập hữu hạn
các bản ghi , trong đó, mỗi bản ghi là một điều, khoản, điểm hoặc một mệnh đề độc
lập có tác động chính sách.
Gọi Dco\_tac\_dong = {d1, d2, d3, . . . , dN } = {di |i∈N ∗, i= 1, . . . , N}là tập hợp chứa
toàn bộNbản ghi.
Mỗi bản ghidi được biểu diễn dưới dạng:
di = (ma\_nguoni,trich\_dan i,noi\_dung i,co\_tac\_dong i,chu\_the\_chiu\_tac\_dong i,
tin\_hieu\_tac\_dongi,linh\_vuc\_tac\_dong i,gia\_tri\_dinh\_luong,dieu\_kien\_ap\_dung i,vi\_tri i,VBQPPL)
trongđó, ma\_nguoni làmãđịnhdanhcủabảnghi, trich\_dani lànguồntríchdẫncủabản
ghi, noi\_dung\_van\_bani là nội dung pháp lý gốc,co\_tac\_dongi là giá trị của trường
chứa bản ghi có tác động chính sách,chu\_the\_chiu\_tac\_dongi là nhóm đối tượng
chịu tác động trực tiếp ,tin\_hieu\_tac\_dongi là những hành vi ,linh\_vuc\_tac\_dongi
là lĩnh vực hoặc khía cạnh mà tác động phát sinh,gia\_tri\_dinh\_luongi là các giá trị
số,ngưỡng, mức phí, tỷ lệ, thời hạn hoặc chỉ tiêu định lượng xuất hiện trong quy định.,
và dieu\_kien\_ap\_dungi là điều kiện, tiêu chí phải thỏa mãn để quy định và tác động
có hiệu lực áp dụng.
Định nghĩa: Gọifmoi\_truong là hàm số lọc các phần tử có tác động chính sách đến
môi trường đi từ tậpDco\_tac\_dong vào tập giá trị{0,1}thỏa mãn:
fmoi\_truong :D co\_tac\_dong → {0,1}
trong đó, với mỗidi ∈D co\_tac\_dong:
fmoi\_truong(di) =



1,nếud i có tác động đến môi trường,
0,nếud i không có tác động đến môi trường,
vớid i ∈D co\_tac\_dong.
(1.1)
Gọi Dmoi\_truong là tập hợp chứa các phần tử có tác động đến môi trường sau khi thực
hiện lọc từDco\_tac\_dong:
Dmoi\_truong ={d 1, d2, d3, . . . , dM }={d i ∈D co\_tac\_dong |f moi\_truong(di) = 1}

4
vớiM≤ |Dco\_tac\_dong| ≤N.
Định nghĩa:Gọi L = {l1, l2, l3, l4, l5} là tập hợp rời rạc chứa 5 nhãn cần gán, trong
đó:
l1:Lợi ích định lượng
l2:Lợi ích định tính
l3:Chi phí định lượng
l4:Chi phí định tính
l5:Ràng buộc
Đây là bài toán phân loại đa lớp đơn nhãn, tức là với mỗi bản ghixi ∈D moi\_truong,
hệ thống gán đúng một nhãn thuộcL.
Ta có thể phát biểu tổng quan bài toán như sau:
Với mỗi bản ghixi ∈D moi\_truong, quá trình gán nhãn các bản ghi từDmoi\_truong vào
tậpLnhư sau:
fphan\_loai :D moi\_truong → L
Ta gọi tập nghiệm của hàm này làY = {y1, y2, y3, . . . , yM }, với yi = {fphan\_loai(xi) |
xi ∈D moi\_truong, yi ∈ L}
Bài toán đặt ra là lọc được các bản ghi có tác động môi trường và phân loại được
các bản ghixi ∈D moi\_truong vào đúng cácli ∈ Lvà thu được tậpY với độ chính xác
cao nhất ơ cả bước lọc và phân loại nhãn, đồng thời, tính điểm tác động.
Tập các nhãn cuối cùng được xác định sau bước kiểm chứng của người nghiên cứu.
Ký hiệu làZ.
GọiC ∈N 5×5 là ma trận nhầm lẫn, trong đó phần tửCij biểu thị số lượng các điều
khoản có nhãn cơ sở làli nhưng LLM phân loại thànhlj:
Cij =
MX
m=1
I(ym =l i ∧ˆym =l j)
Từ ma trậnC, ta định nghĩa các metric đánh giá cho từng nhãn cụ thể lk (với
k∈ {1,2,3,4,5}):
Độ chuẩn xác (Precision -Pk): Tỷ lệ LLM đoán đúng nhãnlk trên tổng số lần nó dự
đoán làl k.
Pk = Ckk
P5
i=1 Cik
Độ phủ (Recall -Rk): Tỷ lệ LLM tìm được đúng nhãnlk trên tổng số nhãnlk thực tế

5
có trong bộ nhãn cơ sở.
Rk = Ckk
P5
j=1 Ckj
Điểm F1 (F1-Score -F 1k): Trung bình điều hòa giữa Precision và Recall, rất quan
trọng đối với các nhãn thiểu số.
F1 k = 2· Pk ·R k
Pk +R k
Để có một con số tổng quát đánh giá toàn bộ Prompt/Model LLM của bạn, hãy sử
dụng Macro-F1 (coi trọng tất cả 5 nhãn như nhau, không phụ thuộc số lượng điều
khoản mỗi nhãn):
Macro-F1= 1
5
5X
k=1
F1 k
Nếu Macro-F1 đạt mức kỳ vọng (ví dụ≥ 0.85), bộ nhãn ˆY từ LLM mới đủ điều kiện
thống kê để đưa vào mô hình CBA.
Theo hướng dẫn của Khung Phân tích Tác động Quy định (Regulatory Impact
Assessment - RIA) được các tổ chức uy tín (như OECD) khuyến nghị, một chính sách
cần được phân tách thành các tác động cụ thể để lượng hóa.
Giả sử hệ thống nhận đầu vào là một tập hợp các điều khoản pháp luật được cấu
trúc hóa dưới định dạng JSON.
Gọi D = {d1, d2, . . . , dN } là không gian toàn bộN điều khoản của văn bản pháp lý.
Áp dụng hàm lọc tiên quyếtfimpact : D → {0, 1} để thu được tập dữ liệu đầu vào
cốt lõi:
X={x∈ D |fimpact(x) = 1}
Trong đó X = {x1, x2, . . . , xM } với M≤N là tập các bản ghi có mang đặc tính tác
động (co\_tac\_dong = true). Bài toán của đề tài được chia làm hai phân hệ chính.
2. Bài toán 1: Phân loại đa nhãn bằng Mô hình Ngôn ngữ Lớn (LLM Classification)
Mục tiêu là gán mỗi điều khoảnxi ∈X vào một nhãn duy nhất mô tả bản chất tác
động môi trường của nó. Không gian nhãn phân loạiL được định nghĩa gồm 5 phần tử:
L={l 1, l2, l3, l4, l5}
Trong đó:
l1: Lợi ích định lượng (Quantitative Benefit)l2: Lợi ích định tính (Qualitative Benefit)
l3: Chi phí định lượng (Quantitative Cost)l4: Chi phí định tính (Qualitative Cost)l5:
Ràng buộc (Constraint)

6
Quá trình gán nhãn thủ công (Ground Truth) được định nghĩa là ánh xạY : X→ L.
Mô hình LLM hoạt động như một hàm xấp xỉˆfLLM : X→ Ltrả về nhãn dự đoán
ˆY.
Hệ đo lường (Evaluation Metrics):
Do sự mất cân bằng tự nhiên của các điều khoản pháp luật (class imbalance), mô
hình không thể chỉ đánh giá bằng độ chính xác (Accuracy). Căn cứ vào Ma trận Nhầm
lẫn (Confusion Matrix) đa lớpC∈N 5×5, độ tin cậy của mô hình LLM phải được đánh
giá qua chỉ số Macro-F1:
Macro-F1= 1
5
5X
k=1
2·P k ·R k
Pk +R k
(VớiP k là Precision vàRk là Recall của từng nhãnlk).
3. Bài toán 2: Mô hình Hóa Toán học và Đánh giá Tác động (Impact Scoring Model)
Với mỗi điều khoảnxi đã được xác nhận nhãn chính xácl(xi) ∈ L, ta cần xây
dựng mô hình toán học để chuyển đổi chúng thành một Điểm tác động chuẩn hóa
(Normalized Impact Score). Bài toán này được giải quyết bằng phương pháp Phân tích
Quyết định Đa tiêu chí (MCDA - Multi-Criteria Decision Analysis), áp dụng các hàm
phân nhánh (Piecewise Functions) tùy theo đặc thù của nhãn.
Gọi si ∈ {−1, +1} là vector hướng tác động (Directional Vector):si = +1nếu thuộc
nhóm Lợi ích (l1, l2), vàs i =−1nếu thuộc nhóm Chi phí hoặc Ràng buộc (l3, l4, l5).
GọiW i là Trọng số hệ sinh thái của đối tượng chịu tác động.
Phân nhánh 1: Nhóm Biến Định Tính (l2, l4)
Áp dụng kỹ thuật Simple Additive Weighting (SAW), điểm thôCi được tính dựa
trên 4 biến đo lường thang Likert \[1-5] gồm Cường độ (M), Phạm vi (S), Thời gian
(D), và Rủi ro (R):
Ci =αM i +βS i +γD i +δR i
(Ghi chú: Các hệ sốα, β, γ, δtuân theo ràng buộc tổng bằng 1, lý tưởng nhất là được
chiết xuất từ ma trận Analytical Hierarchy Process - AHP).
Áp dụng công thức chuyển đổi tuyến tính (Linear Scale Transformation) để chuẩn
hóa về khoảng\[0,1]:
C norm
i = Ci −C min
Cmax −C min
= Ci −1
4
Phân nhánh 2: Nhóm Biến Định Lượng (l1, l3)
Đối với điều khoản chứa giá trị thựcVi (ví dụ: kW, VNĐ, diện tích đất), để đồng
nhất không gian đo lường với nhóm định tính, ta áp dụng hàm Chuẩn hóa Min-Max

7
(Min-Max Normalization) của hệ MCDA trên không gian giá trị nội tại của tập luật:
C norm
i =U(V i) = Vi −V min
Vmax −V min
Phân nhánh 3: Nhóm Ràng Buộc (l5)
Ràng buộc mang rủi ro đứt gãy hệ thống nếu vi phạm. Ta định lượng ràng buộc bằng
điểm Ci tương tự nhóm định tính, nhưng sử dụng Hàm Phạt Phi tuyến (Non-linear
Penalty Function) để khuếch đại mức độ nghiêm trọng:
C norm
i =
 Ci −1
4
κ
(Với hệ số phạtκ >1, ví dụκ= 2).
4. Phương trình Mục tiêu Tác động Tổng hợp (Final Objective Function)
Điểm tác động cuối cùng (Impact Score) của từng điều luật là sự kết hợp của hướng
vector, trọng số đối tượng và giá trị chuẩn hóa:
ImpactScore i =s i ·W i ·C norm
i
Từ đó, Tổng giá trị tác động của toàn bộ khung chính sách (IS total) là hàm tuyến tính
tổng hợp:
IS total =
X
xi∈X
ImpactScore i
Nếu IS total > 0: Hệ thống chính sách (ví dụ: Luật bảo vệ môi trường, năng lượng) đem
lại Thặng dư Tác động dương, khuyến khích phát triển.
Nếu IS total < 0: Gánh nặng chi phí và rào cản ràng buộc đang vượt quá lợi ích dự
kiến, cần thiết kế lại chính sách.
1.4 Mục tiêu nghiên cứu
(4 mục tiêu)
Mục tiêu của đồ án là xây dựng một khung xử lý và đánh giá tác động chính sách
môi trường từ VBQPPL về môi trường,với sự kết hợp của con người và LLM, áp dụng
mô hình toán học để tính điểm tác động, cụ thể:

1. Thiết kế pipeline xử lý dữ liệu pháp lý dạng JSON, bảo đảm có khả năng truy vết
từ kết quả phân tích về văn bản gốc.
2. Xác định rõ hai bước: lọc điều khoản có tác động pháp lý và lọc điều khoản có tác

8
động môi trường.
3) Xây dựng bộ nhãn 5 lớp phản ánh lợi ích, chi phí và ràng buộc trong đánh giá tác
động chính sách môi trường.
4) Thiết kế prompt LLM để phân loại điều khoản môi trường vào 5 nhãn, kèm lý do
và bằng chứng.
5) Xây dựng bộ dữ liệu tham chiếu được gán nhãn thủ công bởi con người (Human-
labeled Reference Dataset) để đánh giá LLM.
6) Tính các metric đánh giá phân loại như độ chính xác tổng thể (Accuracy), Precision,
Recall, F1-score, Macro-F1, ma trận nhầm lẫn (Confusion Matrix) và tỷ lệ cần
con người đính chính (Human Correction Rate).
7) Chuyển nhãn cuối cùng thành các biến định lượng và tính điểm tác động (Impact
Score) bằng mô hình bán định lượng.
8) Tổng hợp, trực quan hóa và diễn giải kết quả dựa trên phân loại nhãn, lĩnh vực
(domain) môi trường và chủ thể chịu tác động.
1.5 Cấu trúc đồ án
Báo cáo được tổ chức thành năm chương. Chương 1 trình bày bối cảnh, khoảng trống,
phát biểu bài toán, mục tiêu, câu hỏi nghiên cứu, phạm vi và đóng góp. Chương 2 trình
bày tổng quan và cơ sở phương pháp gồm RIA, EIA, CBA, LLM, Human Verification,
các metric đánh giá và mô hình bán định lượng. Chương 3 mô tả phương pháp nghiên
cứu, thiết kế hệ thống, dữ liệu đầu vào, bộ nhãn, prompt, tập nhãn con người, đánh
giá LLM và mô hình toán học lượng hóa tác động. Chương 4 trình bày thiết lập thực
nghiệm, thống kê dữ liệu, kết quả phân loại, ma trận nhầm lẫn, kết quả Impact Score,
ví dụ tính tay và nhận xét kết quả. Chương 5 tổng kết, nêu hạn chế và đề xuất hướng
phát triển.

Chương 2
Phương pháp nghiên cứu
2.1 RIA, EIA và CBA
Đánh giá tác động chính sách môi trường là bài toán kết hợp giữa đánh giá chính
sách công, đánh giá tác động môi trường và phân tích lợi ích, chi phí về mặt kinh tế,
tương ứng với ba phương pháp được sử dụng trong đồ án là RIA, EIA và CBA.
RIA (Regulatory Impact Assessment) là phương pháp đánh giá có hệ thống các tác
động dự kiến của một quy định trước, trong hoặc sau khi ban hành. Trong phạm vi
của đồ án, RIA là cơ sở để xác định những bản ghico\_tac\_dong = true . Một điều,
khoản có tác động pháp lý khi nó tạo nghĩa vụ, quyền lợi, trách nhiệm, ưu đãi, điều
kiện áp dụng, thủ tục hành chính, chi phí tuân thủ, lệnh cấm hoặc giới hạn kỹ thuật.
Về mặt toán học, bước này được biểu diễn bởi một hàm số đi từ tập tất cả các bản ghi
Dvào tập giá trị{0,1}:
flegal :D→ {0,1}
EIA (Environment Impact Assessment) xác định trong số các điều khoản có tác động
pháp lý, điều khoản nào thực sự có tác động đến môi trường. Tác động môi trường liên
quan đến nước, không khí, đất, chất thải, khí thải, nước thải, giấy phép môi trường,
quan trắc, biến đổi khí hậu, đa dạng sinh học, tài nguyên thiên nhiên, v.v. Bước này
được biểu diễn bởi một hàm số đi từ tập chứa các điều khoản có tác động pháp lýDlegal
vào tập giá trị{0,1}:
fenv :D legal → {0,1}
CBA (Cost-Benefit Analysis) cung cấp nền tảng để phân biệt lợi ích và chi phí.
Trong phạm vi đồ án, CBA không được triển khai như phân tích đầy đủ bằng tiền do
9

10
văn bản pháp luật thường không cung cấp đủ dữ liệu. Tuy nhiên, CBA giúp xác định
bộ nhãn gồm lợi ích, chi phí, ràng buộc, đồng thời xây dựng mô hình bán định lượng
tính Impact Score.
Ba phương pháp được sử dụng trong đồ án tương ứng với ba lớp logic:
RIA⇒lọc tác động pháp lý,
EIA⇒lọc tác động môi trường và đánh giá mức độ,
CBA⇒phân loại lợi ích, chi phí, ràng buộc và tính điểm.
2.2 Vai trò của mô hình ngôn ngữ lớn
LLM có khả năng xử lý văn bản phức tạp, hỗ trợ tóm tắt, phân loại, trích xuất
thông tin và giải thích ngữ cảnh. Trong miền pháp lý, các nghiên cứu về trích xuất
thông tin từ văn bản luật hoặc tài liệu pháp lý cho thấy LLM có thể đóng vai trò công
cụ hỗ trợ ban đầu \[1], \[2]. Tuy nhiên, văn bản pháp lý thường có đặc điểm nhập nhằng,
liên kết chéo, ngoại lệ và điều kiện áp dụng. Những đặc điểm này khiến kết quả LLM
cần được kiểm chứng, đặc biệt khi sử dụng cho bài toán đánh giá chính sách \[3], \[4].
Vì vậy, hệ thống không xem nhãn LLM là kết quả cuối cùng. LLM chỉ tạo nhãn đề
xuất, lý do gán nhãn, trích dẫn bằng chứng ngắn (evidence\_span) và độ tin cậy. Kết
quả này sau đó được so sánh với nhãn do người nghiên cứu gán.
Trong hệ thống, LLM được mô hình hóa như một hàm xấp xỉ:
ˆfLLM :X env → L.
Nhãn do LLM gán cho mỗixi ∈X env là ˆyi = ˆfLLM(xi), khi đó, ta có tập nhãn LLM:
ˆY={ˆy 1,ˆy2, . . . ,ˆyM }
Đầu ra của LLM không chỉ bao gồm nhãn phân loại mà còn có lý do, bằng chứng và
độ tin cậy, góp phần giúp người nghiên cứu kiểm tra độ chính xác của LLM:
(ˆyi,reason\_i,evidence\_span\_i,confidence\_i).
2.3 Human Verification Workflow trong đánh giá kết quả AI
Khác với một hệ thống pipeline tự động hoàn toàn, quy trình Human Verification
Workflow giúp hệ thống hoạt động có kiểm chứng. Trong quy trình này, người nghiên
cứu tạo nhãn cơ sở, kiểm tra nhãn do LLM đề xuất, phân tích các trường hợp sai và

11
chốt nhãn cuối cùng trước khi đưa dữ liệu vào mô hình tính điểm. Cách tiếp cận này
phù hợp với hướng nghiên cứu Human-in-the-loop trong NLP, nơi con người và mô hình
AI phối hợp để tăng chất lượng dữ liệu và giảm rủi ro ảo giác \[5], \[6], \[7].
Trong phạm vi đồ án, tập nhãn do người nghiên cứu gán được gọi làHuman-labeled
Dataset.
Với mỗi bản ghixi ∈X env, hệ thống có hai loại nhãn:
ˆyi =LLM label, y i =human label.
Hai nhãn này được so sánh với nhau. Nếuˆyi = yi, LLM được xem là phân loại đúng
theo nhãn tham chiếu. Nếuˆyi ̸=y i, bản ghi được đưa vào danh sách review.
Trong phiên bản hiện tại, quy tắc an toàn là:
final\_labeli =y i
trừ khi người nghiên cứu có lý do điều chỉnh sau khi đối chiếu lại. Quy trình này giúp
tránh việc nhãn LLM sai gây ảnh hưởng đến bước tínhImpactScorei.
Với cách diễn đạt như trên ta sẽ mô hình hóa việc so sánh nhãn LLM với nhãn cơ sở
bằng cách sử dụng hàm chỉ thị (hàm đặc trưng)I(·)sao cho:
I=



1,nếu nhãn LLM=nhãn cơ sở,
0,nếu nhãn LLM̸=nhãn cơ sở
(2.1)
2.4 Các chỉ số đánh giá phân loại
Để đánh giá độ chính xác của LLM, hệ thống sử dụng ma trận nhầm lẫn (confusion
matrix) và các chỉ số (metrics) phân loại tiêu chuẩn:
Gọi:
L={l 1, l2, l3, l4, l5}
là không gian 5 nhãn. Ma trận nhầm lẫn được định nghĩa bởi:
Ckj =|{i|y i =l k,ˆyi =l j}|.
Với mỗi nhãnlk:
T Pk =C kk, F Pk =
X
r̸=k
Crk, F Nk =
X
c̸=k
Ckc.

12
Precision, Recall và F1-score được tính bởi:
Pk = T Pk
T Pk +F Pk
, R k = T Pk
T Pk +F Nk
,
F1 k = 2PkRk
Pk +R k
.
Accuracy:
Accuracy =
P5
k=1 Ckk
P5
k=1
P5
j=1 Ckj
.
Macro-F1:
Macro-F1 = 1
5
5X
k=1
F1 k.
Human Correction Rate:
HumanCorrectionRate = |{i|y i ̸= ˆyi}|
M .
trong đó,
•Accuracy: tỷ lệ nhãn LLM đúng trên toàn bộ tập dữ liệu.
• Precision: trong các mẫu được LLM dự đoán thuộc một nhãn, có bao nhiêu mẫu
đúng.
•Recall: trong các mẫu thật thuộc một nhãn, LLM nhận diện đúng bao nhiêu.
•F1-score: trung bình điều hòa giữa Precision và Recall.
•Macro F1: trung bình F1 theo nhãn, phù hợp khi dữ liệu có thể lệch nhãn.
•Confusion Matrix: chỉ ra LLM thường nhầm nhãn nào với nhãn nào.
•Human Correction Rate: tỷ lệ nhãn LLM cần con người sửa.
Việc kết hợp Accuracy với Macro F1 và Confusion Matrix giúp đánh giá kết quả đầy
đủ hơn. Nếu chỉ dùng Accuracy, hệ thống có thể bỏ qua lỗi ở các nhãn ít xuất hiện.
Confusion Matrix đặc biệt hữu ích để phân tích các cặp nhãn dễ nhầm nhưCOST và
CONSTRAINT\[2], \[3], \[8].
2.5 Thang điểm 1–5 và mô hình bán định lượng trong EIA
Trong EIA,không phải mọi tác động đểu có thể được lượng hóa trực tiếp bằng tiền,
đa số tác động thường được đánh giá theo nhiều tiêu chí như cường độ, phạm vi, rủi

13
ro hoặc thời gian và khả năng đảo ngược. Đồ án sử dụng mô hình bán định lượng với
thang điểm 1–5 để đánh giá mức độ tác động. Mô hình bán định lượng cho phép chuyển
nhận định định tính thành điểm số có thể so sánh, đồng thời vẫn thừa nhận rằng việc
chấm điểm phụ thuộc vào quy tắc và người đánh giá \[9], \[10].
Bốn biến được sử dụng là:
Mi, Si, Di, Ri ∈ {1,2,3,4,5}
Trong đó Mi là cường độ tác động,Si là phạm vi ảnh hưởng,Di là thời gian tác
động vàR i là rủi ro hoặc khả năng đảo ngược.
Bảng 2.1: Bảng mô tả mức độ đánh giá cho thang điểm 1–5.
Điểm Mức độ Diễn giải
1 Rất thấp Tác động nhỏ, gián tiếp, phạm vi rất hẹp, ngắn hạn
hoặc dễ kiểm soát.
2 Thấp Tác động có nhưng hạn chế, ảnh hưởng đến ít chủ
thể hoặc ít rủi ro.
3 Trung bình Tác động rõ ràng, có ảnh hưởng đáng kể nhưng chưa
rộng hoặc chưa nghiêm trọng.
4 Cao Tác động mạnh, phạm vi tương đối rộng, kéo dài hoặc
có rủi ro đáng kể.
5 Rất cao Tác động rất mạnh, phạm vi rộng, dài hạn, rủi ro lớn
hoặc khó đảo ngược.
Điểm tổng hợp chưa chuẩn hóa được tính bởi:
Ci =αM i +βS i +γD i +δR i,
trong đó:
α+β+γ+δ= 1.
Trong phiên bản cơ sở có thể dùng trọng số bằng nhau:
α=β=γ=δ= 0.25.
Chuẩn hóa:
C norm
i = Ci −1
4 .

14
Điểm tác động:
ImpactScorei =s i ×W i ×C norm
i .
2.6 Tổng quan quy trình nghiên cứu
Quy trình nghiên cứu của đồ án được thiết kế theo hướng tuần tự, có kiểm chứng và
có khả năng truy vết. Hệ thống tập trung vào pipeline cốt lõi:
Legal JSON→Legal Impact Filtering→Environmental Impact Filtering
→Five-label Classification→Human Verification
→Evaluation Metrics→Impact Scoring.
Tư tưởng thiết kế gồm ba nguyên tắc. Thứ nhất, dữ liệu pháp lý phải có cấu trúc và
có thể truy vết thông quasource\_id, legal\_citation và raw\_text. Thứ hai, LLM
chỉ đóng vai trò hỗ trợ phân loại, không phải là kết quả cuối cùng. Thứ ba, mô hình
định lượng phải minh bạch, có biến, thang điểm, trọng số và công thức rõ ràng.
Các bước chính gồm:

1. Đọc và kiểm tra file JSON đầu vào.
2. Lọc bản ghi cóco\_tac\_dong=trueđể tạoX legal.
3. Lọc bản ghi có tác động môi trường để tạoX.
4. Gọi LLM phân loại từngxi ∈Xvào 5 nhãn.
5. Người nghiên cứu gánhuman\_labelvà kiểm chứng.
6. Tính metric đánh giá LLM.
7. Tạofinal\_label, chuyển nhãn thành biến và tínhImpactScorei.
8. Tổng hợp kết quả theo nhãn, domain và chủ thể.
2.7 Dữ liệu đầu vào và tiền xử lý
Dữ liệu đầu vào là văn bản pháp lý môi trường đã được chuyển sang JSON có cấu
trúc. Mỗi bản ghi tương ứng với một đơn vị pháp lý có ý nghĩa xử lý độc lập. Gọi:
D={d 1, d2, . . . , dN }.

15
Một bản ghi có thể được mô tả bởi:
di = (source\_idi, raw\_texti, legal\_citationi, co\_tac\_dongi, chu\_thei, tin\_hieui, ly\_doi, domaini).
File JSON đầu vào cần giữ được cấu trúc pháp lý, tuân theo văn bản gốc và có
đủ thông tin phục vụ phân loại và tính điểm. Các trường tối thiểu gồmsource\_id,
legal\_citation, raw\_text, co\_tac\_dong, chu\_the, tin\_hieu\_tac\_dong, domain, gia\_tri\_dinh\_luong
vàdieu\_kien\_ap\_dung.
Nguyên tắc tách bản ghi là mỗi record nên tương ứng với một đơn vị pháp lý nhỏ
nhất có ý nghĩa phân tích độc lập. Nếu một khoản có nhiều chủ thể, nhiều nghĩa vụ
hoặc nhiều tác động độc lập, nên tách thành nhiều record để tránh gán nhãn mơ hồ.
Tiền xử lý gồm các bước: kiểm tra JSON hợp lệ, kiểm tra trường bắt buộc, lọc
co\_tac\_dong=true, lọc tác động môi trường, chuẩn hóa các trường phục vụ LLM, tạo
file gán nhãn thủ công và tạo file input cho LLM.
2.8 Bộ nhãn phân loại tác động
Hệ thống sử dụng bộ nhãn 5 lớp:
L={BENEFIT\_QUANTITATIVE,BENEFIT\_QUALITATIVE,COST\_QUANTITATIVE,
COST\_QUALITATIVE,CONSTRAINT}.
Bảng 2.2: Bộ nhãn phân loại tác động
Nhãn Ý nghĩa Dấu
BENEFIT\_QUANTITATIVE Lợi ích có thể lượng hóa trực tiếp bằng tiền, tỷ lệ,
khối lượng, diện tích, công suất hoặc lượng phát
thải giảm.
+1
BENEFIT\_QUALITATIVE Lợi ích môi trường, xã hội, quản lý hoặc kinh tế
nhưng chưa có giá trị số trực tiếp.
+1
COST\_QUANTITATIVE Chi phí hoặc nghĩa vụ tài chính có giá trị định
lượng trực tiếp.
−1
COST\_QUALITATIVE Chi phí hoặc gánh nặng tuân thủ chưa có số cụ
thể, như lập hồ sơ, báo cáo, quan trắc, xin phép.
−1
CONSTRAINT Điều kiện, giới hạn, lệnh cấm, tiêu chuẩn, quy
chuẩn, ngưỡng kỹ thuật, điều kiện vận hành.
−1

16
Quy tắc quan trọng là có số không đồng nghĩa với nhãn định lượng. Nếu con số là
thời hạn, ngưỡng kỹ thuật, hạn mức, hạn ngạch hoặc điều kiện áp dụng, nhãn phù hợp
thường là CONSTRAINT. Nếu điều khoản chứa nhiều tác động độc lập, cần tách record
hoặc đánh dấu là cần người nghuên cứu review.
2.9 Thiết kế prompt LLM
Prompt LLM đóng vai trò như bản đặc tả nhiệm vụ cho mô hình. Prompt cần cung
cấp bối cảnh, định nghĩa 5 nhãn, quy tắc phân biệt nhãn, yêu cầu không suy diễn ngoài
văn bản, yêu cầu trích bằng chứng và định dạng JSON đầu ra.
Đầu vào cho LLM là một JSON record gồmsource\_id, legal\_citation, raw\_text,
chu\_the, tin\_hieu\_tac\_dong, domain, gia\_tri\_dinh\_luong và dieu\_kien\_ap\_dung.
Đầu ra bắt buộc:
1{
2" label ": " B E N E F I T \_ Q U A N T I T A T I V E | B E N E F I T \_ Q U A L I T A T I V E | C O S T \_ Q U A N T I T A T I V E |
C O S T \_ Q U A L I T A T I V E | C O N S T R A I N T " ,
3" reason ": " Giai thich ngan gon bang tieng Viet ." ,
4" e v i d e n c e \_ s p a n ": " Cum tu hoac cau trong ra w\_t ex t lam bang chung ." ,
5" c o n f i d e n c e ": 0.0 ,
6" n e e d s \_ h u m a n \_ r e v i e w ": false
7}
Listing 2.1: Cấu trúc output LLM
Prompt cần nhấn mạnh các quy tắc: chỉ chọn một nhãn, không tạo nhãn mới,
không tự ước lượng chi phí/lợi ích, không xem mọi con số là định lượng, phân biệt
COST\_QUALITATIVE với CONSTRAINT, và đánh dấuneeds\_human\_review=true nếu bản
ghi mơ hồ.
2.10 Xây dựng Human-labeled Reference Dataset
Trong phạm vi đồ án, tập dữ liệu do người nghiên cứu gán nhãn được gọi là nhãn cơ
sở (Human-labeled Reference Dataset) . Đây là tập dữ liệu gồm các bản ghixi ∈X đã
được người nghiên cứu gán nhãn thủ công. Với mỗi bản ghi:
yi ∈L.
Tập nhãn con người:
Y={y 1, y2, . . . , yM }.

17
Mỗi bản ghi trong tập này cần có các nhóm trường: truy vết pháp lý, mô tả
tác động, nhãn thủ công, kết quả LLM và trường dùng cho tính điểm. Các cột
quan trọng gồmsource\_id, legal\_citation, raw\_text, human\_label, human\_reason,
llm\_label,llm\_reason,evidence\_span,final\_label,M i,S i,D i,R i,W i.
Quy trình xây dựng gồm: chuẩn bị tậpX, tạo file Excel/CSV để gán nhãn, người
nghiên cứu gánhuman\_label, ghi human\_reason, đánh dấu các bản ghi mơ hồ, kiểm
tra tính hợp lệ và nhất quán của nhãn.
2.11 Đánh giá LLM so với nhãn con người
Sau khi có nhãn LLMˆyi và nhãn cơ sởyi, hệ thống so sánh:
Ii =



1,nếuy i = ˆyi,
0,nếuy i ̸= ˆyi.
Từ đó xây dựng Confusion Matrix, tính Accuracy, Precision, Recall, F1-score, Macro-
F1 và Human Correction Rate. Các bản ghi có nhãn khác nhau được đưa vào phân
tích lỗi, đặc biệt với các cặp dễ nhầm nhưCOST\_QUALITATIVE và CONSTRAINT. Kết quả
đánh giá được sử dụng để cải thiện prompt theo vòng lặp:
LLM Classif ication→M etrics→Error Analysis→P rompt Ref inement.
2.12 Mô hình toán học lượng hóa tác động
2.12.1 Biến đầu vào
Sau khi cófinal\_label, hệ thống ánh xạ nhãn sang hướng tác động:
s:L → {−1,+1},
s(lk) =



+1, l k ∈ {BENEFIT\_QUANTITATIVE,BENEFIT\_QUALITATIVE},
−1, l k ∈ {COST\_QUANTITATIVE,COST\_QUALITATIVE,CONSTRAINT}.

18
Bảng 2.3: Các biến trong mô hình điểm tác động.
Biến Ý nghĩa Thang đo
si Hướng tác động của điều khoảni.+1hoặc−1
Mi Magnitude – cường độ tác động. 1–5
Si Scope – phạm vi ảnh hưởng. 1–5
Di Duration – thời gian tác động. 1–5
Ri Risk/Reversibility – rủi ro hoặc khó đảo ngược. 1–5
Wi Trọng số theo đối tượng, lĩnh vực hoặc mức ưu tiên. Số dương
α, β, γ, δTrọng số của bốn tiêu chí. Tổng bằng 1
2.12.2 Điểm tổng hợp chưa chuẩn hóa
Với mỗi bản ghii,
si =s(f inal\_labeli).
, điểm tổng hợp chưa chuẩn hóa được tính bởi:
Ci =αM i +βS i +γD i +δR i.
trong đóα+β+γ+δ= 1.
2.12.3 Chuẩn hóa điểm
DoM i,S i,D i,R i đều nằm trên thang 1–5 vàα+β+γ+δ= 1, nênC i cũng nằm
trong khoảng 1–5. Vì vậy, điểm chuẩn hóa được xác định bởi:
C norm
i = Ci −1
4 .
Khi đóC norm
i ∈\[0,1].
2.12.4 Điểm tác động của điều khoản
Điểm tác động của bản ghiiđược tính bởi:
ImpactScorei =s i ×W i ×C norm
i .
2.12.5 Điểm tác động tổng hợp
NếuW i = 1,ImpactScore i ∈\[−1,1].

19
Tổng điểm tác động của toàn bộ tập bản ghi là:
TotalImpact =
nX
i=1
ImpactScorei.
Có thể tổng hợp theo nhãn, domain và chủ thể chịu tác động:
TotalImpact(lk) =
X
{i:f inal\_labeli=lk}
ImpactScorei.
2.12.6 Giả định trọng số
Trong phiên bản hiện tại, nếu chưa có dữ liệu chuyên gia hoặc tài liệu đủ mạnh để
hiệu chỉnh, đồ án sử dụng giả định trọng số bằng nhau:
α=β=γ=δ= 0.25.
vàW i = 1nếu chưa có cơ sở ưu tiên theo domain/chủ thể.
Đây là giả định ban đầu của tác giả, không phải kết luận khách quan. Hướng phát
triển là hiệu chỉnh trọng số bằng chuyên gia, AHP, entropy weighting hoặc phân tích
độ nhạy \[11].

Chương 3
Kết quả và đánh giá thực nghiệm
3.1 Thiết lập thực nghiệm
Thực nghiệm được thiết kế để kiểm tra toàn bộ pipeline từ dữ liệu pháp lý dạng
JSON đến kết quả phân loại, đánh giá và tính điểm. Dữ liệu thực nghiệm định hướng là
Luật Bảo vệ môi trường năm 2020 đã được tách cấu trúc thành JSON. Hệ thống thực
hiện các bước: đọc JSON, kiểm tra chất lượng dữ liệu, lọcco\_tac\_dong=true, lọc tác
động môi trường, tạo file gán nhãn thủ công, gọi LLM phân loại 5 nhãn, so sánh với
human\_label, tính metric và tính Impact Score.
Các cấu hình cần ghi rõ trong thực nghiệm gồm: mô hình LLM sử dụng, phiên
bản prompt, số bản ghi gửi vào LLM, số output hợp lệ, số output lỗi, số bản ghi có
human\_label, số bản ghi dùng để tính metric và bộ trọng số dùng trong mô hình Impact
Score.
3.2 Thống kê dữ liệu
Thống kê dữ liệu cần trình bày số bản ghi qua từng giai đoạn:
20

21
Bảng 3.1: Thống kê tổng quan dữ liệu qua các bước xử lý
Giai đoạn dữ liệu Ký hiệu Số lượng
Tổng số bản ghi pháp lý ban đầuN1000
Bản ghi cóco\_tac\_dong=trueM legal 581
Bản ghi có tác động môi trườngM581
Bản ghi cóhuman\_labelhợp lệM h 581
Bản ghi cóllm\_labelhợp lệM l 581
Bản ghi dùng để tính metricM eval 581
Các tỷ lệ cần tính:
rlegal = Mlegal
N , r env|legal = M
Mlegal
, r env = M
N .
Ngoài thống kê tổng quan, báo cáo cần trình bày phân bố 5 nhãn theohuman\_label,
phân bố 5 nhãn theollm\_label, thống kê theo domain môi trường, theo chủ thể chịu
tác động, theo giá trị định lượng và theo trạng thái cần review.
3.3 Kết quả phân loại của LLM
Kết quả phân loại của LLM gồm nhãn dự đoán, lý do phân loại, đoạn bằng chứng và
mức tự tin. Trước khi đánh giá, cần thống kê output hợp lệ và output lỗi. Một output
hợp lệ cần cólabel thuộc đúng 5 nhãn,reason, evidence\_span, confidence∈ \[0, 1]
vàneeds\_human\_review. Phân bố nhãn LLM được tính bởi:
nLLM
k =|{i|ˆy i =l k}|, p LLM
k = nLLM
k
Mvalid
.
Bảng cần trình bày:
Bảng 3.2: Phân bố nhãn do LLM dự đoán
Nhãn Số lượng Tỷ lệ
BENEFIT\_QUANTITATIVE0 ...
BENEFIT\_QUALITATIVE18 ...
COST\_QUANTITATIVE0 ...
COST\_QUALITATIVE316 ...
CONSTRAINT247 ...

22
Kết quả LLM chỉ là nhãn dự đoán ban đầu, chưa phải nhãn cuối cùng. Chất lượng
của kết quả này được đánh giá ở mục tiếp theo thông qua so sánh vớihuman\_label.
Bảng 3.3: Bảng kết quả đánh giá phân loại tổng hợp.
Metric Giá trị
Accuracy 66.95%
Macro F1 34.73%
Human Correction Rate 33.05%
Bảng 3.4: Bảng metric theo từng nhãn.
Nhãn Precision Recall F1-score Số lượng
BENEFIT\_QUANTITATIVE0.000 0.000 0.000 0
BENEFIT\_QUALITATIVE0.300 0.500 0.375 18
COST\_QUANTITATIVE0.000 0.000 0.000 0
COST\_QUALITATIVE0.700 0.747 0.723 316
CONSTRAINT0.706 0.583 0.639 247
3.4 Phân tích ma trận nhầm lẫn
Ma trận nhầm lẫn giúp chỉ ra LLM thường nhầm giữa nhãn nào với nhãn nào. Trong
bài toán này, một cặp nhãn cần chú ý làCOST và CONSTRAINT, vì nhiều điều khoản
ràng buộc kỹ thuật có thể đồng thời tạo ra chi phí tuân thủ. Việc phân tích lỗi giúp cải
thiện prompt, điều chỉnh quy tắc gán nhãn và tăng độ tin cậy của hệ thống.
Bảng 3.5: Mẫu bảng phân tích các trường hợp LLM phân loại sai.
Record ID Human label LLM label Lý do sai
... ... ... ...
Ma trận nhầm lẫn cho bài toán 5 nhãn được định nghĩa bởi:
Ckj =|{i|y i =l k,ˆyi =l j}|.

23
Bảng 3.6: Mẫu ma trận nhầm lẫn giữa human label và LLM label
Human\\LLMBENEFIT\_QUANTITATIVE BENEFIT\_QUALITATIVE COST\_QUANTITATIVE COST\_QUALITATIVE CONSTRAINT
BENEFIT\_QUANTITATIVEC 11 C12 C13 C14 C15
BENEFIT\_QUALITATIVEC 21 C22 C23 C24 C25
COST\_QUANTITATIVEC 31 C32 C33 C34 C35
COST\_QUALITATIVEC 41 C42 C43 C44 C45
CONSTRAINTC 51 C52 C53 C54 C55
Các phần tử trên đường chéo chínhcij với i = j, i, j= 1,5 là dự đoán đúng. Các
phần tử ngoài đường chéo là lỗi. Các cặp lỗi cần phân tích kỹ gồmCOST\_QUALITATIVE–
CONSTRAINT, BENEFIT\_QUANTITATIVE–BENEFIT\_QUALITATIVE, COST\_QUANTITATIVE–COST\_QUALITATIVE
vàBENEFIT\_QUALITATIVE–CONSTRAINT.
Một số lỗi có thể chỉ làm sai mức độ diễn giải, nhưng một số lỗi làm đổi dấusi. Ví
dụ, nếu CONSTRAINT bị gán thànhBENEFIT\_QUALITATIVE, điểm tác động có thể đổi từ
âm sang dương. Vì vậy, Confusion Matrix không chỉ dùng để tính metric, mà còn để
đánh giá rủi ro lan truyền sai số sang mô hình Impact Score.
3.5 Kết quả tính điểm tác động
Sau khi cófinal\_label, hệ thống tínhsi, chấm Mi, Si, Di, Ri, tính Ci, chuẩn hóa
C norm
i và tínhImpactScore i.
Bảng 3.7: Bảng kết quả tính Impact Score cho từng điều khoản
source\_id legal\_citation final\_labels i Mi Si Di Ri Cnorm
i Wi ImpactScorei
... ... ... ... ... ... ... ... ... ... ...
Tổng điểm tác động:
TotalImpact =
MscoreX
i=1
ImpactScorei.
Có thể tổng hợp theo nhãn:
TotalImpact(lk) =
X
{i:y final
i =lk}
ImpactScorei,
theo domain môi trường và theo chủ thể chịu tác động.
Cần diễn giải rằngImpactScorei là điểm tương đối, không phải giá trị tiền tệ. Điểm

24
âm không đồng nghĩa điều khoản là xấu về chính sách; nó phản ánh chi phí, nghĩa vụ
hoặc ràng buộc đối với chủ thể chịu điều chỉnh trong phạm vi mô hình.
Bảng 3.8: Bảng kết quả tổng hợp điểm tác động.
Chỉ tiêu Giá trị
Tổng Impact Score -373.5625
Impact Score trung bình -0.6430
Số điều khoản điểm dương 18
Số điều khoản điểm âm 563
Điều khoản có điểm dương cao nhất 0.9375
Điều khoản có điểm âm thấp nhất -1.000
Bảng 3.9: Bảng tổng hợp Impact Score theo nhãn.
Nhãn Số lượng Tổng Impact Score Trung bình Impact Score
BENEFIT\_QUANTITATIVE... ... ...
BENEFIT\_QUALITATIVE... ... ...
COST\_QUANTITATIVE... ... ...
COST\_QUALITATIVE... ... ...
CONSTRAINT... ... ...
3.6 Nhận xét kết quả
Phần nhận xét cần trả lời các câu hỏi:
•LLM làm tốt ở nhãn nào?
•LLM dễ sai ở nhãn nào?
•Human Verification giúp phát hiện lỗi gì?
•Impact Score có giúp so sánh điều khoản không?
•Các điểm số có bị phụ thuộc vào trọng số không?
Kết quả thực nghiệm cần được nhận xét theo bốn khía cạnh. Thứ nhất, pipeline
dữ liệu có cấu trúc rõ ràng và phù hợp với bài toán, vì dữ liệu được lọc qua các bước
D→X legal →X . Thứ hai, LLM có khả năng hỗ trợ phân loại ban đầu, nhưng không
đủ để thay thế con người do vẫn có các cặp nhãn dễ nhầm. Thứ ba, Human Verification

25
giúp kiểm soát sai số và tạo cơ sở để đánh giá LLM bằng metric. Thứ tư, mô hình
Impact Score giúp chuyển kết quả phân loại thành điểm tương đối có thể diễn giải.
Kết quả quan trọng nhất của thực nghiệm không chỉ là một con số Accuracy hoặc
TotalImpact, mà là chứng minh chuỗi xử lý có kiểm chứng là khả thi:
Legal JSON→Environmental Impact Records→LLM Label
→Human Label→Evaluation Metrics→Final Label→Impact Score.

Chương 4
Kết luận, hạn chế và hướng phát
triển
4.1 Kết luận
Đồ án đã xây dựng được một khung xử lý và đánh giá tác động chính sách môi
trường từ văn bản pháp lý định dạng JSON. Hệ thống bắt đầu từ dữ liệu đã bóc tách
cấu trúc, lọc các bản ghi có tác động pháp lý, sau đó, từ các bản ghi có tác động pháp
lý, tiếp tục lọc các bản ghi có tác động đến môi trường, dùng LLM để phân loại các
bản ghi có tác động tới môi trường vào 5 nhãn, kiểm chứng bằng nhãn cơ sở do người
nghiên cứu gán, đánh giá bằng metric và tính Impact Score bằng mô hình bán định
lượng.
Về mặt bài toán, đồ án đã mô hình hóa được chuỗi;
D→X legal →X→ˆy→Y→Y final →ImpactScore
Chuỗi này giúp biến các điều khoản pháp lý thành dữ liệu có cấu trúc, có nhãn, có
thể đánh giá độ chính xác và lượng hóa.
Vê mặt hệ thống, pipeline được thiết kế rõ ràng và LLM không được coi là kết quả
cuối cùng. Về mặt phương pháp, đồ án kết họp các kiến thức nền tảng về RIA, EIA,
CBA, Human in the loop và mô hình bán định lượng. Về mặt toán học, đồ án định
nghĩa có biếnMi, Si, Di, Ri, Wi, si, công thức chuẩn hóa và công thứcImpactScore i rõ
ràng.
Hiện tại, đồ án đã đạt được các kết quả sau: xây dựng được pipeline xử lý văn bản
pháp luật dạng JSON, định nghĩa không gian 5 nhãn, dùng LLM hỗ trợ phân loại ban
đầu, xây dựng được bộHuman-label Reference Dataset , đánh giá LLM bằng metric,
26

27
chuyển nhãn thành biến và tính ImpactScore.
Khi có kết quả thực nghiệm, phần kết luận cần trả lời lại các câu hỏi nghiên cứu:
LLM đạt độ chính xác như thế nào so với human label, những lỗi chính của LLM là gì,
Human Verification Workflow đóng vai trò gì và công thức Impact Score có giúp lượng
hóa tác động hay không. Không nên diễn đạt kết quả theo hướng tuyệt đối; cách viết
phù hợp là: phương pháp đề xuất có tính khả thi trong phạm vi dữ liệu thử nghiệm và
cung cấp một khung có thể mở rộng cho các văn bản pháp lý môi trường khác.
4.2 Hạn chế
Thứ nhất, chất lượng kết quả phụ thuộc vào file JSON đầu vào. Nếu văn bản thô được
tách sai cấu trúc, thiếuraw\_text, thiếu legal\_citation hoặc gán saico\_tac\_dong,
các bước phía sau sẽ bị ảnh hưởng.
Thứ hai, phạm vi dữ liệu thực nghiệm còn giới hạn. Nếu mới thử trên một văn bản
như Luật Bảo vệ môi trường 2020, chưa thể kết luận hệ thống hoạt động tốt trên mọi
nghị định, thông tư, quy chuẩn hoặc văn bản pháp lý môi trường khác.
Thứ ba, Human-labeled Reference Dataset có thể còn yếu tố chủ quan nếu chỉ do
một người nghiên cứu gán nhãn.
Thứ tư, LLM vẫn có thể nhầm giữa các nhãn gần nhau nhưCOST\_QUALITATIVE và
CONSTRAINT, hoặc giữa nhãn định lượng và định tính. Kết quả LLM phụ thuộc vào
prompt, mô hình, phiên bản API và cấu hình gọi.
Thứ năm, bài toán hiện tại là phân loại một nhãn. Trong thực tế, một điều khoản
có thể mang nhiều tác động đồng thời. Việc ép vào một nhãn chính có thể làm mất
một phần thông tin.
Thứ sáu, Impact Score là mô hình bán định lượng, chưa phải CBA đầy đủ bằng tiền.
Các biến Mi, Si, Di, Ri và trọng số vẫn có yếu tố giả định. Nếu chưa có phân tích độ
nhạy, chưa thể khẳng định kết quả ổn định khi thay đổi trọng số.
4.3 Hướng phát triển
Từ các hạn chế trên, hệ thống có thể phát triển theo các hướng sau.
Thứ nhất, mở rộng dữ liệu pháp lý đầu vào sang nhiều văn bản môi trường khác
như nghị định, thông tư, quy chuẩn kỹ thuật, văn bản về chất thải, khí thải, nước thải,
biến đổi khí hậu, phát thải khí nhà kính, đa dạng sinh học và xử phạt môi trường.
Thứ hai, hoàn thiện quy trình chuyển văn bản pháp lý thô từ PDF/Word/OCR
sang JSON. Quy trình cần nhận diện đúng chương, mục, điều, khoản, điểm, giữ nguyên

28
nội dung pháp lý gốc, tách record hợp lý và kiểm tra chất lượng schema.
Thứ ba, nâng cấp Human-labeled Reference Dataset thành Gold Dataset bằng cách
có nhiều người gán nhãn độc lập, đo Inter-Annotator Agreement, xử lý bất đồng và
mời chuyên gia xác nhận các trường hợp khó.
Thứ tư, cải thiện prompt và so sánh nhiều LLM. Mỗi phiên bản prompt cần được
lưu lại cùng metric tương ứng. Có thể so sánh Gemini, GPT, Claude, DeepSeek hoặc
các mô hình mã nguồn mở trên cùng tập dữ liệu.
Thứ năm, mở rộng từ phân loại một nhãn sang phân loại đa nhãn hoặc tách record
nhỏ hơn. Điều này giúp xử lý tốt hơn các điều khoản có nhiều tác động đồng thời.
Thứ sáu, nâng cấp mô hình Impact Score bằng cách hiệu chỉnh trọng số theo chuyên
gia, AHP, entropy weighting hoặc phân tích độ nhạy. Có thể bổ sungWi theo domain
môi trường, nhóm chủ thể, mức độ nhạy cảm hoặc ưu tiên chính sách.
Thứ bảy, bổ sung phân tích độ nhạy và phân tích kịch bản. Khi có đủ dữ liệu phân
phối, có thể mở rộng sang Monte Carlo, nhưng chỉ nên triển khai khi có cơ sở dữ liệu
và giả định rõ ràng.
Thứ tám, tiến tới CBA đầy đủ hơn khi có dữ liệu định lượng như chi phí tuân thủ,
lợi ích giảm ô nhiễm, dữ liệu phát thải, lợi ích sức khỏe, tỷ lệ chiết khấu và dòng chi
phí – lợi ích theo thời gian.
Thứ chín, phát triển dashboard trực quan hóa và báo cáo tự động. Dashboard có
thể hỗ trợ tải JSON, xem dữ liệu qua từng bước lọc, gán nhãn human, xem metric, ma
trận nhầm lẫn, Impact Score và xuất báo cáo.
Thứ mười, phát triển Knowledge Graph pháp lý – môi trường để biểu diễn quan hệ
giữa điều khoản, chủ thể, nghĩa vụ, điều kiện, domain, nhãn và điểm tác động. Hướng
này giúp hệ thống không chỉ phân tích bảng dữ liệu mà còn truy vấn được quan hệ
pháp lý – môi trường.

Phụ lục A
Mẫu JSON đầu vào
1{
2" m a\_ ng uon ":
3" t r i c h \_ d a n ":
4" n oi \_d ung ":
5" c o \_ t a c \_ d o n g = true ":
6" c h u \_ t h e \_ c h i u \_ t a c \_ d o n g ":
7" t i n \_ h i e u \_ t a c \_ d o n g ": \[] ,
8" l i n h \_ v u c \_ t a c \_ d o n g ": \[] ,
9" g i a \_ t r i \_ d i n h \_ l u o n g ": \[] ,
10" d i e u \_ k i e n \_ a p \_ d u n g ": \[] ,
11" ly\_do ": ,
12" Vi\_tri ": ,
13" VBQPPL ": " L u a t \_ b a o \_ v e \_ m o i \_ t r u o n g \_ 2 0 2 0 "
14
15}
Listing A.1: Mẫu bản ghi JSON đầu vào
29

Phụ lục B
Prompt LLM
30

Phụ lục C
Hướng dẫn gán nhãn thủ công
Bảng C.1: Hướng dẫn gán nhãn thủ công.
Nhãn Điều kiện gán nhãn Hướng tác
động
BENEFIT Điều khoản tạo lợi ích môi trường, giảm phát
thải, khuyến khích hành vi tích cực hoặc tăng
hiệu quả quản lý.
+1
COST Điều khoản tạo nghĩa vụ, thủ tục, báo cáo, chi
phí đầu tư, vận hành hoặc giám sát.
−1
CONSTRAINT Điều khoản đặt điều kiện, giới hạn, tiêu chuẩn,
ngưỡng kỹ thuật, thời hạn hoặc điều kiện áp
dụng.
−1
31

Phụ lục D
Hướng dẫn chấm điểm 1–5
Bảng D.1: Gợi ý rubric chấm điểm mức độ tác động.
Điểm Ý nghĩa chung
1 Tác động rất thấp, phạm vi hẹp, ngắn hạn hoặc dễ đảo ngược.
2 Tác động thấp, ảnh hưởng có giới hạn, ít rủi ro.
3 Tác động trung bình, ảnh hưởng rõ nhưng chưa rộng hoặc chưa
nghiêm trọng.
4 Tác động cao, phạm vi tương đối rộng, kéo dài hoặc có rủi ro
đáng kể.
5 Tác động rất cao, phạm vi rộng, dài hạn, rủi ro lớn hoặc khó
đảo ngược.
32

Phụ lục E
Mapping tài liệu tham khảo với
thành phần hệ thống
Bảng E.1: Bảng mapping tài liệu tham khảo với quyết định thiết kế.
Thành phần hệ thốngTài liệu chính Vai trò
RIA/EIA background World Bank, European
Commission
Bối cảnh và tính cấp thiết.
CBA OECD, de Zeeuw, Rad-
hakrishnan
Cơ sở lượng hóa lợi ích và chi
phí.
LLM classification Bermejo, Kwak Biện minh dùng LLM và
evidence\_span.
Legal ambiguity Italiani, Demetriou Biện minh phân tích lỗi và
Confusion Matrix.
Human Verification Tsaneva, Bonet-Jover,
Wang
Biện minh human label và cor-
rection rate.
Impact scoring 1–5 Tutuka, IMPERIA Biện minh Mi, Si, Di, Ri và
thang 1–5.
Duration O’Mahony Biện minh biếnD i.
Risk/Reversibility OECD, Espinoza Biện minh biếnRi và penalty.
Weight sensitivity Bompoti Hạn chế và hướng phát triển
trọng số.
33

34
Thành phần hệ thốngTài liệu chính Vai trò
Monte Carlo future work Environment Canada,
Ohlin Saletti
Biện minh chưa dùng Monte
Carlo và hướng mở rộng.

Tài liệu tham khảo
\[1] H. Kwak et al., “Information extraction from legal wills: How well does gpt-4 do?”arXiv preprint,
2023.
\[2] P. Bermejo et al., “Llms outperform outsourced human coders on complex textual analysis,”
Working Paper, 2025.
\[3] D. Italiani et al., “Clash-of-leges: A bilingual dataset for conflict detection and explanation in
statutory law,”Preprint, 2026.
\[4] C. Demetriou, “Assessing chatgpt’s legal reasoning in statutory land consolidation: The case of
cyprus,”Preprint, 2026.
\[5] Z. Wang et al., “Putting humans in the natural language processing loop: A survey,”Proceedings of
the First Workshop on Bridging Human–Computer Interaction and Natural Language Processing,
2021.
\[6] S. Tsaneva et al., “Knowledge graph validation by integrating llms and human-in-the-loop,”
Preprint, 2025.
\[7] S. Bajestani et al., “Human-in-the-loop and large language models in smart manufacturing:
Current applications, challenges, and perspectives,”Preprint, 2026.
\[8] A. Bonet-Jover et al., “Applying human-in-the-loop to construct a dataset for determining content
reliability to combat fake news,”Data in Brief, 2023.
\[9] T. P. Station,Impact significance determination: Assessment methodology, Environmental Impact
Assessment documentation, 2013.
\[10] IMPERIA Project, “Good practices for impact significance determination,” IMPERIA Project,
2013.
\[11] N. Bompoti et al., “Advancing cumulative impact assessment frameworks: The role of context-
specific methodologies,”Preprint, 2026.
35

