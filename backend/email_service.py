import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

def send_alert_email(recipient, city, spike, probability, source, risk_level, alert):
    SENDER_EMAIL = os.getenv("SMTP_EMAIL", "")
    SENDER_PASSWORD = os.getenv("SMTP_APP_PASSWORD", "")

    # DEBUG — print what values are being read
    print(f"[EMAIL DEBUG] SENDER_EMAIL = '{SENDER_EMAIL}'")
    print(f"[EMAIL DEBUG] SENDER_PASSWORD = '{SENDER_PASSWORD[:4]}...'" if SENDER_PASSWORD else "[EMAIL DEBUG] SENDER_PASSWORD = EMPTY")
    print(f"[EMAIL DEBUG] RECIPIENT = '{recipient}'")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("[EMAIL DEBUG] Skipping — credentials missing in .env")
        return {"status": "skipped", "reason": "SMTP credentials not configured"}

    subject = f"🚨 SmogNet Alert - {city}"
    body = f"Spike detected in {city}!\nProbability: {probability*100:.1f}%\nSource: {source}\nRisk: {risk_level}\n\n{alert}"

    try:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg.attach(MIMEText(body, "plain"))

        print("[EMAIL DEBUG] Connecting to SMTP...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())

        print("[EMAIL DEBUG] ✅ Email sent successfully!")
        return {"status": "sent", "recipient": recipient}

    except Exception as e:
        print(f"[EMAIL DEBUG] ❌ Failed: {e}")
        return {"status": "failed", "reason": str(e)}