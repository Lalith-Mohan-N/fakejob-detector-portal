import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

import pandas as pd
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.models import JobPost


def seed_from_emscad(csv_path: Path, sample_size: int = 200, db: Session | None = None):
    df = pd.read_csv(csv_path)
    df = df.sample(n=min(sample_size, len(df)), random_state=42)

    if db is None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()

    for _, row in df.iterrows():
        job = JobPost(
            title=str(row.get("title", "")),
            location=str(row.get("location", "")) if pd.notna(row.get("location")) else None,
            department=str(row.get("department", "")) if pd.notna(row.get("department")) else None,
            salary_range=str(row.get("salary_range", "")) if pd.notna(row.get("salary_range")) else None,
            company_profile=str(row.get("company_profile", "")) if pd.notna(row.get("company_profile")) else None,
            description=str(row.get("description", "")) if pd.notna(row.get("description")) else "",
            requirements=str(row.get("requirements", "")) if pd.notna(row.get("requirements")) else None,
            benefits=str(row.get("benefits", "")) if pd.notna(row.get("benefits")) else None,
            telecommuting=bool(row.get("telecommuting", False)),
            has_company_logo=bool(row.get("has_company_logo", False)),
            has_questions=bool(row.get("has_questions", False)),
            employment_type=str(row.get("employment_type", "")) if pd.notna(row.get("employment_type")) else None,
            required_experience=str(row.get("required_experience", "")) if pd.notna(row.get("required_experience")) else None,
            required_education=str(row.get("required_education", "")) if pd.notna(row.get("required_education")) else None,
            industry=str(row.get("industry", "")) if pd.notna(row.get("industry")) else None,
            function=str(row.get("function", "")) if pd.notna(row.get("function")) else None,
            fraudulent=bool(row.get("fraudulent", False)),
            source="emscad_seed",
        )
        db.add(job)
    db.commit()
    db.close()
    print(f"Seeded {len(df)} real EMSCAD records into the database.")


if __name__ == "__main__":
    csv = Path(__file__).resolve().parent.parent / "data" / "raw" / "fake_job_postings.csv"
    if not csv.exists():
        print(f"CSV not found at {csv}. Run scripts/download_data.py first.")
        sys.exit(1)
    seed_from_emscad(csv)
