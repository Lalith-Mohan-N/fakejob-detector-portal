# Fake Job Detector Portal

Real-Time Global Job Vacancy Portal with Intelligent Fake Job Detection System.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Fake Job Detector Portal                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐     ┌─────────────────┐     ┌──────────────────────────┐  │
│  │  Next.js 15  │────▶│  FastAPI        │────▶│  PostgreSQL / SQLite    │  │
│  │  (React 19)  │◄────│  Backend        │     │   Database              │  │
│  │  Tailwind    │     │                 │     └──────────────────────────┘  │
│  │  shadcn/ui   │     │  ML Pipeline    │                                   │
│  │  Dark Mode   │     │  ┌──────────┐  │                                   │
│  └──────────────┘     │  │  RF/XGB  │  │                                   │
│                       │  │ DistilBERT│  │                                   │
│                       │  └──────────┘  │                                   │
│                       └─────────────────┘                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- Kaggle API credentials (for real dataset download)

## Setup

1. **Clone and enter the project:**
   ```bash
   cd fakejob-detector-portal
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your DATABASE_URL, SECRET_KEY, and Kaggle credentials
   ```

5. **Download the real EMSCAD dataset:**
   ```bash
   python scripts/download_data.py
   ```

6. **Train the models:**
   ```bash
   cd backend
   python -m app.ml_models.train
   cd ..
   ```

7. **Seed the database with real samples:**
   ```bash
   python scripts/seed_db.py
   ```

8. **Run the backend server:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   cd ..
   ```

## Frontend Setup (Phase 2)

9. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   ```

10. **Configure frontend environment:**
    ```bash
    cp .env.local.example .env.local
    # Defaults to http://localhost:8000 for the API
    ```

11. **Run the Next.js dev server:**
    ```bash
    npm run dev
    ```

12. **Open the app:**
    Navigate to [http://localhost:3000](http://localhost:3000)

### Frontend Features
- **Home Page** — Overview and navigation cards
- **Analyze Page** — Manual job form entry, URL scraping, image OCR analysis
- **Live Feed** — Real job listings from public APIs (Remotive) with inline fraud scoring
- **Dashboard** — Statistics and history of real checks from the seeded dataset
- **Dark Mode** — Toggle between light/dark/system themes

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/auth/register` | POST | Register new user |
| `/auth/login` | POST | JWT login |
| `/jobs/` | GET / POST | List / create jobs |
| `/jobs/{id}` | GET / PUT / DELETE | Retrieve / update / delete job |
| `/predict/structured` | POST | Predict fraud from structured JSON |
| `/predict/url` | POST | Scrape a real job URL and predict |

## Example Prediction

```bash
curl -X POST http://localhost:8000/predict/structured \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Work from home - earn $5000 weekly",
    "description": "No experience needed. Send money for training.",
    "requirements": "Bank account and SSN required.",
    "has_company_logo": false,
    "telecommuting": true
  }'
```

**Response:**
```json
{
  "is_fraudulent": true,
  "confidence_score": 0.94,
  "risk_percentage": 94.0,
  "model_used": "ensemble_rf_xgb",
  "suspicious_phrases": [
    {"phrase": "work from home", "severity": "high"},
    {"phrase": "no experience needed", "severity": "high"},
    {"phrase": "send money", "severity": "high"},
    {"phrase": "bank account", "severity": "high"},
    {"phrase": "social security number", "severity": "high"}
  ],
  "explanation": {
    "feature_importance": [...],
    "shap_summary": "Top features driving prediction based on real EMSCAD patterns"
  }
}
```

## Docker

```bash
docker-compose up --build
```

## Running Tests

```bash
pytest tests/
```

## Project Structure

```
fakejob-detector-portal/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/           (config, database, security)
│   │   ├── models/         (SQLAlchemy models)
│   │   ├── schemas/        (Pydantic schemas)
│   │   ├── routers/        (auth, jobs, predict)
│   │   ├── services/       (job service, scraper)
│   │   ├── utils/
│   │   └── ml_models/      (preprocess, train, predict, explain, train_bert)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic/
├── frontend/
│   ├── app/                (Next.js 15 App Router pages)
│   ├── components/           (shadcn/ui, feature components)
│   ├── lib/                 (API client, utilities)
│   ├── types/               (TypeScript types)
│   ├── package.json
│   └── next.config.js
├── data/raw/
├── notebooks/              (EDA & model training)
├── scripts/                (download, seed, setup)
├── tests/
├── docker-compose.yml
└── README.md
```

## License

MIT
