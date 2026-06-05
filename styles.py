# ════════════════════════════════════════════════════════════════
# STYLES.PY — Premium AI Dashboard CSS
# Glassmorphism + Emerald/Cream Theme
# ════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
<style>
/* ══════════════════════════════════════════════════════════ */
/* TYPOGRAPHY & CSS VARIABLES                                */
/* ══════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-base: #F7F5EE;
    --bg-glass: rgba(255, 255, 255, 0.65);
    --bg-glass-strong: rgba(255, 255, 255, 0.85);
    --bg-glass-subtle: rgba(255, 255, 255, 0.45);

    --sidebar-bg: #0E4B2E;
    --sidebar-gradient: linear-gradient(170deg, #071F14 0%, #0A321E 25%, #0E4B2E 50%, #175C3B 85%, #1A6B42 100%);

    --accent-emerald: #1F7A4D;
    --accent-soft: #5FAE6E;
    --accent-light: #A8D5B8;
    --accent-glow: rgba(31, 122, 77, 0.3);
    --accent-gold: #D4A843;

    --text-main: #123524;
    --text-secondary: #2D5A3D;
    --text-muted: #6B7280;

    --border-glass: rgba(31, 122, 77, 0.08);
    --border-glow: rgba(31, 122, 77, 0.2);
    --border-subtle: rgba(0, 0, 0, 0.04);

    --shadow-float: 0 12px 40px rgba(14, 75, 46, 0.06);
    --shadow-glow: 0 0 30px rgba(95, 174, 110, 0.15);
    --shadow-deep: 0 20px 60px rgba(14, 75, 46, 0.1);
    --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.04);

    --radius-xl: 28px;
    --radius-lg: 24px;
    --radius-md: 16px;
    --radius-sm: 12px;
    --radius-xs: 8px;

    --ease-smooth: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* ══════════════════════════════════════════════════════════ */
/* GLOBAL RESETS                                              */
/* ══════════════════════════════════════════════════════════ */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-main);
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Sora', sans-serif !important;
    letter-spacing: -0.02em;
}
code, pre, .stCode {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Hide Default Streamlit Elements */
#MainMenu, header, footer { visibility: hidden; }

/* ══════════════════════════════════════════════════════════ */
/* ABSTRACT BACKGROUND                                        */
/* ══════════════════════════════════════════════════════════ */
.stApp {
    background-color: var(--bg-base);
    background-image:
        radial-gradient(ellipse at 10% 20%, rgba(95, 174, 110, 0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(31, 122, 77, 0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(212, 168, 67, 0.02) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 10%, rgba(95, 174, 110, 0.04) 0%, transparent 40%);
    background-attachment: fixed;
}

/* ══════════════════════════════════════════════════════════ */
/* SIDEBAR                                                    */
/* ══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--sidebar-gradient) !important;
    border-right: none !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.2);
}
[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.9) !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 12px 0 !important;
}

/* Sidebar Radio Navigation — Pill Style */
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio > div {
    gap: 4px !important;
    padding: 0 8px;
}
[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent !important;
    border-radius: 12px !important;
    padding: 11px 16px !important;
    cursor: pointer !important;
    transition: all 0.3s var(--ease-smooth) !important;
    border: 1px solid transparent !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(255,255,255,0.06) !important;
    transform: translateX(4px);
}
[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
[data-testid="stSidebar"] .stRadio > div label:has(input:checked) {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.2) !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    backdrop-filter: blur(10px);
}
[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
    display: none !important;
}

/* ══════════════════════════════════════════════════════════ */
/* GLASS CARDS                                                */
/* ══════════════════════════════════════════════════════════ */
.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 32px;
    box-shadow: var(--shadow-float);
    transition: all 0.4s var(--ease-smooth);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
    opacity: 0.5;
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-float), var(--shadow-glow);
    border-color: var(--border-glow);
    background: var(--bg-glass-strong);
}

.glass-card-static {
    background: var(--bg-glass);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 28px 32px;
    box-shadow: var(--shadow-float);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

/* ══════════════════════════════════════════════════════════ */
/* METRIC CARDS                                               */
/* ══════════════════════════════════════════════════════════ */
.ai-metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 18px;
    margin-bottom: 28px;
}
.ai-metric {
    background: var(--bg-glass);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: var(--shadow-card);
    transition: all 0.35s var(--ease-smooth);
    position: relative;
    overflow: hidden;
}
.ai-metric::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
    opacity: 0.4;
}
.ai-metric:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-glow);
    border-color: var(--accent-emerald);
}
.ai-metric-icon {
    font-size: 1.4rem;
    margin-bottom: 14px;
    background: linear-gradient(135deg, rgba(31,122,77,0.08), rgba(95,174,110,0.08));
    width: 46px; height: 46px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 14px;
    border: 1px solid rgba(31,122,77,0.08);
}
.ai-metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    font-family: 'Inter', sans-serif;
    margin-bottom: 6px;
}
.ai-metric-val {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text-main);
    font-family: 'Sora', sans-serif;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.ai-metric-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 8px;
    font-weight: 500;
}
.ai-metric-sub-green {
    font-size: 0.75rem;
    color: var(--accent-emerald);
    margin-top: 8px;
    font-weight: 600;
}

