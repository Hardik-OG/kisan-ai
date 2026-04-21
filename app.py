"""
KISAN AI v2.0 – Production-Ready Agricultural Intelligence Assistant
────────────────────────────────────────────────────────────────────
Architecture  : Modular (ui / backend / utils)
LLM           : Groq LLaMA-3 70B (free tier)
Retrieval     : TF-IDF cosine similarity (offline)
Persistence   : SQLite via analytics module
Export        : ReportLab PDF
"""

import uuid
import streamlit as st
from datetime import datetime

# ── Project modules ───────────────────────────────────────────────────────────
from config import DEFAULT_THRESHOLD, APP_TITLE, APP_SUBTITLE, VERSION
from ui.styles import inject as inject_css
from ui import components as ui
from utils.language_utils import detect_language, get_suggested_questions
from backend.query_engine import retrieve, best_result
from backend.groq_service import get_groq_answer
from backend.pdf_generator import generate_pdf_bytes
from backend.analytics import init_db, log_query, log_feedback, get_dashboard_stats, get_recent_queries

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = f"{APP_TITLE} – {APP_SUBTITLE}",
    page_icon  = "🌾",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

inject_css()
init_db()

# ── Session state ─────────────────────────────────────────────────────────────
if "chat"       not in st.session_state: st.session_state.chat       = []
if "session_id" not in st.session_state: st.session_state.session_id = str(uuid.uuid4())[:8]
if "page"       not in st.session_state: st.session_state.page       = "chat"


