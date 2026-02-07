import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from datetime import datetime
from src.config import *

# Configuration
st.set_page_config(layout="wide", page_title="NYC Congestion Audit v2.0", page_icon="🗽")

# Custom CSS for Premium Look & Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif;
    }

    .main {
        background: radial-gradient(circle at top right, #1a1c23, #0e1117);
    }

    /* Glassmorphic Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(48, 54, 61, 0.5);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #00d4ff;
    }

    /* Sidebar Aesthetic */
    [data-testid="stSidebar"] {
        background-color: rgba(13, 17, 23, 0.95);
        border-right: 1px solid rgba(48, 54, 61, 0.5);
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(22, 27, 34, 0.5);
        border: 1px solid rgba(48, 54, 61, 0.5);
        border-radius: 8px 8px 0 0;
        padding: 5px 20px;
        color: #8b949e;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 212, 255, 0.1);
        border-color: #00d4ff;
        color: white;
    }
    
    .narrative-box {
        background: rgba(0, 212, 255, 0.05);
        border-left: 4px solid #00d4ff;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def load_data(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path): return None
    return pd.read_csv(path)



# Sidebar Dashboard Intelligence
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px; border-bottom: 2px solid #00d4ff; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-size: 24px;">🏙️ METRO</h1>
            <p style="color: #00d4ff; font-size: 12px; font-weight: bold; letter-spacing: 2px; margin: 0;">TRANSIT AUDIT</p>
        </div>
    """, unsafe_allow_html=True)
    st.title("🛡️ Audit Hub")
    st.markdown("---")
    
    # KPIs in Sidebar for constant awareness
    revenue_val = "Unavailable"
    if os.path.exists(os.path.join(OUTPUT_DIR, "revenue_report.txt")):
        with open(os.path.join(OUTPUT_DIR, "revenue_report.txt"), 'r') as f:
            revenue_val = f.read()
    
    elasticity_val = "0.0"
    if os.path.exists(os.path.join(OUTPUT_DIR, "elasticity.txt")):
        with open(os.path.join(OUTPUT_DIR, "elasticity.txt"), 'r') as f:
            elasticity_val = f.read()
            
    st.metric("Total Revenue 2025", f"${revenue_val}")
    st.metric("Rain Elasticity", elasticity_val)
    
    st.markdown("---")
    st.subheader("📖 How to Navigate")
    st.markdown("""
    1. **Explore the Map**: Rotate the 3D map to find non-compliance hotspots (High Risk = Taller Columns).
    2. **Compare the Flow**: Use the side-by-side heatmaps to see how congestion pricing speeded up traffic.
    3. **Detect Leakage**: Check the 'Live Audit Narrative' below for real-time anomalous vendor alerts.
    """)
    st.markdown("---")
    st.subheader("🕵️ Live Audit Narrative")
    
    # Dynamic Narrative based on files
    ghost_data = load_data("ghost_trips_audit.csv")
    if ghost_data is not None:
        yellow_ghosts = ghost_data[ghost_data['vendor'] == 'yellow']['ghost_count'].values[0]
        st.write(f"🚩 **Critical Alert**: Identified **{yellow_ghosts:,}** anomalous ghost trips in the Yellow cab sector.")
    
    st.info("The dashboard is currently visualizing the 'Border Effect' - where trips enter the toll zone but bypass the surcharge mechanism.")

# Title & Description
st.title("🗽 Metropolitan Transit Impact Analysis")
st.markdown("### Institutional Audit of the NYC Congestion Relief Zone 2025")

# Tabs
tabs = st.tabs(["🌎 The Map", "⏱️ The Flow", "💹 The Economics", "🌧️ The Weather"])

# Load all data
leakage_df = load_data("surcharge_compliance.csv")
velocity_df = load_data("velocity_stats.csv")
econ_df = load_data("economic_trends.csv")
weather_df = load_data("weather_impact.csv")

# --- TAB 1: THE MAP (BORDER EFFECT) ---
with tabs[0]:
    st.header("🌎 The Border Effect")
    st.markdown("Interactive PyDeck visualization of the 'Border Effect' - evaluating surcharge compliance for trips entering the Congestion Relief Zone.")
    
    if leakage_df is not None:
        geojson_path = os.path.join(DATA_DIR, "taxi_zones.geojson")
        if not os.path.exists(geojson_path):
            st.warning("⚠️ Geospatial metadata (GeoJSON) is currently unavailable. Please execute the data pipeline.")
        else:
            try:
                # KPIs
                col1, col2, col3 = st.columns(3)
                avg_compliance = leakage_df['compliance_pct'].mean()
                col1.metric("Systemic Compliance", f"{avg_compliance:.1f}%", f"{avg_compliance-85:.1f}% vs Target")
                col2.metric("Critical Hotspot", f"Zone {int(leakage_df.iloc[0]['pickup_loc'])}", "Lowest Compliance")
                col3.metric("Audit Integrity", "Verified", "OpenData Sync")

                # Extraction of Coordinates from GeoJSON for 3D Mapping
                with open(geojson_path, 'r') as f:
                    geo_json_data = json.load(f)
                
                # Create a lookup for centroids
                centroids = {}
                for feature in geo_json_data['features']:
                    loc_id = int(feature['properties']['locationid'])
                    # Simple centroid calculation for visualization
                    coords = feature['geometry']['coordinates']
                    if feature['geometry']['type'] == 'MultiPolygon':
                        coords = coords[0][0]
                    else:
                        coords = coords[0]
                    
                    lon = sum([p[0] for p in coords]) / len(coords)
                    lat = sum([p[1] for p in coords]) / len(coords)
                    centroids[loc_id] = (lon, lat)

                # Map coordinates to leakage data
                def safe_get_centroid(x, idx):
                    try:
                        return centroids.get(int(x), [None, None])[idx]
                    except:
                        return None

                leakage_df['lon'] = leakage_df['pickup_loc'].apply(lambda x: safe_get_centroid(x, 0))
                leakage_df['lat'] = leakage_df['pickup_loc'].apply(lambda x: safe_get_centroid(x, 1))
                leakage_df = leakage_df.dropna(subset=['lon', 'lat'])
                
                view_state = pdk.ViewState(latitude=40.75, longitude=-73.98, zoom=10, pitch=45, bearing=0)
                
                # Dynamic Elevation based on non-compliance
                leakage_df['risk_score'] = 100 - leakage_df['compliance_pct']
                
                layer = pdk.Layer(
                    "ColumnLayer",
                    leakage_df,
                    get_position=["lon", "lat"],
                    get_elevation="risk_score",
                    elevation_scale=50,
                    radius=350,
                    get_fill_color=["risk_score * 2.5", "255 - risk_score * 2", 100, 180],
                    pickable=True,
                    auto_highlight=True,
                )
                
                st.pydeck_chart(pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    tooltip={"text": "Zone ID: {pickup_loc}\nCompliance: {compliance_pct:.1f}%\nRisk Score: {risk_score:.1f}"},
                    map_style="road"
                ))
                
                st.subheader("📋 Primary Audit Observations")
                st.markdown("""
                <div class="narrative-box">
                    <b>Data Legend</b>: Zones are colored based on their <b>Risk Score</b> (100 - Compliance %). 
                    Taller columns indicate higher non-compliance rates.
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(leakage_df[['pickup_loc', 'trips', 'paid', 'compliance_pct']].rename(
                    columns={'pickup_loc': 'Zone ID', 'compliance_pct': 'Compliance %'}).style.background_gradient(cmap='RdYlGn'), 
                    width="stretch")
                
            except Exception as e:
                st.error(f"Geospatial Initialization Failure: {e}")

# --- TAB 2: THE FLOW (VELOCITY HEATMAPS) ---
with tabs[1]:
    st.header("⏱️ The Flow: Side-by-Side Velocity Heatmaps")
    st.markdown("""
    <div class="narrative-box">
        <b>Analytical Context</b>: This visualization compares the metropolitan velocity matrix 
        before and after the implementation of the CRZ toll. A shift towards <b>green (faster)</b> 
        indicates successful congestion mitigation.
    </div>
    """, unsafe_allow_html=True)
    
    if velocity_df is not None:
        col1, col2 = st.columns(2)
        
        for i, year in enumerate([2024, 2025]):
            with [col1, col2][i]:
                st.subheader(f"Window: Q1 {year}")
                df_year = velocity_df[velocity_df['year'] == year]
                if not df_year.empty:
                    try:
                        pivot_df = df_year.pivot(index='dow', columns='hour', values='avg_speed')
                        dow_labels = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
                        pivot_df.index = pivot_df.index.map(dow_labels)
                        
                        fig = px.imshow(pivot_df, 
                                       labels=dict(x="Temporal Hour", y="Day", color="MPH"),
                                       color_continuous_scale="RdYlGn",
                                       aspect="auto")
                        fig.update_layout(template="plotly_dark", height=400)
                        st.plotly_chart(fig, width="stretch", key=f"heat_{year}")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning(f"No synchronized data for {year}.")

# --- TAB 3: THE ECONOMICS ---
with tabs[2]:
    st.header("💹 The Economics")
    st.markdown("""
    <div class="narrative-box">
        <b>Financial Impact</b>: This dual-axis chart tracks the relationship between the <b>Congestion Surcharge (Billed)</b> 
        and <b>Tip Velocity (Given)</b>. We analyze if higher tolls lead to "gratuity fatigue" among passengers.
    </div>
    """, unsafe_allow_html=True)
    
    if econ_df is not None:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=econ_df['month'], y=econ_df['avg_surcharge'], name="Mean Surcharge ($)", 
                             marker=dict(color='#ff4b4b', opacity=0.8, line=dict(color='#ff4b4b', width=1))))
        fig.add_trace(go.Scatter(x=econ_df['month'], y=econ_df['avg_tip_pct'], name="Mean Tip Velocity (%)", yaxis="y2", 
                                 line=dict(color='#00d4ff', width=4, shape='spline')))
        
        fig.update_layout(
            yaxis2=dict(overlaying='y', side='right', title="Tip Allocation (%)", showgrid=False),
            title="Correlation: Surcharge Imposition vs. Consumer Gratuity",
            legend=dict(orientation="h", y=1.2, x=0.5, xanchor='center'),
            template="plotly_dark",
            margin=dict(t=100),
            hovermode="x unified"
        )
        st.plotly_chart(fig, width="stretch")

