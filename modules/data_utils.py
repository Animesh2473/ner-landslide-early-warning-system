"""
data_utils.py
Loads the static location registry and generates synthetic-but-realistic
time-series data for rainfall, soil moisture and historical landslide
records. In a production deployment, `generate_sensor_timeseries` would be
replaced by live pulls from IMD APIs / IoT soil-moisture sensors / satellite
feeds, and `generate_historical_landslides` would read from a disaster
records database (e.g. NDMA / SDMA archives).
"""

import os
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
LOCATIONS_CSV = os.path.join(DATA_DIR, "locations.csv")


def load_locations() -> pd.DataFrame:
    """Load the static registry of monitored villages / roads / towns."""
    df = pd.read_csv(LOCATIONS_CSV)
    return df


def generate_sensor_timeseries(locations: pd.DataFrame, days: int = 30, seed: int = 42) -> pd.DataFrame:
    """
    Generate a daily synthetic time series of rainfall (mm), soil moisture (%)
    and temperature (C) for every location, for the last `days` days.
    Rainfall follows a monsoon-like pattern with location-specific volatility
    tied to elevation/slope; soil moisture responds to rainfall with lag/decay.
    """
    rng = np.random.default_rng(seed)
    end = pd.Timestamp.today().normalize()
    dates = pd.date_range(end=end, periods=days, freq="D")

    rows = []
    for _, loc in locations.iterrows():
        # base rainfall intensity scales gently with elevation (orographic effect)
        base_rain = 8 + (loc["elevation_m"] / 300)
        soil_moisture = 35.0  # start moderate
        for d in dates:
            seasonal = 10 * max(0, np.sin((d.dayofyear / 365) * 2 * np.pi))
            rain_today = max(0, rng.normal(base_rain + seasonal, 12))
            # occasional cloudburst event
            if rng.random() < 0.06:
                rain_today += rng.uniform(40, 120)
            # soil moisture responds to rain, decays otherwise
            soil_moisture = np.clip(
                soil_moisture * 0.85 + rain_today * 0.9 + rng.normal(0, 2), 5, 100
            )
            temp = np.clip(rng.normal(22 - loc["elevation_m"] / 250, 3), -5, 40)
            rows.append(
                {
                    "location_id": loc["id"],
                    "date": d,
                    "rainfall_mm": round(rain_today, 1),
                    "soil_moisture_pct": round(soil_moisture, 1),
                    "temperature_c": round(temp, 1),
                }
            )
    return pd.DataFrame(rows)


def generate_historical_landslides(locations: pd.DataFrame, seed: int = 7) -> pd.DataFrame:
    """
    Generate synthetic historical landslide/incident records for the past
    ~6 years, with frequency weighted by slope angle (steeper => more events).
    """
    rng = np.random.default_rng(seed)
    rows = []
    severities = ["Minor", "Moderate", "Severe", "Critical"]
    for _, loc in locations.iterrows():
        n_events = rng.poisson(lam=max(0.5, (loc["slope_angle"] - 25) / 6))
        for _ in range(int(n_events)):
            days_back = rng.integers(0, 6 * 365)
            date = pd.Timestamp.today() - pd.Timedelta(days=int(days_back))
            sev = rng.choice(severities, p=[0.45, 0.30, 0.18, 0.07])
            casualties = 0
            if sev == "Severe":
                casualties = rng.integers(0, 3)
            elif sev == "Critical":
                casualties = rng.integers(1, 10)
            damage = {"Minor": 2, "Moderate": 15, "Severe": 60, "Critical": 200}[sev] * rng.uniform(0.6, 1.6)
            rows.append(
                {
                    "location_id": loc["id"],
                    "date": date.normalize(),
                    "severity": sev,
                    "casualties": int(casualties),
                    "damage_lakh_inr": round(damage, 1),
                }
            )
    if not rows:
        return pd.DataFrame(columns=["location_id", "date", "severity", "casualties", "damage_lakh_inr"])
    return pd.DataFrame(rows).sort_values("date", ascending=False).reset_index(drop=True)


def get_latest_readings(sensor_df: pd.DataFrame) -> pd.DataFrame:
    """Return the most recent sensor reading per location."""
    return (
        sensor_df.sort_values("date")
        .groupby("location_id", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )


def rainfall_7day_sum(sensor_df: pd.DataFrame) -> pd.DataFrame:
    """Rolling 7-day rainfall sum per location, latest value."""
    out = []
    for loc_id, g in sensor_df.sort_values("date").groupby("location_id"):
        last7 = g.tail(7)["rainfall_mm"].sum()
        out.append({"location_id": loc_id, "rainfall_7day_mm": round(last7, 1)})
    return pd.DataFrame(out)


def historical_incident_counts(hist_df: pd.DataFrame) -> pd.DataFrame:
    """Count of historical incidents per location (all locations included, 0 if none)."""
    if hist_df.empty:
        return pd.DataFrame(columns=["location_id", "historical_incident_count"])
    counts = hist_df.groupby("location_id").size().reset_index(name="historical_incident_count")
    return counts
