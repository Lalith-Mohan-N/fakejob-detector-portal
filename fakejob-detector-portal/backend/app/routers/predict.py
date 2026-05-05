from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import PredictIn, PredictOut, PredictUrlIn
from app.ml_models.predict import FraudPredictor
from app.ml_models.explain import Explainer
from app.models.models import PredictionLog

router = APIRouter(prefix="/predict", tags=["Prediction"])


# Lazy-loaded singleton predictor to avoid loading at import time
_predictor: FraudPredictor | None = None
_explainer: Explainer | None = None


def _get_predictor() -> FraudPredictor:
    global _predictor
    if _predictor is None:
        try:
            _predictor = FraudPredictor()
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=503,
                detail=f"ML model artifacts not found. Train models first: {e}",
            )
    return _predictor


def _get_explainer() -> Explainer:
    global _explainer
    if _explainer is None:
        try:
            _explainer = Explainer()
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=503,
                detail=f"ML model artifacts not found. Train models first: {e}",
            )
    return _explainer


@router.post("/structured", response_model=PredictOut)
def predict_structured(payload: PredictIn, db: Session = Depends(get_db)):
    try:
        predictor = _get_predictor()
        result = predictor.predict_structured(payload.model_dump())
        explainer = _get_explainer()
        explanation = explainer.explain_structured(payload.model_dump())

        log = PredictionLog(
            is_fraudulent=result["is_fraudulent"],
            confidence_score=result["confidence_score"],
            risk_percentage=result["risk_percentage"],
            model_used=result["model_used"],
            suspicious_phrases=explanation["suspicious_phrases"],
            explanation=explanation,
            raw_input=payload.model_dump(),
        )
        db.add(log)
        db.commit()

        return PredictOut(
            is_fraudulent=result["is_fraudulent"],
            confidence_score=result["confidence_score"],
            risk_percentage=result["risk_percentage"],
            model_used=result["model_used"],
            suspicious_phrases=explanation["suspicious_phrases"],
            explanation=explanation,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/url")
def predict_url(payload: PredictUrlIn, db: Session = Depends(get_db)):
    try:
        scraped = FraudPredictor.scrape_job_url(payload.url)
        predictor = _get_predictor()
        result = predictor.predict_structured(scraped)
        explainer = _get_explainer()
        explanation = explainer.explain_structured(scraped)

        log = PredictionLog(
            is_fraudulent=result["is_fraudulent"],
            confidence_score=result["confidence_score"],
            risk_percentage=result["risk_percentage"],
            model_used=result["model_used"],
            suspicious_phrases=explanation["suspicious_phrases"],
            explanation=explanation,
            raw_input={"url": payload.url, "scraped": scraped},
        )
        db.add(log)
        db.commit()

        return {
            "scraped_data": scraped,
            "prediction": result,
            "explanation": explanation,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
