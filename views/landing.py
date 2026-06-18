import streamlit as st
from backend.constants import MODES


def render():
    st.markdown("""
    <div style="text-align:center; padding:3rem 0 2rem 0">
        <div style="font-size:3.5rem">🏠</div>
        <h1 style="font-size:2.6rem; font-weight:800; color:#1F2937; margin:0.25rem 0">
            Build Your Dream House
        </h1>
        <p style="font-size:1.05rem; color:#6B7280; margin:0.4rem 0">
            Powered by linear regression · Ames Housing Dataset (2,930 homes)
        </p>
        <p style="font-size:1rem; color:#9CA3AF; font-style:italic">
            "How far can your budget really take you?"
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Choose Your Mode")
    cols = st.columns(3)
    current = st.session_state.get("mode", "🌱 Beginner")

    for col, (key, cfg) in zip(cols, MODES.items()):
        selected = current == key
        border = f"3px solid {cfg['color']}" if selected else "2px solid #E5E7EB"
        bg     = cfg["light"] if selected else "white"
        check  = f"<div style='color:{cfg['color']};font-size:0.78rem;font-weight:700;margin-top:0.4rem'>✓ Selected</div>" if selected else ""
        with col:
            st.markdown(f"""
            <div style="border:{border}; border-radius:16px; padding:1.5rem; background:{bg};
                        text-align:center; min-height:155px; transition:all 0.2s">
                <div style="font-size:2.4rem">{cfg['emoji']}</div>
                <div style="font-size:1.15rem; font-weight:700; color:#1F2937; margin:0.4rem 0 0.2rem">
                    {cfg['label']}
                </div>
                <div style="font-size:0.82rem; color:#6B7280">{cfg['tagline']}</div>
                {check}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {cfg['label']}", key=f"sel_{key}",
                         use_container_width=True):
                st.session_state.mode = key
                st.session_state.budget = cfg["default_budget"]
                st.rerun()

    st.markdown("---")
    st.markdown("### Set Your Budget")

    b1, b2, b3, b4 = st.columns([1, 1, 1, 1.6])
    with b1:
        if st.button("$250,000", use_container_width=True):
            st.session_state.budget = 250_000
            st.rerun()
    with b2:
        if st.button("$500,000", use_container_width=True):
            st.session_state.budget = 500_000
            st.rerun()
    with b3:
        if st.button("$1,000,000", use_container_width=True):
            st.session_state.budget = 1_000_000
            st.rerun()
    with b4:
        custom = st.number_input(
            "Custom", min_value=50_000, max_value=10_000_000,
            value=st.session_state.get("budget", 250_000),
            step=5_000, label_visibility="collapsed",
            placeholder="Custom amount",
        )
        st.session_state.budget = int(custom)

    budget = st.session_state.get("budget", 250_000)
    st.markdown(f"""
    <div style="text-align:center; margin:1rem 0; padding:0.85rem;
                background:#F3F4F6; border-radius:12px;">
        <span style="font-size:1.5rem; font-weight:700; color:#1F2937">
            Budget: ${budget:,}
        </span>
    </div>
    """, unsafe_allow_html=True)

    _, cta, _ = st.columns([1, 2, 1])
    with cta:
        if st.button("🏗️  Let's Build →", use_container_width=True, type="primary"):
            st.session_state.page = "builder"
            st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:3rem; color:#9CA3AF; font-size:0.73rem">
        Model trained on 2,930 Ames, Iowa home sales (2006–2010) ·
        State adjustments apply a cost-of-living multiplier · For educational purposes
    </div>
    """, unsafe_allow_html=True)
