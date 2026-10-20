import smtplib, os
from email.mime.text import MIMEText

email = "adnanuetm27@gmail.com"
password = "ieotozqexsfblxmb"   # your 16-char app password
recipient = "adnanuetm27@gmail.com"

msg = MIMEText("SmogNet test alert — SMTP is working!")
msg["Subject"] = "SmogNet Test"
msg["From"] = email
msg["To"] = recipient

with smtplib.SMTP("smtp.gmail.com", 587) as s:
    s.starttls()
    s.login(email, password)
    s.sendmail(email, recipient, msg.as_string())

print("Email sent successfully!")