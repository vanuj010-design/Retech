import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp-relay.brevo.com"
SMTP_PORT = 587

SMTP_LOGIN = os.environ.get("SMTP_EMAIL")      # a28aa1001@smtp-brevo.com
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")  # 16-digit Brevo key
FROM_EMAIL = os.environ.get("FROM_EMAIL")      # verified sender email


def send_otp(receiver_email, otp):
    msg = MIMEText(f"Your ReTech OTP is {otp}. It is valid for 2 minutes.")
    msg["Subject"] = "ReTech Account Verification OTP"
    msg["From"] = FROM_EMAIL
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_LOGIN, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("SMTP SEND FAILED:", e)
        raise