/* ══════════════════════════════════════════════════════════ */
/* BADGES                                                     */
/* ══════════════════════════════════════════════════════════ */
.ai-badge {
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    background: rgba(31,122,77,0.08);
    border: 1px solid rgba(31,122,77,0.15);
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--accent-emerald);
    font-family: 'Inter', sans-serif;
    margin-right: 8px;
    margin-bottom: 8px;
    backdrop-filter: blur(4px);
    transition: all 0.3s ease;
    letter-spacing: 0.03em;
}
.ai-badge:hover {
    background: rgba(31,122,77,0.15);
    transform: translateY(-2px);
}
.ai-badge-gold {
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    background: rgba(212,168,67,0.1);
    border: 1px solid rgba(212,168,67,0.2);
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--accent-gold);
    font-family: 'Inter', sans-serif;
    margin-right: 8px;
    margin-bottom: 8px;
}

/* ══════════════════════════════════════════════════════════ */
/* HERO SECTION                                               */
/* ══════════════════════════════════════════════════════════ */
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #071F14, #0E4B2E 40%, #1F7A4D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: var(--text-muted);
    line-height: 1.7;
    max-width: 640px;
    margin-bottom: 36px;
    font-weight: 400;
}

/* ══════════════════════════════════════════════════════════ */
/* SECTION HEADERS                                            */
/* ══════════════════════════════════════════════════════════ */
.section-header {
    padding: 24px 0 16px 0;
}
.section-title {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-main);
    margin: 8px 0 4px;
    letter-spacing: -0.02em;
}
.section-subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}

/* ══════════════════════════════════════════════════════════ */
/* EXPLANATION CARDS                                          */
/* ══════════════════════════════════════════════════════════ */
.explain-card {
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 28px;
    box-shadow: var(--shadow-card);
    margin-bottom: 20px;
    transition: all 0.3s var(--ease-smooth);
}
.explain-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-float);
    border-color: var(--border-glow);
}
.explain-card-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.explain-card-body {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.7;
}
.explain-card-body code {
    background: rgba(31,122,77,0.08);
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.82rem;
    color: var(--accent-emerald);
}

/* ══════════════════════════════════════════════════════════ */
/* INTERACTIVE PREDICTION                                     */
/* ══════════════════════════════════════════════════════════ */
.pred-input-wrapper textarea {
    background: rgba(255,255,255,0.8) !important;
    border: 1.5px solid rgba(31,122,77,0.12) !important;
    border-radius: 20px !important;
    padding: 20px 24px !important;
    font-size: 1.02rem !important;
    line-height: 1.6 !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.02) !important;
    transition: all 0.3s ease !important;
}
.pred-input-wrapper textarea:focus {
    background: #FFFFFF !important;
    border-color: var(--accent-emerald) !important;
    box-shadow: 0 0 0 4px var(--accent-glow) !important;
}

