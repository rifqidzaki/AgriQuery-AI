# ════════════════════════════════════════════════════════════════
# METRICS — Reusable Metric Card Components
# ════════════════════════════════════════════════════════════════

import streamlit as st


def render_metric_grid(metrics: list):
    """Render floating glass metric cards.
    
    Args:
        metrics: list of dicts with keys: icon, label, value, sub (optional), sub_green (optional)
    """
    cards_html = ""
    for m in metrics:
        sub_html = ""
        if m.get("sub_green"):
            sub_html = f"<div class='ai-metric-sub-green'>{m['sub_green']}</div>"
        elif m.get("sub"):
            sub_html = f"<div class='ai-metric-sub'>{m['sub']}</div>"

        unit = m.get("unit", "")
        unit_html = f"<span style='font-size:1rem;color:var(--text-muted)'>{unit}</span>" if unit else ""

        cards_html += f"""
        <div class='ai-metric'>
            <div class='ai-metric-icon'>{m['icon']}</div>
            <div class='ai-metric-label'>{m['label']}</div>
            <div class='ai-metric-val'>{m['value']}{unit_html}</div>
            {sub_html}
        </div>"""

    st.markdown(f"<div class='ai-metric-grid'>{cards_html}</div>", unsafe_allow_html=True)


def render_badge(text: str, badge_type: str = "default"):
    """Render an AI-style badge."""
    css_class = "ai-badge-gold" if badge_type == "gold" else "ai-badge"
    return f"<span class='{css_class}'>{text}</span>"


def render_badges(badges: list):
    """Render multiple badges."""
    html = " ".join([render_badge(b.get("text", ""), b.get("type", "default")) for b in badges])
    st.markdown(html, unsafe_allow_html=True)


def render_section_header(badge_text: str, title: str, subtitle: str, extra_badges: list = None):
    """Render a page section header with badge, title, subtitle."""
    badges_html = f"<div class='ai-badge'>{badge_text}</div>"
    if extra_badges:
        for eb in extra_badges:
            badge_type = eb.get("type", "default")
            css_class = "ai-badge-gold" if badge_type == "gold" else "ai-badge"
            badges_html += f" <span class='{css_class}'>{eb['text']}</span>"

    st.markdown(f"""
<div class='section-header'>
    {badges_html}
    <div class='section-title'>{title}</div>
    <div class='section-subtitle'>{subtitle}</div>
</div>
""", unsafe_allow_html=True)


def render_glass_card(content_html: str, hover: bool = True):
    """Render a glass card with custom HTML content."""
    card_class = "glass-card" if hover else "glass-card-static"
    st.markdown(f"<div class='{card_class}'>{content_html}</div>", unsafe_allow_html=True)


def render_explain_card(icon: str, title: str, body: str):
    """Render an explanation card."""
    st.markdown(f"""
<div class='explain-card'>
    <div class='explain-card-title'>{icon} {title}</div>
    <div class='explain-card-body'>{body}</div>
</div>
""", unsafe_allow_html=True)


def render_pros_cons(pros: list, cons: list):
    """Render pros and cons cards side by side."""
    pros_items = "".join([f"<div style='margin:6px 0;'>✅ {p}</div>" for p in pros])
    cons_items = "".join([f"<div style='margin:6px 0;'>❌ {c}</div>" for c in cons])

    st.markdown(f"""
<div class='pros-cons-grid'>
    <div class='pros-card'>
        <div style='font-family:Sora; font-weight:700; margin-bottom:10px; color:#1F7A4D;'>Kelebihan</div>
        {pros_items}
    </div>
    <div class='cons-card'>
        <div style='font-family:Sora; font-weight:700; margin-bottom:10px; color:#DC783C;'>Kekurangan</div>
        {cons_items}
    </div>
</div>
""", unsafe_allow_html=True)
