import plotly.graph_objects as go


def score_gauge(score):
    if score >= 90:   color = "#FFD700"
    elif score >= 75: color = "#4CAF50"
    elif score >= 55: color = "#2196F3"
    elif score >= 35: color = "#FF9800"
    else:             color = "#F44336"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "/100", "font": {"size": 30, "color": color}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#ddd"},
            "bar":  {"color": color, "thickness": 0.28},
            "bgcolor": "white",
            "steps": [
                {"range": [0,  35], "color": "#FFEBEE"},
                {"range": [35, 55], "color": "#FFF3E0"},
                {"range": [55, 75], "color": "#E3F2FD"},
                {"range": [75, 90], "color": "#E8F5E9"},
                {"range": [90,100], "color": "#FFFDE7"},
            ],
            "threshold": {"line": {"color": color, "width": 4},
                          "thickness": 0.8, "value": score},
        },
        title={"text": "Dream Home Score", "font": {"size": 14, "color": "#6B7280"}},
    ))
    fig.update_layout(
        margin=dict(t=60, b=0, l=20, r=20), height=240,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def contribution_bar(contributions):
    labels = {
        "Gr Liv Area":   "Living Area",
        "Overall Qual":  "Quality Score",
        "Bedroom AbvGr": "Bedrooms",
        "Full Bath":     "Bathrooms",
        "Year Built":    "Year Built",
    }
    items  = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
    names  = [labels.get(k, k) for k, _ in items]
    values = [round(v, 1) for _, v in items]
    colors = ["#4F46E5", "#7C3AED", "#2563EB", "#0891B2", "#059669"]

    fig = go.Figure(go.Bar(
        x=values, y=names, orientation="h",
        marker_color=colors[:len(names)],
        text=[f"{v:.1f}%" for v in values],
        textposition="outside", cliponaxis=False,
    ))
    fig.update_layout(
        title={"text": "Value Drivers", "font": {"size": 14}},
        xaxis=dict(title="% Contribution", range=[0, max(values) * 1.3]),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=70, t=40, b=10), height=240,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    return fig


def comparison_bar(your_price, avg_price):
    fig = go.Figure(data=[
        go.Bar(name="Your Build",   x=["Market Value"], y=[your_price], marker_color="#4F46E5"),
        go.Bar(name="Ames Average", x=["Market Value"], y=[avg_price],  marker_color="#D1D5DB"),
    ])
    fig.update_layout(
        barmode="group",
        title={"text": "You vs. Ames Average", "font": {"size": 14}},
        yaxis=dict(tickprefix="$", tickformat=","),
        margin=dict(l=10, r=10, t=40, b=10), height=220,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return fig
