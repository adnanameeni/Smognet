# 🌫️ SmogNet — Air Quality Intelligence System

ML-powered pollution spike detection with FastAPI backend, email alerts, and Groq AI integration.

---

## 📦 Project Structure

```
smognet/
├── backend/
│   ├── main.py              # FastAPI app + all endpoints
│   ├── model_loader.py      # joblib model loading
│   ├── predictor.py         # ML prediction logic
│   ├── classifier.py        # Rule-based source classification
│   ├── alert_generator.py   # Alert text generation
│   ├── email_service.py     # Gmail SMTP alerts
│   ├── groq_service.py      # Groq LLM alert enhancer
│   └── schemas.py           # Pydantic request/response models
├── model/
│   └── smognet_model.pkl    # Trained RandomForest model
├── frontend/
│   └── index.html           # Dashboard UI
├── simulate.py              # Real-time simulation script
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your Gmail App Password and Groq API key
```

### 3. Run the backend
```bash
# From the smognet/ directory
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open dashboard
Visit: http://localhost:8000

API docs: http://localhost:8000/docs

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | System status + model info |
| POST | `/predict` | Run ML prediction |
| POST | `/alert/email` | Manually trigger email alert |

### /predict — Request Body
```json
{
  "city": "Lahore",
  "components_co": 0.5,
  "components_no": 0.1,
  "components_no2": 15.0,
  "components_o3": 80.0,
  "components_so2": 5.0,
  "components_pm2_5": 35.0,
  "components_pm10": 50.0,
  "components_nh3": 2.0,
  "temperature_2m": 25.0,
  "relative_humidity_2m": 60.0,
  "hour": 14,
  "month": 11,
  "dayofweek": 2
}
```

### /predict — Response
```json
{
  "city": "Lahore",
  "spike": 1,
  "probability": 0.87,
  "source": "Industrial",
  "risk_level": "High",
  "alert": "⚠️ POLLUTION SPIKE ALERT for Lahore!..."
}
```

---

## 🧠 ML Model Details

- **Algorithm:** RandomForestClassifier (200 trees)
- **Features (13):** CO, NO, NO₂, O₃, SO₂, PM2.5, PM10, NH₃, temperature, humidity, hour, month, dayofweek
- **Output:** Binary classification (0 = no spike, 1 = spike)
- **Threshold:** probability > 0.5 → spike

---

## 🔬 Source Classification Rules

| Source | Condition |
|--------|-----------|
| Crop Burning | NH₃ > 5 AND CO > 1.0 |
| Vehicular | NO₂ > 30 AND NO > 5 |
| Industrial | SO₂ > 10 |
| Dust Storm | PM10 > 2.5× PM2.5 AND PM10 > 80 |
| Mixed | Multiple triggers |

---

## 📧 Gmail Email Setup

1. Go to **myaccount.google.com → Security → 2-Step Verification → App Passwords**
2. Create an App Password for "Mail"
3. Add to `.env`:
   ```
   SMTP_EMAIL=your@gmail.com
   SMTP_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ALERT_EMAIL=recipient@example.com
   ```

Emails are sent automatically when `spike == 1` or `probability > 0.75`.

---

## ⚡ Real-Time Simulation

```bash
python simulate.py
```

Sends 50 random pollution readings to the API at 1.5s intervals, printing live results.

---

## 🚀 Deployment

### Local
```bash
uvicorn backend.main:app --reload
```

### Production (Render)
1. Push to GitHub
2. Create new Web Service on [render.com](https://render.com)
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard

### Production (Railway)
```bash
railway init
railway up
```

---

## 🎓 Viva Defense Q&A

**Q: Why FastAPI instead of Flask?**
FastAPI provides automatic OpenAPI docs, native async support, and Pydantic validation built-in. It's 2–3× faster than Flask and much better suited for ML APIs that need strict input validation and scalability.

**Q: How does the ML model integrate in the API?**
The model is loaded once at startup using joblib (singleton pattern in `model_loader.py`). Each `/predict` request constructs a pandas DataFrame with the exact 13 features the model was trained on, calls `predict_proba()`, and returns the spike class plus confidence probability.

**Q: Why rule-based + ML hybrid (two-layer system)?**
The ML model predicts *whether* a spike occurs, but can't explain *why*. The rule-based classifier adds interpretability — it tells authorities which source (vehicles, industry, crop burning) to target. This is critical for actionable public health response.

**Q: How do email alerts work in real-world systems?**
We use Gmail SMTP with App Passwords (not the main account password) for security. The system auto-triggers alerts when spike probability crosses a threshold. In production, this would connect to an SMS gateway or push notification service for broader reach.

**Q: Why Groq instead of HuggingFace for LLM?**
Groq provides free-tier API access with extremely fast inference (running on custom LPU hardware). No GPU required, no local model download, and it's significantly faster than HuggingFace hosted inference endpoints — ideal for real-time alert generation.

**Q: What is the risk level classification?**
- Critical: probability ≥ 85%
- High: probability ≥ 65%
- Moderate: probability ≥ 45%
- Low: below 45%
