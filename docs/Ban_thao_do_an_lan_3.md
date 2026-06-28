ĐẠI HỌC BÁCH KHOA HÀ NỘI
KHOA TOÁN – TIN
–o0o–
ĐÁNH GIÁ TÁC ĐỘNG CHÍNH SÁCH
MÔI TRƯỜNG: KHUNG ĐỊNH LƯỢNG
CHI PHÍ – LỢI ÍCH – RÀNG BUỘC
ĐỒ ÁN I
Chuyên ngành:TOÁN TIN
Giảng viên hướng dẫn: PGS. TS. Nguyễn Thị Ngọc Anh
Sinh viên thực hiện: Đinh Công Khang
Mã số sinh viên: 20237351
Lớp: Toán–Tin 02–K68
Hà Nội, tháng 6, năm 2026

Nhận xét của giảng viên hướng dẫn
1.Mục tiêu và nội dung của đồ án
(a) Mục tiêu: xây dựng một pipeline hỗ trợ đánh giá tác động chính sách môi
trường từ văn bản quy phạm pháp luật đã được cấu trúc hóa.
(b) Nội dung: nghiên cứu cơ sở phương pháp luận RIA, EIA và CBA; thiết kế
pipeline có kiểm chứng của con người; đánh giá độ chính xác phân loại của
mô hình ngôn ngữ lớn ở bài toán phân loại nhị phân và phân loại đa lớp
đơn nhãn; chuẩn hóa chủ thể,lĩnh vực; xây dựng mô hình bán định lượng
để tính điểm tác động chính sách.
2.Kết quả đạt được
..............................................................................
..............................................................................
..............................................................................
..............................................................................
3.Ý thức làm việc của sinh viên
..............................................................................
..............................................................................
..............................................................................
..............................................................................
Hà Nội, ngày tháng năm 2026
Giảng viên hướng dẫn
PGS. TS. Nguyễn Thị Ngọc Anh
i

Lời cảm ơn
Em xin gửi lời cảm ơn chân thành đến các thầy cô Khoa Toán – Tin, Đại học Bách
khoa Hà Nội, đã trang bị cho em nền tảng kiến thức về toán ứng dụng, tin học và
phương pháp nghiên cứu trong quá trình học tập. Những kiến thức này là cơ sở quan
trọng để em thực hiện đồ án theo hướng kết hợp mô hình toán học, xử lý dữ liệu và
phân tích chính sách môi trường.
Em xin bày tỏ lòng biết ơn sâu sắc đến PGS. TS. Nguyễn Thị Ngọc Anh, giảng viên
hướng dẫn đồ án, đã định hướng đề tài, góp ý về phương pháp, định hướng nghiên cứu
và hỗ trợ em hoàn thiện cách trình bày kết quả. Những nhận xét của cô giúp em điều
chỉnh nội dung theo hướng rõ ràng, có cơ sở phương pháp luận và phù hợp với yêu cầu
của một đồ án chuyên ngành Toán – Tin.
Bên cạnh đó, em cũng muốn gửi lời cảm ơn chân thành đến các anh chị khóa trên,
những người đã nhiệt tình chia sẻ kinh nghiệm, hướng dẫn em trong quá trình thực
hiện đồ án. Sự hỗ trợ và những lời khuyên quý báu từ anh chị đã giúp em vượt qua
nhiều khó khăn và hoàn thiện đồ án của mình.
Mặc dù đã cố gắng xây dựng hệ thống và kiểm tra kết quả ở từng bước, đồ án vẫn
khó tránh khỏi hạn chế về phạm vi, kinh nghiệm và mức độ kiểm chứng . Em kính
mong nhận được các góp ý từ thầy cô để tiếp tục hoàn thiện nghiên cứu trong các giai
đoạn tiếp theo.
ii

Tóm tắt
Đồ án trình bày một pipeline hỗ trợ đánh giá tác động chính sách môi trường từ
văn bản quy phạm pháp luật đã được cấu trúc hóa. Đối tượng thực nghiệm là Luật
Bảo vệ môi trường năm 2020, gồm 581 bản ghi có tác động chính sách. Pipeline được
thiết kế có sự kiểm chứng của con người: lọc tác động môi trường ở tầng một, phân
loại tác động chính sách thành 5 nhãn ở tầng hai, xử lý bất đồng giữa nhãn của người
nghiên cứu và nhãn do mô hình ngôn ngữ lớn dự đoán, chuẩn hóa chủ thể, lĩnh vực
(actor,domain), sau đó lượng hóa điểm tác động bằng mô hình bán định lượng.
Khác với cách tiếp cận tự động hoàn toàn, mô hình ngôn ngữ lớn chỉ được sử dụng
như công cụ hỗ trợ phân loại và trích xuất bằng chứng từ văn bản pháp luật gốc. Nhãn
cuối cùng được chốt thông qua quy trình Human-in-the-loop, trong đó người nghiên
cứu rà soát các trường hợp bất đồng, hiệu chỉnh nhãn và ghi nhận lý do ra quyết định.
Mô hình lượng hóa sử dụng bốn biến thành phần gồm Cường độ tác động (Mi), Phạm
vi tác động (Si), Thời gian tác động (Di), Rủi ro và khả năng phục hồi (Ri), kết hợp
với trọng sốWi và hướng tác độngsi để tínhImpactScoree i.
Kết quả thực nghiệm cho thấy mô hình ngôn ngữ lớn đạt độ chính xác 100% ở
Tầng 1 đối với việc dự đoán các bản ghi tác động môi trường, nhưng chỉ đạt 69.19%
độ chính xác ở Tầng 2 khi phân loại 5 nhãn tác động. Tỷ lệ hiệu chỉnh của con người
ở Tầng 2 là 30.81%, cho thấy quy trình kiểm chứng thủ công là cần thiết để bảo
đảm độ tin cậy, giảm thiểu rủi ro sai số trước khi lượng hóa. Tổng điểm tác động là
TotalImpact = −362.5000và điểm trung bình đạt −0.6239điều này cho thấy phần
lớn các điều khoản tạo nghĩa vụ tuân thủ, ràng buộc kỹ thuật và trách nhiệm quản lý
nhằm phòng ngừa rủi ro sinh thái.
Từ khóa:RIA; EIA; CBA; LLM; HITL; HCR; MCDA; SAW; Impact Score.
iii

Bảng ký hiệu và chữ viết tắt
Ký hiệu / Viết tắtÝ nghĩa
RIA Regulatory Impact Assessment – Đánh giá tác động quy
định hoặc chính sách.
EIA Environmental Impact Assessment – Đánh giá tác động môi
trường.
CBA Cost-Benefit Analysis – Phân tích chi phí – lợi ích.
LLM Large Language Model – Mô hình ngôn ngữ lớn.
HITL Human-in-the-loop – Quy trình có con người tham gia kiểm
chứng.
HCR Human Correction Rate – Tỷ lệ bản ghi cần con người hiệu
chỉnh.
MCDA Multi-Criteria Decision Analysis – Phân tích quyết định đa
tiêu chí.
SAW Simple Additive Weighting – Phương pháp cộng trọng số
đơn giản.
VBQPPL Văn bản quy phạm pháp luật.
ĐTM Đánh giá tác động môi trường.
Dimpact Tập bản ghi đầu vào đã được xác nhận có tác động chính
sách.
Denv Tập bản ghi có tác động chính sách môi trường.
LTập hợp chứa 5 nhãn tác động chính sách môi trường.
yi Nhãn tham chiếu do người nghiên cứu gán cho bản ghi thứ
i.
ˆyi Nhãn do LLM dự đoán cho bản ghi thứi.
$y^{final}_i$ Nhãn cuối cùng sau quy trình xử lý bất đồng.
Mi Magnitude – Cường độ tác động của bản ghi thứi.
Si Scope – Phạm vi chủ thể hoặc không gian chịu tác động
của bản ghi thứi.
ix

Di Duration – Thời gian tác động của bản ghi thứi.
Ri Risk/Reversibility – Rủi ro môi trường và khả năng phục
hồi nếu tác động xảy ra hoặc nếu không tuân thủ.
Wi Trọng số theo đối tượng, lĩnh vực hoặc mức ưu tiên chính
sách của bản ghi thứi.
si Hướng tác động:+1với lợi ích; −1với chi phí tuân thủ
hoặc ràng buộc.
Ci Điểm tổng hợp chưa chuẩn hóa.
$C^{norm}_i$ Điểm tổng hợp đã chuẩn hóa về khoảng[0,1].
ImpactScoreei Điểm tác động chính sách của bản ghi thứi.
TotalImpactTổng điểm tác động của toàn bộ tập bản ghi.
x

Chương 1
Mở đầu
1.1 Bối cảnh và động cơ nghiên cứu
Các văn bản quy phạm pháp luật là công cụ điều tiết vĩ mô, thiết lập nghĩa vụ,
quyền lợi, điều kiện áp dụng và giới hạn hành vi của các chủ thể xã hội. Trong lĩnh vực
môi trường, cấu trúc pháp lý thường phức tạp hơn nhiều so với các miền chính sách
đơn ngành vì một điều khoản có thể đồng thời liên quan đến cơ quan quản lý nhà nước,
doanh nghiệp, chủ dự án đầu tư, cộng đồng dân cư và các thành phần môi trường như
nước, không khí, chất thải, đa dạng sinh học hoặc khí hậu.
Việc đánh giá tác động của một văn bản luật đòi hỏi sự kết hợp giữa ba hướng tiếp
cận. Thứ nhất, Đánh giá tác động quy định (RIA) giúp xác định điều khoản nào thực
sự tạo nghĩa vụ, quyền lợi, điều kiện hoặc ràng buộc chính sách. Thứ hai, Đánh giá
tác động môi trường (EIA) giúp nhận diện mức độ liên quan của điều khoản đến tài
nguyên, hệ sinh thái và rủi ro môi trường. Thứ ba, Phân tích chi phí – lợi ích (CBA)
giúp phân biệt tác động theo chiều lợi ích, chi phí hoặc ràng buộc để phục vụ cho giai
đoạn lượng hóa.
Trong thực tế, đọc và phân loại thủ công hàng trăm điều khoản pháp lý là công việc
tốn thời gian, dễ phụ thuộc vào kinh nghiệm cá nhân và khó tái lập. Các mô hình ngôn
ngữ lớn có khả năng hỗ trợ đọc hiểu, trích xuất tín hiệu pháp lý và đề xuất nhãn ban
đầu. Tuy nhiên, trong miền pháp lý và chính sách công, kết quả của mô hình không
nên được xem là quyết định cuối cùng vì mô hình có thể suy diễn ngoài văn bản, bỏ
sót điều kiện loại trừ hoặc nhầm lẫn giữa nghĩa vụ thủ tục và ràng buộc kỹ thuật.
Vì vậy, đồ án lựa chọn hướng tiếp cận có con người tham gia kiểm chứng. Mô hình
ngôn ngữ lớn được sử dụng như công cụ hỗ trợ phân loại ban đầu; người nghiên cứu
chịu trách nhiệm gán nhãn tham chiếu, xử lý bất đồng và chốt dữ liệu cuối cùng. Sau
đó, các nhãn đã kiểm chứng được chuyển thành biến định lượng để tính điểm tác động
chính sách theo mô hình bán định lượng. Động cơ nghiên cứu của đồ án là xây dựng
1

2
một pipeline minh bạch, có khả năng truy vết từ điểm số cuối cùng về từng bản ghi
trong văn bản quy phạm pháp luật ban đầu.
1.2 Khoảng trống nghiên cứu
Các phương pháp CBA truyền thống thường cần dữ liệu tiền tệ chi tiết như chi phí
tuân thủ của doanh nghiệp, thiệt hại y tế, chi phí xử lý ô nhiễm hoặc giá trị ngoại ứng
môi trường. Ở cấp độ từng điều, khoản, điểm của một văn bản luật, những dữ liệu này
thường chưa có hoặc không đủ chi tiết. Do đó, cần một cách tiếp cận để đánh giá tương
đối tác động từ các nội dung có tác động chính sách.
Bên cạnh đó, các nghiên cứu xử lý ngôn ngữ tự nhiên trong miền pháp lý thường
dừng ở bài toán phân loại văn bản hoặc trích xuất thực thể. Việc chuyển kết quả gán
nhãn định tính thành điểm tác động có công thức toán học rõ ràng vẫn chưa được tích
hợp đầy đủ.
Bên cạnh đó, việc phân tách rõ ràng giữa tác động chính sách chung và tác động môi trường chuyên
biệt. Một bản ghi có thể tạo tác động chính sách nhưng không trực tiếp liên quan đến
môi trường. Nếu không có giai đoạn lọc môi trường riêng biệt, dữ liệu đưa vào phân
loại 5 nhãn sẽ bị nhiễu và làm giảm mức độ rõ ràng của điểm tác động.
1.3 Phát biểu bài toán nghiên cứu
1.3.1 Định nghĩa tập dữ liệu đầu vào có tác động chính sách
Giả sử văn bản quy phạm pháp luật đã được tách cấu trúc thành tập hữu hạn các
bản ghi có tác động chính sách:
Dimpact ={d 1, d2, . . . , dN }, .(1.1)
Mỗi bản ghidi, (i = 1, N)biểu diễn một đơn vị pháp lý nhỏ nhất có thể phân tích độc
lập, chẳng hạn một điều, khoản, điểm hoặc mệnh đề có tác động chính sách. Trong đồ
án, mỗi bản ghi được mô tả bởi bộ thông tin:
di = (source_idi, legal_citationi, raw_texti, actori,
legal_signal i, domaini, quantitative_valuei, conditioni).
(1.2)
Trong đó,source_idi là mã định danh,legal_citation i là trích dẫn pháp lý,raw_texti
là văn bản gốc, actori là chủ thể chịu tác động,legal_signal i là tín hiệu pháp lý,

3
domaini là lĩnh vực môi trường liên quan,quantitative_value i là giá trị định lượng
nếu có, vàconditioni là điều kiện áp dụng.
1.3.2 Bài toán lọc tác động môi trường
Giai đoạn đầu xây dựng một hàm lọc nhị phân:
fenv :D impact → {0,1}.(1.3)
Với mỗid i ∈D impact:
fenv(di) =



1,nếud i có tác động trực tiếp hoặc gián tiếp đến môi trường,
0,nếud i không có tác động đến môi trường,
.
Tập bản ghi môi trường sau lọc được ký hiệu:
Denv ={d i ∈D impact |f env(di) = 1}.(1.4)
1.3.3 Bài toán phân loại năm nhãn tác động chính sách
Giai đoạn hai phân loại mỗi bản ghi trongDenv vào đúng một nhãn trong tập:
L={BQ,BQL,CQ,CQL,CON}.(1.5)
Trong đó:
BQ: lợi ích định lượng,
BQL: lợi ích định tính,
CQ: chi phí định lượng,
CQL: chi phí định tính,
CON: ràng buộc.
Đây là bài toán phân loại đa lớp đơn nhãn:
fclass :D env → L.(1.6)
Nhãn cuối cùng$y^{final}_i$ được xác định sau khi so sánh nhãn người nghiên cứuyi với nhãn
LLMˆyi và thực hiện xử lý bất đồng nếu xảy ra.

