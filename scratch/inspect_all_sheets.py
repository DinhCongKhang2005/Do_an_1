import pandas as pd
from pathlib import Path
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent

for name in ["scoring_input_1.xlsx", "scoring_input_2.xlsx", "scoring_input_3.xlsx"]:
    path = PROJECT_ROOT / "data" / "interim" / name
    if path.exists():
        with pd.ExcelFile(path) as xls:
            print(f"\nFile: {name} | Sheets: {xls.sheet_names}")
            for sheet in xls.sheet_names:
                df = xls.parse(sheet)
                print(f"  Sheet: {sheet} | Shape: {df.shape}")
                # Check non-null values in score columns
                score_cols = [c for c in ["M_i", "S_i", "D_i", "R_i", "W_i"] if c in df.columns]
                if score_cols:
                    print(f"    Score columns non-null count:\n{df[score_cols].notna().sum().to_string()}")
                    # Let's compute sum of impact if they are fully populated
                    if df[score_cols].notna().sum().min() == len(df):
                        # Calculate impact
                        dir_map = {"BENEFIT_QUALITATIVE": 1, "BENEFIT_QUANTITATIVE": 1, "COST_QUALITATIVE": -1, "COST_QUANTITATIVE": -1, "CONSTRAINT": -1}
                        if "final_label" in df.columns:
                            dir_vals = df["final_label"].map(dir_map).fillna(-1)
                            C = 0.25 * df["M_i"].astype(float) + 0.25 * df["S_i"].astype(float) + 0.25 * df["D_i"].astype(float) + 0.25 * df["R_i"].astype(float)
                            C_norm = (C - 1) / 4
                            C_norm = C_norm.clip(0.0, 1.0)
                            w_vals = df["W_i"].astype(float).fillna(1.0)
                            impact = dir_vals * w_vals * C_norm
                            print(f"    Calculated Total Impact: {impact.sum():.4f}")
    else:
        print(f"\nFile {name} does not exist")
