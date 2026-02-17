import os
import requests

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
SENDER_EMAIL = os.environ.get("EMAIL_SENDER")

def send_otp(receiver_email, otp):
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {"email": SENDER_EMAIL, "name": "ReTech"},
        "to": [{"email": receiver_email}],
        "subject": "ReTech Account Verification OTP",
        "htmlContent": f"""
            <h2>Your ReTech OTP</h2>
            <p><b>{otp}</b></p>
            <p>This OTP is valid for 2 minutes.</p>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code not in (200, 201):
        raise Exception(response.text)
