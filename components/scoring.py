from backend.model import load_model, FEATURES


def compute_score(prediction, budget, inputs, mode):
    score = 0.0

    # Budget efficiency (40 pts) — peaks at 95–100% of budget
    usage = prediction / budget
    if usage <= 1.00:
        score += 40 * min(usage / 0.95, 1.0)
    elif usage <= 1.05:
        score += 40 * (1 - (usage - 1.0) / 0.05)

    # Quality (20 pts)
    score += (inputs["quality"] / 10) * 20

    # Value-per-dollar (20 pts)
    score += min((prediction / budget) * 20, 20)

    # Year freshness (10 pts)
    score += ((inputs["year"] - 1900) / (2024 - 1900)) * 10

    # Space efficiency (10 pts) — sweet spot 1200–2500 sqft
    area = inputs["area"]
    if 1200 <= area <= 2500:
        score += 10
    elif area < 1200:
        score += (area / 1200) * 10
    else:
        score += max(0.0, 10 - (area - 2500) / 500)

    mult = {"🌱 Beginner": 1.0, "📈 Investor": 1.1, "💎 Luxury": 1.25}.get(mode, 1.0)
    return min(round(score * mult), 100)


def get_contributions(inputs):
    theta = load_model()
    coefs = {f: float(theta[i + 1]) for i, f in enumerate(FEATURES)}
    vals = {
        "Gr Liv Area":   inputs["area"],
        "Overall Qual":  inputs["quality"],
        "Bedroom AbvGr": inputs["bedrooms"],
        "Full Bath":     inputs["bathrooms"],
        "Year Built":    inputs["year"],
    }
    raw = {f: abs(coefs[f] * vals[f]) for f in FEATURES}
    total = sum(raw.values()) or 1
    return {f: raw[f] / total * 100 for f in FEATURES}


def get_recommendations(inputs, prediction, budget, mode):
    theta = load_model()
    coef_qual = float(theta[2])
    coef_area = float(theta[1])
    coef_year = float(theta[5])

    recs = []

    if inputs["quality"] < 9:
        recs.append({
            "icon": "⭐", "stars": 5,
            "title": f"Raise Quality {inputs['quality']} → {inputs['quality'] + 1}",
            "gain": coef_qual,
            "why": f"Quality is your #1 price driver. Each point adds ~${coef_qual:,.0f} "
                   f"to your predicted value — a design choice, not a cost.",
        })

    if prediction < budget * 0.88:
        area_gain = 200 * coef_area
        recs.append({
            "icon": "📐", "stars": 4,
            "title": "Add 200 sq ft of living area",
            "gain": area_gain,
            "why": f"You have headroom in your budget. 200 extra sq ft adds ~${area_gain:,.0f} "
                   f"to predicted value and market appeal.",
        })

    if prediction > budget * 1.02:
        over = prediction - budget
        sqft_cut = max(int(over / abs(coef_area)), 1)
        recs.append({
            "icon": "✂️", "stars": 0,
            "title": "Trim to stay under budget",
            "gain": 0,
            "why": f"You're ${over:,.0f} over budget. Reducing area by ~{sqft_cut:,} sq ft "
                   f"or lowering quality by one tier brings you back in range.",
        })

    if inputs["year"] < 1985:
        year_gain = (2000 - inputs["year"]) * coef_year
        recs.append({
            "icon": "🔨", "stars": 3,
            "title": f"Build newer (2000 vs {inputs['year']})",
            "gain": year_gain,
            "why": f"Each year of construction age costs ~${coef_year:,.0f} in predicted value. "
                   f"Newer builds also carry lower maintenance.",
        })

    if mode == "📈 Investor":
        roi = (prediction - budget) / budget * 100
        recs.append({
            "icon": "📈", "stars": None,
            "title": "Investor Thesis",
            "gain": None,
            "why": f"Your build shows a {'positive' if roi >= 0 else 'negative'} equity position "
                   f"of {abs(roi):.1f}% vs. budget. Quality 8+ Ames homes appreciate ~12% faster.",
        })

    return recs[:4]
