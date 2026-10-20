import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "smognet_model.pkl")

_model = None

def get_model():
    global _model
    if _model is None:
        try:
            _model = joblib.load(MODEL_PATH)
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    return _model
