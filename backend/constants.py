STATE_MULTIPLIERS = {
    "Iowa — Ames (Baseline)": 1.00,
    "Alabama": 0.85, "Alaska": 1.50, "Arizona": 1.40, "Arkansas": 0.80,
    "California": 2.85, "Colorado": 1.80, "Connecticut": 1.90, "Delaware": 1.55,
    "Florida": 1.55, "Georgia": 1.25, "Hawaii": 3.20, "Idaho": 1.35,
    "Illinois": 1.50, "Indiana": 1.00, "Iowa": 1.00, "Kansas": 0.90,
    "Kentucky": 0.90, "Louisiana": 0.95, "Maine": 1.20, "Maryland": 1.85,
    "Massachusetts": 2.20, "Michigan": 1.10, "Minnesota": 1.30, "Mississippi": 0.75,
    "Missouri": 0.95, "Montana": 1.15, "Nebraska": 0.95, "Nevada": 1.45,
    "New Hampshire": 1.65, "New Jersey": 2.40, "New Mexico": 1.05, "New York": 2.60,
    "North Carolina": 1.20, "North Dakota": 0.90, "Ohio": 1.10, "Oklahoma": 0.85,
    "Oregon": 1.75, "Pennsylvania": 1.40, "Rhode Island": 1.80, "South Carolina": 1.10,
    "South Dakota": 0.90, "Tennessee": 1.15, "Texas": 1.45, "Utah": 1.60,
    "Vermont": 1.45, "Virginia": 1.70, "Washington": 2.10, "West Virginia": 0.75,
    "Wisconsin": 1.15, "Wyoming": 1.10, "Washington D.C.": 3.00,
}

AMES_AVERAGES = {
    "area": 1516, "quality": 6, "bedrooms": 3,
    "bathrooms": 2, "year": 1971, "price": 181_000,
}

CONSTRUCTION_MESSAGES = [
    "📐 Drawing up the blueprints...",
    "🪨 Pouring the foundation...",
    "🧱 Laying the brickwork...",
    "🔧 Roughing in the plumbing...",
    "⚡ Wiring the electrical...",
    "🪵 Framing the walls...",
    "🪟 Installing the windows...",
    "🛁 Tiling the bathrooms...",
    "🎨 Painting the walls...",
    "🔑 Installing the finishing touches...",
    "🏠 Running the appraisal...",
    "📊 Crunching 2,930 Ames home sales...",
]

MODES = {
    "🌱 Beginner": {
        "emoji": "🌱", "label": "Beginner",
        "tagline": "First home, guided experience",
        "color": "#4CAF50", "light": "#E8F5E9",
        "default_budget": 250_000, "default_quality": 5, "default_area": 1500,
        "show_tips": True,
    },
    "📈 Investor": {
        "emoji": "📈", "label": "Investor",
        "tagline": "ROI-focused, data-driven",
        "color": "#1565C0", "light": "#E3F2FD",
        "default_budget": 500_000, "default_quality": 7, "default_area": 2000,
        "show_tips": True,
    },
    "💎 Luxury": {
        "emoji": "💎", "label": "Luxury",
        "tagline": "No limits. Pure quality.",
        "color": "#B8860B", "light": "#FFFDE7",
        "default_budget": 1_000_000, "default_quality": 9, "default_area": 3000,
        "show_tips": False,
    },
}

SCORE_TIERS = [
    (90, "🏆 Dream Home",  "#FFD700", "You nailed it. This is the one."),
    (75, "✨ Smart Build",  "#4CAF50", "Solid choices — your future self approves."),
    (55, "👍 Good Start",  "#2196F3", "On the right track. A few tweaks could go a long way."),
    (35, "🔨 Needs Work",  "#FF9800", "The bones are there. Let's talk renovations."),
    (0,  "🏚️ Fixer Upper", "#F44336", "It's got... character."),
]
