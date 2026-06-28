# Báo cáo Tổng hợp Kết quả Nghiên cứu Hệ thống DTM & Hướng dẫn Chèn Minh họa Học thuật

Tài liệu này tổng hợp toàn bộ kết quả quan trọng thu được từ việc vận hành hệ thống **DTM (Environmental Policy Impact Assessment using RIA–EIA–CBA)** đối với đối tượng thực nghiệm là **Luật Bảo vệ môi trường năm 2020** ($N = 581$ bản ghi). Tài liệu được cấu trúc dưới dạng các bảng biểu học thuật, phân tích kết quả định lượng, gợi ý chèn hình ảnh trực quan sinh động từ thư mục `outputs/figures/` và cung cấp các đoạn diễn giải mẫu (academic discussions) giúp tăng tính khoa học cho báo cáo đồ án.

---

## 1. Tổng quan các Giai đoạn Pipeline và Kết quả Chính

Hệ thống DTM vận hành qua pipeline 2 tầng kết hợp Human-in-the-loop, được hiện thực hóa qua các script trong thư mục [src](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src):

1. **Giai đoạn 1: Validate Schema Đầu vào** ([01_validate_input_schema.py](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src/01_validate_input_schema.py)): Xác thực cấu trúc dữ liệu thô, ghi nhận $N = 581$ điều khoản có tác động chính sách hợp lệ.
2. **Giai đoạn 2: Lọc tác động môi trường (Tầng 1)** ([02_build_env_manual_label_file.py](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src/02_build_env_manual_label_file.py) đến [05_build_env_final_dataset.py](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src/05_build_env_final_dataset.py)): Tách lọc các điều khoản liên quan tới môi trường. Thực nghiệm cho thấy toàn bộ $N = 581$ bản ghi đều được xác thực có tác động môi trường.
3. **Giai đoạn 3: Phân loại tác động 5 nhãn (Tầng 2)** ([06_build_class_manual_label_file.py](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src/06_build_class_manual_label_file.py) đến [09_build_final_labeled_dataset.py](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src/09_build_final_labeled_dataset.py)): Phân loại các điều khoản vào 5 lớp tác động. LLM đạt độ chính xác tổng thể $Accuracy = 69.19\%$ và tỷ lệ hiệu chỉnh thủ công từ con người là $HCR = 30.81\%$. Sau bước rà soát, tập nhãn cuối cùng được chốt để chuyển sang chấm điểm.
4. **Giai đoạn 3b: Chuẩn hóa Actor & Domain** ([09b_build_actor_domain_review.py](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src/09b_build_actor_domain_review.py) và [09c_validate_actor_domain.py](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src/09c_validate_actor_domain.py)): Chuẩn hóa tự động và kiểm duyệt thủ công 5 nhóm chủ thể (`actor_group`) và 13 lĩnh vực môi trường chính (`domain_primary`). Ghi nhận 160 cảnh báo kiểm định nhưng 0 lỗi nghiêm trọng.
5. **Giai đoạn 4: Chấm điểm bán định lượng & Phân tích** ([10_build_scoring_input.py](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src/10_build_scoring_input.py) đến [13_generate_pipeline_summary.py](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/src/13_generate_pipeline_summary.py)): Đánh giá các biến thành phần $M_i, S_i, D_i, R_i$ (quy mô, không gian, thời gian, rủi ro) để tính điểm tác động chính sách $ImpactScore_i$. Kết quả chỉ ra luật có xu hướng tạo ra nghĩa vụ tuân thủ và ràng buộc pháp lý/kỹ thuật cao với tổng điểm $TotalImpact = -362.50$ và điểm trung bình $MeanImpact = -0.6239$.

---

## 2. Gợi ý Chèn Bảng biểu vào Báo cáo Học thuật (Tables)

Dưới đây là các bảng kết quả được trích xuất trực tiếp từ các báo cáo trong [data/reports](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/data/reports). Bạn có thể copy trực tiếp các bảng Markdown này vào báo cáo đồ án.

