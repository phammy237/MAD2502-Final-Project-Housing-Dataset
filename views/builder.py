import streamlit as st
from backend.constants import MODES, STATE_MULTIPLIERS, AMES_AVERAGES
from backend.model import predict


def _tip(msg, color):
    st.markdown(f"""
    <div style="background:{color}12; border-left:3px solid {color};
                padding:0.5rem 0.8rem; border-radius:0 8px 8px 0;
                font-size:0.8rem; color:#374151; margin:0.3rem 0">
        💡 {msg}
    </div>
    """, unsafe_allow_html=True)


def render():
    mode   = st.session_state.get("mode", "🌱 Beginner")
    budget = st.session_state.get("budget", 250_000)
    cfg    = MODES[mode]
    color  = cfg["color"]
    tips   = cfg["show_tips"]

    # Nav header
    back, title = st.columns([1, 7])
    with back:
        if st.button("← Back"):
            st.session_state.page = "landing"
            st.rerun()
    with title:
        st.markdown(f"## {cfg['emoji']} {cfg['label']} Mode &nbsp;·&nbsp; Budget: **${budget:,}**")

    st.markdown("---")
    col_in, col_prev = st.columns([3, 2], gap="large")

    with col_in:
        st.markdown("### Configure Your House")

        prev_inputs = st.session_state.get("inputs", {})
        area = st.slider("📐 Living Area (sq ft)", 600, 5000,
                         prev_inputs.get("area", cfg["default_area"]), 50)
        if tips:
            pct = int((area / AMES_AVERAGES["area"] - 1) * 100)
            if area > AMES_AVERAGES["area"] * 1.25:
                _tip(f"That's {pct}% larger than the average Ames home.", color)
            elif area < 1000:
                _tip("Under 1,000 sq ft is compact — great for budget efficiency.", color)

        quality = st.slider("⭐ Quality Score (1–10)", 1, 10,
                            prev_inputs.get("quality", cfg["default_quality"]))
        if tips:
            if quality <= 4:
                _tip("Low quality significantly reduces predicted value — it's your #1 price driver.", color)
            elif quality >= 9:
                _tip("Premium quality! Top-tier finishes command the highest market premiums.", color)

        bedrooms  = st.select_slider("🛏️ Bedrooms",
                                     options=[1, 2, 3, 4, 5, 6],
                                     value=prev_inputs.get("bedrooms", 3))
        bathrooms = st.select_slider("🛁 Bathrooms",
                                     options=[1, 2, 3, 4, 5],
                                     value=prev_inputs.get("bathrooms", 2))

        year = st.slider("🔨 Year Built", 1900, 2024,
                         prev_inputs.get("year", 2000))
        if tips:
            if year < 1960:
                _tip("Vintage builds have charm but typically higher maintenance costs.", color)
            elif year >= 2010:
                _tip("Modern construction commands a price premium in most markets.", color)

        state = st.selectbox("📍 State",
                             list(STATE_MULTIPLIERS.keys()),
                             index=list(STATE_MULTIPLIERS.keys()).index(
                                 prev_inputs.get("state", "Iowa — Ames (Baseline)")))
        multiplier = STATE_MULTIPLIERS[state]

        if tips and multiplier > 2.0:
            _tip(f"{state} carries a {multiplier:.1f}× market multiplier vs. Iowa baseline.", color)

    with col_prev:
        st.markdown("### Live Preview")

        live  = predict(area, quality, bedrooms, bathrooms, year, multiplier)
        delta = budget - live
        over  = live > budget

        bar_color = "#EF4444" if over else ("#F59E0B" if live > budget * 0.93 else "#10B981")
        status    = "▲ Over budget" if over else ("⚠️ Near limit" if live > budget * 0.93 else "✅ Under budget")
        delta_txt = f"${-delta:,.0f} over" if over else f"${delta:,.0f} remaining"

        st.markdown(f"""
        <div style="background:white; border:2px solid {bar_color}; border-radius:16px;
                    padding:1.5rem; text-align:center;
                    box-shadow:0 4px 20px rgba(0,0,0,0.07); margin-bottom:1rem">
            <div style="font-size:0.82rem; color:#6B7280; margin-bottom:0.2rem">
                Estimated Market Value
            </div>
            <div style="font-size:2.2rem; font-weight:800; color:{bar_color}">
                ${live:,.0f}
            </div>
            <div style="font-size:0.88rem; color:{bar_color}; margin-top:0.3rem">{status}</div>
            <div style="font-size:0.78rem; color:#9CA3AF; margin-top:0.15rem">{delta_txt}</div>
        </div>
        """, unsafe_allow_html=True)

        # Budget usage bar
        pct_used = min(live / budget, 1.5)
        bar_w    = min(pct_used, 1.0) * 100
        st.markdown(f"""
        <div style="margin-bottom:1rem">
            <div style="display:flex; justify-content:space-between;
                        font-size:0.72rem; color:#9CA3AF; margin-bottom:0.25rem">
                <span>$0</span><span>${budget:,}</span>
            </div>
            <div style="background:#F3F4F6; border-radius:8px; height:9px">
                <div style="background:{bar_color}; width:{bar_w:.1f}%;
                            height:100%; border-radius:8px"></div>
            </div>
            <div style="text-align:right; font-size:0.72rem; color:{bar_color}; margin-top:0.15rem">
                {pct_used*100:.1f}% of budget
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Mode-specific bonus metric
        if mode == "📈 Investor":
            roi = (live - budget) / budget * 100
            st.metric("Equity Position", f"{roi:+.1f}%",
                      help="Predicted value vs. your purchase price (budget)")
        elif mode == "💎 Luxury":
            prestige = min(int(quality / 10 * 60 + area / 5000 * 40), 100)
            st.metric("Prestige Score", f"{prestige}/100")
        else:
            r = 0.065 / 12
            n = 360
            mo = (budget * 0.80) * r / (1 - (1 + r) ** -n)
            st.metric("Est. Monthly Mortgage", f"${mo:,.0f}",
                      help="30-yr fixed, 20% down, 6.5% rate")

        if multiplier != 1.0:
            st.caption(f"📍 {state}: {multiplier:.2f}× market multiplier applied")

    st.markdown("---")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("🏗️  Build My House", use_container_width=True, type="primary"):
            st.session_state.inputs = {
                "area":             area,
                "quality":          quality,
                "bedrooms":         bedrooms,
                "bathrooms":        bathrooms,
                "year":             year,
                "state":            state,
                "state_multiplier": multiplier,
            }
            st.session_state.page = "building"
            st.rerun()
