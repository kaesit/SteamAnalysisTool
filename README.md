# Game Oracle 🔮

Game Oracle is a cutting-edge market analysis tool designed specifically to empower game developers. By transforming raw market data into actionable strategies, Game Oracle helps mitigate market risks and enhances the competitiveness of game projects on a global scale. 

Our system connects directly to the Steam Web API to process real-time game data—such as pricing, genres, tags, and reviews. We then pass this data through fine-tuned NLP models (like BERT/LLaMA) to generate highly accurate predictions regarding market saturation, optimal pricing, and overall project success probability.

## 🚀 Features

- **Steam Integration:** Live data ingestion via SteamWebAPI and SteamSpy for tags, prices, and reviews.
- **NLP Market Processing:** Automated sentiment analysis and success prediction using fine-tuned ML models.
- **Cynosure Dashboard:** A highly polished, cyberpunk-inspired "system terminal" interface built with React, Tailwind v4, and Recharts.
- **Market Telemetry:** Dynamic scatter plots and tag velocity tracking to pinpoint profitable niches.

---

## 🛠️ Tech Stack

- **Frontend:** React 19, Vite, Tailwind CSS v4, Lucide React, Recharts
- **Backend:** Python 3.12+, FastAPI, Uvicorn, Pydantic v2
- **Data Processing:** `pandas`, `numpy`, `scikit-learn`, `feature-engine`
- **APIs:** Steam Web API, SteamSpy API
- **ML Ready:** Export to train HuggingFace `transformers` models

---

## 💻 Installation & Setup

Right now, the frontend "Cynosure" terminal is fully built and running on mock data. Here is how to get it running locally.

### 1. Clone the Repository
```bash
git clone https://github.com/kaesit/SteamAnalysisTool.git
cd SteamAnalysisTool
```

### 2. Run the Frontend Dashboard
Navigate to the frontend directory and install the required Node modules.

```bash
cd frontend
npm install
npm run dev
```

The application will start on `http://localhost:5173`.

### 3. Backend Setup

The Python backend handles Steam API integration, data collection, and NLP-ready data processing.

#### Install Backend Dependencies
```bash
cd backend
pip install -e .
# or
pip install -r requirements.txt
```

#### Start the API Server
```bash
python -m uvicorn main:app --reload
```

The API runs on `http://localhost:8000`

#### Access API Documentation
- **Interactive Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

#### Quick API Test
```bash
# Search for a game
curl -X POST http://localhost:8000/api/games/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Portal 2"}'

# Collect game data
curl -X POST http://localhost:8000/api/games/collect \
  -H "Content-Type: application/json" \
  -d '{"title": "Portal 2", "max_reviews": 100}'
```

See [API_ENDPOINTS.md](backend/API_ENDPOINTS.md) for complete endpoint documentation.

---

## 🔌 API Quick Reference

The backend exposes REST endpoints for game data collection:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | API health check |
| `/api/info` | GET | API metadata and capabilities |
| `/api/games/search` | POST | Search for a game by title |
| `/api/games/collect` | POST | Collect reviews and market data for a single game |
| `/api/games/collect-batch` | POST | Batch process multiple games (1-10) |

**Example Response (Single Game Collection):**
```json
{
  "status": "success",
  "total_reviews_collected": 46,
  "positive_ratio": 0.9565,
  "reviews_info": {
    "row_count": 46,
    "columns": ["review_text", "sentiment_score", "sentiment_label", ...]
  },
  "summary_info": {
    "row_count": 1,
    "columns": ["name", "price_usd", "positive_ratio", "estimated_owners_min", ...]
  }
}
```

### Using the API with Python

```python
import requests

# Search for a game
response = requests.post('http://localhost:8000/api/games/search',
    json={'query': 'Portal 2'})
game_data = response.json()

# Collect game data
response = requests.post('http://localhost:8000/api/games/collect',
    json={'title': 'Portal 2', 'max_reviews': 200})
data = response.json()

# Access the data
print(f"Collected {data['total_reviews_collected']} reviews")
print(f"Positive ratio: {data['positive_ratio']:.1%}")
```

---

## 👥 The Team
- **Berkay Sabuncu**
- **Bilal Abiç**
- **Esad Abdullah Kösedağ**
- **Eren Bozyer**
- **Mert Can Yücedağ**

## 📄 License
This project is licensed under the GNU General Public License v3.0 - see the `LICENSE` file for details.