import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

paths = [
    PROJECT_ROOT / "data" / "processed" / "scored_dataset.xlsx",
    PROJECT_ROOT / "data" / "processed" / "old" / "scored_dataset.xlsx",
]

for p in paths:
    if p.exists():
        df = pd.read_excel(p)
        print(f"File: {p.relative_to(PROJECT_ROOT)}")
        print("  Shape:", df.shape)
        if "ImpactScore_i" in df.columns:
            print("  TotalImpact:", df["ImpactScore_i"].sum())
            print("  MeanImpact:", df["ImpactScore_i"].mean())
        else:
            print("  ImpactScore_i not in columns!")
    else:
        print(f"File {p} does not exist")
