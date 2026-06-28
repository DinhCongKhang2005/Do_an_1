"""
src/00_common/label_utils.py
============================
Tiện ích kiểm tra và xử lý nhãn phân loại.

Lý do:
    - Validate nhãn trước khi tính metric để tránh lỗi "UNKNOWN label" lọt vào báo cáo
    - Normalize nhãn (strip whitespace, uppercase) để tránh lỗi do LLM trả về nhãn không chuẩn
    - Map nhãn sang direction (+1/-1) dùng chung giữa script 08 và 11
"""

from typing import Optional

from .config_loader import get_impact_direction, get_valid_labels

# Nhãn hợp lệ cho Tầng 1 (env filtering)
ENV_VALID_VALUES = {0, 1, True, False, "0", "1", "true", "false", "True", "False"}

# Nhãn hợp lệ cho Tầng 2 (5-label)
LABEL_5_VALID = None  # Lazy load từ config


def get_valid_5_labels() -> list:
    """Trả về danh sách 5 nhãn hợp lệ từ config."""
    global LABEL_5_VALID
    if LABEL_5_VALID is None:
        LABEL_5_VALID = get_valid_labels()
    return LABEL_5_VALID


# =============================================================================
# Normalize nhãn
# =============================================================================

def normalize_env_label(value) -> Optional[int]:
    """
    Chuẩn hóa giá trị env_human hoặc env_llm thành 0 hoặc 1.
    
    Args:
        value: Giá trị gốc (bool, int, str)
    
    Returns:
        int: 0 hoặc 1
        None: Nếu không hợp lệ
    
    Examples:
        >>> normalize_env_label(True) → 1
        >>> normalize_env_label("1") → 1
        >>> normalize_env_label("false") → 0
        >>> normalize_env_label("XYZ") → None
    """
    if value is None or (isinstance(value, float) and str(value) == "nan"):
        return None
    s = str(value).strip().lower()
    if s in ("1", "true"):
        return 1
    elif s in ("0", "false"):
        return 0
    else:
        return None


def normalize_5label(value) -> Optional[str]:
    """
    Chuẩn hóa nhãn 5 lớp: strip whitespace, uppercase, kiểm tra hợp lệ.
    
    Args:
        value: Nhãn gốc từ LLM hoặc human
    
    Returns:
        str: Nhãn chuẩn hóa nếu hợp lệ
        None: Nếu không hợp lệ
    
    Examples:
        >>> normalize_5label("benefit_quantitative") → "BENEFIT_QUANTITATIVE"
        >>> normalize_5label("  CONSTRAINT  ") → "CONSTRAINT"
        >>> normalize_5label("BQ") → None  (viết tắt không được chấp nhận trong label cột)
    """
    if value is None or (isinstance(value, float) and str(value) == "nan"):
        return None
    
    normalized = str(value).strip().upper()
    
    valid = get_valid_5_labels()
    if normalized in valid:
        return normalized
    
    # Thử map từ viết tắt (dùng cho LLM output không chuẩn)
    alias_map = {
        "BQ": "BENEFIT_QUANTITATIVE",
        "BQL": "BENEFIT_QUALITATIVE",
        "CQ": "COST_QUANTITATIVE",
        "CQL": "COST_QUALITATIVE",
        "CON": "CONSTRAINT",
        "CONSTRAINT": "CONSTRAINT",
    }
    if normalized in alias_map:
        return alias_map[normalized]
    
    return None


# =============================================================================
# Kiểm tra tính hợp lệ
# =============================================================================

def is_valid_env_label(value) -> bool:
    """Kiểm tra một giá trị có phải nhãn env hợp lệ không."""
    return normalize_env_label(value) is not None


def is_valid_5label(value) -> bool:
    """Kiểm tra một giá trị có phải nhãn 5-class hợp lệ không."""
    return normalize_5label(value) is not None


# =============================================================================
# Map nhãn → direction
# =============================================================================

def get_direction(label: str) -> Optional[int]:
    """
    Trả về hướng tác động (+1 hoặc -1) cho nhãn 5-class.
    
    Args:
        label: Nhãn đầy đủ hoặc viết tắt
    
    Returns:
        int: +1 hoặc -1
        None: Nếu nhãn không hợp lệ
    """
    normalized = normalize_5label(label)
    if normalized is None:
        return None
    try:
        return get_impact_direction(normalized)
    except KeyError:
        return None


# =============================================================================
# Thống kê nhãn
# =============================================================================

def count_invalid_labels(series, label_type: str = "5label") -> dict:
    """
    Đếm số giá trị không hợp lệ trong một Series.
    
    Args:
        series: pd.Series chứa nhãn
        label_type: "env" hoặc "5label"
    
    Returns:
        dict: {"total": int, "invalid": int, "invalid_values": list}
    """
    validator = is_valid_env_label if label_type == "env" else is_valid_5label
    invalid_mask = series.apply(lambda x: not validator(x))
    invalid_values = series[invalid_mask].unique().tolist()
    
    return {
        "total": len(series),
        "invalid": int(invalid_mask.sum()),
        "invalid_rate": float(invalid_mask.mean()),
        "invalid_values": invalid_values
    }
