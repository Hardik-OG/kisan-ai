"""
backend/query_engine.py – Offline TF-IDF retrieval engine
Returns top-K matches with scores for a given query.
"""
import pickle
import numpy as np
from dataclasses import dataclass
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from config import (
    VECTORIZER_EN, MATRIX_EN, METADATA_EN,
    VECTORIZER_HI, MATRIX_HI, METADATA_HI,
    TOP_K,
)


@dataclass
class RetrievalResult:
    rank:           int
    question:       str
    answer:         str
    score:          float
    is_reliable:    bool   # score >= threshold


# ── Lazy-load stores per language ────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def _load_store(lang: str):
    if lang == "hi":
        vec_path, mat_path, meta_path = VECTORIZER_HI, MATRIX_HI, METADATA_HI
    else:
        vec_path, mat_path, meta_path = VECTORIZER_EN, MATRIX_EN, METADATA_EN
    try:
        vectorizer = pickle.load(open(vec_path, "rb"))
        matrix     = pickle.load(open(mat_path, "rb"))
        metadata   = pickle.load(open(meta_path, "rb"))
        return vectorizer, matrix, metadata
    except FileNotFoundError:
        return None, None, None


# ── Public API ────────────────────────────────────────────────────────────────

def retrieve(query: str, lang: str = "en", threshold: float = 0.55) -> list[RetrievalResult]:
    """
    Returns top-K RetrievalResult objects sorted by score (descending).
    Falls back to English store if Hindi store is missing.
    """
    vectorizer, matrix, metadata = _load_store(lang)
    if vectorizer is None:                        # try English fallback
        vectorizer, matrix, metadata = _load_store("en")
    if vectorizer is None:
        return []

    q_vec  = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, matrix).flatten()

    top_indices = np.argsort(scores)[-TOP_K:][::-1]
    results = []
    for rank, idx in enumerate(top_indices, start=1):
        meta  = metadata[idx]
        score = float(scores[idx])
        results.append(RetrievalResult(
            rank        = rank,
            question    = meta.get("question", ""),
            answer      = meta.get("answer", ""),
            score       = score,
            is_reliable = score >= threshold,
        ))
    return results


def best_result(query: str, lang: str = "en", threshold: float = 0.55) -> RetrievalResult | None:
    results = retrieve(query, lang, threshold)
    return results[0] if results else None
