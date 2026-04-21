"""
backend/pdf_generator.py – Professional PDF report generator using ReportLab
"""
import os
import datetime
import textwrap
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# ── Colour palette ────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#1a5c2e")
GREEN_MID   = colors.HexColor("#2d8a4e")
GREEN_LIGHT = colors.HexColor("#d4edda")
GOLD        = colors.HexColor("#f0a500")
DARK_TEXT   = colors.HexColor("#1a1a2e")
GREY_TEXT   = colors.HexColor("#555566")
WHITE       = colors.white


def _styles():
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "KisanTitle",
        parent    = base["Heading1"],
        fontSize  = 22,
        textColor = WHITE,
        alignment = TA_CENTER,
        spaceAfter = 4,
        fontName   = "Helvetica-Bold",
    )
    subtitle_style = ParagraphStyle(
        "KisanSub",
        parent    = base["Normal"],
        fontSize  = 10,
        textColor = colors.HexColor("#ccffdd"),
        alignment = TA_CENTER,
        fontName  = "Helvetica",
    )
    section_style = ParagraphStyle(
        "KisanSection",
        parent    = base["Heading2"],
        fontSize  = 12,
        textColor = GREEN_DARK,
        spaceBefore = 10,
        spaceAfter  = 4,
        fontName    = "Helvetica-Bold",
    )
    q_style = ParagraphStyle(
        "KisanQ",
        parent    = base["Normal"],
        fontSize  = 11,
        textColor = DARK_TEXT,
        fontName  = "Helvetica-Bold",
        spaceAfter = 4,
    )
    a_style = ParagraphStyle(
        "KisanA",
        parent    = base["Normal"],
        fontSize  = 10,
        textColor = DARK_TEXT,
        fontName  = "Helvetica",
        leading   = 15,
        spaceAfter = 6,
    )
    meta_style = ParagraphStyle(
        "KisanMeta",
        parent    = base["Normal"],
        fontSize  = 8,
        textColor = GREY_TEXT,
        fontName  = "Helvetica-Oblique",
    )
    return title_style, subtitle_style, section_style, q_style, a_style, meta_style


def generate_pdf_bytes(chat_data: list[dict]) -> bytes:
    """
    Accepts list of chat dicts, returns PDF as bytes (for st.download_button).
    """
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize     = A4,
        rightMargin  = 18 * mm,
        leftMargin   = 18 * mm,
        topMargin    = 20 * mm,
        bottomMargin = 18 * mm,
    )

    title_s, sub_s, sec_s, q_s, a_s, meta_s = _styles()
    story = []

    # ── Header banner (table trick) ───────────────────────────────────────────
    now_str = datetime.datetime.now().strftime("%d %b %Y  %H:%M")
    header_data = [[
        Paragraph("🌾  KISAN AI", title_s),
        Paragraph(f"Generated: {now_str}", sub_s),
    ]]
    header_table = Table(header_data, colWidths=["65%", "35%"])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), GREEN_DARK),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [GREEN_DARK]),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [6]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10 * mm))

    # ── Summary stats row ─────────────────────────────────────────────────────
    stats_data = [[
        Paragraph(f"<b>{len(chat_data)}</b><br/>Total Queries", meta_s),
        Paragraph(f"<b>KISAN AI v2.0</b><br/>Agricultural Assistant", meta_s),
        Paragraph(f"<b>Groq LLaMA-3</b><br/>LLM Engine", meta_s),
    ]]
    stats_table = Table(stats_data, colWidths=["33%", "34%", "33%"])
    stats_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), GREEN_LIGHT),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 0.5, GREEN_MID),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [4]),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 8 * mm))

    # ── Q&A entries ───────────────────────────────────────────────────────────
    story.append(Paragraph("📋  Chat History", sec_s))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN_MID, spaceAfter=6))

    for i, msg in enumerate(chat_data, start=1):
        if not isinstance(msg, dict):
            continue

        block = []
        block.append(Paragraph(f"Q{i}: {msg.get('query', '')}", q_s))

        score    = msg.get("score", 0)
        matched  = msg.get("matched_question", "")
        off_ans  = msg.get("offline_answer", "")
        on_ans   = msg.get("online_answer", "")

        if off_ans:
            block.append(Paragraph("📦  Offline Match:", sec_s))
            block.append(Paragraph(off_ans, a_s))
            block.append(Paragraph(
                f"Matched: {matched}  |  Confidence: {score:.4f}", meta_s
            ))

        if on_ans:
            block.append(Spacer(1, 3 * mm))
            block.append(Paragraph("🤖  AI Answer (Groq):", sec_s))
            block.append(Paragraph(on_ans, a_s))

        block.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=4))
        story.append(KeepTogether(block))
        story.append(Spacer(1, 3 * mm))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN_DARK))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "KISAN AI  |  Built for Indian Farmers  |  Powered by Groq LLaMA-3 & TF-IDF RAG",
        ParagraphStyle("footer", fontSize=8, textColor=GREY_TEXT, alignment=TA_CENTER)
    ))

    doc.build(story)
    return buf.getvalue()
