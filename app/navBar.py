import streamlit as st


def _inject_global_style():
    """Sidebar'ı gizler, Streamlit chrome'unu kaldırır ve tüm sayfalar için
    ortak renk/tipografi/kart stillerini tanımlar. render_navbar() içinden çağrılır,
    ayrıca sayfa başına tek seferlik enjekte edilir."""
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="collapsedControl"] { display: none; }

        /* Streamlit'in kendi üst çubuğunu (hamburger menü / Deploy butonu) gizle */
        header[data-testid="stHeader"] { display: none !important; }
        div[data-testid="stToolbar"] { display: none !important; }
        div[data-testid="stDecoration"] { display: none !important; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }

        .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1200px; }

        /* ---------- Ortak tipografi ---------- */
        h1, h2, h3 { color: #0B1A3A; font-weight: 800; }

        /* ---------- Nav bar ---------- */
        .navbar-logo {
            background: #FFD400;
            color: #0B1A3A;
            font-weight: 800;
            font-size: 1.05rem;
            padding: 6px 14px;
            border-radius: 6px;
            display: inline-block;
        }
        div[data-testid="stPageLink"] a {
            font-weight: 600;
            color: #334155 !important;
            font-size: 0.95rem;
        }
        div[data-testid="stPageLink"] a:hover { color: #DC2626 !important; }

        div.stButton > button {
            border-radius: 8px;
            font-weight: 700;
            padding: 0.45rem 1.1rem;
        }

        /* ---------- Sayfa başlık bandı (her sayfada page_header() ile kullanılır) ---------- */
        .page-header-wrap {
            background: linear-gradient(135deg, #0B1A3A 0%, #0F2350 100%);
            border-radius: 14px;
            padding: 1.5rem 1.8rem;
            margin-bottom: 1.8rem;
            color: #FFFFFF;
        }
        .page-header-title { font-size: 1.7rem; font-weight: 800; margin: 0; }
        .page-header-sub { color: #C7D2E8; margin-top: 0.4rem; font-size: 0.95rem; }

        /* ---------- Genel panel/kart kutusu ---------- */
        .panel-card {
            background: #FFFFFF;
            border: 1px solid #E5E9F2;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 4px 18px rgba(15,23,42,0.05);
            margin-bottom: 1.2rem;
        }

        /* Streamlit uyarı kutularının köşelerini yumuşat */
        div[data-testid="stAlert"] { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

def render_navbar(active: str = "Home"):
    _inject_global_style()

    page_map = {
    "Home": "home.py",
    "Patient Analysis": "pages/patient.py",
    "Risk Dashboard": "pages/risk_dashboard.py"}

    logo_col, *nav_cols, status_col = st.columns(
        [1.3] + [1] * len(page_map) + [1.4]
    )

    with logo_col:
        st.markdown(
            '<span class="navbar-logo">⚕️ MEDIGUARD</span>',
            unsafe_allow_html=True
        )

    for col, (label, path) in zip(nav_cols, page_map.items()):
        with col:
            st.page_link(path, label=label)

    with status_col:
        st.markdown(
            '<div style="text-align:right; padding-top:0.4rem;">'
            '<span style="color:#16A34A; font-weight:700; font-size:0.85rem;">'
            '● Sistem Aktif</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<hr style="margin-top:-0.6rem; margin-bottom:1.2rem; '
        'border-color:#EEF1F6;">',
        unsafe_allow_html=True
    )

def page_header(title: str, subtitle: str = None, icon: str = "⚕️"):
    """Her sayfanın en üstünde st.title() yerine kullanılacak ortak lacivert başlık bandı."""
    sub_html = f'<div class="page-header-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="page-header-wrap">
        <div class="page-header-title">{icon} {title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)