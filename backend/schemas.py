from pydantic import BaseModel, Field
from typing import Optional

class PredictionRequest(BaseModel):
    city: str = Field(..., example="Lahore")
    components_co: float = Field(..., example=0.5)
    components_no: float = Field(..., example=0.1)
    components_no2: float = Field(..., example=15.0)
    components_o3: float = Field(..., example=80.0)
    components_so2: float = Field(..., example=5.0)
    components_pm2_5: float = Field(..., example=35.0)
    components_pm10: float = Field(..., example=50.0)
    components_nh3: float = Field(..., example=2.0)
    temperature_2m: float = Field(..., example=25.0)
    relative_humidity_2m: float = Field(..., example=60.0)
    hour: int = Field(..., ge=0, le=23, example=14)
    month: int = Field(..., ge=1, le=12, example=11)
    dayofweek: int = Field(..., ge=0, le=6, example=2)

class EmailAlertRequest(BaseModel):
    recipient_email: str
    city: str
    spike: int
    probability: float
    source: str
    risk_level: str
    alert: str

class PredictionResponse(BaseModel):
    city: str
    spike: int
    probability: float
    source: str
    risk_level: str
    alert: str