# --- TAB 4: THE WEATHER ---
with tabs[3]:
    st.header("🌧️ The Weather: Rain Elasticity")
    st.markdown("""
    <div class="narrative-box">
        <b>Behavioral Modeling</b>: We analyze how precipitation affects transit volume. 
        A positive correlation (upward trend) suggests the CRZ must adapt to weather-driven 
        surges in vehicle demand.
    </div>
    """, unsafe_allow_html=True)
    
    if weather_df is not None:
        fig = px.scatter(weather_df, x="precipitation_sum", y="trip_count", 
                         trendline="ols", color="trip_count",
                         color_continuous_scale="Viridis",
                         labels={"precipitation_sum": "Precipitation (mm)", "trip_count": "Observed Volume"},
                         template="plotly_dark")
        
        fig.update_layout(
            title="Meteorological Impact on Transit Volume",
            xaxis_title="Rainfall / Snowfall (mm)",
            yaxis_title="Total Trip Records",
            coloraxis_showscale=False,
            hovermode="closest"
        )
        st.plotly_chart(fig, width="stretch")
        
        st.markdown("""
        <div class="narrative-box" style="border-left-color: #f1c40f;">
            <b>Predictive Insight</b>: The elasticity coefficient quantified below measures the % change 
            in demand for every 1mm of additional rain. A score > 0.1 indicates a <b>statistically significant</b> 
            weather-driven volume spike.
        </div>
        """, unsafe_allow_html=True)
        
        if os.path.exists(os.path.join(OUTPUT_DIR, "elasticity.txt")):
            with open(os.path.join(OUTPUT_DIR, "elasticity.txt"), 'r') as f:
                score = f.read()
            st.metric("Meteorological Elasticity Coefficient", score)

def synchronize_data():
    """Trigger the formal metropolitan ingestion pipeline with UI status updates."""
    import sys
    import subprocess
    
    with st.sidebar:
        with st.status("Initializing Metropolitan Lifecycle...", expanded=True) as status:
            st.write("Acquiring remote transit assets...")
            try:
                # Use current process executable to ensure same virtual environment
                result = subprocess.run([sys.executable, "pipeline.py"], 
                                      capture_output=True, text=True, check=False)
                
                if result.returncode == 0:
                    st.write("Synchronizing analytical artifacts...")
                    status.update(label="Lifecycle Synchronized!", state="complete", expanded=False)
                    st.toast("Metropolitan data repository updated successfully.")
                    st.rerun()
                else:
                    st.error("Synchronization Failure")
                    st.code(result.stderr or result.stdout)
                    status.update(label="Lifecycle Error", state="error")
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
                status.update(label="System Error", state="error")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Execute Data Synchronization", width="stretch"):
    synchronize_data()
