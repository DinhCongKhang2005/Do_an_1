import pandas as pd
from pathlib import Path
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent

si_ol_path = PROJECT_ROOT / "data" / "interim" / "_archive" / "scoring_input_ol.xlsx"
si_std_path = PROJECT_ROOT / "data" / "interim" / "scoring_input_standardized_hethong.xlsx"

for name, path in [("scoring_input_ol", si_ol_path), ("scoring_input_standardized_hethong", si_std_path)]:
    if path.exists():
        with pd.ExcelFile(path) as xls:
            sheet = "scoring_input" if "scoring_input" in xls.sheet_names else xls.sheet_names[0]
            df = xls.parse(sheet)
        print(f"\n=========================================")
        print(f"File: {name} (shape: {df.shape})")
        print(f"=========================================")
        
        # Check 'chu_the' distribution
        if "chu_the" in df.columns:
            print("Distribution of 'chu_the':")
            print(df["chu_the"].value_counts().to_string())
            
        # Check 'actor' distribution
        if "actor" in df.columns:
            print("Distribution of 'actor':")
            print(df["actor"].value_counts().to_string())
            
        # Check 'domain' distribution
        if "domain" in df.columns:
            print("Distribution of 'domain' (top 5):")
            print(df["domain"].value_counts().head(5).to_string())
            
        # Check 'final_label' distribution
        if "final_label" in df.columns:
            print("Distribution of 'final_label':")
            print(df["final_label"].value_counts().to_string())
