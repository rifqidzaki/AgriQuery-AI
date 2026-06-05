# ════════════════════════════════════════════════════════════════
# CHARTS — Plotly Chart Templates (Premium Themed)
# ════════════════════════════════════════════════════════════════

import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Consistent theme for all charts
PLOTLY_THEME = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#4A5568", size=12),
    margin=dict(t=50, b=30, l=30, r=30),
)

# Color palettes
EMERALD_PALETTE = ["#0E4B2E", "#1F7A4D", "#2E8B57", "#3D9B6B", "#5FAE6E", "#7BC17F"]
EMERALD_GRADIENT = [[0, "#F7F5EE"], [0.5, "#A8D5B8"], [1, "#1F7A4D"]]
DUAL_COLORS = ["#0E4B2E", "#5FAE6E"]


def plotly_bar(names, values, title, colors=None, text_format=".2f", show_text=True):
    """Modern bar chart with custom colors."""
    if colors is None:
        colors = EMERALD_PALETTE[:len(names)]

    fig = go.Figure()
    for i, (n, v) in enumerate(zip(names, values)):
        color = colors[i] if i < len(colors) else colors[-1]
        text_val = [f"{v:{text_format}}"] if show_text else None
        fig.add_trace(go.Bar(
            x=[n], y=[v], name=n,
            marker_color=color,
            text=text_val,
            textposition="outside",
            width=0.45,
            marker_line_width=0
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(family="Sora", size=15, color="#123524")),
        yaxis=dict(gridcolor="rgba(31,122,77,0.05)", zerolinecolor="rgba(31,122,77,0.1)"),
        showlegend=False,
        **PLOTLY_THEME
    )
    return fig


def plotly_horizontal_bar(tokens, values, title, color_scale=None):
    """Horizontal bar chart for top tokens."""
    if color_scale is None:
        color_scale = [[0, "#5FAE6E"], [1, "#0E4B2E"]]

    fig = go.Figure(go.Bar(
        x=values[::-1],
        y=tokens[::-1],
        orientation='h',
        marker=dict(color=values[::-1], colorscale=color_scale, showscale=False),
        text=[f"{v:,.0f}" for v in values[::-1]],
        textposition="outside"
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Sora", size=14, color="#123524")),
        xaxis_title="Frequency",
        height=max(400, len(tokens) * 22),
        **PLOTLY_THEME
    )
    return fig


def plotly_grouped_bar(categories, series_data, title, colors=None):
    """Grouped bar chart for metric comparisons."""
    if colors is None:
        colors = EMERALD_PALETTE

    fig = go.Figure()
    for i, (series_name, values) in enumerate(series_data.items()):
        color = colors[i % len(colors)]
        fig.add_trace(go.Bar(
            name=series_name,
            x=categories,
            y=values,
            marker_color=color,
            text=[f"{v:.2f}%" if v > 1 else f"{v:.4f}" for v in values],
            textposition="outside",
        ))

    fig.update_layout(
        barmode="group",
        title=dict(text=title, font=dict(family="Sora", size=15, color="#123524")),
        yaxis=dict(gridcolor="rgba(31,122,77,0.05)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **PLOTLY_THEME
    )
    return fig


def plotly_cm(cm, title, labels):
    """Confusion matrix heatmap."""
    fig = px.imshow(
        cm, text_auto=True,
        labels=dict(x="Predicted", y="Actual"),
        x=labels, y=labels,
        color_continuous_scale=EMERALD_GRADIENT,
        aspect="auto"
    )
    fig.update_layout(
        title=dict(text=title, font=dict(family="Sora", size=14, color="#123524")),
        coloraxis_showscale=False,
        **PLOTLY_THEME
    )
    fig.update_traces(textfont=dict(family="Sora", size=18, color="#123524"))
    return fig


def plotly_radar(series_data, categories, title, colors=None):
    """Radar chart for multi-metric comparison."""
    if colors is None:
        colors = EMERALD_PALETTE

    fig = go.Figure()
    cats_closed = categories + [categories[0]]

    for i, (name, values) in enumerate(series_data.items()):
        color = colors[i % len(colors)]
        vals_closed = list(values) + [values[0]]
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

        fig.add_trace(go.Scatterpolar(
            r=vals_closed, theta=cats_closed,
            fill='toself', name=name,
            line=dict(color=color, width=2),
            fillcolor=f"rgba({r},{g},{b},0.1)"
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 105], tickfont=dict(size=10)),
            angularaxis=dict(tickfont=dict(size=11, family="Inter"))
        ),
        title=dict(text=title, font=dict(family="Sora", size=15, color="#123524")),
        showlegend=True,
        legend=dict(font=dict(size=11)),
        **PLOTLY_THEME
    )
    return fig


