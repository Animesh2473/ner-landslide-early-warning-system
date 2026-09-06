# NER Landslide Early Warning & Monitoring Platform (Streamlit Prototype)

An AI-powered early warning and monitoring platform prototype for predicting
and tracking landslide-prone areas across India's North Eastern Region (NER).

Built to demonstrate every capability in the problem statement:
- Rainfall / soil-moisture / terrain / historical-record data fusion
- AI/ML-based risk prediction (RandomForest, 0–100 risk score + Low/Medium/High/Critical category)
- Real-time GIS dashboard with risk heatmap
- Citizen / field-official geo-tagged photo & video reporting
- Multilingual alerts (English, Hindi, Assamese, Bengali, Manipuri)
- Road connectivity status + emergency response prioritisation
- Offline / low-network mode toggle

> **Note:** All rainfall, soil-moisture and historical-incident data is
> **synthetically generated** for demo purposes (see `modules/data_utils.py`).
> The "System Architecture" tab inside the app explains exactly what to swap
> in for a real deployment (IMD APIs, satellite feeds, IoT sensors, SMS gateway).

---

## 1. Requirements

- Python 3.9 or newer
- pip

## 2. Setup

Unzip the project, then from inside the project folder:

```bash
# (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Run the app

```bash
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`) — open it
in your browser. On first load it may take a couple of seconds while the
demo dataset is generated and the ML model is trained (both are cached).

## 4. Using the app

The sidebar lets you:
- Switch the **UI/alert language** (English, Hindi, Assamese, Bengali, Manipuri)
- Toggle **Offline / Low-Network Mode** (simulates showing last-synced cached data)
- Click **"Simulate live data refresh"** to regenerate a new synthetic data snapshot (simulates a live sensor/rainfall update)
- Navigate between the seven pages:

| Page | What it shows |
|---|---|
| **Overview** | Key stats and state-wise risk summary |
| **GIS Risk Dashboard** | Interactive map with risk heatmap + colored markers, filters by state/risk, ranked location table |
| **Sensor Monitoring** | Per-location rainfall & soil-moisture trends, latest readings across all locations, historical incident log |
| **Field Reporting** | Form for citizens/officials to submit geo-tagged photo/video reports of cracks, slope movement, blocked roads |
| **Alerts & Notifications** | Auto-generated multilingual alert messages for high-risk zones, with a "send" simulation and dispatch log |
| **Road Connectivity Status** | Road-by-road status (Open/Restricted/Blocked) and emergency-response priority ranking |
| **System Architecture** | Production architecture, and what's real vs. simulated in this prototype |

## 5. Project structure

```
ner-landslide-ews/
├── app.py                     # Main Streamlit app (page routing + UI)
├── modules/
│   ├── data_utils.py          # Location registry + synthetic sensor/historical data generation
│   ├── ml_model.py            # RandomForest training + risk prediction
│   ├── alerts.py              # Multilingual UI text + alert message templates
│   └── gis_utils.py           # pydeck map layer builders, risk color coding
├── data/
│   └── locations.csv          # 18 seed locations (villages/roads/towns) across all 8 NER states
├── uploads/                    # Citizen/field-reported photos & videos are saved here at runtime
├── .streamlit/config.toml      # App theme
├── requirements.txt
└── README.md
```

## 6. Extending this into a production system

See the in-app **"System Architecture"** page for the full breakdown. In short:

1. Replace `data_utils.generate_sensor_timeseries` with live pulls from the
   **IMD Weather API**, IoT rain-gauge/soil-moisture sensors, and satellite
   soil-moisture products (e.g. NASA SMAP).
2. Replace `data_utils.generate_historical_landslides` with a real historical
   landslide inventory (e.g. GSI's Bhukosh / NRSC Landslide Atlas / SDMA records).
3. Retrain `ml_model.py`'s RandomForest (or an ensemble incl. rainfall-threshold
   physical models) on that real, labelled data, and validate with domain experts.
4. Wire the "Send SMS/app alert" button in `app.py` to a real SMS gateway /
   push-notification / Cell Broadcast service instead of the in-session log.
5. For true offline support on mobile, wrap the field-reporting form in a PWA
   or native app with local SQLite storage and background sync — the current
   toggle only simulates the *view* of offline/cached data.
