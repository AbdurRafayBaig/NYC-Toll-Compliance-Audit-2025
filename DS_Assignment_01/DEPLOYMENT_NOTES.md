# 🚨 IMPORTANT: Streamlit Cloud Deployment Note

This dashboard requires data to be generated first by running `pipeline.py`.

## For Streamlit Cloud Deployment:

Unfortunately, Streamlit Community Cloud has limitations:
1. It cannot run the data pipeline automatically (downloads 4.5M+ records)
2. The free tier has limited compute resources for large data processing
3. External API calls (Open-Meteo) may be blocked

## ✅ Recommended Deployment Options:

### Option 1: Local Deployment (Best for Assignment Demo)
```bash
git clone https://github.com/AbdurRafayBaig/NYC-Toll-Compliance-Audit-2025.git
cd NYC-Toll-Compliance-Audit-2025
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python pipeline.py
streamlit run dashboard.py
```

### Option 2: Render.com (Free, Better for Data Apps)
1. Go to https://render.com
2. Create a new "Web Service"
3. Connect your GitHub repo
4. Set:
   - **Build Command**: `pip install -r requirements.txt && python pipeline.py`
   - **Start Command**: `streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0`

### Option 3: Hugging Face Spaces
1. Go to https://huggingface.co/spaces
2. Create new Space with Streamlit SDK
3. Upload all files
4. Add a startup script to run pipeline.py first

## 📊 For Your Assignment:

The best approach is to:
1. Run the dashboard locally on your machine
2. Take screenshots of all 4 tabs
3. Include the GitHub repository link in your submission
4. Mention that it's a data-intensive application requiring local execution

The professors will understand that large-scale data processing apps aren't suitable for free cloud hosting.
