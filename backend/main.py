from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.schemas import PredictionRequest, EmailAlertRequest, PredictionResponse
from backend.predictor import predict
from backend.classifier import classify_source
from backend.alert_generator import generate_alert, get_risk_level
from backend.email_service import send_alert_email
from backend.groq_service import enhance_alert_with_groq

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="SmogNet Air Quality Intelligence API",
    description="ML-powered pollution spike detection with email alerts",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "SmogNet API is running. Visit /docs for API documentation."}

@app.get("/health")
def health():
    from backend.model_loader import get_model
    try:
        model = get_model()
        return {
            "status": "healthy",
            "model": "RandomForestClassifier",
            "n_estimators": model.n_estimators,
            "features": list(model.feature_names_in_)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model not loaded: {e}")

@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(request: PredictionRequest):
    try:
        spike, probability = predict(request)
        source = classify_source(request)
        risk_level = get_risk_level(probability)

        # Try Groq-enhanced alert first, fallback to rule-based
        alert = enhance_alert_with_groq(request.city, source, risk_level, probability)
        if not alert:
            alert = generate_alert(request.city, spike, probability, source)

        # Auto-send email if spike detected and probability is high
        alert_email = os.getenv("ALERT_EMAIL", "")
        if alert_email and (spike == 1 or probability > 0.75):
            send_alert_email(alert_email, request.city, spike, probability, source, risk_level, alert)

        return PredictionResponse(
            city=request.city,
            spike=spike,
            probability=probability,
            source=source,
            risk_level=risk_level,
            alert=alert
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/alert/email")
def send_email_endpoint(request: EmailAlertRequest):
    result = send_alert_email(
        recipient=request.recipient_email,
        city=request.city,
        spike=request.spike,
        probability=request.probability,
        source=request.source,
        risk_level=request.risk_level,
        alert=request.alert
    )
    return result
