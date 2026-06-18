from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

FEATURES = ["Gr Liv Area", "Overall Qual", "Bedroom AbvGr", "Full Bath", "Year Built"]
TARGET = "SalePrice"

# Fallback coefficients derived from the Ames Normal Equation model
_FALLBACK_THETA = np.array([
    [-1_057_032.0],
    [       63.2],   # Gr Liv Area ($/sqft)
    [   26_000.0],   # Overall Qual ($/point)
    [  -11_350.0],   # Bedroom AbvGr
    [   -6_613.0],   # Full Bath
    [      524.0],   # Year Built ($/year)
])


@st.cache_resource(show_spinner="Training model on Ames Housing data...")
def load_model():
    base = Path(__file__).parent.parent
    candidates = [
        base / "MAD Final Project Housing Dataset" / "data" / "AmesHousing.csv",
        base / "data" / "AmesHousing.csv",
        Path.cwd() / "MAD Final Project Housing Dataset" / "data" / "AmesHousing.csv",
        Path.cwd() / "data" / "AmesHousing.csv",
    ]
    csv_path = next((p for p in candidates if p.exists()), None)

    if csv_path is None:
        return _FALLBACK_THETA

    df = pd.read_csv(csv_path)
    df = df.drop_duplicates()
    df = df.drop(columns=df.columns[df.isnull().mean() > 0.5].tolist())
    for c in df.select_dtypes(include="number").columns:
        df[c] = df[c].fillna(df[c].median())

    if any(c not in df.columns for c in FEATURES + [TARGET]):
        return _FALLBACK_THETA

    mdf = df[FEATURES + [TARGET]].dropna()
    X = mdf[FEATURES].astype(float).values
    y = mdf[TARGET].astype(float).values.reshape(-1, 1)
    Xd = np.hstack([np.ones((len(X), 1)), X])
    return np.linalg.pinv(Xd) @ y


def predict(area, quality, bedrooms, bathrooms, year, state_multiplier, **_):
    theta = load_model()
    x = np.array([[1, area, quality, bedrooms, bathrooms, year]], dtype=float)
    base = float((x @ theta).item())
    return max(base * state_multiplier, 50_000)


def get_financials(predicted, budget):
    closing = budget * 0.03
    tax = predicted * 0.012
    maint = predicted * 0.01
    r = 0.065 / 12
    n = 360
    mortgage = (budget * 0.80) * r / (1 - (1 + r) ** -n)
    equity = predicted - budget
    return {
        "closing":    closing,
        "tax":        tax,
        "maint":      maint,
        "mortgage":   mortgage,
        "year1_total": budget + closing + tax + maint,
        "equity":     equity,
    }