4
1.4 Mục tiêu nghiên cứu
Đồ án hướng tới bốn mục tiêu chính. Thứ nhất, xây dựng pipeline phân tích văn
bản pháp luật môi trường theo hai giai đoạn: lọc các tác động liên quan tới môi trường
và phân loại vào 5 nhãn tác động. Thứ hai, đánh giá năng lực hỗ trợ của mô hình ngôn
ngữ lớn bằng các chỉ số phân loại trước khi can thiệp chỉnh sửa. Thứ ba, thiết lập cơ
chế kiểm chứng Human-in-the-loop để chốt nhãn cuối cùng, đồng thời chuẩn hóa chủ
thế (actor) và lĩnh vực ( domain) phục vụ cho giai đoạn lượng hóa và tính điểm. Thứ
tư, xây dựng mô hình bán định lượng MSDR để tính điểm tác động, giúp so sánh tác
động theo nhãn, lĩnh vực và nhóm chủ thể.
1.5 Phạm vi nghiên cứu
Phạm vi nghiên cứu của đồ án được giới hạn trên đối tượng thực nghiệm là Luật
Bảo vệ môi trường năm 2020 của Việt Nam. Dữ liệu đầu vào được giả định đã được
bóc tách và cấu trúc hóa thành 581 bản ghi pháp lý dưới định dạng JSON. Mỗi bản
ghi được xem là một đơn vị phân tích độc lập, có thông tin về mã định danh, trích dẫn
pháp lý, nội dung văn bản gốc, chủ thể chịu tác động, tín hiệu pháp lý, lĩnh vực tác
động và điều kiện áp dụng.
Về phương pháp, đồ án tập trung xây dựng pipeline gồm các bước: lọc bản ghi có
tác động môi trường, phân loại tác động vào 5 nhãn chính sách, chuẩn hóa nhóm chủ
thể và lĩnh vực môi trường, sau đó lượng hóa tác động bằng mô hình bán định lượng
MSDR với bốn biến: cường độ(Mi), phạm vi(Si), thời gian(Di)và rủi ro( Ri). Mô
hình ngôn ngữ lớn được sử dụng như công cụ hỗ trợ gán nhãn, trích xuất lý do và bằng
chứng, không được dùng để tự động quyết định kết quả cuối cùng.
Đồ án sử dụng giả định trọng số cơ sở(α = β = γ = δ = 0.25)và( Wi = 1.0).
Nghiên cứu không thực hiện phân tích chi phí - lợi ích bằng tiền tệ, không thẩm định
hiệu lực pháp lý của văn bản và không thay thế ý kiến chuyên gia pháp lý hoặc chuyên
gia môi trường. ImpactScore phục vụ so sánh tác động giữa các điều khoản, lĩnh vực và
nhóm chủ thể.
1.6 Cấu trúc đồ án
Báo cáo gồm bốn chương. Chương 1 trình bày bối cảnh, khoảng trống nghiên cứu,
bài toán,mục tiêu và phạm vi nghiên cứu. Chương 2 mô tả phương pháp nghiên cứu,
kiến trúc hệ thống, cơ chế kiểm chứng và mô hình lượng hóa. Chương 3 trình bày thiết

5
lập thực nghiệm, kết quả phân loại, kiểm định actor/domain và kết quả tính điểm tác
động. Chương 4 tổng kết kết quả đạt được, nêu hạn chế và đề xuất hướng phát triển.

Chương 2
Phương pháp nghiên cứu và kiến
trúc hệ thống
2.1 Tổng quan khung lý thuyết: RIA, EIA và CBA
Khung phương pháp luận của đồ án được xây dựng trên sự kết hợp có hệ thống
giữa ba trụ cột của phân tích chính sách và kinh tế học môi trường: Đánh giá tác
động quy định (Regulatory Impact Assessment – RIA), Đánh giá tác động môi trường
(Environmental Impact Assessment – EIA) và Phân tích chi phí – lợi ích (Cost–Benefit
Analysis – CBA). Ba cách tiếp cận này được tổ chức thành một chuỗi đánh giá nhiều
lớp: từ nhận diện tác động pháp lý, xác định phạm vi môi trường, xác định hướng tác
động, đến lượng hóa bằng mô hình đa tiêu chí.
Ở cấp độ điều, khoản hoặc điểm, nội dung pháp lý thường chưa đi kèm dữ liệu tiền
tệ, dữ liệu phát thải hoặc dữ liệu thị trường đủ chi tiết để thực hiện CBA đầy đủ. Vì
vậy, đồ án không giả định có thể tiền tệ hóa trực tiếp mọi tác động, mà chuyển hóa các
nguyên lý của RIA, EIA và CBA thành một pipeline có khả năng truy vết, kết hợp
phân loại văn bản với chấm điểm các biến trong MSDR.
6

7
Lớp phương pháp Vai trò trong đồ án Đầu ra
RIA Nhận diện điều khoản có tác
độngchínhsáchthôngquanghĩa
vụ, quyền lợi, thủ tục, điều kiện
hoặc ràng buộc pháp lý.
Tập bản ghi cóco_tac_dong
= true, ký hiệuDimpact.
EIA Khoanh vùng tác động môi
trường và mô tả cường độ của
tác động theo lĩnh vực, không
gian, thời gian và rủi ro sinh
thái.
Lĩnh vực môi trường và bốn
biếnM i, Si, Di, Ri.
CBA Phân biệt chiều tác động theo
lợi ích xã hội, chi phí tuân thủ
và ràng buộc hành vi.
Vector hướng tác độngsi ∈
{−1, +1} và hệ nhãn năm
lớp.
MCDA/SAW Tổng hợp các tiêu chí bán định
lượng thành một chỉ số có thể
so sánh giữa các bản ghi.
Chỉ số tác động
ImpactScoreei.
Bảng 2.1: Vai trò của RIA, EIA, CBA và MCDA/SAW trong khung phương pháp của
đồ án.
2.1.1 Đánh giá tác động quy định
Theo cách tiếp cận RIA của OECD, đánh giá tác động quy định là một công cụ có
tính hệ thống nhằm hỗ trợ quá trình xây dựng chính sách thông qua việc nhận diện chi
phí, lợi ích, rủi ro và các hệ quả thực thi của quy định [1]. Trong đồ án này, RIA được
sử dụng như lớp lọc đầu tiên để trả lời câu hỏi: một bản ghi có thực sự tạo ra tác động
chính sách hay không.
Một điều khoản được xem là có tác động chính sách khi nó làm phát sinh nghĩa vụ
hành vi, thiết lập quyền lợi, quy định thủ tục hành chính, đặt điều kiện gia nhập hoặc
duy trì hoạt động, hoặc áp đặt một ràng buộc kỹ thuật đối với chủ thể chịu điều chỉnh.
Ngược lại, các nội dung chỉ mang tính tuyên bố nguyên tắc, định nghĩa chung, mô tả
kỹ thuật thuần túy hoặc dẫn chiếu không tạo ra ma sát tuân thủ trực tiếp sẽ không
được đưa vào tập lượng hóa chính. Kết quả của lớp RIA là tập bản ghiDimpact, trong
đó mỗi bản ghi đã thỏa điều kiệnco_tac_dong = true và có thể tiếp tục được đánh
giá ở các lớp sau.

8
2.1.2 Đánh giá tác động môi trường
EIA cung cấp cơ sở để nhận diện, dự báo và đánh giá các ảnh hưởng tiềm tàng của
một hoạt động, dự án hoặc chính sách đối với môi trường trước khi quyết định được
ban hành [4, 3]. Khi chuyển sang bối cảnh phân tích văn bản pháp luật, vai trò của
EIA trong đồ án không phải là lập báo cáo đánh giá tác động môi trường theo nghĩa
dự án, mà là xác định phần tác động nào của điều khoản có liên quan trực tiếp đến hệ
sinh thái, tài nguyên và công cụ quản lý môi trường.
Đóng góp thứ nhất của EIA là hệ thống hóa lĩnh vực tác động. Các bản ghi được
phân loại vào các nhóm như nước, chất thải, không khí, đất đai, đa dạng sinh học, biến
đổi khí hậu, giấy phép môi trường, quan trắc, kiểm soát ô nhiễm, kinh tế tuần hoàn và
tài chính môi trường. Cách phân nhóm này giúp khoanh vùng đối tượng chịu tác động
và tạo cơ sở cho các phân tích tổng hợp theodomain_primary và domain_secondary
ở các bước sau.
Đóng góp thứ hai của EIA là cung cấp logic để xây dựng thang đo vật lý của tác
động. Đồ án chuyển hóa các đặc trưng môi trường thành bốn tiêu chí chấm điểm trên
thang 1–5: cường độ tác độngMi (Magnitude), phạm vi không gianSi (Spatial scope),
thời gian tác độngDi (Duration) và mức độ rủi ro sinh thái/khả năng phục hồiRi
(Risk and reversibility). Bốn biến này không nhằm thay thế số liệu đo đạc môi trường
chi tiết, mà đóng vai trò là hệ quy chiếu bán định lượng để so sánh tương đối giữa các
điều khoản trong cùng một văn bản luật.
2.1.3 Phân tích chi phí – lợi ích và phân cực hướng tác động
CBA truyền thống hướng tới việc quy đổi các dòng chi phí và lợi ích xã hội thành
giá trị tiền tệ để so sánh thặng dư ròng của phương án chính sách [5]. Tuy nhiên, đối
với một văn bản luật khung về môi trường, nhiều nghĩa vụ pháp lý chưa thể được lượng
hóa trực tiếp bằng tiền do thiếu dữ liệu thị trường, dữ liệu tuân thủ và dữ liệu thiệt
hại môi trường ở cấp độ từng điều khoản. Nếu cố gắng tiền tệ hóa trong bối cảnh này,
kết quả dễ phụ thuộc vào giả định chủ quan hơn là bằng chứng thực nghiệm.
Vì vậy, đồ án kế thừa nguyên lý phân cực của CBA thay vì thực hiện CBA
đầy đủ. Các điều khoản tạo lợi ích xã hội hoặc lợi ích môi trường, tương ứng với
các nhãnBENEFIT_QUANTITATIVE và BENEFIT_QUALITATIVE, được gán hướng dương
si = +1. Ngược lại, các điều khoản làm phát sinh chi phí tài chính, chi phí tuân thủ,
nghĩa vụ thủ tục hoặc hạn chế hành vi, tương ứng với các nhãnCOST_QUANTITATIVE,
COST_QUALITATIVEvàCONSTRAINT, được gán hướng âms i =−1.
Trên cơ sở đó, không gian nhãn năm lớp của đồ án được thiết kế để phân biệt đồng
thời hai chiều thông tin: bản chất phúc lợi của tác động (lợi ích, chi phí hoặc ràng buộc)

9
và mức độ biểu hiện định lượng của tác động (định lượng hoặc định tính). Kết hợp với
các tiêu chí EIA và mô hình ra quyết định đa tiêu chí MCDA/SAW, vectorsi cho phép
chuyển từ mô tả pháp lý sang chỉ sốImpactScoreei có dấu, qua đó phản ánh không chỉ
độ lớn tương đối mà cả chiều tác động của từng bản ghi chính sách.
2.2 Quy trình xử lý và vai trò của mô hình ngôn
ngữ lớn
Hình 2.1: Pipeline đánh giá tác động chính sách môi trường
Hình 2.1 mô tả luồng xử lý tổng quát của hệ thống. Pipeline được thiết kế theo
nguyên tắc tuần tự: mỗi giai đoạn tạo ra một đầu ra có cấu trúc để làm đầu vào cho
giai đoạn tiếp theo. Cách tổ chức này giúp kết quả cuối cùng có khả năng truy vết
ngược về nhãn phân loại, nhóm chủ thể, lĩnh vực môi trường và nội dung văn bản gốc
của từng bản ghi pháp lý.
Luồng xử lý chính
Pipeline gồm sáu giai đoạn chính:
Giai đoạn 1:Chuẩn bị và xác thực dữ liệu đầu vào.Văn bản pháp luật sau
khi được cấu trúc hóa sang định dạng JSON được kiểm tra về mã
định danh, trích dẫn pháp lý, nội dung văn bản gốc, chủ thể, tín

10
hiệu pháp lý, lĩnh vực tác động và điều kiện áp dụng. Kết quả của
giai đoạn này là tập bản ghi có tác động chính sách, ký hiệuDimpact.
Giai đoạn 2:Lọc tác động môi trường ở Tầng 1.TậpDimpact được đưa qua bộ
lọc nhị phân để xác định bản ghi có tác động môi trường. Nhãn do
mô hình dự đoán,env_llm, được so sánh với nhãn tham chiếu của
người nghiên cứu,env_human, để tính các chỉ số đánh giá và phát
hiện các trường hợp cần review. Đầu ra là tập dữ liệu môi trường đã
được hiệu chuẩn, ký hiệuDenv.
Giai đoạn 3:Phân loại tác động chính sách ở Tầng 2.TậpDenv được phân
loại vào năm nhãn tác động: lợi ích định lượng, lợi ích định tính, chi
phí định lượng, chi phí định tính và ràng buộc. Nhãnclass_llm được
đối chiếu vớiclass_human để lập ma trận nhầm lẫn, tính Accuracy,
Macro-F1 và tỷ lệ hiệu chỉnh của con người. Các bản ghi bất đồng
được xử lý theo giao thức adjudication để chốtfinal_label.
Giai đoạn 4:Chuẩnhóachủthểvàlĩnhvựctácđộng.Saukhicó final_label,
hệ thống chuẩn hóa nhóm chủ thể chịu điều chỉnh và lĩnh vực môi
trường chính. Các trường nhưactor_group, domain_primary và
domain_secondary được kiểm tra để bảo đảm tính nhất quán trước
khi sử dụng trong bước chấm điểm.
Giai đoạn 5:Lượng hóa điểm tác động.Mỗi bản ghi được chấm theo bốn biến
của mô hình MSDR: cường độ tác độngMi, phạm vi tác độngSi,
thời gian tác độngDi và rủi ro/khả năng phục hồiRi. Điểm tác
động được tính theo công thức:
ImpactScoreei =s i ×W i ×$C^{norm}_i$ ,
trong đó si = +1đối với lợi ích vàsi = −1đối với chi phí hoặc ràng
buộc.
Giai đoạn 6:Trực quan hóa và tổng hợp báo cáo.Tạo bảng tổng hợp và biểu
đồ phân tích theo nhãn, lĩnh vực môi trường, nhóm chủ thể và phân
phối điểm tác động. Các kết quả này hỗ trợ nhận diện nhóm điều
khoản có tác động mạnh và nhóm chủ thể chịu gánh nặng tuân thủ
lớn.

11
Vai trò hỗ trợ của mô hình ngôn ngữ lớn
Trong pipeline này, mô hình ngôn ngữ lớn không thay thế người nghiên cứu mà
đóng vai trò công cụ hỗ trợ đọc hiểu văn bản pháp luật. Vai trò của mô hình được giới
hạn ở bốn nhóm chức năng:
• Gợi ý phân loại:dự đoán nhãn ở Tầng 1 và Tầng 2 để người nghiên cứu đối
chiếu với nhãn tham chiếu.
• Trích xuất bằng chứng:cung cấp lý do và đoạn bằng chứng trongraw_text
nhằm hỗ trợ kiểm tra quyết định gán nhãn.
• Phát hiện trường hợp cần review:làm nổi bật các bản ghi có bất đồng giữa
nhãn human và nhãn LLM, hoặc có tín hiệu pháp lý dễ gây nhầm lẫn.
• Tăng khả năng truy vết:lưu lại nhãn dự đoán, lý do, bằng chứng và đánh dấu
cần rà soát để phục vụ quá trình kiểm chứng sau này.
Nguyên tắc kiểm soát
Các quyết định ảnh hưởng trực tiếp đến kết quả lượng hóa, bao gồmfinal_label,
nhóm chủ thể, lĩnh vực tác động và điểm MSDR, phải được người nghiên cứu kiểm tra.
Quyết định cuối cùng luôn dựa trênraw_text, bản hướng dẫn (guideline) gán nhãn và
quy trình xử lý bất đồng. Thiết kế này giúp cân bằng giữa hiệu quả xử lý dữ liệu lớn
và tính minh bạch, có căn cứ trong phân tích chính sách pháp luật.
2.3 Quy trình kiểm chứng có con người tham gia
Quy trình kiểm chứng có con người tham gia được thiết kế theo hướngHuman-in-
the-loop. Mục tiêu của quy trình không phải là chấp nhận tự động nhãn do mô hình
ngôn ngữ lớn dự đoán, mà là sử dụng mô hình như một nguồn hỗ trợ để phát hiện bất
đồng, cung cấp bằng chứng và giúp người nghiên cứu ra quyết định cuối cùng một cách
có căn cứ.
2.3.1 Nguyên tắc kiểm chứng
Quy trình kiểm chứng được xây dựng trên ba nguyên tắc chính:
• Tách biệt nhãn ban đầu và nhãn cuối cùng.Hệ thống lưu đồng thời nhãn
do người nghiên cứu gán trước khi xem kết quả LLM, nhãn do LLM dự đoán và