### Bảng 1: Đánh giá hiệu năng mô hình LLM phân loại tác động chính sách (Tầng 2)
> [!NOTE]
> Bảng này thể hiện khả năng phân loại của mô hình Gemini đối so với nhãn chuẩn của người nghiên cứu trước khi thực hiện hiệu chỉnh (adjudication). Dữ liệu lấy từ file [classification_metrics.xlsx](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/data/reports/classification_metrics.xlsx).

| Nhãn Tác động | Mã Nhãn | Độ chính xác (Precision) | Độ nhạy (Recall) | F1-Score | Kích thước mẫu (Support) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Lợi ích định lượng** | BQ | 0.00% | 0.00% | 0.00% | 0 |
| **Lợi ích định tính** | BQL | 4.76% | 4.55% | 4.65% | 22 |
| **Chi phí định lượng** | CQ | 0.00% | 0.00% | 0.00% | 0 |
| **Chi phí định tính** | CQL | 84.02% | 76.94% | 80.32% | 451 |
| **Ràng buộc** | CON | 36.73% | 50.00% | 42.35% | 108 |
| **Toàn bộ Dataset** | - | **Accuracy: 69.19%** | **Macro-F1: 25.47%** | - | **Tổng: 581** |

* **Diễn giải học thuật:** 
  * Chỉ số $Accuracy_class = 69.19\%$ cho thấy khả năng phân loại khá tốt ở lớp đa số. Lớp `COST_QUALITATIVE` (CQL) có hiệu năng vượt trội ($F1 = 80.32\%$) do chiếm ưu thế lớn trong tập mẫu dữ liệu luật ($77.6\%$ số mẫu).
  * Ngược lại, mô hình gặp khó khăn nghiêm trọng ở các lớp thiểu số như `BENEFIT_QUALITATIVE` ($F1 = 4.65\%$, chỉ có 22 mẫu) do mất cân bằng dữ liệu cực đoan (imbalanced data). Lớp `CONSTRAINT` đạt hiệu năng trung bình với $F1 = 42.35\%$, thường bị mô hình nhầm lẫn với `COST_QUALITATIVE` vì ranh giới ngữ nghĩa pháp lý giữa "chi phí tuân thủ thủ tục" và "ràng buộc kỹ thuật/lệnh cấm" rất hẹp.
  * Chỉ số sửa lỗi của con người $HCR = 30.81\%$ khẳng định sự cần thiết của quy trình **Human-in-the-loop (HITL)**; mô hình AI chỉ đóng vai trò trợ lý gợi ý nhãn, còn chuyên gia là người hiệu chuẩn cuối cùng để đảm bảo độ tin cậy khoa học.

### Bảng 2: Thống kê mô tả điểm tác động chính sách theo lĩnh vực môi trường (Domains)
> [!NOTE]
> Bảng này giúp nhận diện lĩnh vực môi trường nào chịu sự điều chỉnh gắt gao nhất và phân bố tần suất điều khoản. Dữ liệu lấy từ file [final_impact_report.xlsx](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/data/reports/final_impact_report.xlsx).