.ai-btn > button {
    background: linear-gradient(135deg, var(--accent-emerald), var(--accent-soft)) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 14px 28px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em;
    box-shadow: 0 8px 24px var(--accent-glow) !important;
    transition: all 0.3s var(--ease-smooth) !important;
    width: 100% !important;
}
.ai-btn > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(31,122,77,0.4) !important;
    filter: brightness(1.05);
}

.pred-result-card {
    background: linear-gradient(145deg, #FFFFFF, #F7F5EE);
    border: 1.5px solid var(--accent-emerald);
    border-radius: 28px;
    padding: 44px;
    text-align: center;
    box-shadow: 0 24px 64px rgba(31,122,77,0.15);
    position: relative;
    overflow: hidden;
    animation: scaleIn 0.5s var(--ease-smooth);
}
.pred-result-card::after {
    content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(95,174,110,0.08) 0%, transparent 60%);
    animation: rotateSlow 25s linear infinite;
    pointer-events: none;
}

/* ══════════════════════════════════════════════════════════ */
/* CONFIDENCE BAR                                             */
/* ══════════════════════════════════════════════════════════ */
.confidence-bar-bg {
    height: 8px;
    background: rgba(0,0,0,0.04);
    border-radius: 10px;
    overflow: hidden;
    margin-top: 12px;
}
.confidence-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #1F7A4D, #5FAE6E, #A8D5B8);
    border-radius: 10px;
    transition: width 1.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}

/* ══════════════════════════════════════════════════════════ */
/* TABLE / COMPARISON CARDS                                   */
/* ══════════════════════════════════════════════════════════ */
.comparison-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: var(--radius-md);
    overflow: hidden;
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
}
.comparison-table th {
    background: linear-gradient(135deg, #0E4B2E, #175C3B);
    color: white;
    padding: 14px 18px;
    text-align: left;
    font-weight: 600;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.comparison-table td {
    padding: 12px 18px;
    border-bottom: 1px solid rgba(0,0,0,0.04);
    transition: background 0.2s ease;
}
.comparison-table tr:hover td {
    background: rgba(31,122,77,0.04);
}
.comparison-table tr:last-child td {
    border-bottom: none;
}
.comparison-table .best-row {
    background: rgba(31,122,77,0.06);
    font-weight: 600;
}

/* ══════════════════════════════════════════════════════════ */
/* STEP CARDS (for preprocessing)                             */
/* ══════════════════════════════════════════════════════════ */
.step-card {
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    border: 1px solid rgba(0,0,0,0.05);
    transition: all 0.2s ease;
}
.step-card:hover {
    transform: translateX(4px);
    box-shadow: var(--shadow-card);
}
.step-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.step-token-badge {
    background: rgba(31,122,77,0.1);
    color: var(--accent-emerald);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-weight: 600;
}
.step-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: #1a1a1a;
    word-break: break-word;
    line-height: 1.5;
}

/* ══════════════════════════════════════════════════════════ */
/* PLOTLY CHART CONTAINERS                                    */
/* ══════════════════════════════════════════════════════════ */
[data-testid="stPlotlyChart"] {
    background: var(--bg-glass);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 20px 16px 8px;
    box-shadow: var(--shadow-float);
    transition: all 0.4s var(--ease-smooth);
    margin-bottom: 20px;
}
[data-testid="stPlotlyChart"]:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-float), var(--shadow-glow);
    border-color: var(--border-glow);
    background: var(--bg-glass-strong);
}

/* DataFrame containers */
[data-testid="stDataFrame"] {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-md);
    padding: 4px;
    box-shadow: var(--shadow-float);
    margin-bottom: 20px;
    overflow: hidden;
}