12
nhãn cuối cùng sau review. Việc tách biệt này giúp tránh nhầm lẫn giữa dữ liệu
đánh giá mô hình và dữ liệu đã được hiệu chỉnh.
• Dựa trên bằng chứng văn bản.Mọi quyết định review phải quay lại nội dung
văn bản gốc, ký hiệuraw_text, và đối chiếu với guideline gán nhãn. Không quyết
định chỉ dựa trên tên nhãn hoặc phần giải thích của LLM.
• Bảo toàn khả năng truy vết.Khi thay đổi nhãn, người nghiên cứu cần ghi lại
quyết định review, nhãn cuối cùng, lý do lựa chọn và loại lỗi nếu có. Các thông
tin này là cơ sở để giải thích kết quả lượng hóa ở các bước sau.
Một nguyên tắc quan trọng là các chỉ số đánh giá LLM phải được tínhtrướckhi
xử lý bất đồng. Không dùng nhãn cuối cùng$y^{final}_i$ để đánh giá LLM như metric ban
đầu, vì nhãn này đã có sự can thiệp của người nghiên cứu.
2.3.2 Luồng xử lý bất đồng nhãn
Với mỗi bản ghi thứi, hệ thống lưu nhãn tham chiếu ban đầu của người nghiên cứu
là yi và nhãn dự đoán của LLM làˆyi. Nếu hai nhãn trùng nhau, bản ghi được xem là
đồng thuận ban đầu. Nếu hai nhãn khác nhau, bản ghi được đưa vào tập review và
được xử lý theo các bước sau:
Bước 1:Đọc lạiraw_textvà trích dẫn pháp lý của bản ghi.
Bước 2: Kiểm tra nhãn người nghiên cứu, nhãn LLM, lý do dự đoán và đoạn
bằng chứng nếu có.
Bước 3: Đối chiếu bản ghi với guideline gán nhãn để xác định tín hiệu pháp lý
chính.
Bước 4:Chọn quyết định review phù hợp theo Bảng 2.2.
Bước 5: Ghi final_label, final_reason, review_decision và error_type
nếu cần.
Bảng 2.2: Các loại quyết định review trong quy trình kiểm chứng.
Giá trị Khi nào dùng Kết quả
KEEP_HUMANHuman đúng, LLM sai.final_label =
class_human.

13
Giá trị Khi nào dùng Kết quả
ACCEPT_LLM LLM đúng, human ban đầu
sai.
final_label =
class_llm.
NEW_LABEL Cả human và LLM đều chưa
phù hợp.
final_label là
nhãn mới do re-
viewer chọn.
AMBIGUOUS_KEEP_HUMAN Còn mơ hồ, chưa đủ cơ sở
đổi nhãn.
Giữ class_human và
giữ cờ cần review.
NEED_EXPERT_REVIEWBản ghi vượt quá khả năng
xác quyết của người nghiên
cứu.
Tạm giữ nhãn tốt
nhất và ghi chú cần
chuyên gia.
2.3.3 Quy tắc phân xử các nhóm bất đồng chính
Đối với bài toán phân loại 5 nhãn tác động, một số nhóm bất đồng xuất hiện thường
xuyên hơn và cần quy tắc phân xử nhất quán. Các quy tắc dưới đây được dùng để hỗ
trợ reviewer, nhưng quyết định cuối cùng vẫn phải dựa trênraw_text của từng bản
ghi.
A. Nhãn chi phí định tính và nhãn ràng buộc
Chọn COST_QUALITATIVE nếu trọng tâm bản ghi là nghĩa vụ thực hiện hoặc thủ tục,
chẳng hạnphải lập, phải nộp, phải báo cáo, phải quan trắc, phải xử lý, phải
chuyển giao hoặc phải có giấy phép môi trường. Ngược lại, chọnCONSTRAINT nếu
trọngtâmlàlệnhcấm,điềukiện,giớihạnkỹthuậthoặcngưỡngpháplý,chẳnghạn không
được,chỉ được,không cấp,đạt quy chuẩn kỹ thuật môi trường,không vượt quá
hoặckhả năng chịu tải.
B.Nhãn chi phí định lượng và định tính
Chọn COST_QUANTITATIVE chỉ khi bản ghi nêu trực tiếp số tiền, đơn giá, mức phí,
mức thuế, mức ký quỹ, mức bồi thường hoặc tỷ lệ chi trả tài chính. Nếu bản ghi chỉ
nêu thời hạn, mã QCVN, số điều/khoản, ngưỡng kỹ thuật, số bộ hồ sơ hoặc nghĩa vụ
tài chính chưa có mức tiền cụ thể thì không gán nhãn chi phí định lượng.

14
C.Nhãn lợi ích định tính và nhãn ràng buộc
Chọn BENEFIT_QUALITATIVE nếu bản ghi trao cơ chế hỗ trợ, ưu đãi, khuyến khích,
tạo điều kiện, phục hồi hoặc cải thiện môi trường. ChọnCONSTRAINTnếu bản ghi chủ
yếu đặt ra điều kiện, quy chuẩn, ngưỡng hoặc giới hạn hành vi, ngay cả khi mục tiêu
sâu xa của điều khoản là bảo vệ môi trường.
D. Nhãn lợi ích định lượng và định tính
Chọn BENEFIT_QUANTITATIVE chỉ khi lợi ích được lượng hóa trực tiếp bằng số tiền
hỗ trợ, tỷ lệ hỗ trợ, tỷ lệ giảm phát thải, khối lượng chất thải giảm/tái chế, diện tích
phục hồi hoặc lượng tài nguyên tiết kiệm. Nếu chỉ có tín hiệukhuyến khích, hỗ trợ,
ưu đãi, bảo vệ hoặc phát triển mà không có giá trị đo lường trực tiếp, nhãn phù
hợp làBENEFIT_QUALITATIVE.
E. Nhóm lợi ích và nhóm chi phí
Chọn nhãn lợi ích nếu bản ghi chủ yếu trao quyền, ưu đãi, hỗ trợ hoặc khuyến khích.
Chọn nhãn chi phí nếu bản ghi chủ yếu bắt buộc chủ thể thực hiện nghĩa vụ, thủ tục,
báo cáo, quan trắc, xử lý, đầu tư, vận hành hoặc chi trả. Nếu bản ghi đồng thời chứa cả
lợi ích và nghĩa vụ, chọn nhãn theo mệnh đề chính và đánh dấuclass_needs_review
= TRUEnếu vẫn còn mơ hồ.
2.3.4 Chỉ số hiệu chỉnh của con người
Để liên kết hiệu năng phân loại của LLM với khối lượng công việc thực tế trong quy
trình kiểm chứng có con người tham gia, đồ án định nghĩa chỉ số tỷ lệ hiệu chỉnh của con
người, ký hiệuHCR (Human Correction Rate). Chỉ số này đo tỷ lệ bản ghi mà nhãn
dự đoán thô của LLM không trùng với nhãn cuối cùng sau phân xử, tức các trường hợp
cần sự can thiệp trực tiếp của người nghiên cứu trong quy trìnhHuman-in-the-loop.
HCR= 1
N
NX
i=1
I
 
$y^{final}_i$ ̸= ˆyLLM
i

,(2.1)
trong đó N là tổng số bản ghi được đánh giá,$y^{final}_i$ là nhãn cuối cùng sau khi người
nghiên cứu phân xử,ˆyLLM
i là nhãn dự đoán ban đầu của LLM vàI(·)là hàm chỉ thị,
nhận giá trị bằng 1 nếu điều kiện bên trong đúng và bằng 0 nếu ngược lại. Nói cách
khác, mỗi bản ghi có$y^{final}_i$ ̸= ˆyLLM
i được xem là một trường hợp LLM cần được hiệu
chỉnh bởi con người.

15
HCR tỷ lệ thuận với khối lượng hiệu chuẩn thủ công và tỷ lệ nghịch với mức độ có
thể sử dụng trực tiếp của nhãn LLM. Thực tế thực nghiệm chỉ ra rằng, nếu chỉ số HCR ở mức thấp, tỷ lệ nhãn LLM
dự đoán so với nhãn sau khi xử lý bất đồng là cao , nếu giá trịHCR cao thì nhu cầu
rà soát lớn và mức độ rủi ro cao hơn khi chấp nhận tự động kết quả của LLM. Do đó,
HCR bổ sung cho các chỉ số hiệu năng phân loại như Accuracy, Precision, Recall và
Macro-F1.
2.4 Các chỉ số đánh giá chất lượng phân loại
Để đánh giá khách quan năng lực nhận diện ngữ nghĩa pháp lý của mô hình ngôn
ngữ lớn trước khi tiến hành hiệu chuẩn nhãn thủ công, đồ án sử dụng bộ chỉ số đánh
giá phân loại tiêu chuẩn trong học máy và truy hồi thông tin [6, 7]. Các chỉ số này
được tính trên nhãn tham chiếu ban đầu của người nghiên cứu và nhãn do LLM dự
đoán, tức được tínhtrướcbước xử lý bất đồng nhãn. Cách làm này giúp tách biệt
đánh giá năng lực mô hình với kết quả cuối cùng đã có sự can thiệp của con người.
Gọi L = {l1, l2, . . . , lk} là không gian nhãn của bài toán phân loại. Với bài toán lọc
tác động môi trường ở Tầng 1,k = 2; với bài toán phân loại tác động chính sách ở
Tầng 2, k = 5. Ma trận nhầm lẫnC∈N k×k được định nghĩa sao cho phần tửCij là
số bản ghi có nhãn tham chiếuli nhưng được LLM dự đoán làlj. Theo quy ước này,
đường chéo chính của ma trận biểu thị số dự đoán đúng, còn các phần tử ngoài đường
chéo biểu thị các dạng nhầm lẫn giữa các nhãn.
2.4.1 Chỉ số theo từng nhãn
Với một nhãn cụ thểlm, ba chỉ số cơ bản gồm Precision, Recall và F1-score. Precision
đo tỷ lệ dự đoán nhãnlm của LLM là đúng so với toàn bộ số lần mô hình dự đoán
nhãn đó, qua đó phản ánh mức độ kiểm soát sai số dương tính giả. Recall đo tỷ lệ các
bản ghi thật sự thuộc nhãnlm được mô hình nhận diện đúng, qua đó phản ánh mức độ
kiểm soát sai số âm tính giả. F1-score là trung bình điều hòa giữa Precision và Recall,
phù hợp khi cần đánh giá cân bằng giữa hai loại sai số.
$$P_m = \frac{C_{mm}}{\sum_{i=1}^{k} C_{im}} \tag{2.2}$$
$$R_m = \frac{C_{mm}}{\sum_{j=1}^{k} C_{mj}} \tag{2.3}$$
$$F1_m = \frac{2 \cdot P_m \cdot R_m}{P_m + R_m} \tag{2.4}$$

16
Trong trường hợp mẫu số của một chỉ số bằng 0, chỉ số tương ứng được đặt bằng 0
để tránh tạo ra giá trị không xác định. Quy ước này đặc biệt cần thiết đối với các nhãn
thiểu số hoặc các nhãn không xuất hiện trong dự đoán của mô hình.
2.4.2 Chỉ số tổng hợp trên toàn bộ tập dữ liệu
Để đánh giá chất lượng tổng thể, đồ án sử dụng hai chỉ số có ý nghĩa bổ sung cho
nhau: Accuracy và Macro-F1. Accuracy đo tỷ lệ dự đoán đúng trên toàn bộ tập dữ liệu:
$$Accuracy = \frac{\sum_{m=1}^{k} C_{mm}}{\sum_{i=1}^{k} \sum_{j=1}^{k} C_{ij}} \tag{2.5}$$
Macro-F1 được tính bằng trung bình cộng không trọng số của F1-score trên tất cả
các nhãn:
$$Macro\text{-}F1 = \frac{1}{k} \sum_{m=1}^{k} F1_m \tag{2.6}$$
Hai chỉ số này phản ánh hai góc nhìn khác nhau. Accuracy cho biết mức độ đúng
chung của mô hình trên toàn bộ tập dữ liệu, nhưng dễ bị chi phối bởi nhãn có số lượng
mẫu lớn. Ngược lại, Macro-F1 xem mỗi nhãn có trọng số ngang nhau, bất kể số lượng
bản ghi của nhãn đó nhiều hay ít. Vì vậy, Macro-F1 là chỉ số nghiêm ngặt hơn khi cần
đánh giá khả năng nhận diện các nhãn ít xuất hiện.
2.4.3 Ý nghĩa của Macro-F1 trong dữ liệu mất cân bằng
Trong phân tích văn bản pháp luật, mất cân bằng phân phối nhãn là hiện tượng
phổ biến vì phần lớn điều khoản thường tập trung vào một số dạng nghĩa vụ hoặc
thủ tục chủ đạo. Thực nghiệm của đồ án cũng cho thấy sự mất cân bằng rõ rệt:
nhãn COST_QUALITATIVE chiếm 444/581 bản ghi, tương đương 76.42%, trong khi nhãn
BENEFIT_QUALITATIVEchỉ gồm 15/581 bản ghi, tương đương 2.58%.
Nếu chỉ sử dụng Accuracy hoặc Micro-F1 làm thước đo chính, kết quả đánh giá có
thể mang thiên lệch lạc quan vì điểm số bị chi phối bởi hiệu năng trên lớp đa số. Một
mô hình dự đoán tốt nhãnCOST_QUALITATIVE vẫn có thể đạt Accuracy tương đối cao,
ngay cả khi nhận diện kém các nhãn lợi ích hoặc nhãn định lượng. Macro-F1 khắc phục
hạn chế này bằng cách đánh giá hiệu năng trên từng nhãn với trọng số ngang nhau.
Do đó, trong đồ án, Accuracy được dùng để mô tả mức đúng tổng quát, còn Macro-F1
được dùng như thước đo chính để kiểm tra mức độ ổn định của mô hình trên toàn bộ
không gian nhãn, đặc biệt là các nhãn thiểu số có ý nghĩa quan trọng trong phân tích
so sánh chính sách.

17
2.5 Phương pháp phân loại, hệ thống nhãn tác động
và chuẩn hóa actor/domain
Mục này mô tả cách hệ thống chuyển một bản ghi pháp lý đã được xác định là có
tác động môi trường thành ba nhóm thông tin đầu ra: 5 nhãn tác động chính sách
môi trường, nhóm chủ thể chịu điều chỉnh (actor) và lĩnh vực môi trường chịu tác
động (domain). Nhãn tác động quyết định hướng tác động trong mô hình lượng hóa,
trong khi actor và domain cung cấp ngữ cảnh để chấm điểm phạm vi tác độngSi và
rủi ro/khả năng phục hồiRi.
2.5.1 Vai trò của nhãn tác động và actor/domain
Trong phạm vi đồ án, mỗi bản ghi được gán một nhãn tác động duy nhất để bảo
đảm tính nhất quán khi tính điểm. Việc chuẩn hóa actor/domain được thực hiện sau
bước phân loại nhãn nhằm tránh việc mô tả tự do trong văn bản pháp luật làm sai
lệch thống kê và lượng hóa. Ba đầu ra chính của bước này gồm:
•final_label : nhãn tác động cuối cùng sau khi đối chiếu giữa nhãn human, nhãn
LLM và quyết định rà soát;
•actor_group : nhóm chủ thể chịu nghĩa vụ, nhận lợi ích hoặc bị ràng buộc trực
tiếp;
•domain_primary và, nếu cần,domain_secondary: lĩnh vực môi trường chính và
phụ gắn với nội dung bản ghi.
Cách tổ chức này giúp tách rõ ba câu hỏi: bản ghi tạo lợi ích, chi phí hay ràng buộc;
tác động đó áp dụng cho chủ thể nào; và tác động liên quan đến lĩnh vực môi trường
nào.
2.5.2 Hệ thống 5 nhãn tác động
Hệ thống nhãn gồm năm nhóm, phản ánh ba hướng phân tích chính của đồ án: lợi
ích, chi phí và ràng buộc. Hai nhóm lợi ích và chi phí được tách thành định lượng/định
tính tùy theo việc bản ghi có nêu trực tiếp giá trị đo lường hay không.

