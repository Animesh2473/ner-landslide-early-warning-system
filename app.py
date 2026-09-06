"""
NER Landslide Early Warning & Monitoring Platform
--------------------------------------------------
A Streamlit prototype demonstrating an AI-powered real-time monitoring and
early-warning system for landslide-prone zones across India's North Eastern
Region (NER), built for the problem statement on climate-resilient disaster
management.

Run with:  streamlit run app.py

All sensor/rainfall/historical data in this prototype is SYNTHETICALLY
GENERATED for demonstration purposes (see modules/data_utils.py). Wiring
this to real IMD rainfall APIs, satellite (SMAP) soil-moisture feeds, and
IoT ground sensors is described in the "System Architecture" tab.
"""

import io
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from modules import data_utils, ml_model, alerts, gis_utils

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="NER Landslide Early Warning Platform",
    page_icon="⛰️",
    layout="wide",
)

# --------------------------------------------------------------------------
# Cached loaders
# --------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_all_data(seed: int):
    locations = data_utils.load_locations()
    sensor_df = data_utils.generate_sensor_timeseries(locations, days=30, seed=seed)
    hist_df = data_utils.generate_historical_landslides(locations, seed=seed + 1)
    return locations, sensor_df, hist_df


@st.cache_resource(show_spinner=False)
def load_model():
    return ml_model.train_model()


def compute_current_risk(locations, sensor_df, hist_df, model):
    latest = data_utils.get_latest_readings(sensor_df)
    rain7 = data_utils.rainfall_7day_sum(sensor_df)
    incident_counts = data_utils.historical_incident_counts(hist_df)

    feat = locations.merge(latest[["location_id", "soil_moisture_pct"]], left_on="id", right_on="location_id")
    feat = feat.merge(rain7, on="location_id", how="left")
    feat = feat.merge(incident_counts, on="location_id", how="left")
    feat["historical_incident_count"] = feat["historical_incident_count"].fillna(0)
    feat["rainfall_7day_mm"] = feat["rainfall_7day_mm"].fillna(0)

    pred = ml_model.predict_risk(model, feat)
    return pred


# --------------------------------------------------------------------------
# Session state defaults
# --------------------------------------------------------------------------
if "data_seed" not in st.session_state:
    st.session_state.data_seed = 42
if "field_reports" not in st.session_state:
    st.session_state.field_reports = []
if "alert_log" not in st.session_state:
    st.session_state.alert_log = []
if "last_sync" not in st.session_state:
    st.session_state.last_sync = datetime.now()

# --------------------------------------------------------------------------
# Sidebar: language, offline mode, navigation
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⛰️ NER-EWS")
    language = st.selectbox(
        "🌐 Language / भाषा / ভাষা",
        ["English", "Hindi", "Assamese", "Bengali", "Manipuri"],
        index=0,
    )
    offline_mode = st.toggle(alerts.t(language, "offline_mode"), value=False)
    if offline_mode:
        st.warning(
            f"📴 {alerts.t(language, 'offline_mode')}\n\nLast synced: "
            f"{st.session_state.last_sync.strftime('%d %b %Y, %H:%M')}"
        )
    else:
        if st.button("🔄 Simulate live data refresh"):
            st.session_state.data_seed += 1
            st.session_state.last_sync = datetime.now()
            st.cache_data.clear()
            st.rerun()

    st.markdown("---")
    page = st.radio(
        "Navigate",
        [
            alerts.t(language, "overview"),
            alerts.t(language, "gis_dashboard"),
            alerts.t(language, "sensor_monitoring"),
            alerts.t(language, "field_reporting"),
            alerts.t(language, "alerts"),
            alerts.t(language, "road_status"),
            alerts.t(language, "about"),
        ],
    )
    st.markdown("---")
    st.caption("Prototype for SIH-style problem statement · Synthetic demo data")

# --------------------------------------------------------------------------
# Load data + model
# --------------------------------------------------------------------------
locations, sensor_df, hist_df = load_all_data(st.session_state.data_seed)
model = load_model()
risk_df = compute_current_risk(locations, sensor_df, hist_df, model)

PAGE_KEYS = {
    alerts.t(language, "overview"): "overview",
    alerts.t(language, "gis_dashboard"): "gis",
    alerts.t(language, "sensor_monitoring"): "sensor",
    alerts.t(language, "field_reporting"): "field",
    alerts.t(language, "alerts"): "alerts",
    alerts.t(language, "road_status"): "road",
    alerts.t(language, "about"): "about",
}
current_page = PAGE_KEYS[page]

