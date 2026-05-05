You are an expert full-stack ML engineer. Build Phase 1 of the "Real-Time Global Job Vacancy Portal with Intelligent Fake Job Detection System" using **only real data** — no synthetic, random, or placeholder data allowed at any point.

Project Name: fakejob-detector-portal

Create the complete folder structure and all necessary files:

Root structure:
fakejob-detector-portal/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── utils/
│   │   └── ml_models/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic/
├── data/
│   └── raw/
├── notebooks/
├── scripts/
├── docker-compose.yml
├── .env.example
├── README.md
└── tests/

Requirements (Strictly Real Data):
1. Use FastAPI + Uvicorn + SQLAlchemy (PostgreSQL for prod, SQLite for dev).
2. Implement JWT authentication.
3. Download the real EMSCAD dataset from Kaggle: https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction (or the original EMSCAD). Place it in data/raw/. Use only this real dataset for training and evaluation.
4. Perform proper EDA and preprocessing on the actual dataset columns (title, location, department, company_profile, description, requirements, benefits, telecommuting, has_company_logo, has_questions, employment_type, required_experience, required_education, industry, function, fraudulent label, etc.).
5. Handle class imbalance using real techniques (class weights, SMOTE, etc.) on the actual data distribution.
6. Engineer features from the real text fields + metadata. Train Random Forest, XGBoost, and a transformer-based model (DistilBERT or similar) using only the real dataset. Save the best model(s) with joblib / HuggingFace format.
7. Create a /predict endpoint that accepts real job details (JSON matching dataset schema) or a real job URL (scrape using BeautifulSoup/Playwright — only real public URLs).
8. Return: is_fraudulent (bool), confidence_score, risk_percentage, highlighted suspicious phrases (from real patterns in dataset), and SHAP/LIME explanation using real feature importance.
9. Seed the database only with real samples extracted from the EMSCAD dataset for testing.
10. Include comprehensive README with setup, real sample predictions (using actual jobs from the dataset), architecture diagram, and training instructions.

Generate ALL code files completely. Everything must be based on real dataset columns and real data patterns. Use Python 3.11+.