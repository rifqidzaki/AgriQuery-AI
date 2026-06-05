# ════════════════════════════════════════════════════════════════
# STYLES.PY — Academic Research Dashboard CSS v6.0
# Clean Minimalist + Agriculture Green Theme
# ════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
<style>
/* ══════════════════════════════════════════════════════════ */
/* TYPOGRAPHY & CSS VARIABLES                                */
/* ══════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary: #1B5E20;
    --secondary: #2E7D32;
    --accent: #66BB6A;
    --accent-light: #A5D6A7;
    --accent-glow: rgba(102,187,106,0.25);

    --bg-base: #FAFAF5;
    --bg-card: #FFFFFF;
    --bg-card-hover: #FEFEFE;

    --sidebar-bg: linear-gradient(180deg, #1B5E20 0%, #2E7D32 60%, #388E3C 100%);

    --text-main: #1A1A1A;
    --text-secondary: #4A4A4A;
    --text-muted: #7A7A7A;

    --border: #E8E8E0;
    --border-hover: #D0D0C8;
    --border-accent: rgba(102,187,106,0.3);

    --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.08);
    --shadow-accent: 0 4px 20px rgba(27,94,32,0.1);

    --radius-xl: 20px;
    --radius-lg: 16px;
    --radius-md: 12px;
    --radius-sm: 8px;
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

#MainMenu, header, footer { visibility: hidden; }

/* ══════════════════════════════════════════════════════════ */
/* BACKGROUND                                                 */
/* ══════════════════════════════════════════════════════════ */
.stApp {
    background-color: var(--bg-base);
}

/* ══════════════════════════════════════════════════════════ */
/* SIDEBAR                                                    */
/* ══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.92) !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
    margin: 12px 0 !important;
}

/* Sidebar Radio — Pill Style */
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; padding: 0 8px; }
[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
[data-testid="stSidebar"] .stRadio > div label:has(input:checked) {
    background: rgba(255,255,255,0.15) !important;
    border-color: rgba(255,255,255,0.25) !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
    display: none !important;
}

/* ══════════════════════════════════════════════════════════ */
/* CARDS                                                      */
/* ══════════════════════════════════════════════════════════ */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px;
    box-shadow: var(--shadow-sm);
    transition: all 0.25s ease;
    margin-bottom: 20px;
}
.card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--border-hover);
    transform: translateY(-2px);
}

.card-static {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 20px;
}

/* ══════════════════════════════════════════════════════════ */
/* KPI / METRIC CARDS                                         */
/* ══════════════════════════════════════════════════════════ */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px;
    box-shadow: var(--shadow-sm);
    transition: all 0.25s ease;
}
.kpi-card:hover {
    box-shadow: var(--shadow-accent);
    border-color: var(--accent);
    transform: translateY(-3px);
}
.kpi-icon {
    font-size: 1.3rem;
    margin-bottom: 10px;
    width: 40px; height: 40px;
    display: flex; align-items: center; justify-content: center;
    background: rgba(102,187,106,0.1);
    border-radius: 10px;
}
.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-main);
    font-family: 'Sora', sans-serif;
    line-height: 1.1;
}
.kpi-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 6px;
}
.kpi-sub-green {
    font-size: 0.72rem;
    color: var(--secondary);
    margin-top: 6px;
    font-weight: 600;
}

/* ══════════════════════════════════════════════════════════ */
/* BADGES                                                     */
/* ══════════════════════════════════════════════════════════ */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 5px 12px;
    background: rgba(27,94,32,0.08);
    border: 1px solid rgba(27,94,32,0.15);
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--primary);
    margin-right: 6px;
    margin-bottom: 6px;
}
.badge-gold {
    display: inline-flex;
    align-items: center;
    padding: 5px 12px;
    background: rgba(245,180,40,0.1);
    border: 1px solid rgba(245,180,40,0.2);
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 600;
    color: #D4A017;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* ══════════════════════════════════════════════════════════ */
/* HERO                                                       */
/* ══════════════════════════════════════════════════════════ */
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: var(--primary);
    margin-bottom: 12px;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-muted);
    line-height: 1.7;
    max-width: 620px;
    margin-bottom: 28px;
}