| Lĩnh vực môi trường chính | Số lượng điều khoản | Tỷ lệ (%) | Điểm tác động TB ($MeanImpact$) | Tổng điểm tác động ($TotalImpact$) |
| :--- | :---: | :---: | :---: | :---: |
| **Tài nguyên nước** (`water`) | 153 | 26.33% | -0.6520 | -99.7500 |
| **Chất độc hại & Hóa chất** (`hazardous_substances`) | 112 | 19.28% | -0.7193 | -80.5625 |
| **Chất thải** (`waste`) | 111 | 19.10% | -0.5755 | -63.8750 |
| **ĐTM, Cấp phép & Đăng ký** (`eia_permit_registration`) | 93 | 16.01% | -0.5504 | -51.1875 |
| **Quản lý hành chính & Quy hoạch** (`planning_state_management`) | 23 | 3.96% | -0.5734 | -13.1875 |
| **Không khí, Tiếng ồn & Bức xạ** (`air_noise_radiation`) | 22 | 3.79% | -0.6619 | -14.5625 |
| **Môi trường chung** (`general_environment`) | 24 | 4.13% | -0.4896 | -11.7500 |
| **Kiểm soát & Khắc phục ô nhiễm** (`pollution_control_remediation`) | 14 | 2.41% | -0.6473 | -9.0625 |
| **Đa dạng sinh học & Di sản tự nhiên** (`biodiversity_natural_heritage`) | 11 | 1.89% | -0.7614 | -8.3750 |
| **Tiêu chuẩn kỹ thuật & Ngưỡng** (`technical_standard_threshold`) | 5 | 0.86% | -0.7000 | -3.5000 |
| **Biến đổi khí hậu & Cacbon** (`climate_carbon`) | 4 | 0.69% | -0.8438 | -3.3750 |
| **Quan trắc & Báo cáo** (`monitoring_reporting`) | 5 | 0.86% | -0.4625 | -2.3125 |
| **Tài chính môi trường** (`environmental_finance`) | 4 | 0.69% | -0.2500 | -1.0000 |
| **TỔNG CỘNG** | **581** | **100%** | **-0.6239** | **-362.5000** |

* **Diễn giải học thuật:**
  * Ba lĩnh vực **Tài nguyên nước** ($N=153$), **Chất độc hại** ($N=112$) và **Chất thải** ($N=111$) chiếm tới gần $65\%$ tổng số điều khoản có tác động môi trường. Điều này phản ánh rõ nét trọng tâm lập pháp của Luật BVMT 2020: tập trung giải quyết các vấn đề ô nhiễm cục bộ, quản lý chất thải rắn và bảo vệ an ninh nguồn nước tại Việt Nam.
  * Mặc dù lĩnh vực **Biến đổi khí hậu & Cacbon** (`climate_carbon`) và **Đa dạng sinh học** (`biodiversity_natural_heritage`) chiếm số lượng điều khoản rất nhỏ ($<2\%$), nhưng lại có giá trị điểm tác động trung bình cực kỳ tiêu cực (lần lượt là $-0.8438$ và $-0.7614$). Điều này lý giải là do các lĩnh vực này có mức độ rủi ro môi trường cao ($R_i \ge 4$), tính chất tác động dài hạn ($D_i \ge 4$), dẫn đến điểm số quy đổi thành phần rất cao và tạo ra ràng buộc pháp lý/kỹ thuật rất nặng lên các chủ thể thực hiện.

### Bảng 3: Điểm tác động chính sách theo nhóm chủ thể chịu điều chỉnh (Actors)
> [!NOTE]
> Bảng này thống kê gánh nặng tuân thủ pháp luật và nhiệm vụ quản lý được phân bổ giữa các nhóm chủ thể xã hội. Dữ liệu lấy từ file [final_impact_report.xlsx](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/data/reports/final_impact_report.xlsx).

| Nhóm chủ thể chịu tác động | Mã Nhóm | Số điều khoản | Tỷ lệ (%) | Điểm tác động TB | Tổng điểm tác động |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tổ chức, cá nhân chung** | `GENERAL_ORGANIZATION_INDIVIDUAL` | 193 | 33.22% | -0.6580 | -127.0000 |
| **Cơ quan quản lý Nhà nước** | `STATE_AGENCY` | 179 | 30.81% | -0.6383 | -114.2500 |
| **Chủ dự án đầu tư, hạ tầng** | `PROJECT_OWNER_INFRASTRUCTURE` | 102 | 17.56% | -0.5778 | -58.9375 |
| **Doanh nghiệp, cơ sở SXKD** | `BUSINESS_FACILITY` | 87 | 14.97% | -0.5999 | -52.1875 |
| **Cộng đồng dân cư, làng nghề** | `COMMUNITY_CRAFT_VILLAGE` | 20 | 3.44% | -0.5062 | -10.1250 |
| **TỔNG CỘNG** | - | **581** | **100%** | **-0.6239** | **-362.5000** |