/* ══════════════════════════════════════════════════════════ */
/* TABS                                                       */
/* ══════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 2px solid rgba(31,122,77,0.06);
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 10px 20px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    color: var(--text-muted) !important;
    border-bottom: 3px solid transparent !important;
    transition: all 0.3s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--accent-emerald) !important;
    background: rgba(31,122,77,0.04) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-emerald) !important;
    font-weight: 600 !important;
    border-bottom: 3px solid var(--accent-emerald) !important;
    background: rgba(31,122,77,0.06) !important;
}

/* ══════════════════════════════════════════════════════════ */
/* EXPANDER                                                   */
/* ══════════════════════════════════════════════════════════ */
.streamlit-expanderHeader {
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    color: var(--text-main) !important;
    background: var(--bg-glass) !important;
    border-radius: var(--radius-sm) !important;
    padding: 14px 18px !important;
    border: 1px solid var(--border-glass) !important;
}

/* ══════════════════════════════════════════════════════════ */
/* SELECTBOX & INPUT                                          */
/* ══════════════════════════════════════════════════════════ */
.stSelectbox > div > div {
    border-radius: 12px !important;
    border-color: rgba(31,122,77,0.12) !important;
    font-family: 'Inter', sans-serif !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--accent-emerald) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ══════════════════════════════════════════════════════════ */
/* ANIMATIONS                                                 */
/* ══════════════════════════════════════════════════════════ */
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.95) translateY(10px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}
@keyframes rotateSlow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; }
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

.animate-in {
    animation: fadeInUp 0.6s var(--ease-smooth);
}
.typing-indicator {
    font-family: 'JetBrains Mono';
    color: var(--accent-emerald);
    animation: pulse 1.5s infinite;
}

/* ══════════════════════════════════════════════════════════ */
/* HIDE DEFAULT STREAMLIT METRIC                              */
/* ══════════════════════════════════════════════════════════ */
div[data-testid="stMetric"] { display: none !important; }

/* ══════════════════════════════════════════════════════════ */
/* SCROLLBAR                                                  */
/* ══════════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(31,122,77,0.15);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(31,122,77,0.3); }

/* ══════════════════════════════════════════════════════════ */
/* PROS / CONS CARDS                                          */
/* ══════════════════════════════════════════════════════════ */
.pros-cons-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 16px 0;
}
.pros-card {
    background: rgba(31,122,77,0.04);
    border: 1px solid rgba(31,122,77,0.1);
    border-radius: var(--radius-md);
    padding: 20px;
}
.cons-card {
    background: rgba(220,120,60,0.04);
    border: 1px solid rgba(220,120,60,0.1);
    border-radius: var(--radius-md);
    padding: 20px;
}

/* ══════════════════════════════════════════════════════════ */
/* ERROR ANALYSIS CARDS                                       */
/* ══════════════════════════════════════════════════════════ */
.error-card {
    background: rgba(239,68,68,0.04);
    border: 1px solid rgba(239,68,68,0.1);
    border-radius: var(--radius-md);
    padding: 20px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}
.error-card:hover {
    transform: translateX(4px);
    border-color: rgba(239,68,68,0.2);
}

/* ══════════════════════════════════════════════════════════ */
/* ABOUT / RESEARCH CARDS                                     */
/* ══════════════════════════════════════════════════════════ */
.research-card {
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 32px;
    box-shadow: var(--shadow-card);
    margin-bottom: 20px;
    transition: all 0.3s var(--ease-smooth);
}
.research-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-float);
}
.research-card-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 12px;
}
.research-card-body {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.7;
}

/* ══════════════════════════════════════════════════════════ */
/* TECH STACK PILLS                                           */
/* ══════════════════════════════════════════════════════════ */
.tech-pill {
    display: inline-flex;
    align-items: center;
    padding: 8px 16px;
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: 100px;
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
    margin: 4px;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}
.tech-pill:hover {
    background: rgba(31,122,77,0.08);
    border-color: var(--accent-emerald);
    transform: translateY(-2px);
    box-shadow: var(--shadow-card);
}
</style>
"""
