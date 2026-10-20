import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"

def enhance_alert_with_groq(city: str, source: str, risk_level: str, probability: float) -> str | None:
    """Use Groq LLM to generate a human-friendly alert. Returns None if not configured or fails."""
    if not GROQ_API_KEY:
        return None

    prompt = (
        f"You are an air quality health advisor. Write a concise 3-sentence public health alert for {city}. "
        f"A pollution spike has been detected with {probability*100:.1f}% confidence. "
        f"Primary source: {source}. Risk level: {risk_level}. "
        f"Address: what it means, who is at risk (children, elderly, asthma patients), and what they should do. "
        f"Be clear, urgent but not panic-inducing."
    )

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200,
                "temperature": 0.5
            },
            timeout=10
        )
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
