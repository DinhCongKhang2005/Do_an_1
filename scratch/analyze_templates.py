import pandas as pd
from pathlib import Path
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load the active scored dataset
scored_active_path = PROJECT_ROOT / "data" / "processed" / "scored_dataset.xlsx"
df_active = pd.read_excel(scored_active_path)

# Let's check other actor domain datasets
paths = {
    "actor_domain_dataset (active)": PROJECT_ROOT / "data" / "processed" / "actor_domain_dataset.xlsx",
    "actor_domain_dataset_1": PROJECT_ROOT / "data" / "processed" / "actor_domain_dataset_1.xlsx",
    "actor_domain_dataset_2": PROJECT_ROOT / "data" / "processed" / "actor_domain_dataset_2.xlsx",
    "actor_domain_dataset_old": PROJECT_ROOT / "data" / "processed" / "old" / "actor_domain_dataset_old.xlsx",
}

for name, p in paths.items():
    if p.exists():
        df = pd.read_excel(p)
        print(f"\n=========================================")
        print(f"Dataset: {name} (shape: {df.shape})")
        print(f"=========================================")
        
        # Count actor_group
        if "actor_group" in df.columns:
            print("Actor group distribution:")
            print(df["actor_group"].value_counts().to_string())
        else:
            print("actor_group not in columns!")
            
        # Count domain_primary
        if "domain_primary" in df.columns:
            print("\nDomain primary distribution (top 5):")
            print(df["domain_primary"].value_counts().head(5).to_string())
            
        # If we calculate impact score with this dataset's actor/domain and the active scores,
        # does it change the total impact?
        # Note: the impact score only depends on final_label, M_i, S_i, D_i, R_i, W_i.
        # It does NOT depend on actor_group or domain_primary directly!
        # Wait, if TotalImpact is different, it means the row-by-row scores or final_labels must be different!
        # Let's check if final_labels or scores differ.
    else:
        print(f"\nDataset {name} does not exist")
