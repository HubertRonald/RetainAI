from __future__ import annotations

from modules.dashboard.prediction_input import (
    build_prediction_input,
    save_prediction_sample,
)
from modules.io.storage import load_dataframe
from retainai.core.paths import PROJECT_ROOT


def main() -> None:
    df = load_dataframe(PROJECT_ROOT / "data/test/ibm_hr_attrition_test.csv")
    sample = build_prediction_input(df)
    save_prediction_sample(
        sample,
        PROJECT_ROOT / "data/prediction_input/ibm_hr_attrition_prediction_sample.csv",
        PROJECT_ROOT / "data/prediction_input/ibm_hr_attrition_prediction_sample.xlsx",
    )
    print("Prediction samples generated.")


if __name__ == "__main__":
    main()
