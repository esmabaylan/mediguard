import streamlit as st
import requests
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
API_BASE_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="Hasta Analizi | MediGuard", page_icon="🩺", layout="wide")
render_navbar(active="Patient Analysis")


@st.cache_data(ttl=300)
def fetch_drugs():
    """Veritabanındaki ilaç listesini çeker. 5 dakika cache'lenir."""
    resp = requests.get(f"{API_BASE_URL}/drugs")
    resp.raise_for_status()
    return resp.json()

page_header(
    "Hasta Analiz ve Reçete Ekranı",
    subtitle="TCKN girerek hasta geçmişini görüntüleyin ve risk kontrollü yeni reçete oluşturun.",
    icon="🩺",
)

tckn_input = st.text_input("🔍 TCKN Giriniz:", max_chars=11, placeholder="11 haneli kimlik numarası...")

if tckn_input and len(tckn_input) == 11:
    with st.spinner("Hasta kayıtları aranıyor..."):
        response = requests.get(f"{API_BASE_URL}/patients/{tckn_input}")

    if response.status_code == 200:
        data = response.json()
        patient = data.get("patient_info", {})
        history = data.get("recent_history", [])

        col_left, col_right = st.columns([2, 1])

        with col_right:
            # ❌ SİL: st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            
            with st.container(border=True): # ✅ SADECE BU KALMALI
                st.subheader("👤 Hasta Profili")
                st.info(f"**Ad Soyad:** {patient.get('first_name', '')} {patient.get('last_name', '')}")
                st.write(f"**Cinsiyet:** {patient.get('gender', '-')} | **Yaş:** {patient.get('age', '-')}")
                st.warning(f"**Kronik Hastalık:** {patient.get('chronic_disease', 'Bilinmiyor')}")

                st.markdown("**Son Ziyaret ve İlaçlar**")
                if history:
                    for presc in history:
                        with st.expander(f"📅 {presc.get('date', 'Tarih Yok')[:10]}"):
                            st.write(f"**İlaç:** {presc.get('drug_name', presc.get('drug_id'))}")
                            st.write(f"**Doz:** {presc.get('dosage_mg')} mg")
                            st.write(f"**Süre:** {presc.get('days')} Gün")
                else:
                    st.write("Sistemde geçmiş reçete kaydı bulunmuyor.")

        with col_left:
            with st.container(border=True):
                st.subheader("✍️ Yeni Reçete Taslağı")
            
            try:
                drug_list = fetch_drugs()
            except requests.exceptions.RequestException:
                drug_list = []
                st.error("İlaç listesi alınamadı. Backend'in çalıştığından emin olun.")

            if not drug_list:
                st.warning("Veritabanında kayıtlı ilaç bulunamadı.")
            else:
                drug_options = {
                    f"{d['name']} ({d.get('strength') or ''}{d.get('strength_unit') or ''}) — {d['category']}": d
                    for d in drug_list
                }

                # Sepet, hasta bazında ayrı tutulur ki farklı bir TCKN'ye
                # geçildiğinde önceki hastanın ilaçları karışmasın.
                cart_key = f"rx_cart_{tckn_input}"
                if cart_key not in st.session_state:
                    st.session_state[cart_key] = []

                st.markdown("**İlaç Ekle**")
                add_col1, add_col2, add_col3, add_col4 = st.columns([3, 1.2, 1.2, 1])
                with add_col1:
                    selected_label = st.selectbox("İlaç", options=list(drug_options.keys()))
                selected_drug = drug_options[selected_label]
                with add_col2:
                    dosage = st.number_input("Günlük Doz (mg)", min_value=0.0, step=50.0)
                with add_col3:
                    days = st.number_input("Süre (Gün)", min_value=1, max_value=30)
                with add_col4:
                    st.markdown("<div style='height:1.85rem'></div>", unsafe_allow_html=True)
                    if st.button("➕ Ekle", use_container_width=True):
                        st.session_state[cart_key].append({
                            "drug_id": selected_drug["drug_id"],
                            "drug_name": selected_drug["name"],
                            "drug_category": selected_drug["category"],
                            "daily_dosage_mg": dosage,
                            "prescribed_days": days,
                        })
                        st.rerun()

                st.caption(
                    f"**Form:** {selected_drug.get('form', '-')} · "
                    f"**Etken Madde:** {selected_drug.get('active_ingredient', '-')} · "
                    f"**Max Günlük Doz:** {selected_drug.get('max_daily_dose', '-')} "
                    f"{selected_drug.get('max_daily_dose_unit') or ''}"
                )

                st.markdown("---")
                st.markdown(f"**Reçetedeki İlaçlar ({len(st.session_state[cart_key])})**")

                if not st.session_state[cart_key]:
                    st.info("Henüz reçeteye ilaç eklenmedi. Yukarıdan bir ilaç seçip 'Ekle' butonuna basın.")
                else:
                    for idx, item in enumerate(st.session_state[cart_key]):
                        row1, row2, row3, row4 = st.columns([3, 1.2, 1.2, 0.6])
                        row1.write(f"💊 **{item['drug_name']}** _{item['drug_category']}_")
                        row2.write(f"{item['daily_dosage_mg']:g} mg/gün")
                        row3.write(f"{item['prescribed_days']} gün")
                        if row4.button("🗑️", key=f"del_{cart_key}_{idx}"):
                            st.session_state[cart_key].pop(idx)
                            st.rerun()

                    st.write("")
                    clear_col, submit_col = st.columns([1, 2])
                    with clear_col:
                        if st.button("Listeyi Temizle", use_container_width=True):
                            st.session_state[cart_key] = []
                            st.rerun()

                    with submit_col:
                        if st.button("Risk Analizinden Geçir", type="primary", use_container_width=True):
                            draft_payload = {
                                "patient_id": tckn_input,
                                "medications": [
                                    {
                                        "drug_id": item["drug_id"],
                                        "drug_category": item["drug_category"],
                                        "daily_dosage_mg": item["daily_dosage_mg"],
                                        "prescribed_days": item["prescribed_days"],
                                    }
                                    for item in st.session_state[cart_key]
                                ],
                            }

                            analyze_resp = requests.post(f"{API_BASE_URL}/prescriptions/analyze", json=draft_payload)

                            if analyze_resp.status_code == 200:
                                result = analyze_resp.json()

                                if result["status"] == "RISK_FOUND":
                                    st.error("🚨 KRİTİK UYARI: Reçete Risk İçeriyor!")
                                    for alert in result["alerts"]:
                                        st.warning(f"**{alert.get('risk_type', 'Uyarı')}:** {alert.get('message', '')}")
                                else:
                                    st.success("✅ Risk saptanmadı. Reçete güvenli!")
                                    save_resp = requests.post(f"{API_BASE_URL}/prescriptions/save", json=draft_payload)
                                    if save_resp.status_code == 200:
                                        st.balloons()
                                        st.success("Reçete başarıyla veritabanına kaydedildi ve Kafka'ya iletildi.")
                                        st.session_state[cart_key] = []
                                    else:
                                        st.error("Kaydetme sırasında bir hata oluştu.")
                            else:
                                st.error("Risk analiz motoruna ulaşılamıyor.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Sistemde bu TCKN ile eşleşen bir hasta bulunamadı.")