import os
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

for root, dirs, files in os.walk(PROJECT_ROOT):
    for file in files:
        if file.endswith(".xlsx") and not file.startswith("~$"):
            path = Path(root) / file
            try:
                with pd.ExcelFile(path) as xls:
                    for sheet in xls.sheet_names:
                        df = xls.parse(sheet)
                        if "source_id" in df.columns:
                            row = df[df["source_id"] == "1.27.2.0"]
                            if not row.empty:
                                score_cols = [c for c in ["M_i", "S_i", "D_i", "R_i", "W_i"] if c in df.columns]
                                scores = row[score_cols].iloc[0].to_dict() if score_cols else {}
                                print(f"File: {path.relative_to(PROJECT_ROOT)} | Sheet: {sheet} | Scores: {scores}")
            except Exception as e:
                pass