def plotly_pie(labels, values, title, colors=None, hole=0.55):
    """Donut/Pie chart."""
    if colors is None:
        colors = DUAL_COLORS

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=hole,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=3)),
        textfont=dict(family="Inter", size=13),
        textinfo="percent+label"
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Sora", size=15, color="#123524")),
        showlegend=True,
        **PLOTLY_THEME
    )
    return fig


def plotly_histogram(df, x_col, color_col, title, nbins=50, color_map=None):
    """Histogram with optional color grouping."""
    if color_map is None:
        color_map = {"AGRICULTURE": "#0E4B2E", "HORTICULTURE": "#5FAE6E"}

    fig = px.histogram(
        df, x=x_col, color=color_col,
        nbins=nbins, opacity=0.8,
        color_discrete_map=color_map,
    )
    fig.update_layout(
        title=dict(text=title, font=dict(family="Sora", size=15, color="#123524")),
        bargap=0.05,
        **PLOTLY_THEME
    )
    return fig


def plotly_scatter_2d(x, y, labels, title, color_map=None):
    """2D scatter plot for embedding visualization."""
    if color_map is None:
        color_map = {0: "#0E4B2E", 1: "#5FAE6E"}

    colors = [color_map.get(l, "#999") for l in labels]

    fig = go.Figure()
    for label_val in sorted(set(labels)):
        mask = [l == label_val for l in labels]
        fig.add_trace(go.Scatter(
            x=[x[i] for i, m in enumerate(mask) if m],
            y=[y[i] for i, m in enumerate(mask) if m],
            mode='markers',
            name=f"Class {label_val}",
            marker=dict(
                color=color_map.get(label_val, "#999"),
                size=5, opacity=0.6,
                line=dict(width=0.5, color='white')
            )
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(family="Sora", size=14, color="#123524")),
        xaxis_title="Component 1",
        yaxis_title="Component 2",
        **PLOTLY_THEME
    )
    return fig


def plotly_heatmap(data, x_labels, y_labels, title, color_scale=None):
    """Generic heatmap."""
    if color_scale is None:
        color_scale = EMERALD_GRADIENT

    fig = px.imshow(
        data, text_auto=".2f",
        x=x_labels, y=y_labels,
        color_continuous_scale=color_scale,
        aspect="auto"
    )
    fig.update_layout(
        title=dict(text=title, font=dict(family="Sora", size=14, color="#123524")),
        **PLOTLY_THEME
    )
    fig.update_traces(textfont=dict(family="Inter", size=12))
    return fig


def plotly_ranking_bar(names, values, title, highlight_best=True):
    """Ranking bar chart with best highlighted."""
    sorted_pairs = sorted(zip(names, values), key=lambda x: x[1], reverse=True)
    sorted_names = [p[0] for p in sorted_pairs]
    sorted_values = [p[1] for p in sorted_pairs]

    colors = []
    for i, v in enumerate(sorted_values):
        if i == 0 and highlight_best:
            colors.append("#D4A843")  # Gold for best
        elif i == 1 and highlight_best:
            colors.append("#A8A8A8")  # Silver
        elif i == 2 and highlight_best:
            colors.append("#CD7F32")  # Bronze
        else:
            colors.append("#5FAE6E")

    fig = go.Figure(go.Bar(
        x=sorted_values[::-1],
        y=sorted_names[::-1],
        orientation='h',
        marker_color=colors[::-1],
        text=[f"{v:.2f}%" for v in sorted_values[::-1]],
        textposition="outside"
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Sora", size=15, color="#123524")),
        xaxis_title="Accuracy (%)",
        height=max(400, len(names) * 38),
        **PLOTLY_THEME
    )
    return fig
