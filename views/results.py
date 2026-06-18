import streamlit as st
import pandas as pd
from backend.constants import MODES, AMES_AVERAGES, SCORE_TIERS
from components.badges import render_badges
from components.charts import score_gauge, contribution_bar, comparison_bar

FEATURE_LABELS = {
    "Gr Liv Area":   "Living Area",
    "Overall Qual":  "Quality Score",
    "Bedroom AbvGr": "Bedrooms",
    "Full Bath":     "Bathrooms",
    "Year Built":    "Year Built",
}


def _tier(score):
    for threshold, label, color, msg in SCORE_TIERS:
        if score >= threshold:
            return label, color, msg
    return SCORE_TIERS[-1][1:]


def render():
    mode       = st.session_state.mode
    budget     = st.session_state.budget
    prediction = st.session_state.prediction
    fin        = st.session_state.fin
    score      = st.session_state.score
    badges     = st.session_state.badges
    inputs     = st.session_state.inputs
    contribs   = st.session_state.contributions
    recs       = st.session_state.recommendations

    tier_label, tier_color, tier_msg = _tier(score)
    delta = budget - prediction
    over  = prediction > budget

    # Header row
    back, hdr = st.columns([1, 8])
    with back:
        if st.button("← Rebuild"):
            st.session_state.page = "builder"
            st.rerun()
    with hdr:
        st.markdown("## 🏠 Your House is Ready!")

    # Top metric strip
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Predicted Value",  f"${prediction:,.0f}")
    m2.metric("Budget",           f"${budget:,}",
              delta=f"${delta:,.0f} remaining" if not over else f"${-delta:,.0f} over budget",
              delta_color="normal" if not over else "inverse")
    m3.metric("Your Score",       f"{score} / 100")
    m4.metric("Badges Earned",    str(len(badges)))

    # Score tier banner
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{tier_color}22,{tier_color}0a);
                border:1.5px solid {tier_color}55; border-radius:12px;
                padding:0.9rem 1.5rem; margin:1rem 0; text-align:center">
        <span style="font-size:1.35rem; font-weight:800; color:{tier_color}">{tier_label}</span>
        <span style="color:#4B5563; margin-left:1rem; font-size:0.95rem">{tier_msg}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Insights", "💡 Recommendations"])

    # ── TAB 1: Overview ────────────────────────────────────────────────────────
    with tab1:
        left, right = st.columns([2, 3], gap="large")

        with left:
            st.plotly_chart(score_gauge(score), use_container_width=True)
            st.markdown("#### 🏆 Badges")
            render_badges(badges)

        with right:
            st.markdown("#### 💰 Financial Breakdown")
            rows = [
                ("Purchase Price (Budget)",      f"${budget:,}"),
                ("Closing Costs (3%)",            f"${fin['closing']:,.0f}"),
                ("Annual Property Tax (1.2%)",    f"${fin['tax']:,.0f}"),
                ("Annual Maintenance (1%)",       f"${fin['maint']:,.0f}"),
                ("── Total Year 1 Cash Outlay",   f"${fin['year1_total']:,.0f}"),
                ("Est. Monthly Mortgage",         f"${fin['mortgage']:,.0f} / mo"),
                ("Appraised Market Value",        f"${prediction:,.0f}"),
                ("Immediate Equity",              f"${fin['equity']:+,.0f}"),
            ]
            df = pd.DataFrame(rows, columns=["Item", "Amount"])
            st.dataframe(df, hide_index=True, use_container_width=True)

            if over:
                st.error(f"⚠️ ${-delta:,.0f} over budget — see Recommendations to trim.")
            else:
                st.success(f"✅ ${delta:,.0f} under budget. Well managed!")

            st.markdown("#### 🏠 Your Build at a Glance")
            s = inputs
            st.markdown(f"""
| Feature | Your Choice | Ames Average |
|---------|------------|--------------|
| Living Area | {s['area']:,} sq ft | {AMES_AVERAGES['area']:,} sq ft |
| Quality | {s['quality']}/10 | {AMES_AVERAGES['quality']}/10 |
| Bedrooms | {s['bedrooms']} | {AMES_AVERAGES['bedrooms']} |
| Bathrooms | {s['bathrooms']} | {AMES_AVERAGES['bathrooms']} |
| Year Built | {s['year']} | {AMES_AVERAGES['year']} |
| State | {s['state']} | Iowa (Ames) |
""")

    # ── TAB 2: Insights ────────────────────────────────────────────────────────
    with tab2:
        st.markdown("#### 📈 What's Driving Your Price?")
        st.plotly_chart(contribution_bar(contribs), use_container_width=True)

        top_feat = max(contribs, key=contribs.get)
        top_name = FEATURE_LABELS.get(top_feat, top_feat)
        top_pct  = contribs[top_feat]
        extra = ("Raising it by one point adds ~$26,000 to predicted value."
                 if top_feat == "Overall Qual" else
                 "Adjusting this feature has the most leverage on your price.")

        st.markdown(f"""
        <div style="background:#EEF2FF; border-left:4px solid #4F46E5;
                    border-radius:0 12px 12px 0; padding:1rem 1.25rem; margin:0.75rem 0">
            <strong>💡 Key Insight:</strong> <strong>{top_name}</strong> accounts for
            <strong>{top_pct:.1f}%</strong> of your predicted price. {extra}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🏘️ You vs. The Ames Market")
        st.plotly_chart(comparison_bar(prediction, AMES_AVERAGES["price"]),
                        use_container_width=True)
        diff_pct = (prediction - AMES_AVERAGES["price"]) / AMES_AVERAGES["price"] * 100
        direction = "above" if diff_pct > 0 else "below"
        st.caption(f"Your predicted price is {abs(diff_pct):.1f}% {direction} the Ames "
                   f"market average of ${AMES_AVERAGES['price']:,}.")

        with st.expander("🔬 Model Explainability"):
            st.markdown("""
**How this works:** Ordinary Least Squares (Normal Equation) linear regression trained on 2,930
Ames, Iowa home sales (2006–2010).

**Formula:** `Price = β₀ + β₁·Area + β₂·Quality + β₃·Bedrooms + β₄·Bathrooms + β₅·Year`

**Normal Equation:** `β = (XᵀX)⁻¹ Xᵀy`

**Why bedrooms/bathrooms can show negative coefficients:** Multicollinearity — when holding square
footage constant, more bedrooms implies smaller rooms, which correlates with lower prices in the
Ames data. This is mathematically correct, not a bug.

**State multipliers** are approximate cost-of-living adjustments applied to the Iowa baseline.
All predictions are for educational purposes only.
""")

    # ── TAB 3: Recommendations ─────────────────────────────────────────────────
    with tab3:
        st.markdown("#### 💡 How to Level Up Your Build")

        for rec in recs:
            icon  = rec.get("icon", "💡")
            title = rec.get("title", "")
            gain  = rec.get("gain")
            stars = rec.get("stars")
            why   = rec.get("why", "")

            gain_html  = (f"<div style='font-size:0.83rem;color:#10B981;font-weight:600;"
                          f"margin:0.3rem 0'>Value gain: +${gain:,.0f}</div>")  \
                          if (gain and gain > 0) else ""
            stars_html = "⭐" * int(stars) if stars else ""

            st.markdown(f"""
            <div style="background:white; border:1.5px solid #E5E7EB; border-radius:14px;
                        padding:1.2rem 1.4rem; margin-bottom:0.8rem;
                        box-shadow:0 2px 8px rgba(0,0,0,0.05)">
                <div style="display:flex; align-items:center; margin-bottom:0.4rem">
                    <span style="font-size:1.35rem; margin-right:0.55rem">{icon}</span>
                    <span style="font-size:0.97rem; font-weight:700; color:#1F2937">{title}</span>
                    <span style="margin-left:auto; font-size:0.82rem">{stars_html}</span>
                </div>
                {gain_html}
                <div style="font-size:0.83rem; color:#4B5563; line-height:1.55">{why}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            if st.button("🔄  Rebuild with New Settings", use_container_width=True):
                st.session_state.page = "builder"
                st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:3rem; color:#9CA3AF; font-size:0.7rem;
                border-top:1px solid #E5E7EB; padding-top:1.25rem">
        Build Your Dream House · OLS Regression · Ames Housing Dataset (2006–2010) ·
        For educational purposes only
    </div>
    """, unsafe_allow_html=True)
