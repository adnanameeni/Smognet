from backend.schemas import PredictionRequest

def classify_source(req: PredictionRequest) -> str:
    co   = req.components_co
    no   = req.components_no
    no2  = req.components_no2
    so2  = req.components_so2
    pm25 = req.components_pm2_5
    pm10 = req.components_pm10
    nh3  = req.components_nh3

    sources = []

    if nh3 > 5 and co > 1.0:
        sources.append("Crop Burning")
    if no2 > 30 and no > 5:
        sources.append("Vehicular")
    if so2 > 10:
        sources.append("Industrial")
    if pm10 > pm25 * 2.5 and pm10 > 80:
        sources.append("Dust Storm")

    if len(sources) == 0:
        return "Unknown"
    if len(sources) == 1:
        return sources[0]
    return "Mixed (" + " + ".join(sources) + ")"
