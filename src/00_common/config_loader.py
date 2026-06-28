"""
src/00_common/config_loader.py
==============================
Load và parse các file cấu hình YAML cho pipeline DTM.

Lý do:
    - Tập trung việc đọc config vào 1 chỗ, có validation cơ bản
    - Script chính chỉ cần gọi get_config() và dùng key, không cần biết chi tiết YAML
    - Khi thay đổi tên key trong YAML, chỉ sửa ở đây
"""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from .io_utils import get_project_root


# Cache config đã load để không đọc file nhiều lần
_config_cache: Dict[str, Any] = {}


def _load_yaml(filepath: Path) -> Dict:
    """Load một file YAML và trả về dict."""
    if not filepath.exists():
        raise FileNotFoundError(f"Không tìm thấy file config: {filepath}")
    with open(filepath, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_project_config() -> Dict:
    """
    Load config/project_config.yaml.
    
    Chứa: đường dẫn, tên file, tên cột, cấu hình LLM, cấu hình pipeline 2 tầng.
    
    Returns:
        Dict: Toàn bộ nội dung project_config.yaml
    """
    cache_key = "project_config"
    if cache_key not in _config_cache:
        path = get_project_root() / "config" / "project_config.yaml"
        _config_cache[cache_key] = _load_yaml(path)
    return _config_cache[cache_key]


def get_labels_config() -> Dict:
    """
    Load config/labels.yaml.
    
    Chứa: 5 nhãn, impact_direction, valid_labels, label_colors.
    
    Returns:
        Dict: Cấu hình nhãn
    """
    cache_key = "labels"
    if cache_key not in _config_cache:
        path = get_project_root() / "config" / "labels.yaml"
        _config_cache[cache_key] = _load_yaml(path)
    return _config_cache[cache_key]


def get_scoring_config() -> Dict:
    """
    Load config/scoring_config.yaml.
    
    Chứa: score_range, weights (alpha/beta/gamma/delta), default_W_i, normalize formula.
    
    Returns:
        Dict: Cấu hình tính điểm
    """
    cache_key = "scoring"
    if cache_key not in _config_cache:
        path = get_project_root() / "config" / "scoring_config.yaml"
        _config_cache[cache_key] = _load_yaml(path)
    return _config_cache[cache_key]


def get_keywords_config() -> Dict:
    """
    Load config/env_filter_keywords.yaml.
    
    Chứa: environment_domains với từ khóa theo 10 domain.
    
    Returns:
        Dict: Cấu hình từ khóa môi trường
    """
    cache_key = "keywords"
    if cache_key not in _config_cache:
        path = get_project_root() / "config" / "env_filter_keywords.yaml"
        _config_cache[cache_key] = _load_yaml(path)
    return _config_cache[cache_key]


# =============================================================================
# Các hàm tiện ích truy cập config nhanh
# =============================================================================

def get_valid_labels() -> list:
    """Trả về danh sách 5 nhãn hợp lệ."""
    return get_labels_config()["valid_labels"]


def get_impact_direction(label: str) -> int:
    """
    Trả về hướng tác động (+1 hoặc -1) cho một nhãn.
    
    Args:
        label: Tên nhãn đầy đủ (ví dụ: "BENEFIT_QUANTITATIVE")
    
    Returns:
        int: +1 hoặc -1
    
    Raises:
        KeyError: Nếu nhãn không hợp lệ
    """
    direction_map = get_labels_config()["impact_direction"]
    if label not in direction_map:
        raise KeyError(f"Nhãn không hợp lệ: '{label}'. Nhãn hợp lệ: {list(direction_map.keys())}")
    return direction_map[label]


def get_scoring_weights() -> Dict[str, float]:
    """
    Trả về dict trọng số {alpha, beta, gamma, delta}.
    Kiểm tra alpha + beta + gamma + delta == 1.0.
    """
    weights = get_scoring_config()["weights"]
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"Tổng trọng số phải = 1.0, hiện tại = {total:.4f}")
    return weights


def get_col(section: str, key: str) -> str:
    """
    Lấy tên cột từ project_config.yaml.
    
    Args:
        section: "env_filter" hoặc "classification"
        key: "human_label_column", "llm_label_column", "final_label_column", ...
    
    Returns:
        str: Tên cột
    
    Example:
        >>> get_col("env_filter", "human_label_column")
        "env_human"
        >>> get_col("classification", "final_label_column")
        "final_label"
    """
    cfg = get_project_config()
    return cfg[section][key]


def get_path(key: str) -> Path:
    """
    Lấy đường dẫn từ project_config.yaml[paths] và resolve thành Path tuyệt đối.
    
    Args:
        key: Tên key trong paths (ví dụ: "raw_data", "interim_data", "reports")
    
    Returns:
        Path: Đường dẫn tuyệt đối
    """
    cfg = get_project_config()
    relative = cfg["paths"][key]
    return get_project_root() / relative


def get_prompt(prompt_type: str) -> str:
    """
    Đọc và trả về nội dung file prompt.
    
    Args:
        prompt_type: "env_filter" hoặc "classify_5"
    
    Returns:
        str: Nội dung prompt
    """
    cfg = get_project_config()
    key_map = {
        "env_filter": "prompt_env_filter",
        "classify_5": "prompt_classify_5"
    }
    if prompt_type not in key_map:
        raise ValueError(f"prompt_type phải là 'env_filter' hoặc 'classify_5', nhận được: '{prompt_type}'")
    
    prompt_path = get_project_root() / cfg["llm"][key_map[prompt_type]]
    if not prompt_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file prompt: {prompt_path}")
    
    return prompt_path.read_text(encoding="utf-8")


def clear_cache() -> None:
    """Xóa cache config (dùng khi test hoặc reload config)."""
    global _config_cache
    _config_cache = {}
