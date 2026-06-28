import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

for root, dirs, files in os.walk(PROJECT_ROOT):
    for file in files:
        if file.endswith((".md", ".txt", ".csv", ".json", ".xlsx")):
            path = Path(root) / file
            if "compare_scores.py" in file or "search_number.py" in file or "bao_cao_ket_qua_tinh_diem.md" in file or "walkthrough.md" in file or "analysis_results.md" in file:
                continue
            try:
                if file.endswith(".xlsx"):
                    import pandas as pd
                    with pd.ExcelFile(path) as xls:
                        for sheet in xls.sheet_names:
                            df = xls.parse(sheet)
                            for col in df.columns:
                                try:
                                    # check if -362.5 is in cells
                                    if df[col].astype(str).str.contains("362\\.5").any():
                                        print(f"Excel match: {path.relative_to(PROJECT_ROOT)} | Sheet: {sheet} | Col: {col}")
                                except Exception:
                                    pass
                else:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "362.5" in content:
                            print(f"Text match: {path.relative_to(PROJECT_ROOT)}")
            except Exception as e:
                # print(f"Error reading {file}: {e}")
                pass
