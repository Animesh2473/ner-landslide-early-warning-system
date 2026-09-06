"""
ml_model.py
Trains a RandomForest classifier on synthetically generated landslide-risk
training data (features: 7-day rainfall, soil moisture, slope angle,
elevation, historical incident count) and exposes a predict_risk() helper
that returns a 0-100 risk score plus a Low/Medium/High/Critical category.

NOTE: This is a demonstration model. In production it should be trained on
real historical landslide inventories (e.g. Bhukosh/GSI, NRSC Landslide
Atlas) combined with live IMD rainfall + satellite soil-moisture (SMAP)
data, and validated with domain experts before operational use.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

FEATURE_COLS = [
    "rainfall_7day_mm",
    "soil_moisture_pct",
    "slope_angle",
    "elevation_m",
    "historical_incident_count",
]

CATEGORIES = ["Low", "Medium", "High", "Critical"]


def _synthetic_risk_label(row, rng) -> str:
    """
    Ground-truth rule used only to LABEL synthetic training examples
    (a stand-in for real labelled historical outcomes). The RandomForest
    then learns a generalizable, noisy, non-linear approximation of this
    relationship rather than just replaying the rule.
    """
    score = (
        0.035 * row["rainfall_7day_mm"]
        + 0.55 * row["soil_moisture_pct"]
        + 1.1 * row["slope_angle"]
        + 0.01 * row["elevation_m"]
        + 4.0 * row["historical_incident_count"]
    )
    score += rng.normal(0, 12)  # noise so it isn't a perfect rule
    if score < 55:
        return "Low"
    elif score < 85:
        return "Medium"
    elif score < 115:
        return "High"
    else:
        return "Critical"


def build_training_data(n: int = 1200, seed: int = 123) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "rainfall_7day_mm": rng.uniform(0, 400, n),
            "soil_moisture_pct": rng.uniform(5, 100, n),
            "slope_angle": rng.uniform(10, 55, n),
            "elevation_m": rng.uniform(30, 2200, n),
            "historical_incident_count": rng.poisson(1.2, n),
        }
    )
    df["risk_category"] = df.apply(lambda r: _synthetic_risk_label(r, rng), axis=1)
    return df


def train_model(seed: int = 123):
    train_df = build_training_data(seed=seed)
    X = train_df[FEATURE_COLS]
    y = train_df["risk_category"]
    model = RandomForestClassifier(
        n_estimators=200, max_depth=8, random_state=seed, class_weight="balanced"
    )
    model.fit(X, y)
    return model


def predict_risk(model, features_df: pd.DataFrame) -> pd.DataFrame:
    """
    features_df must contain FEATURE_COLS. Returns the input df with
    added columns: risk_score (0-100), risk_category.
    """
    X = features_df[FEATURE_COLS]
    proba = model.predict_proba(X)
    class_order = list(model.classes_)
    # risk_score = weighted severity index scaled 0-100
    severity_weight = {"Low": 0, "Medium": 40, "High": 70, "Critical": 100}
    weights = np.array([severity_weight[c] for c in class_order])
    risk_score = (proba * weights).sum(axis=1)
    pred_idx = proba.argmax(axis=1)
    pred_cat = [class_order[i] for i in pred_idx]

    out = features_df.copy().reset_index(drop=True)
    out["risk_score"] = np.round(risk_score, 1)
    out["risk_category"] = pred_cat
    return out