# ═════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🌾 KISAN AI")
    st.markdown(f"<small>v{VERSION} &nbsp;|&nbsp; Session: `{st.session_state.session_id}`</small>",
                unsafe_allow_html=True)
    st.markdown("---")

    # Navigation
    page = st.radio(
        "Navigate",
        ["💬 Chat", "📊 Dashboard", "📜 History"],
        index=0,
        label_visibility="collapsed",
    )
    st.session_state.page = page

    st.markdown("---")
    st.markdown("#### ⚙️ Settings")

    output_lang = st.selectbox(
        "🌍 Output Language",
        ["Hindi", "English", "Hinglish"],
        index=0,
    )

    mode = st.radio(
        "🧠 Mode",
        ["🌐 Online (Groq LLM)", "📦 Offline Only"],
        index=0,
    )

    threshold = st.slider(
        "📌 Confidence Threshold",
        min_value=0.0, max_value=1.0,
        value=DEFAULT_THRESHOLD, step=0.01,
    )

    show_similar = st.checkbox("Show Top 3 Similar Queries", value=True)

    st.markdown("---")

    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat = []
        st.rerun()

    # PDF download (sidebar shortcut)
    if st.session_state.chat:
        pdf_bytes = generate_pdf_bytes(st.session_state.chat)
        st.download_button(
            label     = "⬇️ Download PDF Report",
            data      = pdf_bytes,
            file_name = f"kisan_ai_{st.session_state.session_id}.pdf",
            mime      = "application/pdf",
        )

    st.markdown("---")
    st.info("💡 Type in Hindi or English — KISAN AI auto-detects the language.")


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: CHAT
# ═════════════════════════════════════════════════════════════════════════════
if "Chat" in st.session_state.page:

    # Hero header
    ui.hero_header()

    # ── Suggested questions ───────────────────────────────────────────────────
    with st.expander("💡 Suggested Questions (click to copy)", expanded=False):
        suggested = get_suggested_questions("hi")
        ui.suggested_chips(suggested)
        st.caption("Tip: Copy any question above and paste it in the input box below.")

    # ── Query input ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Ask Your Question</div>', unsafe_allow_html=True)

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        query = st.text_input(
            label       = "query_input",
            placeholder = "Example: सरसों में माहू (aphid) कैसे रोकें?  |  How to control wheat rust?",
            label_visibility = "collapsed",
            key         = "query_box",
        )
    with col_btn:
        ask_clicked = st.button("🔍 Ask", use_container_width=True)

    # ── Processing ────────────────────────────────────────────────────────────
    if query and ask_clicked:
        query_lang = detect_language(query)

        with st.spinner("🔍 Searching offline database…"):
            all_results = retrieve(query, lang=query_lang, threshold=threshold)

        if not all_results:
            st.error("❌ Offline store not found. Please check your .pkl files in /data.")
            st.stop()

        top = all_results[0]
        online_answer = None

        if "Online" in mode:
            with st.spinner("🌐 Groq LLaMA-3 is generating your answer…"):
                online_answer = get_groq_answer(
                    query            = query,
                    matched_question = top.question,
                    database_answer  = top.answer,
                    score            = top.score,
                    output_language  = output_lang,
                )

        # Save to SQLite
        qid = log_query(
            query       = query,
            lang        = query_lang,
            mode        = mode,
            score       = top.score,
            matched_q   = top.question,
            offline_ans = top.answer,
            online_ans  = online_answer or "",
            session_id  = st.session_state.session_id,
        )

        # Save to session
        ts = datetime.now().strftime("%H:%M")
        st.session_state.chat.append({
            "query":           query,
            "lang":            query_lang,
            "ts":              ts,
            "offline_answer":  top.answer,
            "matched_question": top.question,
            "score":           top.score,
            "online_answer":   online_answer,
            "all_results":     all_results,
            "qid":             qid,
        })

    # ── Render all chats ──────────────────────────────────────────────────────
    if st.session_state.chat:
        st.markdown("---")
        st.markdown("## 💬 Conversation")
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

        for idx, msg in enumerate(reversed(st.session_state.chat)):
            ts   = msg.get("ts", "")
            lang = msg.get("lang", "en")

            # User bubble
            ui.user_bubble(msg["query"], lang, ts)

            # AI bubble
            if msg.get("online_answer"):
                ui.ai_bubble(
                    msg["online_answer"],
                    mode_label = f"Groq LLaMA-3 | {output_lang}",
                    ts         = ts,
                )

            # Offline bubble
            if msg["score"] >= threshold:
                ui.offline_bubble(
                    msg["offline_answer"],
                    msg["matched_question"],
                    msg["score"],
                    ts = ts,
                )
            else:
                ui.low_confidence_bubble(msg["score"], threshold)

            # Top-3 similar
            if show_similar and msg.get("all_results"):
                with st.expander(f"🔍 Top 3 Similar DB Matches", expanded=False):
                    ui.similar_queries_panel(msg["all_results"])

            # Feedback
            rating = ui.feedback_row(idx)
            if rating:
                log_feedback(msg.get("qid", 0), rating)
                st.toast("✅ Thank you for your feedback!", icon="✅")

            st.markdown("<hr style='border-color:rgba(255,255,255,0.05);margin:16px 0'>",
                        unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    ui.footer()


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
elif "Dashboard" in st.session_state.page:
    st.markdown("## 📊 Analytics Dashboard")

    stats = get_dashboard_stats()

    c1, c2, c3, c4 = st.columns(4)
    with c1: ui.metric_card(stats["total"],     "Total Queries")
    with c2: ui.metric_card(stats["today"],     "Queries Today")
    with c3: ui.metric_card(stats["thumb_up"],  "👍 Positive")
    with c4: ui.metric_card(stats["thumb_down"], "👎 Negative")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🌍 Language Distribution")
        if stats["lang_dist"]:
            for lang, cnt in stats["lang_dist"].items():
                st.progress(
                    cnt / max(stats["lang_dist"].values()),
                    text=f"{lang.upper()}: {cnt} queries"
                )
        else:
            st.info("No data yet.")

    with col_b:
        st.markdown("#### 🔥 Top 5 Asked Topics")
        for i, t in enumerate(stats["top_topics"], 1):
            st.markdown(f"""
            <div class="similar-card">
                <b>#{i}</b> {t['query'][:80]}
                <span class="score-pill score-high" style="float:right">{t['count']}x</span>
            </div>
            """, unsafe_allow_html=True)
        if not stats["top_topics"]:
            st.info("No data yet.")

    ui.footer()


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: HISTORY
# ═════════════════════════════════════════════════════════════════════════════
elif "History" in st.session_state.page:
    st.markdown("## 📜 Query History")

    rows = get_recent_queries(30)
    if not rows:
        st.info("No history yet. Go ask a question!")
    else:
        for row in rows:
            with st.expander(f"🕐 {row['timestamp'][:16]}  |  {row['query'][:60]}"):
                st.markdown(f"**Language:** `{row['lang'].upper()}`  |  **Mode:** `{row['mode']}`  |  **Score:** `{row['score']:.4f}`")
                if row["online_ans"]:
                    st.markdown("**🤖 AI Answer:**")
                    st.write(row["online_ans"])
                if row["offline_ans"]:
                    st.markdown("**📦 Offline Answer:**")
                    st.write(row["offline_ans"])

    ui.footer()
