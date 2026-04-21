"""
utils/language_utils.py – Language detection & translation helpers
"""
import re


DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")

LANG_LABELS = {
    "en":       "English",
    "hi":       "Hindi",
    "hinglish": "Hinglish",
}

SUGGESTED_QUESTIONS = {
    "en": [
        "How to control aphids on mustard crop?",
        "What fertilizer is best for wheat?",
        "How to apply PM Kisan Yojana?",
        "What is the cure for rice blast disease?",
        "How to improve soil fertility naturally?",
        "Best irrigation method for sugarcane?",
        "How to control locusts in my farm?",
    ],
    "hi": [
        "सरसों में माहू कीट कैसे रोकें?",
        "गेहूं के लिए सबसे अच्छा खाद कौन सा है?",
        "पीएम किसान योजना में आवेदन कैसे करें?",
        "धान की ब्लास्ट बीमारी का इलाज क्या है?",
        "मिट्टी की उर्वरता कैसे बढ़ाएं?",
        "गन्ने के लिए सबसे अच्छी सिंचाई विधि कौन सी है?",
        "टिड्डी दल को खेत से कैसे भगाएं?",
    ],
}


def detect_language(text: str) -> str:
    """Return 'hi' if Devanagari script detected, else 'en'."""
    if DEVANAGARI_RE.search(str(text)):
        return "hi"
    return "en"


def get_suggested_questions(lang: str = "en") -> list[str]:
    return SUGGESTED_QUESTIONS.get(lang, SUGGESTED_QUESTIONS["en"])
