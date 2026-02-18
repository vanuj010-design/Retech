import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_LOGIN = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
FROM_EMAIL = os.environ.get("FROM_EMAIL")

def send_otp(receiver_email, otp):
    msg = MIMEText(f"Your ReTech OTP is {otp}. It is valid for 5 minutes.")
    msg["Subject"] = "ReTech Account Verification OTP"
    msg["From"] = FROM_EMAIL
    msg["To"] = receiver_email

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_LOGIN, SMTP_PASSWORD)
    server.sendmail(FROM_EMAIL, receiver_email, msg.as_string())
    server.quit()
