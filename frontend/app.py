import streamlit as st
import requests
from datetime import date

# Flask backend base URL (Docker internal network)
API_BASE = "https://crop-disease-backend-v53d.onrender.com"

st.set_page_config(page_title="Crop Disease Predictor", layout="wide")
st.title("🌾 Crop Stage & Disease Predictor (Docker + Flask API)")

@st.cache_data(ttl=600)
def fetch_crops():
    try:
        res = requests.get(f"{API_BASE}/crops")
        if res.status_code == 200:
            return res.json().get("crops", [])
        else:
            return []
    except Exception as e:
        st.error(f"⚠️ Could not fetch crops: {e}")
        return []

crops = fetch_crops()

if crops:
    crop_name = st.selectbox("🌱 Select Crop", options=crops, index=0)
else:
    st.warning("⚠️ No crops available. Make sure the backend is running.")
    crop_name = st.text_input("Or enter crop manually", "")

sowing_date = st.date_input("📅 Sowing Date", value=date(2025, 10, 1))
today = date.today()
days_since = (today - sowing_date).days

if st.button("🔍 Predict Disease"):
    payload = {"crop_name": crop_name, "sowing_date": sowing_date.strftime("%Y-%m-%d")}
    try:
        res = requests.post(f"{API_BASE}/predict", json=payload)
        if res.status_code == 200:
            data = res.json()
            st.success(f"✅ Prediction successful for '{crop_name.title()}'")
            st.metric("Days Since Sowing", data.get("days_since"))
            st.metric("Current Stage", data.get("stage"))
            st.subheader("🦠 Possible Diseases:")
            diseases = data.get("diseases", [])
            if diseases:
                for d in diseases:
                    st.write(f"- {d}")
            else:
                st.info("No diseases listed for this stage.")
        else:
            st.error(f"❌ Error: {res.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"⚠️ Could not connect to backend: {e}")
