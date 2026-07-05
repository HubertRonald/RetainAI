from __future__ import annotations

import pandas as pd
import pytest


@pytest.fixture
def sample_hr_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Age": [25, 35, 45, 29, 41, 31],
            "Attrition": ["Yes", "No", "No", "Yes", "No", "No"],
            "BusinessTravel": [
                "Travel_Frequently",
                "Travel_Rarely",
                "Non-Travel",
                "Travel_Frequently",
                "Travel_Rarely",
                "Non-Travel",
            ],
            "Department": [
                "Sales",
                "Research & Development",
                "Research & Development",
                "Sales",
                "Human Resources",
                "Sales",
            ],
            "DistanceFromHome": [10, 2, 5, 12, 1, 7],
            "EmployeeCount": [1, 1, 1, 1, 1, 1],
            "EmployeeNumber": [1, 2, 3, 4, 5, 6],
            "Gender": ["Male", "Female", "Male", "Female", "Male", "Female"],
            "JobLevel": [1, 2, 3, 1, 4, 2],
            "JobRole": [
                "Sales Representative",
                "Research Scientist",
                "Manager",
                "Laboratory Technician",
                "Human Resources",
                "Sales Executive",
            ],
            "JobSatisfaction": [1, 4, 3, 2, 4, 3],
            "MonthlyIncome": [2500, 5000, 9000, 2700, 11000, 6200],
            "Over18": ["Y", "Y", "Y", "Y", "Y", "Y"],
            "OverTime": ["Yes", "No", "No", "Yes", "No", "No"],
            "StandardHours": [80, 80, 80, 80, 80, 80],
            "StockOptionLevel": [0, 1, 2, 0, 3, 1],
            "TotalWorkingYears": [2, 10, 20, 3, 22, 8],
            "YearsAtCompany": [1, 5, 12, 2, 14, 4],
            "YearsWithCurrManager": [0, 3, 7, 1, 8, 2],
        }
    )


@pytest.fixture
def minimal_schema() -> dict:
    return {
        "dataset": "synthetic_hr",
        "target": "Attrition",
        "target_values": ["Yes", "No"],
        "required_columns": ["Age", "Attrition", "OverTime", "YearsAtCompany"],
    }
