# Game Oracle 🔮
> **Data-driven games. Global reach.**

Game Oracle is a Steam market analysis platform built specifically for Turkish game developers. It pulls live data from the Steam Web API and SteamSpy, processes it with statistical scoring methods, and presents actionable market insights through a polished cyberpunk-style dashboard.

---

## 🎯 What It Does

Turkish indie developers often ship games without any formal market research. Game Oracle fixes that by turning raw Steam data into structured analysis — genre saturation scores, sentiment ratios, sales estimates, and localization signals — all without requiring developers to have a data science background.

---

## 🚀 Features

- **Genre Saturation Analysis** — See how crowded a genre is on Steam before committing to development
- **Review Sentiment Scoring** — Ratio-based analysis derived from existing Steam user reviews
- **Estimated Sales Range** — SteamSpy-powered ownership estimates based on genre and pricing
- **Localization Insights** — Regional response data for specific genres and price points
- **Cynosure Dashboard** — A cyberpunk-inspired terminal UI built with React, Tailwind v4, and Recharts
- **Downloadable Reports** — Export results for use in AI assistant tools or strategy sessions

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, Recharts, Lucide React |
| Backend | Python 3.12+, FastAPI, Uvicorn, Pydantic v2 |
| Data Processing | pandas, numpy, scikit-learn, feature-engine |
| APIs | Steam Web API, SteamSpy API |
| Dev Environment | Jupyter Notebook, Python Virtual Environment |

---

## 💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kaesit/SteamAnalysisTool.git
cd SteamAnalysisTool
```

### 2. Frontend (Cynosure Dashboard)

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:5173`

### 3. Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Runs on `http://localhost:8000`

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/api/info` | GET | API metadata |
| `/api/games/search` | POST | Search a game by title |
| `/api/games/collect` | POST | Collect reviews & market data for a single game |
| `/api/games/collect-batch` | POST | Batch process multiple games (1–10) |

**Example — Collect a game:**

```bash
curl -X POST http://localhost:8000/api/games/collect \
  -H "Content-Type: application/json" \
  -d '{"title": "Portal 2", "max_reviews": 100}'
```

**Example Response:**

```json
{
  "status": "success",
  "total_reviews_collected": 46,
  "positive_ratio": 0.9565,
  "summary_info": {
    "columns": ["name", "price_usd", "positive_ratio", "estimated_owners_min"]
  }
}
```

---

## 🏗️ How It Works

```
User Input (genre, price, tags, region)
        ↓
Steam Web API + SteamSpy API
        ↓
Data Processing (pandas, scikit-learn, feature-engine)
Statistical Scoring (saturation index, sentiment ratio, sales estimate)
        ↓
Cynosure Dashboard (React + Recharts)
        ↓
Downloadable Report
```

---

## 👥 Team

| Name | Role |
|---|---|
| Esad Abdullah Kösedağ | Scrum Master, Full-Stack Developer |
| Bilal Abiç | API Integration Engineer |
| Berkay Sabuncu | API Integration Engineer |
| Mert Can Yücedağ | Data Analysis Engineer |
| Eren Bozyer | Data Analysis Engineer |

Developed at **Fırat Üniversitesi, Teknoloji Fakültesi** — 2026

---

## 📄 License

GNU General Public License v3.0 — see `LICENSE` for details.
