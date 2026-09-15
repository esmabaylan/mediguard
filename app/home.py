import streamlit as st
from navBar import render_navbar
import streamlit.components.v1 as components

# =========================================================
# Sayfa temel ayarları (Kodun en başında olmalıdır)
# =========================================================
st.set_page_config(
    page_title="MediGuard | Klinik Yönetim Sistemi",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Sidebar'ı gizleyip Vademecum tarzı üst nav barı çizer
render_navbar(active="Home")

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
# =========================================================
# Global CSS - Koyu lacivert hero, kırmızı vurgu, kart tasarımı
# =========================================================
st.markdown("""
<style>
    /* Genel sayfa boşluklarını daralt */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* ---------- HERO ---------- */
    .hero-wrap {
        background: linear-gradient(135deg, #0B1A3A 0%, #0F2350 100%);
        border-radius: 18px;
        padding: 3rem 2.5rem;
        margin-bottom: 1.2rem;
        color: #FFFFFF;
    }
    .hero-badge {
        display: inline-block;
        background: #FFD400;
        color: #0B1A3A;
        font-weight: 800;
        font-size: 0.85rem;
        padding: 4px 10px;
        border-radius: 6px;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 1rem;
    }
    .hero-sub {
        color: #C7D2E8;
        font-size: 1.05rem;
        max-width: 480px;
        margin-bottom: 1.6rem;
    }

    /* Sağdaki canlı sorgu kartı */
    .query-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        color: #0B1A3A;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }
    .query-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 700;
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
    }
    .live-dot {
        color: #16A34A;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .query-input-fake {
        border: 1.5px solid #DC2626;
        border-radius: 8px;
        padding: 10px 12px;
        color: #DC2626;
        font-family: monospace;
        font-size: 0.92rem;
        margin-bottom: 0.6rem;
    }
    .query-result-box {
        background: #F8FAFC;
        border: 1px dashed #CBD5E1;
        border-radius: 10px;
        min-height: 130px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #94A3B8;
        font-size: 0.9rem;
    }

    /* ---------- STAT ŞERİDİ ---------- */
    .stat-strip {
        background: #0B1A3A;
        border-radius: 14px;
        padding: 1.6rem 1rem;
        margin-bottom: 2.2rem;
        display: flex;
        justify-content: space-around;
        text-align: center;
        flex-wrap: wrap;
    }
    .stat-num {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 800;
    }
    .stat-num span { color: #EF4444; }
    .stat-label {
        color: #AAB6CE;
        font-size: 0.85rem;
        margin-top: 2px;
    }

    /* ---------- BÖLÜM BAŞLIĞI ---------- */
    .section-title {
        text-align: center;
        font-size: 1.9rem;
        font-weight: 800;
        color: #0B1A3A;
        margin-bottom: 0.4rem;
    }
    .section-sub {
        text-align: center;
        color: #64748B;
        max-width: 620px;
        margin: 0 auto 2rem auto;
    }

    /* ---------- ÖZELLİK KARTLARI ---------- */
    .feature-panel {
        background: #FFFFFF;
        border: 1px solid #E5E9F2;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 18px rgba(15,23,42,0.06);
        margin-bottom: 2.2rem;
    }
    .feature-tag {
        display: inline-block;
        background: #FEE2E2;
        color: #DC2626;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 999px;
        margin-bottom: 0.6rem;
    }
    .feature-panel h3 { margin: 0 0 0.3rem 0; color: #0B1A3A; }
    .mini-card {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        height: 100%;
        border: 1px solid #EEF1F6;
    }
    .mini-icon {
        font-size: 1.4rem;
        margin-bottom: 0.5rem;
    }
    .mini-card b { color: #0B1A3A; font-size: 0.98rem; }
    .mini-card p { color: #64748B; font-size: 0.85rem; margin-top: 0.3rem; }

    /* ---------- SEKTÖREL / MODÜL KARTLARI ---------- */
    .module-card {
        background: #FFFFFF;
        border: 1px solid #E5E9F2;
        border-radius: 14px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        height: 100%;
    }
    .module-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    .module-card b { color: #0B1A3A; }
    .module-card p { color: #64748B; font-size: 0.85rem; margin-top: 0.3rem; }

    /* Streamlit butonlarını kırmızı/yeşil vurgulu hale getir */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 700;
        padding: 0.5rem 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO BÖLÜMÜ
# =========================================================

st.markdown("""
<div class="hero-wrap" style="padding-bottom:0;">
    <span class="hero-badge">⚕️ MEDIGUARD</span>
    <div class="hero-title">Reçeteyi Yazıyorum,<br>Hastamı Koruyorum!</div>
    <div class="hero-sub">
        Klinisyenlerin güvenle kullandığı, gerçek zamanlı ilaç etkileşimi ve
        doz risk analiziyle donatılmış klinik karar destek altyapısı.
    </div>
</div>
""", unsafe_allow_html=True)



# =========================================================
# İSTATİSTİK ŞERİDİ
# =========================================================
st.markdown("""
<div class="stat-strip">
    <div><div class="stat-num">7.500<span>+</span></div><div class="stat-label">Etken Madde</div></div>
    <div><div class="stat-num">3,5M<span>+</span></div><div class="stat-label">Günlük Reçete Kontrolü</div></div>
    <div><div class="stat-num">35.000<span>+</span></div><div class="stat-label">İlaç Kaydı</div></div>
    <div><div class="stat-num">90.000<span>+</span></div><div class="stat-label">Aktif Kullanıcı</div></div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# ÖZELLİK BÖLÜMÜ (Klinik Karar Destek)
# =========================================================
st.markdown('<div class="section-title">MediGuard\'da Neler Var?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Sağlık profesyonellerinin ihtiyaç duyduğu tüm klinik güvenlik araçlarına tek panelden erişim.</div>', unsafe_allow_html=True)

st.markdown("""
<span class="feature-tag">ETKİLEŞİM &amp; GÜVENLİK</span>
<h3>Klinik Karar Destek ve Güvenlik</h3>
<p style="color:#64748B; margin-bottom:1.2rem;">Reçete yazarken hayat kurtaran güvenlik ağları ve etkileşim kontrolleri</p>
""", unsafe_allow_html=True)

fc1, fc2, fc3, fc4 = st.columns(4)
feature_cards = [
    ("🧬", "Çoklu Etkileşim Analizi", "İlaç-İlaç, İlaç-Hastalık ve İlaç-Hasta etkileşimlerinin anlık kontrolü"),
    ("⏱️", "Antibiyotik Süre Uyarısı", "14 günü aşan reçeteler otomatik olarak risk motoruna takılır"),
    ("🛡️", "NSAID / PPI Kontrolü", "Tekrarlı NSAID yazımında mide koruyucu eksikliği uyarıları"),
    ("📈", "Risk Grubu Uyarıları", "Polifarmasi ve AMR vakalarına özel maksimal doz uyarıları"),
]
for col, (icon, title, desc) in zip([fc1, fc2, fc3, fc4], feature_cards):
    with col:
        st.markdown(f"""
        <div class="mini-card">
            <div class="mini-icon">{icon}</div>
            <b>{title}</b>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SİSTEM BİLDİRİMLERİ
# =========================================================
st.subheader("📌 Güncel Sistem Bildirimleri")
st.markdown("""
* **Duyuru 1:** Antibiyotik yazımlarında 14 günü aşan reçeteler otomatik olarak risk motoruna takılmaktadır. Lütfen endikasyon sürelerine dikkat ediniz.
* **Duyuru 2:** NSAID (Ağrı Kesici) grubu ilaçların tekrarlı yazımında mide koruyucu (PPI) eksikliği uyarıları aktif edilmiştir.
* **Sistem Durumu:** Tüm mikroservisler (PostgreSQL, Kafka, Risk Motoru) aktif ve senkron çalışmaktadır.
""")