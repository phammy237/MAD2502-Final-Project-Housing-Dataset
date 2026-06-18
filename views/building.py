import time
import streamlit as st
from backend.constants import CONSTRUCTION_MESSAGES
from backend.model import predict, get_financials
from components.scoring import compute_score, get_contributions, get_recommendations
from components.badges import award_badges


def render():
    _, center, _ = st.columns([1, 3, 1])
    with center:
        st.markdown("""
        <div style="text-align:center; padding:3rem 0 1.5rem">
            <div style="font-size:4rem">🏗️</div>
            <h2 style="color:#1F2937">Building your house...</h2>
            <p style="color:#6B7280">Hang tight — our model is crunching the numbers.</p>
        </div>
        """, unsafe_allow_html=True)

        bar    = st.progress(0)
        status = st.empty()
        msgs   = CONSTRUCTION_MESSAGES

        for i, msg in enumerate(msgs):
            status.markdown(
                f"<div style='text-align:center;font-size:1.05rem;color:#374151'>{msg}</div>",
                unsafe_allow_html=True,
            )
            bar.progress((i + 1) / len(msgs))
            time.sleep(0.32)

        time.sleep(0.5)

    inputs = st.session_state.inputs
    budget = st.session_state.budget
    mode   = st.session_state.mode

    pred = predict(**inputs)
    st.session_state.prediction      = pred
    st.session_state.fin             = get_financials(pred, budget)
    st.session_state.score           = compute_score(pred, budget, inputs, mode)
    st.session_state.badges          = award_badges(pred, budget, inputs,
                                                    st.session_state.score, mode)
    st.session_state.contributions   = get_contributions(inputs)
    st.session_state.recommendations = get_recommendations(inputs, pred, budget, mode)
    st.session_state.page            = "results"
    st.rerun()