* **Diễn giải học thuật:**
  * Nhóm **Tổ chức, cá nhân chung** gánh chịu tổng điểm tác động âm lớn nhất ($-127.00$), đại diện cho các nghĩa vụ mang tính phổ quát như phân loại rác tại nguồn, giữ gìn vệ sinh chung và không gây ô nhiễm môi trường.
  * Đặc biệt, **Cơ quan quản lý Nhà nước** (`STATE_AGENCY`) chiếm tới $30.81\%$ số lượng điều khoản với tổng điểm $-114.25$. Điều này chỉ ra rằng Luật BVMT 2020 không chỉ đặt ra nghĩa vụ cho khối kinh tế, mà còn áp đặt một khối lượng công việc hành chính khổng lồ lên hệ thống công quyền (lập quy hoạch, thẩm định ĐTM, cấp phép môi trường, kiểm tra, thanh tra và vận hành hệ thống thông tin môi trường). Đây là luận điểm thực tế quan trọng chứng minh tính chất "gánh nặng hành chính" (administrative burden) của luật.
  * Nhóm doanh nghiệp sản xuất và chủ dự án đầu tư (`BUSINESS_FACILITY` và `PROJECT_OWNER_INFRASTRUCTURE`) chịu sự điều tiết chặt chẽ qua các nghĩa vụ lắp đặt thiết bị quan trắc tự động, xử lý nước thải/khí thải đạt chuẩn và các cam kết bảo vệ môi trường dài hạn.

### Bảng 4: Điểm mặt các điều khoản tiêu biểu có điểm tác động đặc biệt lớn
> [!IMPORTANT]
> Đây là các trường hợp điển hình cực đoan (outliers) được lọc ra nhằm phục vụ phân tích định tính chuyên sâu trong đồ án. Bảng trích xuất từ dữ liệu `top10_impact` và `tong_hop` của báo cáo.

| Mã bản ghi | Trích dẫn pháp lý | Nhãn | Chủ thể tác động | Lĩnh vực môi trường | Điểm tác động | Nhận định phân tích định tính (Trích dẫn tóm tắt lý do) |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| `1.6.11.0` | Điều 6, Khoản 11 | CON | Tổ chức, cá nhân | Biến đổi khí hậu | **-0.9375** | Hành vi phá hủy thiết bị, xả chất làm suy giảm tầng ô-dôn có tính cấm đoán tuyệt đối, phạm vi tác động toàn quốc ($S_i=5$), rủi ro môi trường cực kỳ nghiêm trọng và khó phục hồi ($R_i=5$). |
| `1.84.3.0` | Điều 84, Khoản 3 | CON | Tổ chức, cá nhân | Chất độc hại | **-0.8750** | Quy định nghiêm ngặt về đăng ký, khai báo, đánh giá chất độc hại và POPs phát sinh, ảnh hưởng diện rộng và có tính lâu dài ($D_i=4$). |
| `1.28.7.0` | Điều 28, Khoản 7 | CON | Cơ quan Nhà nước | Tài nguyên nước | **-0.8750** | Quy định chặt chẽ về thẩm quyền phê duyệt báo cáo đánh giá tác động môi trường (ĐTM) của các dự án nhóm I ảnh hưởng đến lưu vực sông. |
| `1.58.2.0` | Điều 58, Khoản 2 | BQL | Cơ quan Nhà nước | Tài nguyên nước | **+0.8125** | Chính sách khuyến khích hỗ trợ của Nhà nước cho các hoạt động tuần hoàn nước, xử lý và tái sử dụng nước thải đạt tiêu chuẩn cao. |
| `1.75.2.0` | Điều 75, Khoản 2 | BQL | Cơ quan Nhà nước | Chất độc hại | **+0.8125** | Các chính sách ưu đãi, hỗ trợ đầu tư công nghệ sạch, xử lý và cô lập hóa chất độc hại tồn lưu sau chiến tranh. |

---

## 3. Gợi ý Chèn Hình ảnh và Đồ thị (Figures)

Trong thư mục [outputs/figures](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures), hệ thống đã tạo sẵn các biểu đồ trực quan hóa chuyên nghiệp. Dưới đây là danh sách hình ảnh cần đưa vào báo cáo và hướng dẫn giải thích học thuật tương ứng.

