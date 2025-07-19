# scripts/emailer.py

import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib

EMAIL = os.environ.get("EMAIL_USER")
PASS = os.environ.get("EMAIL_PASS")

def send_report_email(filepath):
    print(f"[INFO] Preparing to email report: {filepath}")
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = "trader.pradeep96@gmail.com"
    msg["Subject"] = "📊 Daily GoAlgo Strategy Report"

    msg.attach(MIMEText("Hello CEO,\n\nPlease find the attached strategy report for today.\n\n— GoAlgo AI Team", "plain"))

    with open(filepath, "rb") as f:
        part = MIMEApplication(f.read(), Name="Strategy_Report.pdf")
        part["Content-Disposition"] = 'attachment; filename="Strategy_Report.pdf"'
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASS)
            server.send_message(msg)
        print("[✅] Email sent successfully.")
    except Exception as e:
        print(f"[❌] Email sending failed: {e}")
