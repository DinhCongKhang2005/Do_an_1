import os
import pandas as pd
from pathlib import Path

APP_DATA_DIR = Path(r"C:\Users\ADMIN\.gemini\antigravity\brain")

for root, dirs, files in os.walk(APP_DATA_DIR):
    for file in files:
        if file.endswith(".xlsx") and not file.startswith("~$"):
            path = Path(root) / file
            try:
                with pd.ExcelFile(path) as xls:
                    for sheet in xls.sheet_names:
                        df = xls.parse(sheet)
                        for col in df.columns:
                            try:
                                s = df[col].astype(float).sum()
                                if abs(s - (-362.5)) < 0.1:
                                    print(f"FOUND! File: {path} | Sheet: {sheet} | Col: {col} | Sum: {s}")
                            except Exception:
                                pass
            except Exception as e:
                pass
print("App data scan completed.")
