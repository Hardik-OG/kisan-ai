"""
backend/analytics.py – SQLite-powered analytics & chat persistence
"""
import sqlite3
import json
from datetime import datetime
from config import DB_PATH


# ── Schema ────────────────────────────────────────────────────────────────────

DDL = """
CREATE TABLE IF NOT EXISTS queries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   TEXT    NOT NULL,
    query       TEXT    NOT NULL,
    lang        TEXT    NOT NULL,
    mode        TEXT    NOT NULL,
    score       REAL,
    matched_q   TEXT,
    offline_ans TEXT,
    online_ans  TEXT,
    session_id  TEXT
);

CREATE TABLE IF NOT EXISTS feedback (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id   INTEGER REFERENCES queries(id),
    rating     TEXT    NOT NULL,   -- 'up' or 'down'
    timestamp  TEXT    NOT NULL
);
"""


def _conn():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with _conn() as con:
        con.executescript(DDL)


def log_query(query, lang, mode, score, matched_q, offline_ans, online_ans, session_id="default") -> int:
    with _conn() as con:
        cur = con.execute(
            """INSERT INTO queries
               (timestamp,query,lang,mode,score,matched_q,offline_ans,online_ans,session_id)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (datetime.utcnow().isoformat(), query, lang, mode,
             score, matched_q, offline_ans, online_ans, session_id)
        )
        return cur.lastrowid


def log_feedback(query_id: int, rating: str):
    with _conn() as con:
        con.execute(
            "INSERT INTO feedback (query_id,rating,timestamp) VALUES (?,?,?)",
            (query_id, rating, datetime.utcnow().isoformat())
        )


def get_dashboard_stats() -> dict:
    with _conn() as con:
        total       = con.execute("SELECT COUNT(*) FROM queries").fetchone()[0]
        today_count = con.execute(
            "SELECT COUNT(*) FROM queries WHERE timestamp LIKE ?",
            (datetime.utcnow().strftime("%Y-%m-%d") + "%",)
        ).fetchone()[0]
        lang_dist   = {r["lang"]: r["cnt"] for r in con.execute(
            "SELECT lang, COUNT(*) AS cnt FROM queries GROUP BY lang"
        ).fetchall()}
        top_topics  = con.execute(
            "SELECT query, COUNT(*) AS cnt FROM queries GROUP BY query ORDER BY cnt DESC LIMIT 5"
        ).fetchall()
        thumb_up    = con.execute("SELECT COUNT(*) FROM feedback WHERE rating='up'").fetchone()[0]
        thumb_down  = con.execute("SELECT COUNT(*) FROM feedback WHERE rating='down'").fetchone()[0]

    return {
        "total":      total,
        "today":      today_count,
        "lang_dist":  lang_dist,
        "top_topics": [{"query": r["query"], "count": r["cnt"]} for r in top_topics],
        "thumb_up":   thumb_up,
        "thumb_down": thumb_down,
    }


def get_recent_queries(limit: int = 20) -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM queries ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]