18
Bảng 2.3: Hệ thống 5 nhãn tác động chính sách.
Nhãn Điều kiện gán Không gán nếu
BENEFIT_QUANTITATIVE Bản ghi tạo lợi ích môi
trường, xã hội hoặc kinh tế
xanh và lợi ích được lượng
hóa trực tiếp bằng số tiền,
tỷ lệ, khối lượng, diện tích,
mức giảm phát thải, mức
hỗ trợ hoặc đại lượng đo
được.
Con số chỉ là thời hạn, số
điều/khoản, mã QCVN,
ngưỡng điều kiện cấp
phép hoặc bản ghi chỉ
nêu khuyến khích/hỗ trợ
mà không có giá trị định
lượng.
BENEFIT_QUALITATIVE Bản ghi tạo lợi ích môi
trường hoặc lợi ích quản lý
môi trường nhưng chưa có
con số đo lường trực tiếp.
Trọng tâm là nghĩa vụ
tuân thủ, thủ tục, lệnh
cấm, điều kiện kỹ thuật
hoặc chi phí tài chính.
COST_QUANTITATIVE Bản ghi tạo nghĩa vụ tài
chính hoặc chi phí tuân thủ
có giá trị định lượng trực
tiếp như số tiền, tỷ lệ tiền,
đơn giá hoặc mức chi trả cụ
thể.
Chỉ có tín hiệu chi
trả/bồi thường chung,
thời hạn, mã QCVN, số
điều/khoản hoặc ngưỡng
kỹ thuật không phải chi
phí.
COST_QUALITATIVE Bản ghi đặt ra nghĩa vụ
tuân thủ, thủ tục, hồ sơ,
báo cáo, vận hành, quan
trắc, đăng ký hoặc xin
phép, làm phát sinh chi phí
thời gian, nhân lực hoặc tổ
chức thực hiện nhưng chưa
có giá trị tiền tệ cụ thể.
Trọng tâm là lệnh cấm,
giới hạn kỹ thuật, điều
kiện cấp phép/vận hành
hoặc đã có mức phí,
khoản tiền cụ thể.
CONSTRAINT Bản ghi đặt ra lệnh cấm,
điều kiện, giới hạn, ngưỡng
kỹ thuật, quy chuẩn, tiêu
chuẩn, điều kiện cấp phép
hoặc điều kiện vận hành,
qua đó hạn chế hoặc giới
hạn hành vi của chủ thể.
Trọng tâm là thủ tục
hành chính, báo cáo,
quan trắc, cơ chế khuyến
khích/hỗ trợ hoặc nghĩa
vụ tài chính có số tiền cụ
thể.

19
2.5.3 Dấu hiệu nhận diện nhãn
Các dấu hiệu dưới đây được dùng như tín hiệu hỗ trợ, không thay thế việc đọc
raw_text của bản ghi. Khi nhiều tín hiệu cùng xuất hiện, nhãn cuối cùng được chọn
theo trọng tâm pháp lý của điều khoản.
Bảng 2.4: Dấu hiệu thường gặp theo từng nhãn.
Nhãn Dấu hiệu thường gặp
BENEFIT_QUANTITATIVE được hỗ trợ ... đồng ; được giảm ... %; giảm
... tấn CO2; tăng ... ha; thu hồi/tái chế
... %; tiết kiệm ... kWh; được miễn/giảm một
khoản phí cụ thể.
BENEFIT_QUALITATIVE khuyến khích ; hỗ trợ; ưu đãi; tạo điều kiện;
bảo vệ; cải thiện; phục hồi; phát triển kinh
tế tuần hoàn;thúc đẩy công nghệ sạch.
COST_QUANTITATIVE phải nộp ... đồng ; phí bảo vệ môi trường;
thuế; ký quỹ; bồi thường; chi trả; mức đóng
góp;mức phạt;đơn giá ... đồng/tấn.
COST_QUALITATIVE phải lập ; phải trình; phải nộp; phải báo cáo;
phải đăng ký;phải quan trắc;phải phân loại;
phải thu gom; phải xử lý; phải có giấy phép
môi trường;có trách nhiệm thực hiện.
CONSTRAINT nghiêm cấm ; không được; không phê duyệt;
không cấp giấy phép; chỉ được; trừ trường
hợp; không vượt quá; phải đáp ứng; đạt quy
chuẩn kỹ thuật môi trường;hạn ngạch;ngưỡng;
khả năng chịu tải.
2.5.4 Quy tắc ưu tiên khi có nhiều dấu hiệu
Vì hệ thống sử dụng một nhãn duy nhất cho mỗi bản ghi, các trường hợp có nhiều
tín hiệu được xử lý theo nguyên tắc chọn tác động chính. Trọng tâm được xác định
dựa trên mệnh đề pháp lý chính, chủ thể chịu tác động trực tiếp và hệ quả chính sách
rõ nhất của bản ghi.

20
Bảng 2.5: Quy tắc ưu tiên theo bản chất tác động chính.
Nếu trọng tâm bản ghi là Nhãn ưu tiên
Hỗ trợ, ưu đãi, khuyến khích hoặc cải thiện môi trường
có số cụ thể
BENEFIT_QUANTITATIVE
Hỗ trợ, ưu đãi, khuyến khích hoặc cải thiện môi trường
không có số cụ thể
BENEFIT_QUALITATIVE
Phí, thuế, ký quỹ, bồi thường hoặc chi trả có số tiền
cụ thể
COST_QUANTITATIVE
Nghĩa vụ lập hồ sơ, báo cáo, quan trắc, đăng ký, xin
phép hoặc tổ chức thực hiện
COST_QUALITATIVE
Cấm, không được, chỉ được, không phê duyệt, điều
kiện, quy chuẩn, ngưỡng hoặc hạn ngạch
CONSTRAINT
Một số trường hợp biên được xử lý như sau:
• Vừa có thủ tục vừa có điều kiện:nếu mệnh đề chính là lập, nộp, báo cáo,
quan trắc, đăng ký hoặc xin phép thì thường chọnCOST_QUALITATIVE; nếu mệnh
đề chính là không được, không cấp, chỉ được, đạt quy chuẩn hoặc không vượt
ngưỡng thì thường chọnCONSTRAINT.
• Vừa có lợi ích vừa có nghĩa vụ:nếu bản ghi trao quyền, hỗ trợ hoặc ưu đãi
cho chủ thể thì ưu tiên nhãn lợi ích; nếu bản ghi buộc chủ thể thực hiện công
việc phát sinh gánh nặng thì ưu tiên nhãn chi phí hoặc ràng buộc.
• Không xác định rõ trọng tâm:gán theo tín hiệu pháp lý mạnh hơn và
giữ class_needs_review = TRUE để người nghiên cứu rà soát trước khi chốt
final_label.
2.5.5 Chuẩn hóa actor/domain phục vụ lượng hóa
Sau khi chốt nhãn tác động, tiến hành chuẩn hóa actor và domain để kết nối kết
quả phân loại với mô hình lượng hóa. Việc chuẩn hóa này nhằm đạt ba mục tiêu:
• Bảo đảm tính nhất quán dữ liệu:các cách diễn đạt khác nhau trong văn bản
pháp luật được quy về một tập nhóm chuẩn để có thể thống kê và so sánh.
• Hỗ trợ lượng hóa tác động:actor giúp xác định phạm vi chủ thể chịu tác
động, còn domain giúp xác định mức độ rủi ro môi trường của lĩnh vực liên quan.

21
• Tăng khả năng giải thích kết quả:điểm tác động cuối cùng có thể được phân
tích theo nhóm chủ thể và lĩnh vực, thay vì chỉ xem xét từng điều khoản riêng lẻ.
2.5.5.1 Chuẩn hóa nhóm chủ thể chịu tác động
Actor được chuẩn hóa thành năm nhóm chính. Việc gán nhóm dựa trên chủ thể
được nêu trực tiếp trongraw_text, trích dẫn pháp lý và tín hiệu nghĩa vụ/quyền lợi
của bản ghi.
Bảng 2.6: Nhóm actor chuẩn hóa trong hệ thống.
Nhóm actor Đối tượng điển hình Vai trò trong lượng hóa
Doanh nghiệp/cơ sở
sản xuất kinh doanh
BUSINESS_FACILITY
Cơ sở sản xuất, kinh doanh,
dịch vụ, khu sản xuất, làng
nghề
Thường liên quan đến nghĩa
vụ tuân thủ, chi phí vận
hành hoặc yêu cầu xử lý môi
trường.
Chủ dự án đầu tư/hạ tầng
PROJECT_OWNER_INFRASTRUCTURE
Chủ dự án, nhà đầu tư, đơn
vị triển khai công trình, khu
đô thị, khu công nghiệp
Thường liên quan đến ĐTM,
giấy phép môi trường, đầu tư
công nghệ hoặc trách nhiệm
trước khi vận hành.
Cơ quan nhà nước
STATE_AGENCY
Bộ, Ủy ban nhân dân, cơ
quan chuyên môn, cơ quan
thẩm định, thanh tra
Thường liên quan đến trách
nhiệm quản lý, thẩm định,
cấp phép, kiểm tra và giám
sát.
Tổ chức/cá nhân
GENERAL_ORGANIZATION_INDIVIDUAL
Hộ gia đình, cá nhân, tổ chức
xã hội, đơn vị phát sinh chất
thải nhỏ lẻ
Thường phản ánh phạm vi
tác động rộng nhưng mức độ
nghĩa vụ có thể phân tán.
Cộng đồng dân cư/làng nghề
COMMUNITY_CRAFT_VILLAGE
Cộng đồng dân cư, khu dân
cư, làng nghề, nhóm dân cư
chịu ảnh hưởng
Thường liên quan đến lợi ích
môi trường, rủi ro sức khỏe
hoặc tác động xã hội tại địa
phương.
Actor hỗ trợ chấmSi vì phạm vi tác động phụ thuộc trực tiếp vào số lượng và loại
chủ thể chịu sự điều chỉnh. Ví dụ, một nghĩa vụ áp dụng cho mọi cơ sở sản xuất kinh
doanh thường có phạm vi rộng hơn một nghĩa vụ chỉ áp dụng cho một nhóm dự án đặc
thù.

22
2.5.5.2 Chuẩn hóa lĩnh vực môi trường
Domain được chuẩn hóa theo lĩnh vực môi trường chính mà bản ghi tác động đến.
Một bản ghi có thể có một domain chính và, nếu cần, một domain phụ để phản ánh
trường hợp có nhiều nội dung môi trường trong cùng điều khoản.
Bảng 2.7: Nhóm domain chuẩn hóa trong hệ thống.
Nhóm domain Nội dung điển hình
Nước
water
Nước thải, nguồn nước, lưu vực sông, khả năng chịu
tải của môi trường nước.
Chất thải
waste
Chất thải rắn, chất thải sinh hoạt, chất thải công
nghiệp, phân loại, thu gom, tái chế và xử lý chất thải.
Chất độc hại
hazardous_substances
Hóa chất, chất ô nhiễm khó phân hủy, chất nguy hại,
phế liệu, chất thải nguy hại.
Không khí/tiếng ồn/bức xạ
air_noise_radiation
Khí thải, bụi, tiếng ồn, độ rung, bức xạ và kiểm soát
phát thải vào không khí.
ĐTM/cấp phép/đăng ký
eia_permit_registration
Đánh giá tác động môi trường, giấy phép môi trường,
đăng ký môi trường và thủ tục phê duyệt.
Quan trắc/báo cáo
monitoring_reporting
Quan trắc môi trường, báo cáo định kỳ, công khai
thông tin và hệ thống giám sát.
Quy chuẩn kỹ thuật
technical_standard_threshold
Quy chuẩn, tiêu chuẩn, ngưỡng kỹ thuật, điều kiện
vận hành và điều kiện xả thải.
Quản lý nhà nước
planning_state_management
Phân công trách nhiệm, thanh tra, kiểm tra, quy
hoạch, cơ sở dữ liệu và tổ chức thực hiện.
Tài chính môi trường
environmental_finance
Phí, thuế, ký quỹ, bồi thường, chi trả dịch vụ hệ sinh
thái và ưu đãi tài chính.
Khí hậu/các-bon
climate_carbon
Giảm phát thải khí nhà kính, thị trường các-bon,
thích ứng biến đổi khí hậu và phát triển các-bon
thấp.
Đa dạng sinh học
biodiversity_natural_heritage
Hệ sinh thái, loài, khu bảo tồn, phục hồi tự nhiên và
bảo tồn đa dạng sinh học.
Kiểm soát & khắc phục ô nhiễm
pollution_control_remediation
Sự cố môi trường, ô nhiễm đất, khắc phục môi
trường bị suy thoái, ứng phó khẩn cấp và phục hồi
hệ sinh thái khu vực bị ảnh hưởng.

23
Nhóm domain Nội dung điển hình
Môi trường chung
general_environment
Nguyên tắc chung về bảo vệ môi trường, chính sách
phát triển bền vững, giáo dục môi trường, quyền và
nghĩa vụ phổ quát của cộng đồng/tổ chức.
Domain hỗ trợ chấmRi vì mỗi lĩnh vực có mức rủi ro môi trường, khả năng phục
hồi và mức độ lan truyền tác động khác nhau. Ví dụ, bản ghi liên quan đến chất thải
nguy hại hoặc nguồn nước thường có hàm ý rủi ro cao hơn bản ghi chỉ quy định thủ
tục báo cáo thông thường.
2.5.6 Quy trình gán và kiểm tra actor/domain
Việc chuẩn hóa actor/domain được thực hiện theo trình tự sau:
Bước 1: Trích xuất actor/domain từraw_text, trích dẫn pháp lý và các trường
dữ liệu đã cấu trúc hóa.
Bước 2: Gán actor/domain theo bảng chuẩn hóa và bộ từ khóa pháp lý tương
ứng.
Bước 3: Đánh dấu trường hợp mơ hồ, bản ghi có nhiều chủ thể hoặc nhiều lĩnh
vực cùng xuất hiện.
Bước 4: Người nghiên cứu rà soát các trường hợp được đánh dấu để chốt
actor_group,domain_primaryvàdomain_secondarynếu có.
Bước 5:Kiểm tra tính hợp lệ trước khi đưa vào bước chấm điểmSi vàR i.
Trong trường hợp một bản ghi có nhiều actor hoặc nhiều domain, hệ thống ưu tiên
chủ thể và lĩnh vực gắn trực tiếp với nghĩa vụ, lợi ích hoặc ràng buộc chính của bản
ghi. Nếu vẫn không xác định được trọng tâm, bản ghi được giữ cờ cần review để tránh
gán nhóm tùy tiện.
2.6 Mô hình toán học lượng hóa tác động chính
sách
2.6.1 Các biến thành phần
Mô hình sử dụng bốn biến thành phần trên thang điểm 1–5:

24
•M i: cường độ tác động, phản ánh mức thay đổi hành vi, quy trình, công nghệ
hoặc nghĩa vụ;
•S i: phạm vi tác động, phản ánh số lượng chủ thể hoặc không gian bị điều chỉnh;
•D i: thời gian tác động, phản ánh tác động ngắn hạn, trung hạn hay dài hạn;
•R i: rủi ro và khả năng phục hồi, phản ánh mức độ nghiêm trọng nếu điều khoản
không được tuân thủ.
Các biến thành phần được chấm theo cùng thang 1–5, trong đó điểm cao hơn thể
hiện mức tác động mạnh hơn, phạm vi rộng hơn, thời gian dài hơn hoặc rủi ro môi
trường lớn hơn. Rubric chi tiết cho từng biến được trình bày trong các bảng dưới đây
để bảo đảm việc chấm điểm nhất quán và có thể giải thích.
Bảng 2.8: Rubric chấm điểm biếnMi – cường độ tác động.
Điểm Mức độ Mô tả Ví dụ
1 Không đáng kể Thay đổi rất nhỏ, chủ yếu là ghi nhận,
cung cấp thông tin hoặc yêu cầu hành
chính nhẹ
Ghi nhận thông tin môi
trường trong hồ sơ
2 Thấp Có yêu cầu thực hiện nhưng đơn giản,
ít làm thay đổi vận hành chính
Dán nhãn, phân loại thông
tin, báo cáo đơn giản
3 Trung bình Tác động rõ đến quy trình quản lý hoặc
vận hành
Lập báo cáo, đăng ký môi
trường, quan trắc định kỳ
4 Cao Buộc thay đổi đáng kể về công nghệ, hạ
tầng, quy trình sản xuất hoặc quản lý
Lắp đặt hệ thống xử lý
nước thải, tổ chức thu
gom/xử lý chất thải
5 Rất cao Tác động mang tính chuyển đổi, thay
đổi mô hình hoạt động hoặc ảnh hưởng
lớn đến toàn ngành
Cấm hoàn toàn một hoạt
động gây ô nhiễm nghiêm
trọng, bắt buộc chuyển đổi
công nghệ lớn
Bảng 2.9: Rubric chấm điểm biếnSi – phạm vi ảnh hưởng.
Điểm Phạm vi Mô tả Ví dụ
1 Cá nhân/cơ sở
đơn lẻ
Tác động đến một chủ thể hoặc một dự
án cụ thể
Một dự án/cơ sở riêng lẻ
2 Nhóm nhỏ/địa
phương hẹp
Tác động đến một nhóm chủ thể hoặc
một khu vực nhỏ
Một cụm dân cư, một
xã/huyện

25
Điểm Phạm vi Mô tả Ví dụ
3 Ngành, tỉnh hoặc
nhóm chủ thể
rộng
Tác động đến một ngành, một cấp tỉnh
hoặc nhóm doanh nghiệp/cơ sở rộng
Chủ dự án, cơ sở sản xuất
kinh doanh, UBND cấp
tỉnh
4 Liên tỉnh, vùng
hoặc đa ngành
Tác động đến nhiều địa phương, nhiều
ngành hoặc lưu vực lớn
Sông hồ liên tỉnh, khu vực
liên vùng
5 Quốc gia hoặc
xuyên biên giới
Tác động toàn quốc, toàn nền kinh tế
hoặc có yếu tố toàn cầu
Khí nhà kính, tầng ô-dôn,
chính sách chất thải toàn
quốc
Bảng 2.10: Rubric chấm điểm biếnDi – thời gian tác động.
Điểm Thời gian Mô tả Ví dụ
1 Ngắn hạn, một
lần
Tác động dưới 1 năm hoặc phát sinh
một lần
Báo cáo sự cố một lần
2 Ngắn hạn 1–5 năm hoặc trong giai đoạn chuyển
tiếp ngắn
Thời hạn khắc phục ngắn
3 Trung hạn 5–20 năm hoặc theo chu kỳ kế
hoạch/quản lý thông thường
Kế hoạch, quy hoạch, nghĩa
vụ vận hành chưa xác định
dài hạn
4 Dài hạn Trên 20 năm hoặc kéo dài theo vòng đời
dự án/cơ sở
Hạ tầng xử lý nước thải,
quản lý chất thải lâu dài
5 Rất dài hạn/khó
đảo ngược
Tác động gần như vĩnh viễn hoặc gắn
với hệ sinh thái khó phục hồi
Đa dạng sinh học, di sản
thiên nhiên, ô nhiễm lâu
dài
Bảng 2.11: Rubric chấm điểm biếnRi – rủi ro và khả năng phục hồi.
Điểm Rủi ro/khả
năng phục hồi
Mô tả Ví dụ
1 Rủi ro thấp Hậu quả chủ yếu là chậm thủ tục, ít tác
động trực tiếp đến môi trường
Chậm nộp báo cáo ít
nghiêm trọng
2 Rủi ro thấp–trung
bình
Có thể gây tác động môi trường nhỏ, dễ
khắc phục
Thiếu phân loại hoặc lưu
giữ tạm thời ở mức nhẹ
3 Rủi ro trung bình Có nguy cơ ô nhiễm hoặc suy giảm môi
trường rõ, cần chi phí khắc phục
Ô nhiễm cục bộ, quan trắc
không đầy đủ
4 Rủi ro cao Có thể gây ô nhiễm nghiêm trọng hoặc
khó phục hồi hoàn toàn
Ô nhiễm nước ngầm, chất
thải nguy hại, sự cố môi
trường lớn

26
Điểm Rủi ro/khả
năng phục hồi
Mô tả Ví dụ
5 Rủi ro rất cao Tác động khó đảo ngược, lâu dài hoặc
có quy mô lớn
Mất đa dạng sinh học, suy
giảm tầng ô-dôn, phát thải
khí nhà kính lớn, ô nhiễm
độc hại kéo dài
2.6.2 Trọng số ưu tiên và hướng tác động
Trong phiên bản cơ sở, bốn biến được gán trọng số bằng nhau:
$$\alpha = \beta = \gamma = \delta = 0.25 \tag{2.7}$$
Trọng số ưu tiênWi được giữ bằng 1.0 cho toàn bộ bản ghi vì đồ án chưa có khảo
sát chuyên gia hoặc phương pháp AHP để xác định trọng số khác nhau theo domain.
Hướng tác độngsi được xác định theo nhãn cuối cùng:
$$s_i = \begin{cases} +1, & y^{final}_i \in \{\text{BENEFIT\_QUANTITATIVE}, \text{BENEFIT\_QUALITATIVE}\} \\ -1, & y^{final}_i \in \{\text{COST\_QUANTITATIVE}, \text{COST\_QUALITATIVE}, \text{CONSTRAINT}\} \end{cases} \tag{2.8}$$
2.6.3 Công thức tính điểm tổng hợp
Với mỗi bản ghidi ∈ Lđược gán nhãn , điểm tổng hợp chưa chuẩn hóa:
$$C_i = \alpha M_i + \beta S_i + \gamma D_i + \delta R_i \tag{2.9}$$
Vì các biến thành phần nằm trên thang 1–5, điểm chuẩn hóa được tính bằng:
$$C^{norm}_i = \frac{C_i - 1}{4} \tag{2.10}$$
Điểm tác động cuối cùng:
$$ImpactScoree_i = s_i \times W_i \times C^{norm}_i \tag{2.11}$$
Tổng điểm tác động :
$$TotalImpact = \sum_{i=1}^{M} ImpactScoree_i \tag{2.12}$$

27
2.6.4 Phân tích độ nhạy và mô hình mở rộng
Trọng số bằng nhau là trường hợp cơ sở để bảo đảm tính minh bạch và có khả năng
tái lập. Trong các nghiên cứu tiếp theo, có thể kiểm tra độ nhạy bằng cách tăng trọng
số cho Ri trong nếu muốn nhấn mạnh rủi ro hoặc tăng trọng số choSi nếu muốn nhấn
mạnh phạm vi tác động. Các hướng mở rộng khác gồm hàm phạt phi tuyến cho các
ràng buộc nghiêm trọng, trọng số domain dựa trên AHP và chuẩn hóa định lượng khi
có dữ liệu chi phí/lợi ích bằng tiền.

Chương 3
Thiết lập thực nghiệm và kết quả
3.1 Thiết lập thực nghiệm
Đối tượng thực nghiệm là Luật Bảo vệ môi trường năm 2020 bao gồmN = 581bản
ghi, trong đó mọi bản ghi đều có tác động chính sách. Mô hình ngôn ngữ lớn được sử
dụng là Gemini 3.5 Flash. Các kết quả phân loại của mô hình được so sánh với tập
nhãn tham chiếu do người nghiên cứu gán trước khi thực hiện xử lý bất đồng.
Mô hình tính điểm sử dụng trọng số cơ sởα = β = γ = δ = 0.25và Wi = 1.0cho
toàn bộ bản ghi. Các điểmMi, Si, Di, Ri được chấm dựa trên các tiêu chí (rubric) đã
định nghĩa, bản hướng dẫn (guideline) xác định actor/domain và ghi chú giải thích cho
từng bản ghi.
3.2 Kết quả thực nghiệm Giai đoạn 2 : lọc tác động
môi trường
Giai đoạn hai là bộ lọc nhị phân để xác định bản ghi có tác động môi trường. Vì
đối tượng thực nghiệm là một đạo luật chuyên ngành về môi trường, cả nhãn người
nghiên cứu và nhãn LLM đều xác định 581/581 bản ghi có tác động môi trường. Kết
quả đạt được:
•Đồng thuận (agreement):581/581bản ghi;
•Bất đồng (disagreement):0/581bản ghi;
•Accuracy env =P recisionenv =Recall env =F1 env = 1.0;
•HCR env = 0.0.
28

29
Kết quả này cho thấy giai đoạn một không phải là rào cản kỹ thuật trong thực nghiệm
hiện tại. Tuy nhiên, điều này không phản ánh rằng LLM luôn lọc đúng mọi văn bản
pháp luật. Kết quả 100% phần lớn đến từ đặc điểm của dữ liệu: toàn bộ văn bản thuộc
Luật Bảo vệ môi trường đã được xác nhận là có tác động chính sách.
3.3 Kết quả thực nghiệm Giai đoạn 3: phân loại 5
nhãn tác động
3.3.1 Đánh giá hiệu năng tổng thể của LLM
Ở giai đoạn ba, LLM phải phân loại từng bản ghi vào một trong năm nhãn tác
động. Kết quả trước khi xử lý bất đồng (adjudication) cho thấy mô hình dự đoán
đúng 402/581 bản ghi, tương đươngAccuracyclass = 69.19%. Số bản ghi bất đồng là
179, tương đươngHCR class = 30.81%. Macro-F1 đạt 25.47%, thấp hơn nhiều so với
Accuracy vì dữ liệu mất cân bằng và mô hình nhận diện kém các nhãn thiểu số.
Bảng 3.1: Hiệu năng phân loại của LLM theo từng nhãn tác động
Nhãn tác động Mã Precision Recall F1 Kích thước mẫu
Lợi ích định lượng BQ 0.00% 0.00% 0.00% 0
Lợi ích định tính BQL 4.76% 4.55% 4.65% 22
Chi phí định lượng CQ 0.00% 0.00% 0.00% 0
Chi phí định tính CQL 84.02% 76.94% 80.32% 451
Ràng buộc CON 36.73% 50.00% 42.35% 108
Kết quả trong bảng 3.1 cho thấy hiệu năng phân loại của LLM không phân bố đồng
đều giữa các nhãn. Nhãnchi phí định tính(CQL) là lớp đa số, chiếm 77.6% tổng số
mẫu thực tế vớiN = 451. Nhờ số lượng mẫu lớn và các tín hiệu pháp lý tương đối rõ
ràng như nghĩa vụ lập hồ sơ, báo cáo, quan trắc, xử lý hoặc xin phép, mô hình đạt hiệu
năng tốt nhất ở lớp này vớiF1 = 80.32%, Precision đạt 84.02% và Recall đạt 76.94%.
Kết quả này cho thấy LLM nhận diện khá tốt các câu luật thiết lập nghĩa vụ tuân thủ
thông thường.
Ngược lại, hiệu năng giảm mạnh ở các lớp thiểu số và các lớp có ranh giới ngữ nghĩa
chưa rõ ràng. Đối với nhãnlợi ích định tính(BQL), tập mẫu chỉ cóN = 22, khiến mô
hình khó xác định các mẫu biểu đạt chính sách hỗ trợ hoặc khuyến khích. F1 của nhãn
này chỉ đạt 4.65% với Precision 4.76%, phản ánh hạn chế của LLM trong bối cảnh dữ
liệu lệch lớp. Nhãnràng buộc(CON) đạt mức trung bình vớiF 1 = 42.35%và Recall

30
50.00%. Đây là nhóm dễ bị nhầm với CQL vì nhiều điều khoản vừa đặt ra nghĩa vụ
thực hiện, vừa chứa điều kiện kỹ thuật, ngưỡng pháp lý hoặc giới hạn hành vi. Nói cách
khác, lỗi chính không chỉ đến từ số lượng mẫu mà còn từ sự chồng lấn ngữ nghĩa giữa
ràng buộc hành vi/kỹ thuật và nghĩa vụ tuân thủ phát sinh chi phí.
Hai nhãn định lượng, gồmlợi ích định lượng(BQ) vàchi phí định lượng(CQ), không
xuất hiện trong tập nhãn tham chiếu ban đầu (N = 0). Vì vậy, các giá trị Precision,
Recall và F1 bằng 0% trong bảng chủ yếu là quy ước báo cáo khi không có mẫu đánh
giá chứ không được hiểu rằng mô hình thất bại ở hai nhãn này. Kết quả này phù hợp
với đặc thù của văn bản quy phạm pháp luật: thường quy định nguyên tắc, nghĩa vụ
và cơ chế định tính, còn các mức tiền, đơn giá, tỷ lệ hỗ trợ hoặc thông số tài chính cụ
thể thường được quy định ở nghị định, thông tư hoặc văn bản hướng dẫn thi hành.
Từ góc độ phương pháp luận, sự chênh lệch hiệu năng giữa các nhãn khẳng định
vai trò cần thiết của quy trình Human-in-the-loop. Nếu sử dụng trực tiếp nhãn LLM
để lượng hóa, sai số ở các nhãn yếu như BQL và CON có thể làm sai lệch hướng tác
động hoặc mức điểm thành phần. Do đó, bước adjudication của người nghiên cứu là
điều kiện quan trọng để hiệu chỉnh các trường hợp bất đồng, giảm sai số thô và bảo
đảm tập nhãn đầu vào đủ tin cậy trước khi tínhImpactScoreei.
Hình 3.1: So sánh Precision, Recall và F1 theo từng nhãn tác động.
Biểu đồ trong hình 3.1 trực quan hóa rõ sự lệch pha giữa lớp đa số CQL và các lớp
thiểu số, qua đó cho thấy rõ hơn sự cần thiết cho nhu cầu kiểm chứng thủ công trước
khi lượng hóa.

31
3.3.2 Phân tích hiệu năng theo từng nhãn và ma trận nhầm
lẫn
Ma trận nhầm lẫn cho thấy lỗi quan trọng nhất nằm ở ranh giới giữa chi phí định
tính và ràng buộc. Nhiều điều khoản vừa yêu cầu chủ thể thực hiện nghĩa vụ, vừa đặt
điều kiện kỹ thuật như đạt quy chuẩn, không vượt ngưỡng hoặc chỉ được thực hiện
trong trường hợp nhất định. Trong các trường hợp này, LLM có xu hướng chọn nhãn
phổ biến hơn là chi phí định tính.
Hình 3.2: Ma trận nhầm lẫn của bài toán phân loại 5 nhãn.
Ma trận chuẩn hóa hữu ích khi so sánh tỷ lệ lỗi giữa các nhãn có kích thước mẫu
rất khác nhau; ma trận số lượng tuyệt đối hữu ích khi muốn nhấn mạnh khối lượng
bản ghi cần review.
3.3.3 Rà soát lỗi phân loại
Có hai nhóm lỗi có ảnh hưởng lớn đến hệ thống. Nhóm thứ nhất là nhầm lẫn giữa
COST_QUALITATIVE và CONSTRAINT. Lỗi này không làm đổi dấu tác động vì cả hai đều
có si = −1, nhưng có thể làm thay đổi cách chấmMi và Ri. Nhóm thứ hai là nhầm
lẫn giữaBENEFIT_QUALITATIVE và COST_QUALITATIVE. Đây là lỗi nghiêm trọng hơn vì
làm đảo chiều tác động từ dương sang âm nếu không được người nghiên cứu hiệu chỉnh.