st.title(f"⛰️ {alerts.t(language, 'app_title')}")

# ==========================================================================
# PAGE: OVERVIEW
# ==========================================================================
if current_page == "overview":
    st.subheader(alerts.t(language, "overview"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monitored locations", len(risk_df))
    c2.metric("High / Critical risk zones", int((risk_df["risk_category"].isin(["High", "Critical"])).sum()))
    c3.metric("Avg. risk score", f"{risk_df['risk_score'].mean():.1f} / 100")
    c4.metric("Historical incidents logged", len(hist_df))

    st.markdown(
        """
This prototype demonstrates an **AI-powered early warning and monitoring platform**
for landslide-prone zones across the North Eastern Region, covering:

- 🛰️ **Multi-source data fusion** — rainfall, soil moisture, terrain/slope, satellite imagery, historical records
- 🤖 **AI/ML risk prediction** — a RandomForest model scores each zone 0–100 and classifies Low/Medium/High/Critical risk
- 🗺️ **GIS dashboard** — real-time risk heatmap over villages, roads, and infrastructure
- 📸 **Citizen/field reporting** — geo-tagged photo/video uploads of cracks, slope movement, blocked roads
- 📢 **Multilingual alerts** — SMS/app-style early warnings in English, Hindi, Assamese, Bengali, Manipuri
- 📴 **Offline/low-network mode** — cached last-synced view for remote areas
        """
    )

    st.markdown("#### Current risk snapshot by state")
    state_summary = (
        risk_df.groupby("state")
        .agg(locations=("name", "count"), avg_risk=("risk_score", "mean"),
             high_critical=("risk_category", lambda s: s.isin(["High", "Critical"]).sum()))
        .reset_index()
        .sort_values("avg_risk", ascending=False)
    )
    state_summary["avg_risk"] = state_summary["avg_risk"].round(1)
    st.dataframe(state_summary, use_container_width=True, hide_index=True)

# ==========================================================================
# PAGE: GIS DASHBOARD
# ==========================================================================
elif current_page == "gis":
    st.subheader(alerts.t(language, "gis_dashboard"))

    fcol1, fcol2, fcol3 = st.columns(3)
    state_filter = fcol1.multiselect("Filter by state", sorted(risk_df["state"].unique()))
    risk_filter = fcol2.multiselect("Filter by risk category", ["Low", "Medium", "High", "Critical"])
    show_heatmap = fcol3.checkbox("Show heatmap layer", value=True)

    filtered = risk_df.copy()
    if state_filter:
        filtered = filtered[filtered["state"].isin(state_filter)]
    if risk_filter:
        filtered = filtered[filtered["risk_category"].isin(risk_filter)]

    if filtered.empty:
        st.info("No locations match the selected filters.")
    else:
        deck = gis_utils.build_deck(filtered, show_heatmap=show_heatmap, show_markers=True)
        st.pydeck_chart(deck, use_container_width=True)

    legend_cols = st.columns(4)
    for col, cat in zip(legend_cols, ["Low", "Medium", "High", "Critical"]):
        rgba = gis_utils.color_for(cat)
        col.markdown(
            f"<div style='display:flex;align-items:center;gap:6px'>"
            f"<div style='width:14px;height:14px;border-radius:50%;"
            f"background-color:rgba({rgba[0]},{rgba[1]},{rgba[2]},{rgba[3]/255});'></div>"
            f"<span>{cat}</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown("#### Risk-ranked locations")
    display_cols = ["name", "state", "type", "risk_category", "risk_score", "rainfall_7day_mm",
                     "soil_moisture_pct", "slope_angle", "historical_incident_count"]
    st.dataframe(
        filtered[display_cols].sort_values("risk_score", ascending=False).reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

# ==========================================================================
# PAGE: SENSOR MONITORING
# ==========================================================================
elif current_page == "sensor":
    st.subheader(alerts.t(language, "sensor_monitoring"))

    loc_names = risk_df.sort_values("risk_score", ascending=False)["name"].tolist()
    selected_name = st.selectbox("Select a location", loc_names)
    loc_row = risk_df[risk_df["name"] == selected_name].iloc[0]
    loc_id = loc_row["id"]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Risk score", f"{loc_row['risk_score']}/100", loc_row["risk_category"])
    m2.metric("7-day rainfall", f"{loc_row['rainfall_7day_mm']} mm")
    m3.metric("Soil moisture", f"{loc_row['soil_moisture_pct']} %")
    m4.metric("Slope angle", f"{loc_row['slope_angle']}°")

    loc_sensor = sensor_df[sensor_df["location_id"] == loc_id].sort_values("date")
    st.markdown("##### Rainfall (mm/day) — last 30 days")
    st.bar_chart(loc_sensor.set_index("date")["rainfall_mm"])
    st.markdown("##### Soil moisture (%) — last 30 days")
    st.line_chart(loc_sensor.set_index("date")["soil_moisture_pct"])

    st.markdown("##### Latest readings — all monitored locations")
    latest_all = data_utils.get_latest_readings(sensor_df).merge(
        locations[["id", "name", "state"]], left_on="location_id", right_on="id"
    )[["name", "state", "date", "rainfall_mm", "soil_moisture_pct", "temperature_c"]]
    st.dataframe(latest_all.sort_values("rainfall_mm", ascending=False), use_container_width=True, hide_index=True)

    with st.expander("📜 Historical landslide records for this location"):
        loc_hist = hist_df[hist_df["location_id"] == loc_id]
        if loc_hist.empty:
            st.caption("No historical incidents recorded for this location.")
        else:
            st.dataframe(loc_hist, use_container_width=True, hide_index=True)

# ==========================================================================
# PAGE: FIELD REPORTING
# ==========================================================================
elif current_page == "field":
    st.subheader(alerts.t(language, "field_reporting"))
    st.caption("Citizens and field officials can submit geo-tagged evidence of cracks, slope movement, or blocked roads.")

    with st.form("field_report_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        reporter_type = col1.selectbox("Reporter type", ["Citizen", "Field Official", "Local Authority"])
        issue_type = col2.selectbox("Issue type", ["Ground crack", "Slope movement", "Blocked road", "Damaged infrastructure", "Other"])
        near_location = st.selectbox("Nearest monitored location", locations["name"].tolist())
        c3, c4 = st.columns(2)
        lat_in = c3.number_input("Latitude (auto-filled if using mobile GPS)",
                                  value=float(locations[locations["name"] == near_location]["lat"].iloc[0]),
                                  format="%.4f")
        lon_in = c4.number_input("Longitude (auto-filled if using mobile GPS)",
                                  value=float(locations[locations["name"] == near_location]["lon"].iloc[0]),
                                  format="%.4f")
        description = st.text_area("Description", placeholder="e.g. Fresh crack ~3m long on hillside above the highway, visible after last night's rain.")
        media = st.file_uploader("Upload geo-tagged photo/video", type=["jpg", "jpeg", "png", "mp4", "mov"])
        submitted = st.form_submit_button("📤 Submit report")

        if submitted:
            filename = None
            if media is not None:
                filename = f"{int(time.time())}_{media.name}"
                with open(f"uploads/{filename}", "wb") as f:
                    f.write(media.getbuffer())
            st.session_state.field_reports.insert(0, {
                "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
                "reporter_type": reporter_type,
                "issue_type": issue_type,
                "near_location": near_location,
                "lat": lat_in,
                "lon": lon_in,
                "description": description,
                "media_file": filename,
            })
            st.success("✅ Report submitted. District administration & disaster management team notified.")

    st.markdown("#### Recent field reports")
    if not st.session_state.field_reports:
        st.caption("No field reports submitted yet.")
    else:
        for r in st.session_state.field_reports:
            with st.container(border=True):
                cA, cB = st.columns([3, 1])
                cA.markdown(
                    f"**{r['issue_type']}** near **{r['near_location']}** — reported by *{r['reporter_type']}*  \n"
                    f"🕒 {r['timestamp']} · 📍 ({r['lat']:.4f}, {r['lon']:.4f})  \n"
                    f"{r['description'] or '_No description provided_'}"
                )
                if r["media_file"]:
                    fpath = f"uploads/{r['media_file']}"
                    if r["media_file"].lower().endswith((".jpg", ".jpeg", ".png")):
                        cB.image(fpath, use_container_width=True)
                    else:
                        cB.video(fpath)

# ==========================================================================
# PAGE: ALERTS & NOTIFICATIONS
# ==========================================================================
elif current_page == "alerts":
    st.subheader(alerts.t(language, "alerts"))

    threshold = st.select_slider(
        "Minimum risk category to generate an alert",
        options=["Low", "Medium", "High", "Critical"],
        value="High",
    )
    order = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}
    to_alert = risk_df[risk_df["risk_category"].map(order) >= order[threshold]].sort_values(
        "risk_score", ascending=False
    )

    st.markdown(f"**{len(to_alert)} location(s)** meet or exceed the **{threshold}** threshold.")

    for _, row in to_alert.iterrows():
        msg = alerts.get_alert_message(language, row["name"], row["state"], row["risk_category"], row["risk_score"])
        with st.container(border=True):
            badge_color = {"Low": "green", "Medium": "orange", "High": "orange", "Critical": "red"}[row["risk_category"]]
            st.markdown(f":{badge_color}[**{row['risk_category']} — {row['risk_score']}/100**]  ·  {row['name']} ({row['state']})")
            st.write(msg)
            if st.button("📲 Send SMS / app alert now", key=f"send_{row['id']}"):
                st.session_state.alert_log.insert(0, {
                    "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
                    "location": row["name"],
                    "category": row["risk_category"],
                    "language": language,
                    "message": msg,
                })
                st.toast(f"Alert dispatched for {row['name']}", icon="📨")

    st.markdown("#### 📜 Dispatch log")
    if not st.session_state.alert_log:
        st.caption("No alerts dispatched yet in this session.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.alert_log), use_container_width=True, hide_index=True)

# ==========================================================================
# PAGE: ROAD CONNECTIVITY STATUS
# ==========================================================================
elif current_page == "road":
    st.subheader(alerts.t(language, "road_status"))

    roads = risk_df[risk_df["type"] == "road"].copy()

    def status_for(cat):
        return {"Low": "🟢 Open", "Medium": "🟡 Open — Caution", "High": "🟠 Restricted (single-lane / escort)", "Critical": "🔴 Blocked"}[cat]

    roads["status"] = roads["risk_category"].apply(status_for)
    roads["priority_rank"] = roads["risk_score"].rank(ascending=False).astype(int)

    st.dataframe(
        roads[["name", "state", "status", "risk_category", "risk_score", "priority_rank"]]
        .sort_values("priority_rank"),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### 🚨 Emergency response prioritisation")
    st.caption("Locations ranked by combined risk severity — guides where disaster response teams and resources should be pre-positioned.")
    top5 = roads.sort_values("risk_score", ascending=False).head(5)
    for i, (_, row) in enumerate(top5.iterrows(), start=1):
        st.markdown(f"**{i}. {row['name']}** ({row['state']}) — {row['status']}, risk {row['risk_score']}/100")

# ==========================================================================
# PAGE: ABOUT / SYSTEM ARCHITECTURE
# ==========================================================================
elif current_page == "about":
    st.subheader(alerts.t(language, "about"))
    st.markdown(
        """
### Proposed production architecture

| Layer | Component | Notes |
|---|---|---|
| **Data ingestion** | IMD weather API, satellite feeds (INSAT/SMAP), IoT soil-moisture & rain-gauge sensors, DEM/terrain-slope data (GSI/Bhukosh), historical landslide inventories | Scheduled + streaming ingestion via cloud pub/sub |
| **Processing** | Cloud-based ETL, feature store, model training/retraining pipeline | Auto-retrain as new incident data arrives |
| **AI/ML engine** | Ensemble models (RandomForest/XGBoost + rainfall-threshold physical models) for risk scoring | This prototype uses a RandomForest classifier trained on synthetic data as a stand-in |
| **Serving** | Risk-scoring microservice, GIS tile server, alert-dispatch service | REST/GraphQL APIs |
| **Delivery** | Web/mobile app (this dashboard), SMS gateway, IVR, Cell Broadcast, WhatsApp/app push | Multilingual templates |
| **Field data** | Citizen/field-official geo-tagged photo & video uploads | Feeds back into model retraining & ground-truthing |
| **Offline support** | Local cache + background sync (mobile), SMS fallback for zero-connectivity zones | Toggle in sidebar simulates this |

### What this prototype demonstrates vs. production gaps

- ✅ End-to-end UX across all required capabilities (a–f in the problem statement)
- ✅ Real ML model (RandomForest) producing calibrated 0–100 risk scores
- ✅ GIS heatmap + prioritisation logic + multilingual alerting
- ⚠️ Uses **synthetic** rainfall/soil-moisture/historical data — production needs live IMD/SMAP/IoT feeds
- ⚠️ SMS/app dispatch is **simulated** (logged in-session) — production needs a licensed SMS gateway / push service integration
- ⚠️ True offline-first mobile sync (SQLite/local-store + background sync) needs a native or PWA mobile client
        """
    )
