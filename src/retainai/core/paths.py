from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

CONFIG_DIR = PROJECT_ROOT / "configs"
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
FIGS_DIR = PROJECT_ROOT / "figs"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
TRAIN_DATA_DIR = DATA_DIR / "train"
VALIDATION_DATA_DIR = DATA_DIR / "validation"
TEST_DATA_DIR = DATA_DIR / "test"
PREDICTION_INPUT_DIR = DATA_DIR / "prediction_input"

SCHEMA_DIR = CONFIG_DIR / "schema"

IBM_HR_DATASET_DIR = RAW_DATA_DIR / "ibm_hr_attrition"
IBM_HR_DATASET_FILE = IBM_HR_DATASET_DIR / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
IBM_HR_SCHEMA_FILE = SCHEMA_DIR / "ibm_hr_attrition.yaml"

IBM_HR_PROCESSED_FILE = PROCESSED_DATA_DIR / "ibm_hr_attrition_processed.csv"
IBM_HR_TRAIN_FILE = TRAIN_DATA_DIR / "ibm_hr_attrition_train.csv"
IBM_HR_VALIDATION_FILE = VALIDATION_DATA_DIR / "ibm_hr_attrition_validation.csv"
IBM_HR_TEST_FILE = TEST_DATA_DIR / "ibm_hr_attrition_test.csv"


def ensure_data_directories() -> None:
    for directory in [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        TRAIN_DATA_DIR,
        VALIDATION_DATA_DIR,
        TEST_DATA_DIR,
        PREDICTION_INPUT_DIR,
        IBM_HR_DATASET_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