32
Kết quả này giải thích vì sao giao thức xử lý bất đồng là bắt buộc. Nếu dùng trực
tiếp nhãn LLM để tính điểm, tổng điểm tác động có thể bị lệch đáng kể, đặc biệt ở các
điều khoản lợi ích thiểu số.
3.4 Kết quả thực nghiệm Giai đoạn 4: chuẩn hóa
và kiểm định actor/domain
Sau khi chốt nhãn cuối cùng, hệ thống chuẩn hóa actor và domain để phục vụ chấm
Si và Ri. Tập dữ liệu sau kiểm định gồm 581 bản ghi. Actor được chuẩn hóa thành 5
nhóm chính; domain chính được chuẩn hóa thành 13 lĩnh vực. Các cảnh báo còn lại chủ
yếu liên quan đến bản ghi có actor chung, domain rủi ro cao hoặc trường hợp nhiều
domain cùng xuất hiện.
3.5 Kết quả thực nghiệm Giai đoạn 5 : lượng hóa
điểm tác động
3.5.1 Thống kê mô tả điểm tác động
Sau khi chấmMi,S i,D i,R i vàW i cho 581 bản ghi, điểm tác động được tổng hợp
theo công thức đã trình bày ở Chương 2. Trước khi diễn giải điểm tổng hợp, cần quan
sát phân phối của bốn biến thành phần vì đây là cấu trúc đầu vào quyết định độ lớn
củaC i và, sau khi chuẩn hóa, củaImpactScoreei.

33
Hình 3.3: Phân phối điểm các chiều kíchM,S,D,Rtrong toàn bộ tập dữ liệu.
Hình 3.3 cho thấy biến cường độ tác độngMi tập trung chủ yếu ở mức 3 và 4. Điều
này phản ánh đặc trưng của Luật Bảo vệ môi trường khi phần lớn điều khoản không
chỉ mang tính khuyến nghị, mà thiết lập các nghĩa vụ hành vi hoặc yêu cầu vận hành
có mức tác động từ trung bình đến mạnh, chẳng hạn lập báo cáo môi trường, quan
trắc định kỳ, vận hành công trình xử lý chất thải hoặc đáp ứng điều kiện kỹ thuật. Các
điểm rất thấp hoặc rất cao xuất hiện ít hơn, cho thấy đa số quy định nằm quanh vùng
tác động nhưng chưa đạt mức chuyển đổi cực đoan.
Hai biến phạm vi tác độngSi và thời gian tác độngDi có xu hướng nghiêng rõ về
các điểm cao, đặc biệt ở mức 4 và 5. Đây là đặc điểm dễ hiểu của một văn bản luật cấp
quốc gia do nhiều quy định có phạm vi áp dụng rộng, liên quan đến nhiều nhóm chủ
thể hoặc nhiều địa phương, đồng thời có hiệu lực dài hạn trong suốt quá trình thực
thi luật. Tương tự, biến rủi ro và khả năng phục hồiRi cũng tập trung ở vùng điểm
cao vì các domain xuất hiện nhiều nhưwater, hazardous_substances, waste hoặc
climate_carbon đều gắn với nguy cơ ô nhiễm, suy giảm hệ sinh thái hoặc tác động
khó phục hồi nếu không được kiểm soát đúng mức.
Sự hội tụ của các biến thành phần ở vùng điểm trung bình cao giải thích vì sao
điểm tổng hợpCi của nhiều bản ghi duy trì ở mức lớn, thường nằm trên ngưỡng3.5
trên thang 1–5. Do đó, bước chuẩn hóa tuyến tính về đoạn[0, 1]là cần thiết để đưa các

34
biến khác nhau về cùng một miền so sánh trước khi nhân với hướng tác độngsi. Điều
này giúp điểm cuối cùng phản ánh nhất quán hơn mức độ gánh nặng tuân thủ hoặc lợi
ích chính sách mà từng điều khoản tạo ra.
Bảng 3.2: Thống kê mô tả điểm tác động tích lũy toàn bộ văn bản
Chỉ số Giá trị Diễn giải
TotalImpact-362.5000 Tổng điểm tác động của toàn bộ 581 bản ghi.
M eanImpact-0.6239 Điểm tác động trung bình trên mỗi bản ghi.
StdImpact0.2356 Mức phân tán điểm quanh trung bình.
M axImpact+0.8125 Điểm lợi ích cao nhất được ghi nhận.
M inImpact-0.9375 Điểm ràng buộc/chi phí mạnh nhất được ghi nhận.
Số tác động tiêu cực 566 Chiếm97.42%tổng số điều luật.
Số tác động tích cực 15 Chiếm2.58%tổng số điều luật.
N581 Số bản ghi được tính điểm.
Các thống kê trong bảng 3.2 cho thấy toàn bộ văn bản cóTotalImpact = −362.5000
và điểm trung bìnhM eanImpact= −0.6239. Giá trị âm tích lũy này không có nghĩa
là luật làm suy giảm phúc lợi xã hội, bởi vì trong bối cảnh chính sách môi trường, điểm
âm chủ yếu phản ánh gánh nặng tuân thủ tương đối và mức độ ràng buộc pháp lý cần
thiết để nội hóa các ngoại ứng tiêu cực từ hoạt động sản xuất, tiêu dùng và khai thác
tài nguyên. Nói cách khác, văn bản mang đậm sự điều tiết có kiểm soát: đặt ra nghĩa
vụ hành vi, tiêu chuẩn kỹ thuật, quy trình hành chính và giới hạn xả thải nhằm bảo vệ
tài nguyên chung.
Độ lệch chuẩnStdImpact = 0.2356ở mức tương đối thấp cho thấy điểm số hội
tụ khá mạnh quanh giá trị trung bình. Điều này có nghĩa là áp lực điều tiết được
duy trì tương đối đồng nhất giữa các nhóm điều khoản, thay vì chỉ tập trung vào
một số quy định cá biệt. Tuy nhiên, khoảng biến thiên từM inImpact= −0.9375đến
M axImpact= +0.8125vẫn cho thấy văn bản có sự phân hóa rõ về cường độ tác động
của chính sách: một phía là các lệnh cấm, điều kiện kỹ thuật hoặc quy chuẩn nghiêm
ngặt; phía còn lại là các cơ chế khuyến khích, hỗ trợ hoặc ưu đãi nhằm thúc đẩy hành
vi môi trường tích cực. Dù nhóm tác động tích cực chỉ chiếm 2.58%, các điều khoản
này vẫn có vai trò định hướng, tạo động lực cho tái chế, đổi mới công nghệ sạch, kinh
tế tuần hoàn và phát triển các-bon thấp.

35
Hình 3.4: Phân phối tần suất điểm tác động chính sách.
Hình 3.4 làm rõ hơn cấu trúc bất đối xứng của điểm tác động. Phổ điểm âm chiếm
ưu thế tuyệt đối và tập trung chủ yếu trong khoảng từ−0.3đến −1.0, phản ánh đặc
trưng của các nghĩa vụ tuân thủ, điều kiện kỹ thuật và ràng buộc hành vi. Trong đó,
nhóm điểm từ khoảng−0.5đến −0.7chiếm 65.06% số mẫu, tương ứng với mức tác
động phổ biến của các nghĩa vụ hành chính và vận hành môi trường. Phần đuôi tiến
gần cận dưới−0.9375chiếm 32.36% số mẫu, đại diện cho các quy định có cường độ
kiểm soát cao hơn, chẳng hạn lệnh cấm nghiêm ngặt, giới hạn kỹ thuật hoặc yêu cầu
gắn với rủi ro môi trường khó phục hồi.
Ở phía điểm dương, các quan sát xuất hiện thưa hơn và nằm chủ yếu trong vùng từ
khoảng+0 .5đến+0 .8. Cấu trúc này cho thấy các chính sách tạo lợi ích không được
phân bổ dàn trải trong toàn bộ luật, mà tập trung vào một số cơ chế khuyến khích
hoặc hỗ trợ cụ thể. Đường trung bình tại−0.6239có thể xem là trọng tâm điều tiết
của văn bản: Luật Bảo vệ môi trường năm 2020 chủ yếu vận hành như một hệ thống
thiết lập nghĩa vụ và ràng buộc để kiểm soát rủi ro sinh thái, trong khi các điều khoản
lợi ích đóng vai trò bổ trợ nhằm thúc đẩy chuyển dịch hành vi theo hướng bền vững
hơn. Việc hầu như không có điểm trung tính quanh 0 cũng cho thấy các bản ghi được
đưa vào lượng hóa đều mang tác động chính sách , thay vì chỉ là các điều khoản mô tả
hoặc tuyên bố chung.

36
3.5.2 Phân tích điểm tác động theo nhãn, lĩnh vực và nhóm
chủ thể
A. Phân tích theo nhãn tác động
Bảng 3.3: Thống kê điểm tác động theo nhãn cuối cùng
Nhãn cuối cùng Số lượng Điểm trung bình Tổng điểm
BENEFIT_QUALITATIVE15 +0.6625 +9.9375
CONSTRAINT122 -0.7628 -93.0625
COST_QUALITATIVE444 -0.6292 -279.3750
Kết quả trong table 3.3 cho thấyCOST_QUALITATIVE là nhóm chi phối tuyệt đối
trong tập dữ liệu, với 444 bản ghi, tương đương 76.42% tổng số điều khoản được lượng
hóa. Nhóm này cũng đóng góp lớn nhất vào tổng điểm âm, đạt−279.3750. Về mặt
quản lý nhà nước, đây là dấu hiệu cho thấy cấu trúc nền tảng của Luật Bảo vệ môi
trường chủ yếu dựa trên các nghĩa vụ tuân thủ thường xuyên như lập hồ sơ, thực hiện
thủ tục báo cáo, quan trắc định kỳ, phân loại, thu gom hoặc xử lý chất thải. Các quy
định này không nhất thiết mang tính cấm đoán tuyệt đối, nhưng tạo ra gánh nặng
hành chính và vận hành liên tục cho các chủ thể chịu điều chỉnh.
Mặc dùCONSTRAINT chỉ có 122 bản ghi, tương đương khoảng 21.00% tổng số điều
khoản, đây lại là nhóm có điểm trung bình âm mạnh nhất, đạt−0.7628, thấp hơn đáng
kể so với−0.6292của COST_QUALITATIVE. Sự khác biệt này cho thấy các điều khoản
thuộc nhóm này thường đặt ra lệnh cấm, điều kiện cấp phép, quy chuẩn kỹ thuật,
ngưỡng xả thải hoặc giới hạn hành vi trực tiếp. Do đó, chúng thường được chấm cao
hơn ở các chiều kích cường độ tác độngMi và rủi ro/khả năng phục hồiRi, phản ánh
khả năng cưỡng chế pháp lý mạnh hơn so với các thủ tục tuân thủ thông thường.
Ở chiều ngược lại,BENEFIT_QUALITATIVE chỉ gồm 15 bản ghi, tương đương 2.58%
tổng số điều khoản, nhưng có điểm trung bình dương khá cao, đạt+0.6625. Điều này
cho thấy các quy định mang tính khuyến khích, hỗ trợ hoặc ưu đãi môi trường tuy
không nhiều, nhưng thường có phạm vi ảnh hưởng và thời gian hiệu lực tương đối
đáng kể. Việc không xuất hiện các nhãn định lượng nhưBENEFIT_QUANTITATIVE và
COST_QUANTITATIVE trong nhãn cuối cùng do văn bản luật chủ yếu xác lập nguyên tắc,
nghĩa vụ và định hướng chính sách, còn các mức tiền, đơn giá, tỷ lệ hỗ trợ hoặc chế tài
tài chính cụ thể thường được chi tiết hóa ở nghị định, thông tư hoặc văn bản dưới luật.

37
B. Phân tích theo lĩnh vực môi trường chính
Bảng 3.4: Điểm tác động theo lĩnh vực môi trường chính
Domain chính Số lượng Điểm trung bình Tổng điểm
water153 -0.6520 -99.7500
hazardous_substances112 -0.7193 -80.5625
waste111 -0.5755 -63.8750
eia_permit_registration93 -0.5504 -51.1875
air_noise_radiation22 -0.6619 -14.5625
planning_state_management23 -0.5734 -13.1875
general_environment24 -0.4896 -11.7500
pollution_control_remediation14 -0.6473 -9.0625
biodiversity_natural_heritage11 -0.7614 -8.3750
technical_standard_threshold5 -0.7000 -3.5000
climate_carbon4 -0.8438 -3.3750
monitoring_reporting5 -0.4625 -2.3125
environmental_finance4 -0.2500 -1.0000
Kết quả trong table 3.4 cho thấy điểm tác động tích lũy của đạo luật tập trung mạnh
vào một số lĩnh vực quản trị môi trường cốt lõi. Bốn lĩnh vực có quy mô lớn nhất gồm
tài nguyên nước (water), chất độc hại (hazardous_substances), quản lý chất thải
(waste) và công cụ ĐTM, cấp phép, đăng ký môi trường (eia_permit_registration)
chiếm 469/581 bản ghi, tương đương 80.7% tổng số điều khoản được lượng hóa. Đồng
thời, bốn lĩnh vực này đóng góp−295.3750điểm, tức khoảng 81.5% độ lớn điểm âm
tích lũy của toàn bộ văn bản. Điều này phản ánh trọng tâm quản trị của Luật Bảo vệ
môi trường năm 2020: nguồn lực lập pháp được ưu tiên cho các lĩnh vực phát sinh ô
nhiễm trực tiếp và các công cụ hành chính dùng để kiểm soát nguồn thải trong thực tế.
Tuy nhiên, nếu xét theo điểm trung bình, cường độ tác động không biến thiên với
quy mô điều khoản. Hai lĩnh vực có số lượng bản ghi nhỏ là ứng phó biến đổi khí
hậu và các-bon (climate_carbon, −0.8438) và đa dạng sinh học, di sản thiên nhiên
(biodiversity_natural_heritage, −0.7614) lại có điểm trung bình âm rất cao. Kết
quả này phù hợp với đặc điểm kinh tế học sinh thái của các lĩnh vực này do chúng
thường gắn với rủi ro hệ thống, tác động dài hạn và khả năng phục hồi thấp. Vì vậy,
các điều khoản thuộc nhóm này có xu hướng nhận điểm cao hơn ở biến thời gian tác
độngD i và rủi ro/khả năng phục hồiRi, dù số lượng quy định không nhiều.
Ở chiều ngược lại, tài chính môi trường (environmental_finance) có điểm trung

38
bình âm thấp nhất, đạt−0.2500. Đây không phải là dấu hiệu cho thấy lĩnh vực này
ít quan trọng, mà phản ánh bản chất chính sách mềm hơn của các công cụ tài chính.
Nhiều điều khoản trong nhóm này gắn với ưu đãi, hỗ trợ, ký quỹ, chi trả dịch vụ hệ
sinh thái hoặc cơ chế bù đắp kinh tế, qua đó làm giảm gánh nặng tuân thủ và cường
độ tác động âm đối với đối tượng chịu điều chỉnh.
Hình 3.5: Biểu đồ phân phối điểm tác động theo lĩnh vực môi trường .
Hình 3.5 trực quan hóa các khác biệt nêu trên bằng biểu đồ thanh ngang theo điểm
tác động trung bình của 13 lĩnh vực môi trường , đồng thời hiển thị cỡ mẫun trên từng
thanh. Toàn bộ các thanh đều nằm về phía âm của trục hoành, cho thấy áp lực điều
tiết của Luật Bảo vệ môi trường phủ rộng lên mọi lĩnh vực được lượng hóa. Không có
lĩnh vực nào đạt điểm trung bình dương , do đó, văn bản này chủ yếu vận hành như
một hệ thống thiết lập nghĩa vụ, điều kiện và ràng buộc hành vi, thay vì phân phối lợi
ích kinh tế thuần túy.
Biểu đồ cũng làm rõ sự tương phản giữa cường độ tác động và quy mô điều
khoản. Các thanh xa trục x = 0nhất thuộc về những lĩnh vực rủi ro cao như
climate_carbon và biodiversity_natural_heritage, mặc dù cỡ mẫu lần lượt chỉ là
n = 4và n = 11. Ngược lại, các lĩnh vực nhưwater, hazardous_substances, waste
và eia_permit_registration không nhất thiết có điểm trung bình âm thấp nhưng
lại có số lượng bản ghi áp đảo. Do đó, đây là các khu vực tạo ra gánh nặng tuân thủ
thường xuyên và diện rộng nhất trong toàn bộ tập dữ liệu.
Quan sát biểu đồ phân bố, thanh biểu diễn của nhóm tài chính môi trường (environmental_finance) nằm gần trục x = 0

