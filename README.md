# 🌾 KISAN AI — Agricultural Intelligence Assistant

<div align="center">

![KISAN AI Banner](https://img.shields.io/badge/KISAN_AI-v2.0-brightgreen?style=for-the-badge&logo=leaf)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.33-red?style=for-the-badge&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA--3_70B-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**AI-powered agricultural helpdesk for 140M+ Indian farmers**  
Bilingual · Offline-Capable · RAG Pipeline · Analytics Dashboard

[🚀 Live Demo](#) · [📄 Report Bug](issues) · [💡 Request Feature](issues)

</div>

---

## 🎯 Problem Statement

Indian farmers—especially in rural areas—lack immediate, reliable, and language-accessible guidance on crop diseases, pest control, fertilizer use, and government schemes. Existing solutions require internet connectivity, are English-only, or lack domain specificity.

**KISAN AI solves this** with a bilingual (Hindi + English), offline-first RAG pipeline backed by Groq's LLaMA-3 70B for enhanced online answers.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Offline TF-IDF Search** | Instant answers even without internet using cosine similarity on a curated agricultural QA dataset |
| 🤖 **RAG Pipeline** | Retrieved context + Groq LLaMA-3 70B generates expert, contextualised answers |
| 🌍 **Multi-language** | Auto-detects Hindi (Devanagari) vs English; outputs in Hindi / English / Hinglish |
| 📊 **Analytics Dashboard** | Real-time query counts, language distribution, top topics, feedback tracking |
| 📜 **Chat History** | All conversations persisted in SQLite; viewable in-app |
| 📄 **PDF Export** | Beautifully formatted ReportLab PDF with branding, Q&A layout, and metadata |
| 👍👎 **Feedback System** | Per-answer thumbs up/down logged to database |
| 💡 **Suggested Questions** | Language-aware query suggestions for quick access |
| 🏆 **Top-3 Similar Matches** | Shows three closest database entries for every query |
| 🔒 **Secure API Keys** | `.env`-based key management, never hardcoded |

---

## 🏗️ Architecture

```
kisan-ai/
├── app.py                    # Streamlit entry point (3 pages: Chat, Dashboard, History)
├── config.py                 # Centralised config & constants
├── requirements.txt
├── .env.example              # API key template
│
├── backend/
│   ├── query_engine.py       # TF-IDF retrieval (Top-K cosine similarity)
│   ├── groq_service.py       # Groq LLaMA-3 RAG call (structured RAG prompt)
│   ├── pdf_generator.py      # ReportLab PDF generator (branded, formatted)
│   └── analytics.py          # SQLite persistence (queries, feedback, stats)
│
├── ui/
│   ├── styles.py             # Dark glassmorphism CSS (injected via st.markdown)
│   └── components.py         # Reusable bubble/card/chip components
│
├── utils/
│   └── language_utils.py     # Language detection + suggested questions
│
└── data/
    ├── tfidf_vectorizer_en.pkl
    ├── tfidf_matrix_en.pkl
    ├── metadata_en.pkl
    ├── tfidf_vectorizer_hi.pkl
    ├── tfidf_matrix_hi.pkl
    └── metadata_hi.pkl
```

### RAG Pipeline

```
User Query
    │
    ▼
Language Detection (Devanagari regex)
    │
    ▼
TF-IDF Offline Search ──► Top-3 Results + Scores
    │
    ├── Score ≥ threshold? → Show Offline Answer
    │
    ▼
[Online Mode] Groq LLaMA-3 RAG
    │  System: Expert agricultural advisor
    │  Context: matched_question + db_answer + score
    │  Output: Language-specific expert answer
    ▼
Display + Log to SQLite + Feedback
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Free Groq API key → [console.groq.com](https://console.groq.com/)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/kisan-ai.git
cd kisan-ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
cp .env.example .env
# Edit .env and paste your Groq API key

# 5. Add your .pkl data files to /data folder
#    (tfidf_vectorizer_en.pkl, tfidf_matrix_en.pkl, metadata_en.pkl)

# 6. Run the app
streamlit run app.py
```

App opens at **http://localhost:8501**

---

## 📸 Screenshots

> *Add screenshots of Chat page, Dashboard, and PDF export here*

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit 1.33 + Custom CSS (Glassmorphism) |
| LLM | Groq API — LLaMA-3 70B (free tier) |
| Retrieval | Scikit-learn TF-IDF + Cosine Similarity |
| RAG Orchestration | Custom Python pipeline |
| Database | SQLite (via Python `sqlite3`) |
| PDF Generation | ReportLab |
| Language Detection | Unicode Devanagari regex |
| Config Management | `python-dotenv` |

---

## 🌐 Deployment

### Streamlit Cloud (Recommended — Free)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set `app.py` as entry point
4. Add `GROQ_API_KEY` in **Secrets** settings
5. Deploy ✅

### Render (Alternative)
```bash
# Build command:
pip install -r requirements.txt

# Start command:
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 📊 Dataset

The offline QA database covers:
- 🌱 Crop diseases (wheat, rice, mustard, maize, sugarcane, cotton)
- 🐛 Pest management (aphids, locusts, stem borer, whitefly)
- 💊 Fertilizer recommendations (NPK, micro-nutrients, organic)
- 🏛️ Government schemes (PM Kisan, Fasal Bima Yojana, KCC, eNAM)
- 💧 Irrigation methods
- 🌍 Soil health & organic farming

---

## 🔮 Roadmap

- [ ] Sentence-Transformer embeddings (replace TF-IDF)
- [ ] FAISS vector database integration
- [ ] Voice input (Whisper API)
- [ ] Text-to-speech output
- [ ] FastAPI backend + React frontend
- [ ] User authentication (JWT)
- [ ] Weather API integration for crop advisory
- [ ] Image-based disease detection (CNN)

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss major changes.

```bash
git checkout -b feature/your-feature
git commit -m "feat: add voice input support"
git push origin feature/your-feature
# Open a Pull Request
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Your Name**  
📧 your.email@example.com  
🔗 [LinkedIn](https://linkedin.com/in/your-profile) · [GitHub](https://github.com/your-username)

---

<div align="center">
⭐ Star this repo if it helped you! &nbsp;|&nbsp; Built with ❤️ for Indian Farmers
</div>
