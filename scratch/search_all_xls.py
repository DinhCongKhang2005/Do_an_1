import os
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

for root, dirs, files in os.walk(PROJECT_ROOT):
    for file in files:
        if file.endswith(".xlsx") and not file.startswith("~$"):
            path = Path(root) / file
            try:
                # Read all sheets
                with pd.ExcelFile(path) as xls:
                    for sheet in xls.sheet_names:
                        df = xls.parse(sheet)
                        # Look for ImpactScore_i or something similar
                        impact_cols = [c for c in df.columns if "impact" in str(c).lower() or "score" in str(c).lower()]
                        for col in impact_cols:
                            try:
                                s = df[col].astype(float).sum()
                                if abs(s - (-362.5)) < 0.1:
                                    print(f"FOUND! File: {path.relative_to(PROJECT_ROOT)} | Sheet: {sheet} | Col: {col} | Sum: {s}")
                                elif abs(s - (-378.6875)) < 0.1:
                                    print(f"Info: {path.relative_to(PROJECT_ROOT)} | Sheet: {sheet} | Col: {col} | Sum: {s}")
                            except Exception:
                                pass
            except Exception as e:
                # print(f"Error reading {file}: {e}")
                pass