39
nhất, phù hợp với điểm trung bình−0.2500trong table 3.4. Hình ảnh này cho thấy các
cơ chế tài chính và công cụ khuyến khích có khả năng làm giảm cường độ điều tiết âm
so với các nhóm quy định mang tính mệnh lệnh–kiểm soát.
C. Phân tích theo nhóm chủ thể chịu điều chỉnh
Bảng 3.5: Điểm tác động theo nhóm chủ thể chịu điều chỉnh
Nhóm chủ thể Số lượng Điểm trung bình Tổng điểm
GENERAL_ORGANIZATION_INDIVIDUAL193 -0.6580 -127.0000
STATE_AGENCY179 -0.6383 -114.2500
PROJECT_OWNER_INFRASTRUCTURE102 -0.5778 -58.9375
BUSINESS_FACILITY87 -0.5999 -52.1875
COMMUNITY_CRAFT_VILLAGE20 -0.5062 -10.1250
Kết quả trong hình 3.5 cho thấy tác động của Luật Bảo vệ môi trường năm 2020
không chỉ tập trung vào doanh nghiệp hay cơ sở sản xuất, mà được phân bổ trên nhiều
nhóm chủ thể khác nhau. Nhóm tổ chức, cá nhân chung có quy mô lớn nhất với 193
bản ghi, tương đương 33.22% tổng số điều khoản được lượng hóa, đồng thời chịu tổng
điểm âm lớn nhất, đạt−127.0000. Điều này phản ánh tính phổ quát của luật khi nhiều
nghĩa vụ được thiết kế cho mọi cá nhân và tổ chức trong xã hội, chẳng hạn phân loại
chất thải tại nguồn, giữ gìn vệ sinh môi trường, tuân thủ quy định về xả thải hoặc thực
hiện trách nhiệm bảo vệ môi trường trong sinh hoạt và sản xuất.
Nhóm cơ quan nhà nước (STATE_AGENCY) đứng thứ hai cả về số lượng bản ghi lẫn
tổng điểm tác động, với 179 bản ghi và−114.2500điểm. Các điều khoản thuộc nhóm
này thường yêu cầu bộ máy quản lý lập quy hoạch, ban hành hướng dẫn, thẩm định
báo cáo ĐTM, cấp phép môi trường, thanh tra, kiểm tra, quan trắc và tổ chức giám
sát. Vì vậy, điểm âm của nhómSTATE_AGENCY cho thấy Luật Bảo vệ môi trường không
chỉ đặt nghĩa vụ lên đối tượng bị quản lý, mà còn đặt áp lực công vụ đối với hệ thống
hành chính công.
Đối với các thực thể kinh tế, hai nhóm chủ dự án, hạ tầng và cơ sở sản xuất, kinh
doanh cùng chịu tổng tác động âm tương đối, lần lượt là−58.9375và −52.1875. Điểm
trung bình của hai nhóm này dao động quanh mức−0.58đến −0.60, phản ánh các
nghĩa vụ tuân thủ về công nghệ, vận hành và quy trình quản lý môi trường. Đây là
những yêu cầu thông thường như lập báo cáo đánh giá tác động môi trường, xây dựng
hệ thống xử lý chất thải, lắp đặt thiết bị quan trắc, quản lý hồ sơ xả thải hoặc duy
trì điều kiện vận hành sau cấp phép. Kết quả này phù hợp với nguyên tắc người gây

40
ô nhiễm phải chi trả, theo đó một phần đáng kể gánh nặng bảo vệ môi trường được
chuyển về phía các chủ thể khai thác và sử dụng tài nguyên trong hoạt động kinh tế.
Nhóm cộng đồng dân cư và làng nghề (COMMUNITY_CRAFT_VILLAGE) có quy mô nhỏ
nhất, với 20 bản ghi, tương đương 3.44% tổng số điều khoản, nhưng điểm trung bình
vẫn đạt −0.5062. Điều này cho thấy luật đã bước đầu thiết lập hành lang quản lý cho
các không gian đặc thù của Việt Nam như khu dân cư, nông thôn và làng nghề, nơi ô
nhiễm thường gắn với sinh kế và tập quán sản xuất địa phương. Tuy vậy, mật độ quy
định dành cho nhóm này vẫn thấp hơn đáng kể so với khu công nghiệp, dự án đầu tư
và bộ máy quản lý nhà nước.
Hình 3.6: Biểu đồ phân phối điểm tác động theo nhóm chủ thể chịu điều chỉnh.
Hình 3.6 thể hiện góc nhìn trực quan về cường độ tác động trung bình giữa các
nhóm chủ thể. Tất cả các thanh đều nằm bên trái trụcx = 0, cho thấy không có nhóm
chủ thể nào đứng ngoài hệ thống nghĩa vụ tuân thủ của Luật Bảo vệ môi trường năm
2020.Điều đó cho thấy trách nhiệm bảo vệ môi trường được phân bổ đồng thời cho cá
nhân, tổ chức, doanh nghiệp, chủ dự án, cộng đồng địa phương và cơ quan quản lý nhà
nước.
Đánh giá một cách tổng thể, sự kết hợp giữa bảng 3.5 và hình 3.6 cho thấy cấu trúc tác động theo chủ
thể có hai lớp rõ rệt. Lớp thứ nhất là tác động phổ quát lên toàn xã hội và bộ máy
nhà nước, thể hiện qua quy mô lớn của nhómGENERAL_ORGANIZATION_INDIVIDUAL và
STATE_AGENCY. Lớp thứ hai là áp lực tuân thủ chuyên biệt lên các chủ thể kinh tế và
cộng đồng.

41
3.5.3 Phân tích các trường hợp tác động điển hình
Sau khi tính điểm cho toàn bộ 581 bản ghi, hai trường hợp điển hình được chọn để
kiểm tra khả năng giải thích của mô hình MSDR: bản ghi có tác động âm mạnh nhất
và bản ghi có tác động dương cao nhất. Hai ví dụ này được chọn bởi vì chúng đại diện
cho hai cơ chế điều tiết khác nhau của luật Bảo vệ môi trường năm 2020, một bên là
ràng buộc pháp lý nghiêm ngặt nhằm ngăn chặn rủi ro sinh thái, bên còn lại là cơ chế
khuyến khích nhằm thúc đẩy hành vi môi trường tích cực.
A. Trường hợp tác động âm mạnh nhất: bản ghi1.6.11.0
Bản ghi1.6.11.0 thuộc Điều 6, Khoản 11, liên quan đến hành vi sản xuất, nhập
khẩu, tạm nhập, tái xuất và tiêu thụ chất làm suy giảm tầng ô-dôn trái quy định của
điều ước quốc tế. Về phân loại, bản ghi được chốt nhãnCONSTRAINT, do trọng tâm
pháp lý là một lệnh cấm trực tiếp. Vì vậy, hướng tác động được xác định làsi =−1.
Các tham số lượng hóa của bản ghi này đều nằm ở mức cao. Cường độ tác động đạt
Mi = 5vì điều khoản sử dụng tín hiệu pháp lý mạnh nhất là “cấm”, tạo lực cưỡng chế
hành vi tuyệt đối. Phạm vi tác động đạtSi = 5do quy định có hiệu lực trên toàn quốc
và gắn với nghĩa vụ tuân thủ điều ước quốc tế. Thời gian tác động được chấmDi = 4,
phản ánh hiệu lực dài hạn trong suốt vòng đời của luật. Cuối cùng, rủi ro và khả năng
phục hồi đạtRi = 5vì suy giảm tầng ô-dôn và biến đổi khí hậu là các rủi ro môi trường
có quy mô hệ thống, khó đảo ngược và có khả năng tạo hệ quả xuyên biên giới.
Với bộ trọng số mặc định bằng nhau(α = β = γ = δ = 0.25), điểm thô của bản ghi
được tính như sau:
Ci = 0.25×(5 + 5 + 4 + 5) = 4.75.
Sau chuẩn hóa về khoảng[0,1], ta có:
$C^{norm}_i$ = 4.75−1
4 = 0.9375.
Dos i =−1vàW i = 1.0, điểm tác động cuối cùng là:
ImpactScoreei =−1×1.0×0.9375 =−0.9375.
Giá trị −0.9375tiệm cận mức âm cực đại của thang đo, cho thấy mô hình đã nhận
diện đúng một điều khoản có tính chất mạnh trong quản trị môi trường. Đây không
phải là nghĩa vụ thủ tục thông thường, mà là một ràng buộc cấm đoán nhằm bảo vệ
lợi ích sinh thái có tính toàn cầu. Trường hợp này minh họa khả năng của mô hình
MSDR trong việc cô lập các điều khoản có cường độ cưỡng chế cao, phạm vi rộng và

42
rủi ro môi trường nghiêm trọng.
B. Trường hợp tác động dương cao nhất: bản ghi1.58.2.0
Bản ghi1.58.2.0 thuộc Điều 58, Khoản 2, quy định việc Nhà nước khuyến khích,
ưu đãi và hỗ trợ tổ chức, cá nhân tham gia các hoạt động tuần hoàn nước, xử lý và tái
sử dụng nước thải đạt chuẩn. Khác với trường hợp trên, bản ghi này được chốt nhãn
BENEFIT_QUALITATIVE vì trọng tâm chính sách là tạo động lực tích cực cho các chủ
thể tham gia hoạt động môi trường. Do đó, hướng tác động được xác định làsi = +1.
Về tham số lượng hóa, cường độ tác động đạtMi = 4vì điều khoản không chỉ nêu
định hướng chung mà còn gắn với các công cụ ưu đãi và hỗ trợ. Phạm vi tác động đạt
Si = 5do chính sách có thể áp dụng rộng rãi cho nhiều nhóm tổ chức, cá nhân trên
phạm vi toàn quốc. Thời gian tác động được chấmDi = 4, phản ánh định hướng dài
hạn của chính sách kinh tế tuần hoàn và quản lý tài nguyên nước. Rủi ro lĩnh vực đạt
Ri = 4vì an ninh tài nguyên nước và xử lý nước thải là các vấn đề có độ nhạy cảm
cao, liên quan trực tiếp đến sức khỏe cộng đồng, sản xuất và hệ sinh thái.
Điểm thô của bản ghi được tính như sau:
Ci = 0.25×(4 + 5 + 4 + 4) = 4.25.
Sau chuẩn hóa, ta có:
$C^{norm}_i$ = 4.25−1
4 = 0.8125.
Vớis i = +1vàW i = 1.0, điểm tác động cuối cùng là:
ImpactScoreei = +1×1.0×0.8125 = +0.8125.
Giá trị+0 .8125cho thấy đây là một trong những điều khoản lợi ích có tác động
mạnh nhất trong tập dữ liệu. Về mặt chính sách, điều khoản này thể hiện vai trò kiến
tạo của pháp luật môi trường, Nhà nước sử dụng cơ chế ưu đãi và hỗ trợ để định hướng
hành vi thị trường. Cách tiếp cận này góp phần chuyển hoạt động xử lý và tái sử dụng
nước thải từ một gánh nặng tuân thủ thuần túy thành một cơ hội tạo giá trị trong mô
hình kinh tế tuần hoàn.
3.6 Thảo luận và nhận xét kết quả thực nghiệm
Từ các kết quả thực nghiệm thu được, ta có thể rút ra ba nhận xét chính về mặt
công nghệ và phương pháp luận để đánh giá tác động chính sách. Các nhận xét này
không chỉ phản ánh hiệu năng của mô hình ngôn ngữ lớn trong bài toán phân loại văn

43
bản pháp luật, mà còn cho thấy giá trị của cách tiếp cận Human-in-the-loop kết hợp
với mô hình lượng hóa bán định lượng.
Thứ nhất, kết quả thực nghiệm cho thấy trí tuệ nhân tạo vẫn có giới hạn rõ rệt
trong miền pháp lý. Ở Tầng 1, mô hình hoạt động tốt vì dữ liệu thuộc một đạo luật
chuyên ngành và bài toán chủ yếu là nhận diện điều khoản có liên quan đến môi trường.
Tuy nhiên, ở Tầng 2, tỷ lệ hiệu chỉnh của con người đạtHCR = 30.81%, cho thấy dự
đoán thô của mô hình chưa đủ tin cậy để sử dụng trực tiếp trong phân loại đa nhãn
tác động chính sách. Nguyên nhân nằm ở tính trừu tượng, tính phụ thuộc ngữ cảnh và
sự đan xen giữa nghĩa vụ, lợi ích, chi phí và ràng buộc trong ngôn ngữ lập pháp. Nếu
bỏ qua bước kiểm chứng của con người, sai lệch ở nhãn cuối cùng có thể dẫn đến sai
lệch ở hướng tác độngsi, từ đó làm giảm độ tin cậy của toàn bộ bước lượng hóa phía
sau. Vì vậy, trong bối cảnh nghiên cứu này, mô hình ngôn ngữ lớn nên được xem là
công cụ hỗ trợ đọc, gợi ý và trích xuất bằng chứng, chứ chưa thể thay thế vai trò phân
tích và ra quyết định của người nghiên cứu.
Thứ hai, kết quả phân loại cho thấy mô hình chịu ảnh hưởng đáng kể của mất cân
bằng dữ liệu. Sự chênh lệch giữa lớp đa sốCOST_QUALITATIVE với F1 = 80.32%và lớp
thiểu sốBENEFIT_QUALITATIVE với F1 = 4.65%phản ánh khuynh hướng mô hình ưu
tiên các nhãn xuất hiện thường xuyên hơn. Trong văn bản luật môi trường, điều này
dẫn đến xu hướng “an toàn hóa” dự đoán bằng cách gán nhiều điều khoản về nhóm
nghĩa vụ hoặc chi phí định tính, trong khi các cơ chế khuyến khích, hỗ trợ hoặc ưu đãi
dễ bị nhận diện thiếu chính xác. Các hướng cải thiện có thể bao gồm thiết kế prompt
theo dạng few-shot với các cặp ví dụ đối lập giữa nghĩa vụ và lợi ích, bổ sung hướng
dẫn phân biệt nhãn thiểu số rõ hơn, hoặc tinh chỉnh mô hình trên tập dữ liệu pháp
luật chuyên biệt để tăng độ nhạy đối với các điều khoản mang tính khuyến khích.
Thứ ba, mô hình MSDR cho thấy ưu điểm nổi bật về tính giải thích. Khác với việc
chỉ dừng ở nhãn phân loại, mô hình chuyển nội dung pháp lý thành điểm tác động
thông qua bốn thành phần có ý nghĩa rõ ràng: cường độ tác độngMi, phạm vi tác
động Si, thời gian tác độngDi và rủi ro/khả năng phục hồiRi. Nhờ cơ chế phân rã
này, mỗi giá trịImpactScoreei đều có thể được truy vết về các giả định chấm điểm cụ
thể, giúp người nghiên cứu giải thích vì sao một điều khoản có tác động âm mạnh, tác
động dương cao hoặc chỉ tạo ra gánh nặng tuân thủ ở mức thấp.
Tổng hợp ba nhận xét trên, pipeline đề xuất phù hợp với vai trò của một hệ thống
hỗ trợ phân tích chính sách. Mô hình ngôn ngữ lớn giúp tăng tốc quá trình đọc và gợi ý
nhãn, quy trình Human-in-the-loop bảo đảm chất lượng phân loại trong miền pháp lý,
còn mô hình MSDR cung cấp cơ chế lượng hóa có khả năng giải thích. Sự kết hợp này
tạo ra một khung phân tích vừa tận dụng được năng lực xử lý ngôn ngữ tự nhiên, vừa
duy trì được tính kiểm chứng và trách nhiệm trong nghiên cứu chính sách môi trường.

