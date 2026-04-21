"""
ui/components.py – Reusable Streamlit HTML components for KISAN AI
"""
import streamlit as st
from datetime import datetime


def hero_header():
    st.markdown("""
    <div class="hero-card">
        <p class="hero-title">🌾 KISAN AI</p>
        <p class="hero-sub">Agricultural Intelligence Assistant — Crop Diseases · Pests · Fertilizers · Government Schemes</p>
        <br>
        <span class="badge">📦 Offline TF-IDF Search</span>
        <span class="badge">🤖 Groq LLaMA-3 RAG</span>
        <span class="badge">🌍 Hindi · English · Hinglish</span>
        <span class="badge">📄 PDF Export</span>
        <span class="badge">📊 Analytics Dashboard</span>
    </div>
    """, unsafe_allow_html=True)


def user_bubble(query: str, lang: str, ts: str = ""):
    ts = ts or datetime.now().strftime("%H:%M")
    st.markdown(f"""
    <div class="bubble bubble-user">
        <div class="bubble-label">👨‍🌾 Farmer</div>
        {query}
        <div class="bubble-meta">🕐 {ts} &nbsp;|&nbsp; Language: {lang.upper()}</div>
    </div>
    """, unsafe_allow_html=True)


def ai_bubble(answer: str, mode_label: str, ts: str = ""):
    ts = ts or datetime.now().strftime("%H:%M")
    st.markdown(f"""
    <div class="bubble bubble-ai">
        <div class="bubble-label">🤖 KISAN AI (Groq)</div>
        {answer}
        <div class="bubble-meta">🕐 {ts} &nbsp;|&nbsp; {mode_label}</div>
    </div>
    """, unsafe_allow_html=True)


def offline_bubble(answer: str, matched_q: str, score: float, ts: str = ""):
    ts = ts or datetime.now().strftime("%H:%M")
    score_class = "score-high" if score >= 0.65 else ("score-mid" if score >= 0.40 else "score-low")
    st.markdown(f"""
    <div class="bubble bubble-offline">
        <div class="bubble-label">📦 Offline Database</div>
        {answer}
        <div class="bubble-meta">
            🕐 {ts} &nbsp;|&nbsp;
            Matched: <i>{matched_q[:60]}…</i> &nbsp;|&nbsp;
            Score: <span class="score-pill {score_class}">{score:.4f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def low_confidence_bubble(score: float, threshold: float):
    st.markdown(f"""
    <div class="bubble bubble-offline">
        <div class="bubble-label">📦 Offline Database</div>
        ⚠️ No confident offline match found. Try rephrasing your question.
        <div class="bubble-meta">
            Score: <span class="score-pill score-low">{score:.4f}</span>
            &nbsp;|&nbsp; Threshold: {threshold:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)


def similar_queries_panel(results: list, label: str = "Top Similar Matches"):
    st.markdown(f'<div class="section-heading">{label}</div>', unsafe_allow_html=True)
    for r in results:
        score_class = "score-high" if r.score >= 0.65 else ("score-mid" if r.score >= 0.40 else "score-low")
        st.markdown(f"""
        <div class="similar-card">
            <b>#{r.rank}</b> {r.question}
            <div style="margin-top:6px;">
                <span class="score-pill {score_class}">{r.score:.4f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def suggested_chips(questions: list[str]):
    """Render clickable-looking suggestion chips (display only)."""
    st.markdown('<div class="section-heading">💡 Suggested Questions</div>', unsafe_allow_html=True)
    chips_html = '<div class="chip-row">' + "".join(
        f'<span class="chip">{q}</span>' for q in questions
    ) + "</div>"
    st.markdown(chips_html, unsafe_allow_html=True)


def metric_card(number, label: str):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{number}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def feedback_row(query_id: int):
    """Thumbs up/down feedback buttons. Returns ('up'/'down'/None)."""
    col1, col2, _ = st.columns([1, 1, 8])
    rating = None
    with col1:
        if st.button("👍", key=f"up_{query_id}"):
            rating = "up"
    with col2:
        if st.button("👎", key=f"down_{query_id}"):
            rating = "down"
    return rating


def footer():
    st.markdown("""
    <div class="footer">
        🌾 KISAN AI v2.0 &nbsp;|&nbsp; Built for Indian Farmers &nbsp;|&nbsp;
        Powered by Groq LLaMA-3 &amp; TF-IDF RAG &nbsp;|&nbsp;
        Open Source · Hackathon Ready
    </div>
    """, unsafe_allow_html=True)
