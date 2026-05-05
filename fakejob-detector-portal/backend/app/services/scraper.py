from app.ml_models.predict import FraudPredictor


def scrape_and_predict(url: str) -> dict:
    scraped = FraudPredictor.scrape_job_url(url)
    predictor = FraudPredictor()
    prediction = predictor.predict_structured(scraped)
    from app.ml_models.explain import Explainer
    explanation = Explainer().explain_structured(scraped)
    return {
        "scraped_data": scraped,
        "prediction": prediction,
        "explanation": explanation,
    }