Chương 4
Kết luận, hạn chế và hướng phát
triển
4.1 Kết luận
Đồ án đã xây dựng và vận hành hoàn chỉnh hệ thống cho bài toán đánh giá tác
động chính sách môi trường từ văn bản pháp luật. Với dữ liệu Luật Bảo vệ môi trường
năm 2020 gồm 581 bản ghi, hệ thống đã thực hiện đầy đủ các bước: lọc tác động môi
trường, phân loại 5 nhãn, xử lý bất đồng, chuẩn hóa actor/domain, chấm điểm MSDR
và tính Impact Score.
Kết quả đã giải quyết được các câu hỏi nghiên cứu. Thứ nhất, mô hình ngôn ngữ
lớn có thể hỗ trợ hiệu quả ở bước đọc và gợi ý nhãn, nhưng chưa thể thay thế người
nghiên cứu trong miền pháp lý. Thứ hai, quy trình Human-in-the-loop là cần thiết vì
giai đoạn hai có 179 bản ghi bất đồng, tương đương 30.81% dữ liệu cần rà soát. Thứ
ba, mô hình MSDR có thể chuyển nhãn định tính và nội dung pháp lý thành điểm tác
động bán định lượng có khả năng giải thích, qua đó hỗ trợ phân tích theo nhãn, lĩnh
vực và chủ thể.
Tổng điểm tác động âm của toàn bộ văn bản phản ánh đặc trưng điều tiết của luật
môi trường. Luật môi trường thường đặt ra nghĩa vụ và ràng buộc để giảm rủi ro dài
hạn. Vì vậy, điểm âm được hiểu là mức độ gánh nặng tuân thủ và ràng buộc pháp lý,
trong khi lợi ích môi trường dài hạn được thể hiện thông qua mục tiêu phòng ngừa và
kiểm soát rủi ro.
44

45
4.2 Hạn chế
Hạn chế thứ nhất là chất lượng kết quả phụ thuộc vào dữ liệu đầu vào. Nếu một
bản ghi gộp quá nhiều mệnh đề hoặc thiếu ngữ cảnh điều khoản, việc gán nhãn, xác
định actor/domain và chấm điểm có thể bị lệch.
Hạn chế thứ hai là tập nhãn tham chiếu và điểm MSDR trong phạm vi đồ án do
một người nghiên cứu thực hiện.
Hạn chế thứ ba là dữ liệu bị mất cân bằng mạnh. Các nhãn lợi ích và nhãn định
lượng có rất ít hoặc không có mẫu, khiến Macro-F1 thấp và làm cho việc đánh giá nhãn
thiểu số chưa ổn định.
Hạn chế thứ tư là mô hình tính điểm sử dụng trọng số bằng nhau vàWi = 1.0cho
toàn bộ bản ghi. Cách làm này minh bạch và dễ tái lập, nhưng chưa phản ánh ưu tiên
khác nhau giữa các lĩnh vực như khí hậu, đa dạng sinh học, chất thải nguy hại hoặc tài
nguyên nước.
4.3 Hướng phát triển trong tương lai
Hướng phát triển thứ nhất là mở rộng dữ liệu sang nghị định, thông tư và quy
chuẩn kỹ thuật môi trường để kiểm tra khả năng tổng quát hóa của pipeline. Khi dữ
liệu đa dạng hơn, giai đoạn một sẽ có ý nghĩa kiểm định mạnh hơn vì không phải mọi
bản ghi đầu vào đều mặc nhiên liên quan đến môi trường.
Hướng phát triển thứ hai là nâng cấp tập dữ liệu tham chiếu bằng nhiều người gán
nhãn độc lập, đo đồng thuận liên chủ thể và thiết lập hội đồng chuyên gia để xử lý bất
đồng.
Hướng phát triển thứ ba là tối ưu hóa prompt và thử nghiệm nhiều mô hình ngôn
ngữ lớn khác nhau. Cần đặc biệt tăng số ví dụ cho các nhãn thiểu số, nhất là lợi ích
định tính, để giảm lỗi đảo chiều tác động từ lợi ích sang chi phí.
Hướng phát triển thứ tư là hiệu chuẩn trọng số bằng AHP hoặc khảo sát chuyên gia.
Bộ trọng số(α, β, γ, δ)và Wi có thể được điều chỉnh theo mục tiêu chính sách, mức độ
nhạy cảm sinh thái hoặc nhóm chủ thể ưu tiên.
Hướng phát triển cuối cùng là xây dựng dashboard để người dùng tải văn bản, theo
dõi pipeline, chỉnh nhãn, chấm điểm và xuất báo cáo tự động. Khi kết hợp với đồ thị
tri thức pháp lý, hệ thống có thể hỗ trợ truy vấn theo điều khoản, chủ thể, lĩnh vực và
mức độ tác động.

Phụ lục A
Mẫu dữ liệu JSON cấu trúc
Phụ lục này minh họa một phần bản ghi đầu vào đã được cấu trúc hóa từ Luật Bảo vệ môi trường năm 2020 (Điều 4, Khoản 6). Do giới hạn độ dài trang của báo cáo, tệp dữ liệu đầy đủ của 581 bản ghi được lưu trữ trực tuyến.

* **Dữ liệu minh họa cấu trúc:**
```json
{
  "source_id": "1.4.6.0",
  "legal_citation": "Điều 4, Khoản 6",
  "raw_text": "Điều 4. Nguyên tắc bảo vệ môi trường... Khoản 6. Cơ quan, tổ chức, cộng đồng dân cư, hộ gia đình và cá nhân được hưởng lợi từ môi trường có nghĩa vụ đóng góp tài chính cho hoạt động bảo vệ môi trường; gây ô nhiễm, sự cố và suy thoái môi trường phải chi trả, bồi thường thiệt hại, khắc phục, xử lý và chịu trách nhiệm khác theo quy định của pháp luật.",
  "co_tac_dong": true,
  "chu_the": "Cơ quan, tổ chức, cộng đồng dân cư, hộ gia đình và cá nhân",
  "tin_hieu_tac_dong": [
    "có nghĩa vụ đóng góp tài chính",
    "phải chi trả, bồi thường thiệt hại, khắc phục, xử lý"
  ],
  "domain": ["pollution_control_remediation", "environmental_finance"]
}
```
* **Kho lưu trữ trực tuyến:** Toàn bộ tập dữ liệu 581 bản ghi cấu trúc JSON được cung cấp tại đường dẫn: [data/raw/Luat_bao_ve_moi_truong_2020.json](https://github.com/DinhCongKhang2005/Do_an_1/blob/main/data/raw/Luat_bao_ve_moi_truong_2020.json).

---

Phụ lục B
Prompt Mô hình ngôn ngữ lớn (Gemini)
Phụ lục này tóm tắt cấu trúc Prompt hệ thống dùng cho Google Gemini ở Tầng 1 và Tầng 2. Nội dung Prompt thô đầy đủ với các tập ví dụ chi tiết (Few-shot examples) được tối ưu hóa bằng cách lưu trữ trên GitHub nhằm giảm tải số trang báo cáo.

* **B.1. Prompt Lọc Môi trường (Tầng 1):**
  * *Nhiệm vụ:* Đọc một bản ghi JSON và phân loại nhị phân xem bản ghi có tác động môi trường trực tiếp hay gián tiếp (`env_label` = true/false).
  * *Ràng buộc:* Bắt buộc trích dẫn bằng chứng (`evidence_span`) trực tiếp từ văn bản gốc, cấm suy diễn tự do.
  * *Prompt đầy đủ:* [prompts/env_filter_system_prompt.txt](https://github.com/DinhCongKhang2005/Do_an_1/blob/main/prompts/env_filter_system_prompt.txt)

* **B.2. Prompt Phân loại Tác động 5 nhãn (Tầng 2):**
  * *Nhiệm vụ:* Phân loại bản ghi môi trường vào một trong 5 nhãn chính sách: `BENEFIT_QUANTITATIVE`, `BENEFIT_QUALITATIVE`, `COST_QUANTITATIVE`, `COST_QUALITATIVE`, `CONSTRAINT`.
  * *Ràng buộc:* Yêu cầu xuất kết quả dưới dạng cấu trúc JSON sạch, phân tích cặn kẽ ý nghĩa số liệu định lượng (nếu có).
  * *Prompt đầy đủ:* [prompts/classify_5_labels_system_prompt.txt](https://github.com/DinhCongKhang2005/Do_an_1/blob/main/prompts/classify_5_labels_system_prompt.txt)

---

Phụ lục C
Hướng dẫn gán nhãn thủ công
Phụ lục này tóm tắt hướng dẫn gán nhãn nghiệp vụ (Labeling Guideline) cho người nghiên cứu để thực hiện gán nhãn thủ công làm dữ liệu đối chứng (Ground Truth) trong quy trình Human-in-the-loop.

| Mã nhãn | Nhãn đầy đủ | Ý nghĩa nghiệp vụ | Hướng tác động ($s_i$) |
| :--- | :--- | :--- | :--- |
| **BQ** | BENEFIT_QUANTITATIVE | Lợi ích môi trường/xã hội được lượng hóa bằng số liệu hoặc tiền tệ cụ thể. | $+1$ |
| **BQL** | BENEFIT_QUALITATIVE | Lợi ích định tính, các cơ chế khuyến khích, ưu đãi, hỗ trợ bảo vệ môi trường. | $+1$ |
| **CQ** | COST_QUANTITATIVE | Chi phí tài chính tuân thủ trực tiếp (thuế, phí, mức đóng góp, mức phạt cụ thể bằng tiền). | $-1$ |
| **CQL** | COST_QUALITATIVE | Chi phí định tính phát sinh từ nghĩa vụ thực hiện thủ tục hành chính, báo cáo, quan trắc. | $-1$ |
| **CON** | CONSTRAINT | Ràng buộc hành vi, lệnh cấm, giới hạn kỹ thuật, ngưỡng quy chuẩn bắt buộc tuân thủ. | $-1$ |

* **Tài liệu hướng dẫn đầy đủ:** Quy tắc gán nhãn chi tiết cho từng trường hợp giao thoa và ví dụ phân tích được lưu trữ tại: [docs/guidelines/labeling_guideline.md](https://github.com/DinhCongKhang2005/Do_an_1/blob/main/docs/guidelines/labeling_guideline.md).

---

Phụ lục D
Hướng dẫn chấm điểm và Quy chuẩn MSDR
Để tránh trùng lặp nội dung, toàn bộ các bảng Rubric chấm điểm từ 1 đến 5 cho 4 biến thành phần Cường độ ($M_i$), Phạm vi ($S_i$), Thời gian ($D_i$), và Rủi ro/Khả năng phục hồi ($R_i$) đã được trình bày chi tiết tại **Mục 2.6.1** (Bảng 2.8, 2.9, 2.10, và 2.11) của Chương 2. 

Người đọc có thể tham khảo tài liệu hướng dẫn chấm điểm và biên biện minh chứng điểm số chi tiết cho từng điều khoản tại kho lưu trữ: [docs/guidelines/scoring_guideline.md](https://github.com/DinhCongKhang2005/Do_an_1/blob/main/docs/guidelines/scoring_guideline.md).

---

Phụ lục E
Quy trình xử lý bất đồng nhãn và Adjudication
Phụ lục này tóm tắt quy trình xử lý bất đồng nhãn giữa nhãn gán của người nghiên cứu ($y_i$) và nhãn dự đoán của LLM ($\hat{y}_i$).

1. **Bước 1:** Trích xuất tự động các bản ghi bất đồng ($y_i 
eq \hat{y}_i$) ra tệp Excel rà soát.
2. **Bước 2:** Đối chiếu nội dung văn bản gốc (`raw_text`) và bằng chứng do LLM cung cấp (`evidence_span`).
3. **Bước 3:** Chốt nhãn cuối cùng ($y^{final}_i$) dựa trên bộ quy tắc ưu tiên tại Mục 2.3.3.
4. **Bước 4:** Ghi nhận lý do phân xử và loại sai số của mô hình học máy vào tệp kết quả.

* **Tệp quy trình và log lịch sử phân xử đầy đủ:** Được lưu trữ trực tuyến tại: [docs/guidelines/adjudication_protocol.md](https://github.com/DinhCongKhang2005/Do_an_1/blob/main/docs/guidelines/adjudication_protocol.md).

---

Phụ lục F
Mapping tài liệu tham khảo với quyết định thiết kế
Bảng F.1 dưới đây tổng hợp mối liên kết giữa các tài liệu khoa học tham khảo chính và các quyết định thiết kế hệ thống của đồ án:

| Thành phần hệ thống | Tài liệu chính | Vai trò trong thiết kế hệ thống |
| :--- | :--- | :--- |
| **RIA/EIA background** | World Bank, European Commission | Cung cấp bối cảnh và tính cấp thiết của lượng hóa chính sách. |
| **CBA** | OECD, de Zeeuw, Radhakrishnan | Định hình cơ sở lượng hóa hướng tác động có dấu lợi ích/chi phí. |
| **LLM classification** | Bermejo, Kwak | Biện minh cho phương pháp dùng LLM trích xuất bằng chứng ngữ cảnh. |
| **Legal ambiguity** | Italiani, Demetriou | Định hướng phương pháp phân tích lỗi và ma trận nhầm lẫn Confusion Matrix. |
| **Human Verification** | Tsaneva, Bonet-Jover, Wang | Thiết lập cơ chế kiểm chứng human label và tỷ lệ hiệu chỉnh HCR. |
| **Impact scoring 1–5** | Tutuka, IMPERIA | Xây dựng khung thang đo Likert và rubric chấm điểm cho các biến thành phần. |
| **Duration** | O’Mahony | Định nghĩa phương pháp lượng hóa biến thời gian tác động ($D_i$). |
| **Risk/Reversibility** | OECD, Espinoza | Thiết lập biến rủi ro sinh thái và khả năng phục hồi ($R_i$). |
| **Weight sensitivity** | Bompoti | Định hướng phân tích độ nhạy của trọng số ưu tiên. |

---

Tài liệu tham khảo
[1] OECD,Regulatory Impact Assessment: Best Practices in OECD Countries. OECD
Publishing.
[2] L. B. Leopold, F. E. Clarke, B. B. Hanshaw, and J. R. Balsley,A Procedure for
Evaluating Environmental Impact. U.S. Geological Survey Circular 645, 1971.
[3] L. W. Canter,Environmental Impact Assessment, 2nd ed. McGraw-Hill, 1996.
[4] United Nations Environment Programme,Assessing Environmental Impacts: A
Global Review of Legislation. UNEP, 2018.
[5] A. E. Boardman, D. H. Greenberg, A. R. Vining, and D. L. Weimer,Cost-Benefit
Analysis: Concepts and Practice. Cambridge University Press.
[6] M. Sokolova and G. Lapalme, “A systematic analysis of performance measures for
classification tasks,”Information Processing & Management, vol. 45, no. 4, pp.
427–437, 2009.
[7] C. D. Manning, P. Raghavan, and H. Sch¨ utze,Introduction to Information Retrieval.
Cambridge University Press, 2008.
[8] Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam,Luật Bảo vệ môi trường, Luật
số 72/2020/QH14, 2020.
97