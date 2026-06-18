import streamlit as st

st.set_page_config(
    page_title="Build Your Dream House",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Global styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px; }

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: transform 0.1s ease, box-shadow 0.1s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    border: none;
    color: white;
    font-size: 1.05rem;
    padding: 0.65rem 1rem;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    border: 1px solid #F3F4F6;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    font-weight: 600;
}

/* Dataframe */
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Hide Streamlit default menu/footer for cleaner presentation */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Session state defaults
_DEFAULTS = {
    "page":            "landing",
    "mode":            "🌱 Beginner",
    "budget":          250_000,
    "inputs":          {},
    "prediction":      None,
    "fin":             None,
    "score":           None,
    "badges":          [],
    "contributions":   {},
    "recommendations": [],
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Router
page = st.session_state.page

if page == "landing":
    from views.landing import render
elif page == "builder":
    from views.builder import render
elif page == "building":
    from views.building import render
elif page == "results":
    from views.results import render
else:
    from views.landing import render

render()
