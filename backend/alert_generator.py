def get_risk_level(probability: float) -> str:
    if probability >= 0.85:
        return "Critical"
    elif probability >= 0.65:
        return "High"
    elif probability >= 0.45:
        return "Moderate"
    else:
        return "Low"

SOURCE_ADVICE = {
    "Crop Burning": "Smoke from crop burning contains fine particles and toxic gases. Avoid outdoor activities, keep windows closed, and use N95 masks if going outside.",
    "Vehicular": "High traffic emissions detected. Avoid main roads during peak hours. Children and elderly should stay indoors.",
    "Industrial": "Industrial pollutants including sulfur dioxide are elevated. Residents near industrial zones should take extra precautions.",
    "Dust Storm": "High dust levels detected. Cover your nose and mouth if outdoors. Keep children and pets inside.",
    "Mixed": "Multiple pollution sources detected simultaneously. This is a compound smog event — all at-risk groups should remain indoors.",
    "Unknown": "Pollution spike detected. Limit outdoor exposure and monitor air quality updates.",
}

def generate_alert(city: str, spike: int, probability: float, source: str) -> str:
    risk = get_risk_level(probability)
    if spike == 0:
        return f"Air quality in {city} is currently within acceptable limits. No immediate health risk detected."

    base_source = source.split("(")[0].strip()
    advice = SOURCE_ADVICE.get(base_source, SOURCE_ADVICE["Unknown"])

    return (
        f"⚠️ POLLUTION SPIKE ALERT for {city}! "
        f"Confidence: {probability*100:.1f}% | Risk Level: {risk}. "
        f"Primary source identified: {source}. "
        f"{advice} "
        f"High-risk groups: children, elderly, asthma and heart patients."
    )
