# NER Landslide Early Warning & Monitoring Platform

**An AI-powered landslide risk prediction, early warning, and monitoring platform for India's North Eastern Region (NER).**

🚀 **Live Demo:** https://ner-landslide-ews.streamlit.app/

💻 **GitHub Repository:** https://github.com/Animesh2473/ner-landslide-early-warning-system

---

## 📌 Overview

The **NER Landslide Early Warning & Monitoring Platform** is a Streamlit-based AI/ML prototype designed to demonstrate how multiple environmental, terrain, historical, and field-reporting data sources can be combined to support landslide risk assessment and emergency response across India's **North Eastern Region (NER)**.

The platform provides an interactive dashboard for monitoring risk levels, visualizing vulnerable locations, tracking sensor conditions, managing field reports, generating multilingual alerts, and prioritizing emergency response.

> **⚠️ Prototype Notice:** Rainfall, soil-moisture, and historical landslide data used in this demonstration are **synthetically generated** for prototyping purposes. The application includes a **System Architecture** section explaining how these components could be replaced with real-world data sources for production deployment.

---

## 🚀 Live Demo

### Try the deployed application

👉 **https://ner-landslide-ews.streamlit.app/**

The live application demonstrates the complete prototype, including:

* 🗺️ Interactive GIS risk dashboard
* 🤖 AI/ML-based landslide risk prediction
* 🌧️ Rainfall and soil-moisture monitoring
* 📍 Location-based risk assessment
* 📸 Citizen/field-official reporting
* 🔔 Multilingual early-warning alerts
* 🚧 Road connectivity monitoring
* 🚑 Emergency response prioritization
* 📡 Offline / low-network simulation

---

## ✨ Key Features

### 🤖 AI/ML Risk Prediction

* Random Forest-based risk prediction
* Risk score from **0–100**
* Risk categories:

  * 🟢 Low
  * 🟡 Medium
  * 🟠 High
  * 🔴 Critical
* Combines environmental and historical indicators for risk assessment

### 🌧️ Environmental Monitoring

The platform demonstrates data fusion involving:

* Rainfall
* Soil moisture
* Terrain characteristics
* Historical landslide records
* Location information

### 🗺️ GIS Risk Dashboard

Interactive geospatial visualization featuring:

* Landslide risk heatmap
* Risk-colored location markers
* State-level filtering
* Risk-level filtering
* Ranked high-risk locations
* Interactive map exploration

### 📡 Sensor Monitoring

Provides:

* Rainfall trends
* Soil-moisture trends
* Latest sensor readings
* Location-wise monitoring
* Historical incident information

### 📸 Field Reporting

Citizens and field officials can submit reports containing:

* Geo-tagged information
* Photos
* Videos
* Slope movement reports
* Ground cracks
* Blocked-road reports

### 🔔 Multilingual Alerts

The prototype supports alert/UI languages including:

* English
* Hindi
* Assamese
* Bengali
* Manipuri

High-risk locations can generate simulated warning notifications.

### 🚧 Road Connectivity & Emergency Response

The platform monitors road conditions such as:

* Open
* Restricted
* Blocked

It also provides emergency-response prioritization based on risk and connectivity conditions.

### 📱 Offline / Low-Network Mode

An offline/low-network mode is included to simulate the experience of accessing previously synchronized/cached information in areas with limited connectivity.

---

## 🖥️ Application Pages

| Page                         | Description                                                           |
| ---------------------------- | --------------------------------------------------------------------- |
| **Overview**                 | Key statistics and state-wise landslide risk summary                  |
| **GIS Risk Dashboard**       | Interactive risk map, heatmap, filters, and ranked locations          |
| **Sensor Monitoring**        | Rainfall, soil-moisture trends, sensor readings, and incident history |
| **Field Reporting**          | Geo-tagged citizen and field-official photo/video reporting           |
| **Alerts & Notifications**   | Multilingual risk alerts and simulated notification dispatch          |
| **Road Connectivity Status** | Road conditions and emergency-response priority ranking               |
| **System Architecture**      | Production architecture and prototype-vs-real implementation details  |

---

## 🛠️ Tech Stack

| Technology                    | Purpose                             |
| ----------------------------- | ----------------------------------- |
| **Python**                    | Core programming language           |
| **Streamlit**                 | Interactive web application         |
| **Pandas**                    | Data processing                     |
| **NumPy**                     | Numerical computation               |
| **Scikit-learn**              | Random Forest ML model              |
| **PyDeck**                    | Interactive GIS/map visualization   |
| **CSV**                       | Location and demonstration data     |
| **Git & GitHub**              | Version control and project hosting |
| **Streamlit Community Cloud** | Application deployment              |

---

## 📂 Project Structure

