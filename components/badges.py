import streamlit as st

BADGE_DEFS = {
    "🎯 Budget Master": {
        "check":  lambda r: r["prediction"] <= r["budget"] * 1.02,
        "desc":   "Stayed within 2% of budget",
        "rarity": "Common", "color": "#607D8B",
    },
    "💎 Luxury Builder": {
        "check":  lambda r: r["inputs"]["quality"] >= 9,
        "desc":   "Built at the highest quality tier",
        "rarity": "Rare", "color": "#7B1FA2",
    },
    "🏠 First-Time Buyer": {
        "check":  lambda r: r["mode"] == "🌱 Beginner" and r["budget"] <= 300_000,
        "desc":   "First home under $300k",
        "rarity": "Common", "color": "#388E3C",
    },
    "📈 House Flipper": {
        "check":  lambda r: r["prediction"] > r["budget"] * 1.20,
        "desc":   "Predicted value 20%+ above budget",
        "rarity": "Uncommon", "color": "#1565C0",
    },
    "🏦 Savvy Investor": {
        "check":  lambda r: r["mode"] == "📈 Investor" and r["score"] >= 75,
        "desc":   "Top-tier ROI in Investor mode",
        "rarity": "Uncommon", "color": "#00838F",
    },
    "👑 Prestige": {
        "check":  lambda r: r["inputs"]["quality"] == 10 and r["inputs"]["area"] >= 3000,
        "desc":   "Max quality + 3,000 sq ft",
        "rarity": "Legendary", "color": "#F9A825",
    },
    "🕰️ Vintage Charm": {
        "check":  lambda r: r["inputs"]["year"] < 1960,
        "desc":   "Built before 1960 — classic character",
        "rarity": "Uncommon", "color": "#6D4C41",
    },
    "🚀 Space Commander": {
        "check":  lambda r: r["inputs"]["area"] >= 3500,
        "desc":   "3,500+ sq ft of living space",
        "rarity": "Uncommon", "color": "#283593",
    },
    "🏆 Dream Home": {
        "check":  lambda r: r["score"] >= 90,
        "desc":   "Scored 90+ — the perfect build",
        "rarity": "Legendary", "color": "#E65100",
    },
    "🔬 Minimalist Genius": {
        "check":  lambda r: r["inputs"]["area"] < 1500 and r["inputs"]["quality"] >= 8,
        "desc":   "Small footprint, premium quality",
        "rarity": "Rare", "color": "#00695C",
    },
}


def award_badges(prediction, budget, inputs, score, mode):
    ctx = {"prediction": prediction, "budget": budget,
           "inputs": inputs, "score": score, "mode": mode}
    return [name for name, b in BADGE_DEFS.items() if b["check"](ctx)]


def render_badges(badge_names):
    if not badge_names:
        st.caption("No badges yet — keep building to unlock them!")
        return
    n_cols = min(len(badge_names), 4)
    cols = st.columns(n_cols)
    for i, name in enumerate(badge_names):
        b = BADGE_DEFS.get(name, {})
        color = b.get("color", "#555")
        with cols[i % n_cols]:
            st.markdown(f"""
            <div style="
                border: 2px solid {color};
                border-radius: 14px;
                padding: 1rem 0.75rem;
                text-align: center;
                background: linear-gradient(135deg, {color}18, {color}06);
                margin-bottom: 0.5rem;
                min-height: 130px;
            ">
                <div style="font-size:1.8rem">{name.split()[0]}</div>
                <div style="font-weight:700; color:{color}; font-size:0.85rem; margin:0.25rem 0">
                    {" ".join(name.split()[1:])}
                </div>
                <div style="color:#888; font-size:0.68rem">{b.get("rarity","")}</div>
                <div style="color:#555; font-size:0.72rem; margin-top:0.25rem; line-height:1.3">
                    {b.get("desc","")}
                </div>
            </div>
            """, unsafe_allow_html=True)
