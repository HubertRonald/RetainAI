import pandas as pd


def compute_overview_kpis(df: pd.DataFrame, target: str = "Attrition") -> dict:
    total = int(len(df))
    attrition_count = int((df[target] == "Yes").sum()) if target in df.columns else 0
    return {
        "total_employees": total,
        "attrition_count": attrition_count,
        "non_attrition_count": total - attrition_count,
        "attrition_rate": attrition_count / total if total else 0.0,
    }
