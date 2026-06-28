import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

new_path = PROJECT_ROOT / "data" / "interim" / "scoring_input.xlsx"
backup_path = PROJECT_ROOT / "data" / "interim" / "scoring_input_backup.xlsx"

print("Reading new template sheets into memory...")
sheets_new = {}
with pd.ExcelFile(new_path) as xls_new:
    for sheet_name in xls_new.sheet_names:
        sheets_new[sheet_name] = xls_new.parse(sheet_name)

print("Reading backup into memory...")
with pd.ExcelFile(backup_path) as xls_backup:
    df_backup = xls_backup.parse("scoring_template")

df_new = sheets_new["scoring_template"]

# Create a mapping from source_id to scores in backup
backup_cols = ["source_id", "M_i", "S_i", "D_i", "R_i", "W_i", "scoring_note"]
df_backup_subset = df_backup[backup_cols].copy()

# Drop the columns from df_new first so we can merge them
df_new_cleaned = df_new.drop(columns=["M_i", "S_i", "D_i", "R_i", "W_i", "scoring_note"], errors="ignore")

# Merge
df_merged = pd.merge(df_new_cleaned, df_backup_subset, on="source_id", how="left")

# Print verification stats
print("Merged shape:", df_merged.shape)
print("Non-null scores:")
print(df_merged[["M_i", "S_i", "D_i", "R_i", "W_i"]].notna().sum())

# Replace in our sheets dictionary
sheets_new["scoring_template"] = df_merged

# Write back to new_path
print("Writing back to Excel...")
with pd.ExcelWriter(new_path, engine="openpyxl") as writer:
    for sheet_name, df_sheet in sheets_new.items():
        df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

print("Scoring restoration completed successfully!")