/* ══════════════════════════════════════════════════════════ */
/* SECTION HEADERS                                            */
/* ══════════════════════════════════════════════════════════ */
.section-header { padding: 20px 0 12px 0; }
.section-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-main);
    margin: 6px 0 4px;
}
.section-subtitle {
    color: var(--text-muted);
    font-size: 0.9rem;
    line-height: 1.5;
}

/* ══════════════════════════════════════════════════════════ */
/* TABLES                                                     */
/* ══════════════════════════════════════════════════════════ */
.data-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: var(--radius-md);
    overflow: hidden;
    font-size: 0.85rem;
}
.data-table th {
    background: var(--primary);
    color: white;
    padding: 12px 16px;
    text-align: left;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.data-table td {
    padding: 10px 16px;
    border-bottom: 1px solid var(--border);
}
.data-table tr:hover td {
    background: rgba(102,187,106,0.04);
}
.data-table .best-row {
    background: rgba(102,187,106,0.08);
    font-weight: 600;
}

/* ══════════════════════════════════════════════════════════ */
/* PIPELINE STEP CARDS                                        */
/* ══════════════════════════════════════════════════════════ */
.step-card {
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 8px;
    border: 1px solid var(--border);
    transition: all 0.2s ease;
}
.step-card:hover {
    transform: translateX(4px);
    box-shadow: var(--shadow-sm);
}
.step-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}
.step-token-badge {
    background: rgba(102,187,106,0.12);
    color: var(--secondary);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.68rem;
    font-weight: 600;
}
.step-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #1a1a1a;
    word-break: break-word;
    line-height: 1.5;
}

/* ══════════════════════════════════════════════════════════ */
/* PREDICTION RESULT                                          */
/* ══════════════════════════════════════════════════════════ */
.pred-result-card {
    background: var(--bg-card);
    border: 2px solid var(--accent);
    border-radius: var(--radius-xl);
    padding: 36px;
    text-align: center;
    box-shadow: var(--shadow-accent);
    animation: fadeInUp 0.4s ease;
}

.confidence-bar-bg {
    height: 8px;
    background: #F0F0E8;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 10px;
}
.confidence-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    border-radius: 10px;
    transition: width 1s ease;
}

/* ══════════════════════════════════════════════════════════ */
/* INSIGHT CARD (Error Analysis)                              */
/* ══════════════════════════════════════════════════════════ */
.insight-card {
    background: rgba(27,94,32,0.04);
    border: 1px solid rgba(27,94,32,0.12);
    border-left: 4px solid var(--secondary);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 16px 20px;
    margin-bottom: 12px;
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* ══════════════════════════════════════════════════════════ */
/* PLOTLY & DATAFRAME                                         */
/* ══════════════════════════════════════════════════════════ */
[data-testid="stPlotlyChart"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 16px 12px 4px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 16px;
}
[data-testid="stDataFrame"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 4px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 16px;
    overflow: hidden;
}

/* ══════════════════════════════════════════════════════════ */
/* TABS                                                       */
/* ══════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 2px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 8px 18px !important;
    font-size: 0.85rem !important;
    color: var(--text-muted) !important;
    border-bottom: 3px solid transparent !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--secondary) !important;
    background: rgba(102,187,106,0.04) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--primary) !important;
    font-weight: 600 !important;
    border-bottom: 3px solid var(--primary) !important;
}

/* ══════════════════════════════════════════════════════════ */
/* SELECTBOX & INPUT                                          */
/* ══════════════════════════════════════════════════════════ */
.stSelectbox > div > div {
    border-radius: 10px !important;
    border-color: var(--border) !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ══════════════════════════════════════════════════════════ */
/* ANIMATIONS                                                 */
/* ══════════════════════════════════════════════════════════ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; }
}
.typing-indicator {
    color: var(--accent);
    animation: pulse 1.5s infinite;
}

/* ══════════════════════════════════════════════════════════ */
/* MISC                                                       */
/* ══════════════════════════════════════════════════════════ */
div[data-testid="stMetric"] { display: none !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(27,94,32,0.15); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(27,94,32,0.3); }

.pipeline-arrow {
    text-align: center;
    font-size: 1.5rem;
    color: var(--accent);
    padding: 4px 0;
}
</style>
"""
