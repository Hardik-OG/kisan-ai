"""
ui/styles.py – Centralised CSS for KISAN AI (dark glassmorphism)
"""

GLOBAL_CSS = """
<style>
/* ── Base ──────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: #050b14 !important;
    color: #e8eef5 !important;
}

/* ── Sidebar ────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#060d1a 0%,#040810 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* ── Hero card ──────────────────────────────────────────────────── */
.hero-card {
    background: linear-gradient(135deg,
        rgba(10,40,80,0.90) 0%,
        rgba(6,55,50,0.75) 60%,
        rgba(20,10,60,0.65) 100%);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 24px;
    padding: 32px 36px;
    margin-bottom: 24px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.55),
                0 0 0 1px rgba(0,200,120,0.08) inset;
    position: relative; overflow: hidden;
}
.hero-card::before {
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 20% 50%,rgba(0,200,120,0.07) 0%,transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-size: 36px; font-weight: 800;
    background: linear-gradient(135deg,#ffffff 30%,#7affc8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 8px;
}
.hero-sub {
    font-size: 15px; font-weight: 400;
    color: rgba(255,255,255,0.65); margin: 0;
}
.badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 13px;
    margin: 8px 6px 0 0;
    border-radius: 999px;
    font-size: 12px; font-weight: 500;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.80);
}

/* ── Chat bubbles ───────────────────────────────────────────────── */
.chat-wrap { margin: 16px 0; display: flex; flex-direction: column; gap: 12px; }

.bubble {
    max-width: 78%; padding: 14px 18px;
    border-radius: 20px; line-height: 1.6; font-size: 14px;
    position: relative;
    animation: fadeUp 0.3s ease both;
}
@keyframes fadeUp {
    from { opacity:0; transform: translateY(10px); }
    to   { opacity:1; transform: translateY(0); }
}

.bubble-user {
    margin-left: auto;
    background: linear-gradient(135deg,rgba(0,122,255,0.22),rgba(0,80,200,0.15));
    border: 1px solid rgba(0,122,255,0.30);
    border-bottom-right-radius: 6px;
}
.bubble-ai {
    margin-right: auto;
    background: linear-gradient(135deg,rgba(0,210,140,0.14),rgba(0,160,100,0.08));
    border: 1px solid rgba(0,210,140,0.22);
    border-bottom-left-radius: 6px;
}
.bubble-offline {
    margin-right: auto;
    background: linear-gradient(135deg,rgba(240,165,0,0.12),rgba(200,120,0,0.07));
    border: 1px solid rgba(240,165,0,0.22);
    border-bottom-left-radius: 6px;
}

.bubble-label {
    font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
    margin-bottom: 6px; opacity: 0.75;
    text-transform: uppercase;
}
.bubble-meta {
    font-size: 11px; opacity: 0.50; margin-top: 8px;
}

/* ── Score pill ─────────────────────────────────────────────────── */
.score-pill {
    display: inline-block; padding: 2px 10px;
    border-radius: 999px; font-size: 11px; font-weight: 600;
}
.score-high { background:rgba(0,210,100,0.20); color:#6dffc0; border:1px solid rgba(0,210,100,0.35); }
.score-mid  { background:rgba(240,165,0,0.20);  color:#ffd066; border:1px solid rgba(240,165,0,0.35); }
.score-low  { background:rgba(255,80,80,0.20);   color:#ff9999; border:1px solid rgba(255,80,80,0.35); }

/* ── Similar queries card ───────────────────────────────────────── */
.similar-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 8px;
    cursor: pointer; transition: background 0.2s;
}
.similar-card:hover { background: rgba(255,255,255,0.07); }

/* ── Dashboard metric card ──────────────────────────────────────── */
.metric-card {
    background: linear-gradient(135deg,rgba(15,30,60,0.90),rgba(10,50,40,0.70));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px 24px;
    text-align: center;
}
.metric-number { font-size: 36px; font-weight: 800; color: #7affc8; }
.metric-label  { font-size: 12px; opacity: 0.60; margin-top: 4px; }

/* ── Section headings ───────────────────────────────────────────── */
.section-heading {
    font-size: 14px; font-weight: 700;
    color: rgba(255,255,255,0.55);
    letter-spacing: 1px; text-transform: uppercase;
    margin: 20px 0 10px;
}

/* ── Suggestion chips ───────────────────────────────────────────── */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }
.chip {
    padding: 6px 14px; border-radius: 999px; font-size: 12px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.75);
    cursor: pointer; transition: all 0.2s;
    display: inline-block;
}
.chip:hover { background: rgba(0,210,140,0.15); border-color: rgba(0,210,140,0.40); }

/* ── Input override ─────────────────────────────────────────────── */
.stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #e8eef5 !important;
    padding: 12px 16px !important;
    font-size: 15px !important;
}
.stTextInput input:focus {
    border-color: rgba(0,210,140,0.50) !important;
    box-shadow: 0 0 0 3px rgba(0,210,140,0.10) !important;
}

/* ── Button override ────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg,#1a5c2e,#0d3d20) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,160,80,0.35) !important;
}

/* ── Footer ─────────────────────────────────────────────────────── */
.footer {
    text-align: center; font-size: 12px;
    opacity: 0.40; margin-top: 32px; padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.06);
}
</style>
"""


def inject():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
