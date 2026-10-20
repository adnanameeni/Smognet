import pandas as pd
from backend.model_loader import get_model
from backend.schemas import PredictionRequest

FEATURE_ORDER = [
    "components_co", "components_no", "components_no2", "components_o3",
    "components_so2", "components_pm2_5", "components_pm10", "components_nh3",
    "temperature_2m", "relative_humidity_2m", "hour", "month", "dayofweek"
]

# Thresholds for rule-based fallback spike scoring
SPIKE_THRESHOLDS = {
    "components_pm2_5": 75.0,
    "components_pm10": 150.0,
    "components_no2": 40.0,
    "components_so2": 20.0,
    "components_co": 2.0,
    "components_nh3": 8.0,
}

def rule_based_probability(request: PredictionRequest) -> float:
    """Score-based fallback when model only has one class in training data."""
    score = 0.0
    data = {f: getattr(request, f) for f in FEATURE_ORDER}
    for feat, thresh in SPIKE_THRESHOLDS.items():
        val = data.get(feat, 0)
        if val > thresh:
            score += min(1.0, val / thresh - 1.0) * 0.25
    return round(min(score, 0.99), 4)

def predict(request: PredictionRequest) -> tuple[int, float]:
    model = get_model()
    data = {feat: getattr(request, feat) for feat in FEATURE_ORDER}
    df = pd.DataFrame([data])

    classes = list(model.classes_)

    # Model has both classes — use ML probability
    if 1 in classes or "1" in classes:
        proba_matrix = model.predict_proba(df)
        spike_idx = classes.index(1) if 1 in classes else classes.index("1")
        proba = float(proba_matrix[0][spike_idx])
    else:
        # Model was trained with only class 0 (no spikes in training data)
        # Fall back to rule-based scoring using pollutant thresholds
        proba = rule_based_probability(request)

    spike = int(proba > 0.5)
    return spike, round(proba, 4)
