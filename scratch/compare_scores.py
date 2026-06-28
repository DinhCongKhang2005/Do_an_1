import pandas as pd
from pathlib import Path
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent

si_active_path = PROJECT_ROOT / "data" / "interim" / "scoring_input.xlsx"
si_ol_path = PROJECT_ROOT / "data" / "interim" / "_archive" / "scoring_input_ol.xlsx"
si_std_path = PROJECT_ROOT / "data" / "interim" / "scoring_input_standardized_hethong.xlsx"

df_active = pd.read_excel(si_active_path, sheet_name="scoring_template")
print("Active shape:", df_active.shape)

for name, path in [("scoring_input_ol", si_ol_path), ("scoring_input_standardized_hethong", si_std_path)]:
    if path.exists():
        with pd.ExcelFile(path) as xls:
            print(f"\n{name} sheet names: {xls.sheet_names}")
            sheet = "scoring_template" if "scoring_template" in xls.sheet_names else xls.sheet_names[0]
            df_other = xls.parse(sheet)
        print(f"=========================================")
        print(f"Comparing with {name} (sheet: {sheet}, shape: {df_other.shape})")
        print(f"=========================================")
        
        # Check available columns
        print("Available columns in other:", df_other.columns.tolist())
        
        # Identify common columns to compare
        common_cols = ["source_id"]
        for c in ["M_i", "S_i", "D_i", "R_i", "actor_group", "domain_primary", "final_label"]:
            if c in df_other.columns:
                common_cols.append(c)
                
        print("Common columns being compared:", common_cols)
        
        merged = pd.merge(
            df_active[["source_id", "M_i", "S_i", "D_i", "R_i", "actor_group", "domain_primary", "final_label"]],
            df_other[common_cols],
            on="source_id",
            suffixes=("_active", "_other")
        )
        
        score_cols_to_check = [c for c in ["M_i", "S_i", "D_i", "R_i"] if c in df_other.columns]
        if score_cols_to_check:
            diff_conditions = []
            for c in score_cols_to_check:
                diff_conditions.append(merged[f"{c}_active"] != merged[f"{c}_other"])
            
            # Combine conditions with OR
            any_diff_score = diff_conditions[0]
            for cond in diff_conditions[1:]:
                any_diff_score = any_diff_score | cond
                
            diff_scores = merged[any_diff_score]
            print(f"Number of rows with different scores {score_cols_to_check}: {len(diff_scores)}")
        else:
            print("No score columns to check.")
            
        if "actor_group" in df_other.columns:
            diff_actors = merged[merged["actor_group_active"] != merged["actor_group_other"]]
            print(f"Number of rows with different actor_group: {len(diff_actors)}")
        else:
            print("actor_group not present in other file.")
            
        if "domain_primary" in df_other.columns:
            diff_domains = merged[merged["domain_primary_active"] != merged["domain_primary_other"]]
            print(f"Number of rows with different domain_primary: {len(diff_domains)}")
        else:
            print("domain_primary not present in other file.")
            
        if "final_label" in df_other.columns:
            diff_labels = merged[merged["final_label_active"] != merged["final_label_other"]]
            print(f"Number of rows with different final_label: {len(diff_labels)}")
        else:
            print("final_label not present in other file.")
            
        # Calculate impact
        def calc_scores(df_in, label_col, m_col, s_col, d_col, r_col, w_col):
            dir_map = {"BENEFIT_QUALITATIVE": 1, "BENEFIT_QUANTITATIVE": 1, "COST_QUALITATIVE": -1, "COST_QUANTITATIVE": -1, "CONSTRAINT": -1}
            dir_vals = df_in[label_col].map(dir_map).fillna(-1)
            
            C = 0.25 * df_in[m_col].astype(float) + 0.25 * df_in[s_col].astype(float) + 0.25 * df_in[d_col].astype(float) + 0.25 * df_in[r_col].astype(float)
            C_norm = (C - 1) / 4
            C_norm = C_norm.clip(0.0, 1.0)
            
            w_vals = df_in[w_col].astype(float).fillna(1.0)
            impact = dir_vals * w_vals * C_norm
            return impact.sum(), impact.mean()
            
        try:
            act_sum, act_mean = calc_scores(df_active, "final_label", "M_i", "S_i", "D_i", "R_i", "W_i")
            print(f"Calculated Active Total Impact: {act_sum:.4f} (Mean: {act_mean:.4f})")
            
            # Check if all required cols are in df_other to compute its impact
            if all(c in df_other.columns for c in ["final_label", "M_i", "S_i", "D_i", "R_i", "W_i"]):
                oth_sum, oth_mean = calc_scores(df_other, "final_label", "M_i", "S_i", "D_i", "R_i", "W_i")
                print(f"Calculated Other Total Impact: {oth_sum:.4f} (Mean: {oth_mean:.4f})")
            else:
                # Find if we can align with final_label/W_i from active
                df_other_aligned = pd.merge(df_other, df_active[["source_id", "final_label", "W_i"]], on="source_id")
                oth_sum, oth_mean = calc_scores(df_other_aligned, "final_label", "M_i", "S_i", "D_i", "R_i", "W_i")
                print(f"Calculated Other Aligned Total Impact: {oth_sum:.4f} (Mean: {oth_mean:.4f})")
        except Exception as e:
            print("Could not calculate impact:", str(e))
            
        if score_cols_to_check and len(diff_scores) > 0:
            print("\nSample of score differences:")
            cols_show = ["source_id"] + [f"{c}_active" for c in score_cols_to_check] + [f"{c}_other" for c in score_cols_to_check]
            print(diff_scores[cols_show].head(5).to_string())
    else:
        print(f"\n{name} path does not exist.")
