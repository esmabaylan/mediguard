import streamlit as st
from navBar import render_navbar, page_header


st.markdown(
    """
    <style>
    /* Ana kapsayıcıdaki devasa boşlukları sıfırlar ve %100 genişliğe zorlar */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Risk Dashboard | MediGuard", page_icon="📊", layout="wide")
render_navbar(active="Risk Dashboard")

page_header(
    "Hastane Makro Analiz ve Risk Paneli",
    subtitle="Başhekimlik ve sistem yöneticileri için canlı Grafana verileri.",
    icon="📊",
)

# Public Dashboard linki ve kiosk parametresi
GRAFANA_PUBLIC_URL = "http://localhost:3000/public-dashboards/07f1b8e9712742bd8584a557281ab722?kiosk=tv"

# Streamlit component yerine doğrudan saf HTML Iframe ile %100 genişliğe zorluyoruz
st.markdown(
    f"""
    <iframe 
        src="{GRAFANA_PUBLIC_URL}" 
        width="100%" 
        height="850" 
        style="border: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" 
        scrolling="yes">
    </iframe>
    """, 
    unsafe_allow_html=True
)