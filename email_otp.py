import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")


# ================= OTP MAIL =================
def send_otp(receiver_email, otp):
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials missing")

    try:
        msg = MIMEText(f"Your ReTech OTP is {otp}. It is valid for 5 minutes.")
        msg["Subject"] = "ReTech Account Verification OTP"
        msg["From"] = SMTP_EMAIL
        msg["To"] = receiver_email

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("OTP sent to:", receiver_email)

    except Exception as e:
        print("SMTP OTP ERROR:", e)
        raise


# ================= SUPPORT MAIL =================
def send_support_mail(subject, message):
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials missing")

    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = SMTP_EMAIL

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("Support mail sent")

    except Exception as e:
        print("SMTP SUPPORT ERROR:", e)
        raise
