"""
KISAN AI – Central Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Groq ──────────────────────────────────────────────────────────────────────
GROQ_API_KEY  = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"          # free tier

# ── Offline Store ─────────────────────────────────────────────────────────────
DATA_DIR      = os.path.join(os.path.dirname(__file__), "data")
VECTORIZER_EN = os.path.join(DATA_DIR, "tfidf_vectorizer_en.pkl")
MATRIX_EN     = os.path.join(DATA_DIR, "tfidf_matrix_en.pkl")
METADATA_EN   = os.path.join(DATA_DIR, "metadata_en.pkl")
VECTORIZER_HI = os.path.join(DATA_DIR, "tfidf_vectorizer_hi.pkl")
MATRIX_HI     = os.path.join(DATA_DIR, "tfidf_matrix_hi.pkl")
METADATA_HI   = os.path.join(DATA_DIR, "metadata_hi.pkl")

# Fallback to root-level pkl files (backwards-compat)
for attr, fallback in [
    ("VECTORIZER_EN", "tfidf_vectorizer.pkl"),
    ("MATRIX_EN",     "tfidf_matrix.pkl"),
    ("METADATA_EN",   "metadata.pkl"),
]:
    path = globals()[attr]
    if not os.path.exists(path) and os.path.exists(fallback):
        globals()[attr] = fallback

# ── Analytics DB ──────────────────────────────────────────────────────────────
DB_PATH       = "kisan_analytics.db"

# ── Search ───────────────────────────────────────────────────────────────────
DEFAULT_THRESHOLD = 0.55
TOP_K             = 3

# ── App ───────────────────────────────────────────────────────────────────────
APP_TITLE     = "KISAN AI"
APP_SUBTITLE  = "Agricultural Intelligence Assistant"
VERSION       = "2.0.0"