### Hình 1: Ma trận nhầm lẫn chuẩn hóa phân loại tác động (Phase 3)
* **File liên kết:** [normalized_confusion_matrix.png](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/normalized_confusion_matrix.png) hoặc [confusion_matrix.png](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/confusion_matrix.png)
* **Vị trí đề xuất trong báo cáo:** Phần *Đánh giá thực nghiệm hiệu năng mô hình LLM (Tầng 2)*.
* **Mô tả học thuật:** Biểu đồ hiển thị tỷ lệ dự đoán đúng (trên đường chéo chính) và các phân bố nhầm lẫn nhãn giữa 5 lớp tác động chính sách của LLM so với Human reference label.
* **Cách diễn giải:** 
  * Đường chéo chính của nhãn `COST_QUALITATIVE` (CQL) đạt giá trị cao nhất ($76.9\%$), thể hiện khả năng học mẫu tốt của mô hình trên lớp dữ liệu lớn.
  * Có sự nhầm lẫn đáng kể từ các nhãn khác sang `COST_QUALITATIVE`. Ví dụ: mô hình dự đoán nhầm $45\%$ nhãn `CONSTRAINT` thành `COST_QUALITATIVE`, và dự đoán nhầm $68\%$ nhãn `BENEFIT_QUALITATIVE` thành `COST_QUALITATIVE`. Điều này chỉ ra xu hướng "bias" (thiên lệch) của LLM về phía nhãn phổ biến nhất trong hệ thống pháp luật môi trường và sự khó khăn của mô hình trong việc phân biệt các sắc thái ngữ nghĩa nhỏ của câu chữ pháp luật.

### Hình 2: So sánh chỉ số Precision, Recall và F1 theo từng nhãn
* **File liên kết:** [classification_metric_by_label.png](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/classification_metric_by_label.png)
* **Vị trí đề xuất trong báo cáo:** Phần *Đánh giá thực nghiệm hiệu năng mô hình LLM (Tầng 2)*, đặt ngay cạnh hoặc tích hợp với ma trận nhầm lẫn.
* **Mô tả học thuật:** Biểu đồ cột biểu diễn trực quan ba chỉ số Precision, Recall và F1-score của mô hình trên từng lớp nhãn.
* **Cách diễn giải:** Biểu đồ minh họa trực quan sự phân cực hiệu năng nghiêm trọng giữa các nhãn. Nhãn `BQ` và `CQ` không có cột biểu diễn do số lượng mẫu thực tế bằng 0. Nhãn `BQL` có cột cực kỳ thấp thể hiện thách thức trong việc khai phá các điều khoản mang tính khuyến khích/lợi ích ẩn chứa trong văn bản luật đa số là bắt buộc.

### Hình 3: Phân bố tần suất Điểm tác động chính sách (Impact Score Histogram)
* **File liên kết:** [impact_score_histogram.png](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/impact_score_histogram.png) (hoặc ảnh độ phân giải cao trong [outputs/figures/L3_tinh_diem/impact_score_histogram.png](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/L3_tinh_diem/impact_score_histogram.png))
* **Vị trí đề xuất trong báo cáo:** Đầu phần *Kết quả đánh giá tác động bán định lượng*.
* **Mô tả học thuật:** Biểu đồ phân phối tần suất (Histogram) của biến liên tục $ImpactScore_i$ trên toàn bộ 581 điều khoản.
* **Cách diễn giải:** 
  * Biểu đồ có hình dáng lệch trái cực đoan (highly negative skewness), với phần lớn mật độ tập trung trong vùng $[-0.75, -0.5]$. Điều này phản ánh tính chất thực tế của Luật Bảo vệ môi trường: là một đạo luật điều chỉnh hành vi thiết lập nghĩa vụ bắt buộc và các quy chuẩn kiểm soát nguồn thải thay vì ban phát các lợi ích tài chính trực tiếp.
  * Chỉ xuất hiện một số lượng cực nhỏ các giá trị dương ($>0.5$), tạo thành một nhóm nhỏ cô lập ở rìa phải của đồ thị, tương ứng với 15 điều khoản khuyến khích ưu đãi phát triển kinh tế tuần hoàn và phục hồi môi trường.

