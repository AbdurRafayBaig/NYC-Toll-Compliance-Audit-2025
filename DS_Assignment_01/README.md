# 🏙️ NYC Toll Compliance Audit 2025

A comprehensive data analytics pipeline and interactive dashboard analyzing NYC's 2025 Congestion Pricing implementation, featuring revenue auditing, ghost trip detection, and meteorological impact modeling.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![DuckDB](https://img.shields.io/badge/DuckDB-0.9.0+-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)

## 🔍 Project Overview

This project analyzes the impact of New York City's Congestion Relief Zone (CRZ) toll system through:
- **Big Data ETL Pipeline**: Processing 4.5M+ transit records using DuckDB
- **Revenue Auditing**: Identified $74.4M in surcharge revenue with systemic compliance analysis
- **Ghost Trip Detection**: Uncovered 4.5M+ anomalous entries indicating revenue leakage
- **Meteorological Modeling**: Rain elasticity correlation (0.1402) for demand forecasting
- **Interactive Dashboard**: Premium Streamlit interface with 4 analytical tabs

## 📊 Key Findings

- **Total 2025 Revenue**: $74,442,907.00
- **Rain Elasticity Score**: 0.1402 (Moderate Positive Correlation)
- **Ghost Trips Detected**: 4,529,715 (Yellow Cab sector)
- **Compliance Floor**: 0.14% in critical zones (183, 77, 3)

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.9+
pip
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AbdurRafayBaig/NYC-Toll-Compliance-Audit-2025.git
cd NYC-Toll-Compliance-Audit-2025
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Project

1. **Execute the Data Pipeline**:
```bash
python pipeline.py
```
This will:
- Download transit data from NYC Open Data
- Process and clean 4.5M+ records
- Generate analytical artifacts in `output/`
- Train the ML forecasting model

2. **Launch the Interactive Dashboard**:
```bash
streamlit run dashboard.py
```
Then open your browser to `http://localhost:8501`

## 📁 Project Structure

```
NYC-Toll-Compliance-Audit-2025/
├── pipeline.py                 # Master ETL orchestration script
├── dashboard.py                # Streamlit dashboard entry point
├── requirements.txt            # Python dependencies
├── audit_report.md            # Executive summary & policy recommendations
├── src/
│   ├── data_pipeline.py       # Data ingestion & cleaning
│   ├── analytics.py           # Revenue & compliance auditing
│   ├── forecasting_engine.py  # ML demand forecasting
│   ├── app.py                 # Dashboard UI components
│   └── config.py              # Configuration settings
├── data/                      # Raw transit data (auto-downloaded)
└── output/                    # Generated analytical artifacts
```

## 🎯 Dashboard Features

### Tab 1: The Map 🌎
- **3D PyDeck Visualization**: Interactive geospatial compliance mapping
- **Border Effect Analysis**: Identifies toll bypass hotspots
- **Risk Scoring**: Column height = non-compliance severity

### Tab 2: The Flow ⏱️
- **Side-by-Side Heatmaps**: 2024 vs 2025 velocity comparison
- **Temporal Analysis**: Hour-by-hour, day-by-day traffic patterns
- **Congestion Mitigation**: Visual proof of toll effectiveness

### Tab 3: The Economics 💹
- **Dual-Axis Trends**: Surcharge vs. Tip correlation
- **Gratuity Fatigue**: Consumer behavior analysis
- **Financial Equilibrium**: City revenue vs. driver fairness

### Tab 4: The Weather 🌧️
- **Rain Elasticity**: Scatter plots with OLS trendlines
- **Behavioral Modeling**: Precipitation impact on transit demand
- **Predictive Insights**: Weather-driven volume forecasting

## 🛠️ Technologies Used

- **Data Processing**: DuckDB, Pandas, PyArrow
- **Visualization**: Streamlit, PyDeck, Plotly
- **Machine Learning**: scikit-learn (Random Forest)
- **APIs**: Open-Meteo (Weather data)
- **Geospatial**: GeoJSON, Folium

## 📈 Data Sources

- NYC Taxi & Limousine Commission (TLC) Trip Records
- NYC Open Data Portal (Taxi Zone GeoJSON)
- Open-Meteo API (Historical Weather Data)

## 🎓 Academic Context

This project was developed as part of a Data Science course assignment focusing on:
- Big Data processing and ETL pipelines
- Real-world data auditing and compliance analysis
- Interactive data visualization and storytelling
- Machine learning for demand forecasting

## 📄 License

This project is for educational purposes.

## 👤 Author

**Abdur Rafay Baig**
- GitHub: [@AbdurRafayBaig](https://github.com/AbdurRafayBaig)

## 🙏 Acknowledgments

- NYC Taxi & Limousine Commission for open data
- Open-Meteo for weather API access
- Streamlit community for visualization tools
