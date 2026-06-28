"""
src/00_common/__init__.py
=========================
Package chứa các module dùng chung cho toàn bộ pipeline DTM.

Modules:
    - io_utils: Đọc/ghi file (JSON, Excel), tạo thư mục
    - config_loader: Load và cache YAML configs
    - label_utils: Normalize và validate nhãn
    - metric_utils: Tính metric đánh giá LLM (cả 2 tầng)
    - llm_client: Gọi LLM (Google AI Studio / Vertex AI)

Cách import trong script:
    from src.00_common.io_utils import load_json, save_excel
    from src.00_common.config_loader import get_project_config
    from src.00_common.metric_utils import compute_env_metrics

Hoặc thêm project root vào sys.path và import trực tiếp:
    import sys; sys.path.insert(0, str(Path(__file__).parent.parent))
    from common.io_utils import load_json
"""