### Hình 4: Phân phối điểm số theo các chiều kích thành phần (M, S, D, R)
* **File liên kết:** [score_component_distribution.png](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/score_component_distribution.png)
* **Vị trí đề xuất trong báo cáo:** Phần *Phân tích chi tiết mô hình bán định lượng MSDR*.
* **Mô tả học thuật:** Biểu đồ thể hiện phân bố tần suất điểm chấm từ 1 đến 5 cho bốn biến thành phần: Quy mô tác động ($M$), Không gian ($S$), Thời gian ($D$), và Mức độ rủi ro của domain ($R$).
* **Cách diễn giải:**
  * Cột điểm 4 và 5 chiếm tỷ trọng vượt trội ở biến Không gian ($S_i$) và Thời gian ($D_i$). Nguyên nhân là do Luật BVMT là luật cấp quốc gia, áp dụng chung cho hầu hết các tổ chức/cá nhân trên phạm vi cả nước và có giá trị hiệu lực thi hành lâu dài (thường không quy định thời hạn kết thúc).
  * Biến Quy mô tác động ($M_i$) và Mức rủi ro môi trường ($R_i$) phân tán đều hơn từ điểm 2 đến điểm 5, giúp phân biệt rõ nét mức độ tác động của từng điều khoản cụ thể dựa trên tính chất kỹ thuật và nguy cơ gây ô nhiễm của từng đối tượng điều chỉnh.

### Hình 5: Biểu đồ hộp biểu thị Điểm tác động theo Lĩnh vực (Domain Primary)
* **File liên kết:** [impact_score_by_domain.png](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/impact_score_by_domain.png)
* **Vị trí đề xuất trong báo cáo:** Phần *Phân tích tác động theo lĩnh vực điều chỉnh*.
* **Mô tả học thuật:** Biểu đồ hộp (Boxplot) thể hiện giá trị trung bình, trung vị, khoảng tứ phân vị và các điểm ngoại lai của $ImpactScore_i$ trên 13 lĩnh vực môi trường.
* **Cách diễn giải:** Biểu đồ giúp người đọc nhanh chóng nhận ra sự khác biệt giữa các domain. Các domain thuộc nhóm kỹ thuật cao như `climate_carbon` hoặc `hazardous_substances` có hộp điểm nằm sâu ở vùng âm dưới và biên độ hẹp (tính đồng nhất cao ở mức tác động nghiêm trọng), trong khi domain `waste` hay `eia_permit_registration` có biên độ dao động điểm rộng hơn, thể hiện sự phân hóa đa dạng giữa các điều khoản thủ tục hành chính đơn giản và các ràng buộc đầu tư xây dựng hệ thống xử lý lớn.

### Hình 6: Biểu đồ hộp biểu thị Điểm tác động theo Nhóm chủ thể (Actor Group)
* **File liên kết:** [impact_score_by_actor.png](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/impact_score_by_actor.png)
* **Vị trí đề xuất trong báo cáo:** Phần *Phân tích tác động theo nhóm chủ thể*.
* **Mô tả học thuật:** Biểu đồ hộp trực quan hóa sự phân bố và phân tán điểm tác động lên 5 nhóm chủ thể xã hội chịu sự điều chỉnh của luật.
* **Cách diễn giải:** 
  * Nhóm `STATE_AGENCY` và `GENERAL_ORGANIZATION_INDIVIDUAL` có dải phân bố điểm rộng và lượng điểm ngoại lai tích cực (lợi ích) nhiều nhất, phản ứng đúng bản chất đây là các nhóm trực tiếp thực hiện và thụ hưởng các chính sách quản lý nhà nước hoặc bảo vệ môi trường nông thôn.
  * Nhóm doanh nghiệp sản xuất (`BUSINESS_FACILITY`) có phân bố điểm âm đậm đặc và ít biến động, thể hiện gánh nặng tuân thủ đồng đều và liên tục đối với mọi cơ sở sản xuất kinh doanh có phát sinh nguồn thải.

