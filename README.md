# 🏙️ NYC Toll Compliance Audit 2025

A comprehensive data analytics pipeline and interactive dashboard analyzing NYC's 2025 Congestion Pricing implementation, featuring revenue auditing, ghost trip detection, and meteorological impact modeling.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![DuckDB](https://img.shields.io/badge/DuckDB-0.9.0+-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)

## 📂 Project Location

**All project files are located in the [`DS_Assignment_01`](./DS_Assignment_01) folder.**

👉 **[Click here to view the complete project](./DS_Assignment_01)**

## 🔍 Quick Overview

- **Total 2025 Revenue**: $74,442,907.00
- **Rain Elasticity Score**: 0.1402 (Moderate Positive Correlation)
- **Ghost Trips Detected**: 4,529,715 (Yellow Cab sector)
- **Compliance Floor**: 0.14% in critical zones

## 🚀 Quick Start

```bash
git clone https://github.com/AbdurRafayBaig/NYC-Toll-Compliance-Audit-2025.git
cd NYC-Toll-Compliance-Audit-2025/DS_Assignment_01
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python pipeline.py
streamlit run dashboard.py
```

## 📊 Key Features

- **Big Data ETL Pipeline**: Processing 4.5M+ transit records using DuckDB
- **Interactive Dashboard**: Premium Streamlit interface with 4 analytical tabs
- **Ghost Trip Detection**: Uncovered systemic revenue leakage
- **Meteorological Modeling**: Rain elasticity correlation for demand forecasting

## 📁 Repository Structure

```
NYC-Toll-Compliance-Audit-2025/
└── DS_Assignment_01/          ← Main project folder
    ├── src/                   ← Source code modules
    ├── pipeline.py            ← Master ETL script
    ├── dashboard.py           ← Streamlit dashboard
    ├── requirements.txt       ← Dependencies
    ├── README.md              ← Detailed documentation
    └── audit_report.md        ← Executive summary
```

## 👤 Author

**Abdur Rafay Baig**
- GitHub: [@AbdurRafayBaig](https://github.com/AbdurRafayBaig)

---

**📖 For complete documentation, installation instructions, and detailed project information, please visit the [`DS_Assignment_01`](./DS_Assignment_01) folder.**
