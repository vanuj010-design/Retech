import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "vermaalka705@gmail.com"
APP_PASSWORD = "gpdhqmxgviotfhmy"  # Gmail App Password

def send_otp(receiver_email, otp):
    msg = MIMEText(f"Your ReTech OTP is {otp}. It is valid for 2 minutes.")
    msg["Subject"] = "ReTech Account Verification OTP"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)


from email.mime.text import MIMEText

ADMIN_EMAIL = "vermaalka705@gmail.com"     # 🔴 your gmail
APP_PASSWORD = "gpdhqmxgviotfhmy"      # 🔴 Gmail App Password

def send_support_mail(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = ADMIN_EMAIL
    msg["To"] = ADMIN_EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(ADMIN_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()