```text
ner-landslide-ews/
│
├── app.py
│   └── Main Streamlit application and page routing
│
├── modules/
│   ├── data_utils.py
│   │   └── Location registry and synthetic data generation
│   │
│   ├── ml_model.py
│   │   └── Random Forest training and risk prediction
│   │
│   ├── alerts.py
│   │   └── Multilingual UI text and alert templates
│   │
│   └── gis_utils.py
│       └── PyDeck map layers and risk visualization
│
├── data/
│   └── locations.csv
│       └── 18 seed locations across the 8 NER states
│
├── uploads/
│   └── Runtime storage for citizen/field reports
│
├── .streamlit/
│   └── config.toml
│       └── Streamlit application theme
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Animesh2473/ner-landslide-early-warning-system.git
cd ner-landslide-early-warning-system
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

On the first launch, the application may take a few seconds to generate the demonstration dataset and train the cached ML model.

---

## 🧪 Demo Data

This project currently uses **synthetically generated data** for demonstration purposes.

The synthetic data includes:

* Rainfall measurements
* Soil-moisture measurements
* Historical landslide incidents
* Location information
* Risk-related features

The purpose is to demonstrate the complete workflow without depending on external APIs or live sensor infrastructure.

---

## 🏗️ Production Extension

The prototype is designed so that its simulated components can eventually be replaced with real-world infrastructure.

### 1. Live Weather & Sensor Data

Replace the synthetic sensor-data generation with:

* IMD weather data
* IoT rain gauges
* Soil-moisture sensors
* Satellite-based soil-moisture products
* Other environmental monitoring systems

### 2. Historical Landslide Inventory

Replace the synthetic historical records with validated datasets from sources such as:

* Geological Survey of India
* NRSC Landslide Atlas
* State Disaster Management Authorities
* Other verified landslide inventories

### 3. Production ML Model

Retrain and validate the model using real labelled landslide data.

Possible future approaches include:

* Random Forest
* Gradient Boosting
* XGBoost
* Ensemble ML models
* Rainfall-threshold + ML hybrid models
* Deep learning approaches

Model performance should be validated using real-world data and domain expertise.

### 4. Real-Time Alert Infrastructure

The simulated alert functionality could be connected to:

* SMS gateways
* Mobile push notifications
* Government alert systems
* Cell Broadcast
* Emergency response systems

### 5. True Offline Support

For production mobile deployment, the field-reporting module could be implemented as a:

* Progressive Web App (PWA)
* Native Android/iOS application
* Local SQLite-based storage system

Reports could then be synchronized automatically when network connectivity becomes available.

---

## 🧠 System Architecture

The application separates the major components into:

```text
Environmental Data
       │
       ├── Rainfall
       ├── Soil Moisture
       ├── Terrain
       └── Historical Records
              │
              ▼
       Data Processing
              │
              ▼
       ML Risk Prediction
              │
              ▼
       Risk Score (0–100)
              │
       ┌──────┴──────┐
       ▼             ▼
   GIS Dashboard   Alerts
       │             │
       ▼             ▼
 Risk Monitoring  Emergency
                  Response
       │
       ▼
 Field Reports + Road Status
```

---

## ⚠️ Prototype vs Production

| Component             | Current Prototype         | Production Version               |
| --------------------- | ------------------------- | -------------------------------- |
| Rainfall              | Synthetic                 | Live weather/sensor data         |
| Soil Moisture         | Synthetic                 | IoT + satellite data             |
| Historical Landslides | Synthetic                 | Verified landslide inventory     |
| ML Model              | Random Forest             | Validated production ensemble    |
| GIS                   | PyDeck                    | Production GIS infrastructure    |
| Alerts                | Simulated                 | SMS / Push / Cell Broadcast      |
| Offline Mode          | Simulated                 | PWA / Native + local database    |
| Field Reports         | Local runtime storage     | Cloud storage + backend          |
| Database              | Prototype data structures | PostgreSQL/PostGIS or equivalent |

---

## 🎯 Project Objective

The objective of this project is to demonstrate how **AI/ML, geospatial visualization, environmental monitoring, citizen reporting, multilingual communication, and emergency-response prioritization** can be integrated into a unified landslide early-warning platform.

The prototype focuses specifically on the **North Eastern Region of India**, where terrain, rainfall, connectivity, and remote-location challenges make early warning and monitoring particularly important.

---

## 🔮 Future Improvements

Potential future improvements include:

* Real-time IMD weather integration
* Satellite imagery integration
* IoT sensor integration
* Advanced terrain/elevation features
* Explainable AI for risk predictions
* Automated anomaly detection
* Real-time SMS alerts
* Mobile application
* PWA-based offline reporting
* Cloud database integration
* Role-based access for citizens, officials, and administrators
* Historical risk trend analysis
* Model monitoring and automatic retraining

---

## 👨‍💻 Author

**Animesh Kewale**

Computer Science & Engineering — Data Science

---

## 🔗 Links

🌐 **Live Application:**
https://ner-landslide-ews.streamlit.app/

💻 **GitHub Repository:**
https://github.com/Animesh2473/ner-landslide-early-warning-system

---

## 📄 License

This project is a prototype created for demonstration, learning, and development purposes.
