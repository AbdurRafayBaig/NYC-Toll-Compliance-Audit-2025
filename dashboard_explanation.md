# 📊 NYC Congestion Audit 2025: Dashboard User Guide

This document provides a comprehensive explanation of every component within the **Metropolitan Transit Impact Analysis** dashboard. Use this structure for your assignment documentation.

---

## 🛡️ 1. The Audit Hub (Sidebar)
The sidebar acts as the dashboard's "Command Center," providing high-level metrics and system controls that remain visible as you navigate through different tabs.

*   **Branding Header**: A stylized "🏙️ METRO TRANSIT AUDIT" logo that establishes the institutional authority of the report.
*   **Key Performance Indicators (KPIs)**:
    *   **Total Revenue 2025**: A real-time estimate of the total surcharge collected (approx. **$74.4M**), calculated from transaction logs.
    *   **Rain Elasticity**: A decimal score (e.g., **0.14**) indicating how sensitive taxi demand is to precipitation.
*   **Navigation Guide**: A quick-start instruction set to help stakeholders interact with the 3D maps and heatmaps effectively.
*   **Live Audit Narrative**: A dynamic alert section that flags the total volume of **"Ghost Trips"** (manual entry mismatches). It specifically highlights the Yellow Cab sector if it exceeds compliance thresholds.
*   **Data Synchronization Button**: A backend trigger that re-executes the Python `pipeline.py` script to refresh the analytical data without leaving the browser.

---

## 🌎 2. Tab 1: The Border Effect (Compliance Map)
This tab visualizes "geospatial leakage"—where vehicles enter the congestion zone but the surcharge isn't successfully processed.

*   **3D Column Map**: Built using **PyDeck**, this interactive map allows you to rotate and zoom into Manhattan.
    *   **Column Height**: Represents the **Risk Score** (100 minus Compliance %). Taller columns indicate areas where drivers are potentially bypassing the toll.
    *   **Color Gradient**: Ranges from Green (High Compliance) to Red (High Risk), providing an instant heat-map of enforcement needs.
*   **Primary Audit Table**: A stylized data grid providing the exact numbers (Trips vs. Paid Surcharges) for every zone ID, allowing for granular inspection.

---

## ⏱️ 3. Tab 2: The Flow (Velocity Heatmaps)
This section focuses on the secondary goal of congestion pricing: improving traffic speeds.

*   **Side-by-Side Comparison**: Two heatmaps are placed together to compare **Q1 2024 (Before Toll)** against **Q1 2025 (After Toll)**.
*   **Temporal Hour Matrix**: The X-axis shows the hour of the day (0-23), while the Y-axis shows the day of the week.
*   **Velocity Scale (MPH)**:
    *   **Red/Yellow**: Indicates gridlock or slow-moving traffic.
    *   **Green**: Indicates free-flowing metropolitan traffic.
*   **Analytical Context**: A narrative box explains the "Velocity Delta," helping the viewer understand if the toll successfully "thinned out" the traffic.

---

## 💹 4. Tab 3: The Economics (Financial Trends)
An econometric view of how the $2.50 surcharge impacts consumer behavior, specifically their willingness to tip.

*   **Dual-Axis Chart**:
    *   **Bar Chart (Red)**: Displays the **Mean Surcharge** billed per month.
    *   **Line Chart (Cyan)**: Tracks the **Mean Tip Percentage** from passengers.
*   **Gratuity Fatigue Analysis**: This chart helps identify if passengers are "offsetting" the new congestion toll by reducing the tips they give to drivers.
*   **Interactive Tooltips**: Hovering over any month reveals a unified view of both metrics for precise comparison.

---

## 🌧️ 5. Tab 4: The Weather (Rain Elasticity)
A scientific modeling of external environmental factors on the transit system.

*   **Regression Scatter Plot**: Every dot represents a day's worth of data.
*   **OLS Trendline**: An "Ordinary Least Squares" line shows the overall trend. An upward-sloping line proves that as rain increases (X-axis), the volume of trips increases (Y-axis).
*   **Behavioral Modeling Context**: Explains that a score above **0.1** is "Statistically Significant," meaning the city must increase fleet availability specifically during wet weather.
*   **Elasticity Metric Card**: Displays the final Pearson Correlation coefficient derived from the Open-Meteo API data.

---
*Document Ends*
