"""
src/00_common/io_utils.py
========================
Tiện ích đọc/ghi file dùng chung cho toàn pipeline DTM.

Lý do tách ra module riêng:
    - DRY principle: tránh lặp code đọc/ghi Excel/JSON ở mỗi script
    - Xử lý lỗi nhất quán (file không tồn tại, thư mục chưa tạo)
    - Dễ thay đổi thư viện (openpyxl → xlsxwriter) mà không sửa toàn bộ scripts
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


# =============================================================================
# Phát hiện project root (thư mục chứa config/)
# =============================================================================

def get_project_root() -> Path:
    """
    Trả về đường dẫn tuyệt đối đến project root (thư mục DTM/).
    
    Quy ước: project root là thư mục cha của src/.
    Nếu script được chạy từ bất kỳ đâu, hàm này vẫn tìm đúng root.
    """
    # __file__ là đường dẫn đến io_utils.py → cha là 00_common/ → cha nữa là src/ → cha nữa là root
    return Path(__file__).resolve().parent.parent.parent


# =============================================================================
# Đọc file JSON
# =============================================================================

def load_json(filepath: str | Path) -> List[Dict]:
    """
    Đọc file JSON và trả về list of dicts.
    
    Args:
        filepath: Đường dẫn đến file JSON (tuyệt đối hoặc tương đối so với project root)
    
    Returns:
        List[Dict]: Danh sách bản ghi
    
    Raises:
        FileNotFoundError: Nếu file không tồn tại
        json.JSONDecodeError: Nếu file không phải JSON hợp lệ
    """
    filepath = Path(filepath)
    if not filepath.is_absolute():
        filepath = get_project_root() / filepath
    
    if not filepath.exists():
        raise FileNotFoundError(f"Không tìm thấy file JSON: {filepath}")
    
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    
    # Hỗ trợ cả dạng list và dạng {records: [...]}
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "records" in data:
        return data["records"]
    else:
        return [data]


# =============================================================================
# Đọc file Excel
# =============================================================================

def load_excel(filepath: str | Path, sheet_name: str | int = 0) -> pd.DataFrame:
    """
    Đọc file Excel và trả về DataFrame.
    
    Args:
        filepath: Đường dẫn đến file Excel
        sheet_name: Tên hoặc index của sheet (mặc định: sheet đầu tiên)
    
    Returns:
        pd.DataFrame
    
    Raises:
        FileNotFoundError: Nếu file không tồn tại
    """
    filepath = Path(filepath)
    if not filepath.is_absolute():
        filepath = get_project_root() / filepath
    
    if not filepath.exists():
        raise FileNotFoundError(f"Không tìm thấy file Excel: {filepath}")
    
    df = pd.read_excel(filepath, sheet_name=sheet_name, dtype=str)
    # Loại bỏ khoảng trắng thừa trong tên cột
    df.columns = [str(c).strip() for c in df.columns]
    return df


# =============================================================================
# Ghi file Excel
# =============================================================================

def save_excel(
    df: pd.DataFrame,
    filepath: str | Path,
    sheet_name: str = "Sheet1",
    index: bool = False,
    overwrite: bool = True
) -> Path:
    """
    Ghi DataFrame ra file Excel. Tự động tạo thư mục nếu chưa tồn tại.
    
    Args:
        df: DataFrame cần ghi
        filepath: Đường dẫn đầu ra
        sheet_name: Tên sheet (mặc định: "Sheet1")
        index: Có ghi index vào file không (mặc định: False)
        overwrite: Có ghi đè nếu file đã tồn tại không (mặc định: True)
    
    Returns:
        Path: Đường dẫn tuyệt đối đến file đã ghi
    
    Raises:
        FileExistsError: Nếu overwrite=False và file đã tồn tại
    """
    filepath = Path(filepath)
    if not filepath.is_absolute():
        filepath = get_project_root() / filepath
    
    # Tạo thư mục nếu chưa tồn tại
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if not overwrite and filepath.exists():
        raise FileExistsError(f"File đã tồn tại: {filepath}. Dùng overwrite=True để ghi đè.")
    
    df.to_excel(filepath, sheet_name=sheet_name, index=index)
    print(f"  ✅ Đã lưu: {filepath.relative_to(get_project_root())} ({len(df):,} dòng)")
    return filepath


def save_excel_multisheet(
    sheets: Dict[str, pd.DataFrame],
    filepath: str | Path,
    index: bool = False
) -> Path:
    """
    Ghi nhiều DataFrame vào một file Excel với nhiều sheet.
    
    Args:
        sheets: Dict mapping tên sheet → DataFrame
        filepath: Đường dẫn đầu ra
        index: Có ghi index không
    
    Returns:
        Path: Đường dẫn tuyệt đối
    """
    filepath = Path(filepath)
    if not filepath.is_absolute():
        filepath = get_project_root() / filepath
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=index)  # Excel giới hạn 31 ký tự tên sheet
    
    print(f"  ✅ Đã lưu multisheet: {filepath.relative_to(get_project_root())} ({len(sheets)} sheets)")
    return filepath


# =============================================================================
# Kiểm tra và tạo thư mục
# =============================================================================

def ensure_dir(dirpath: str | Path) -> Path:
    """
    Đảm bảo thư mục tồn tại, tạo nếu chưa có.
    
    Args:
        dirpath: Đường dẫn thư mục
    
    Returns:
        Path: Đường dẫn tuyệt đối đến thư mục
    """
    dirpath = Path(dirpath)
    if not dirpath.is_absolute():
        dirpath = get_project_root() / dirpath
    dirpath.mkdir(parents=True, exist_ok=True)
    return dirpath


# =============================================================================
# Kiểm tra tính hợp lệ cơ bản
# =============================================================================

def validate_required_columns(df: pd.DataFrame, required_cols: List[str], context: str = "") -> None:
    """
    Kiểm tra DataFrame có đủ các cột bắt buộc không.
    
    Args:
        df: DataFrame cần kiểm tra
        required_cols: Danh sách tên cột bắt buộc
        context: Tên script/bước để thông báo lỗi rõ hơn
    
    Raises:
        ValueError: Nếu thiếu cột
    """
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        ctx = f"[{context}] " if context else ""
        raise ValueError(f"{ctx}Thiếu các cột bắt buộc: {missing}\nCột hiện có: {list(df.columns)}")


def print_section(title: str, char: str = "=", width: int = 60) -> None:
    """In header section cho log output."""
    print(f"\n{char * width}")
    print(f"  {title}")
    print(f"{char * width}")


def print_step(step_num: int, description: str) -> None:
    """In tên bước đang thực hiện."""
    print(f"\n[Bước {step_num}] {description}")
