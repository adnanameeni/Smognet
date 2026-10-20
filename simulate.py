"""
simulate.py — Real-time simulation for SmogNet
Loops through random samples and hits the /predict API.
Run: python simulate.py
"""
import time
import random
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000/predict"

CITIES = ["Lahore", "Karachi", "Faisalabad", "Multan", "Islamabad"]

def random_sample(high_smog: bool = False) -> dict:
    scale = 3.5 if high_smog else 1.0
    return {
        "city": random.choice(CITIES),
        "components_co": round(random.uniform(0.1, 2.5 * scale), 2),
        "components_no": round(random.uniform(0.0, 10.0 * scale), 2),
        "components_no2": round(random.uniform(2.0, 40.0 * scale), 1),
        "components_o3": round(random.uniform(20.0, 120.0), 1),
        "components_so2": round(random.uniform(0.5, 15.0 * scale), 1),
        "components_pm2_5": round(random.uniform(5.0, 80.0 * scale), 1),
        "components_pm10": round(random.uniform(10.0, 120.0 * scale), 1),
        "components_nh3": round(random.uniform(0.5, 8.0 * scale), 1),
        "temperature_2m": round(random.uniform(5.0, 42.0), 1),
        "relative_humidity_2m": round(random.uniform(20.0, 95.0), 0),
        "hour": random.randint(0, 23),
        "month": random.randint(1, 12),
        "dayofweek": random.randint(0, 6),
    }

def run_simulation(total_steps: int = 50, interval_seconds: float = 1.5):
    print("=" * 60)
    print("  SmogNet Real-Time Simulation Mode")
    print("=" * 60)
    spike_count = 0

    for step in range(1, total_steps + 1):
        # Simulate occasional high-smog events
        high_smog = random.random() > 0.65
        sample = random_sample(high_smog)

        try:
            response = requests.post(API_URL, json=sample, timeout=5)
            data = response.json()

            ts = datetime.now().strftime("%H:%M:%S")
            icon = "🔴 SPIKE" if data["spike"] else "🟢 OK   "

            print(
                f"[{ts}] Step {step:02d} | {icon} | "
                f"{data['city']:<12} | "
                f"P={data['probability']*100:5.1f}% | "
                f"Risk={data['risk_level']:<8} | "
                f"Source={data['source']}"
            )

            if data["spike"]:
                spike_count += 1
                print(f"         ⚠️  ALERT: {data['alert'][:80]}...")

        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Cannot connect to API at {API_URL}. Is the backend running?")
            break
        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(interval_seconds)

    print("=" * 60)
    print(f"Simulation complete. {spike_count}/{total_steps} spikes detected.")

if __name__ == "__main__":
    run_simulation()
