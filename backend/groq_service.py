"""
backend/groq_service.py – Groq LLaMA-3 LLM service (free API)
"""
import os
import requests
from config import GROQ_API_KEY, GROQ_MODEL

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPTS = {
    "Hindi": (
        "आप एक विशेषज्ञ कृषि सलाहकार हैं। किसानों को हिंदी में सरल, "
        "व्यावहारिक और सटीक उत्तर दें। तकनीकी शब्दों को भी हिंदी में समझाएं।"
    ),
    "English": (
        "You are an expert agricultural advisor. Provide clear, practical, "
        "and accurate answers to farmers in simple English."
    ),
    "Hinglish": (
        "Aap ek expert agricultural advisor hain. Farmers ko Hinglish mein "
        "simple aur practical jawab dein. Hindi aur English mix karein."
    ),
}

RAG_TEMPLATE = """
You are KISAN AI, an expert agricultural assistant for Indian farmers.

RETRIEVED CONTEXT (from offline database):
---
Matched Question : {matched_question}
Database Answer  : {database_answer}
Confidence Score : {score:.4f}
---

USER QUERY: {query}

INSTRUCTIONS:
- Use the retrieved context as primary reference.
- Add any additional expert knowledge if helpful.
- Keep the answer concise, practical, and easy for a farmer to understand.
- If context is irrelevant, use your own knowledge.
- Do NOT mention "retrieved context" or "database" in your answer.
- Answer in {output_language}.
"""


def get_groq_answer(
    query: str,
    matched_question: str,
    database_answer: str,
    score: float,
    output_language: str = "Hindi",
) -> str:
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not configured. Set it in your .env file."

    prompt = RAG_TEMPLATE.format(
        matched_question = matched_question,
        database_answer  = database_answer,
        score            = score,
        query            = query,
        output_language  = output_language,
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type":  "application/json",
    }

    payload = {
        "model":    GROQ_MODEL,
        "messages": [
            {"role": "system",  "content": SYSTEM_PROMPTS.get(output_language, SYSTEM_PROMPTS["Hindi"])},
            {"role": "user",    "content": prompt},
        ],
        "temperature": 0.4,
        "max_tokens":  800,
    }

    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        return f"❌ API Error: {e.response.status_code} – {e.response.text[:200]}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"