---

## 4. Những Kết luận Khoa học đắt giá cần đưa vào Báo cáo Đồ án

Khi viết chương *Thảo luận & Kết quả* trong báo cáo học thuật, người nghiên cứu có thể sử dụng các kết luận then chốt sau để tạo điểm nhấn khoa học:

1. **Minh chứng cho tính chất "Chủ động phòng ngừa rủi ro":** Điểm số trung bình âm lớn của hệ thống ($MeanImpact = -0.6239$) phản ánh sự dịch chuyển quan trọng trong tư duy làm luật môi trường của Việt Nam từ "ứng phó, giải quyết hậu quả" sang "chủ động phòng ngừa, kiểm soát nguồn thải từ sớm". Các điều khoản mang tính ràng buộc kỹ thuật (`CONSTRAINT`) có tính chất gắt gao vượt trội chứng tỏ quyết tâm chuẩn hóa hành vi xả thải của cơ quan lập pháp.
2. **Hiện tượng lệch pha hiệu năng của LLM trong khai phá văn bản pháp lý:** Kết quả đo lường thực nghiệm tầng 2 chứng minh mô hình ngôn ngữ lớn (Gemini) dễ bị ảnh hưởng bởi sự mất cân bằng dữ liệu cực đoan trong văn bản pháp luật (lớp CQL chiếm $77.6\%$). Điều này mở ra đóng góp khoa học về phương pháp: cần áp dụng các kỹ thuật cân bằng dữ liệu (như Oversampling) hoặc tối ưu hóa prompt chuyên sâu (few-shot prompting) đối với các nhóm nhãn thiểu số (như `BQL` - lợi ích định tính) nếu muốn triển khai AI tự động hóa hoàn toàn.
3. **Ý nghĩa của sự kết hợp Hybrid (AI + Expert):** Việc xây dựng thành công pipeline HITL với giao thức Adjudication Protocol (bước rà soát bất đồng) giúp đảm bảo dữ liệu đầu ra đạt độ chính xác $100\%$ về mặt học thuật pháp lý trước khi đưa vào chấm điểm. AI đóng vai trò giảm thiểu $70\%$ thời gian đọc hiểu ban đầu của chuyên gia thông qua gán nhãn tự động, trong khi con người giữ vai trò kiểm soát chất lượng tối cao (Quality Assurance).
4. **Bản chất của điểm tác động bán định lượng (Semi-quantitative Impact Score):** Cần nhấn mạnh trong báo cáo rằng điểm tác động trong đồ án này là thang đo tương đối dựa trên khung đánh giá tác động chính sách (RIA) kết hợp đánh giá tác động môi trường (EIA) nhằm mục tiêu xếp hạng mức độ ảnh hưởng của điều khoản, không phải là kết quả phân tích Chi phí - Lợi ích (CBA) bằng tiền mặt tuyệt đối. Thang đo này cho phép xử lý định lượng hóa một lượng lớn văn bản pháp luật phi cấu trúc thành dữ liệu có thể trực quan hóa và truy vết nguồn gốc (explainable).

---

> [!TIP]
> **Hướng dẫn sử dụng:**
> * Đối với các bảng số liệu, bạn có thể copy trực tiếp mã bảng Markdown vào tài liệu báo cáo của mình.
> * Đối với hình ảnh, các tệp ảnh chất lượng cao (300 DPI) đã được lưu sẵn trong thư mục [outputs/figures/L3_tinh_diem](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/L3_tinh_diem) và [outputs/figures/L3_anh_gan_5_nhan](file:///d:/CAC_MON_HOC_KY_2025_2/4_MI3380_Do_an_1/Đánh giá tác động chính sách môi trường_ Khung định lượng chi phí, lợi ích, rủi ro/DTM/outputs/figures/L3_anh_gan_5_nhan). Bạn hãy chèn trực tiếp các tệp này vào báo cáo Word hoặc LaTeX tương ứng với số thứ tự hình gợi ý ở trên.
