import smtplib, ssl
import random
import os

host = "smtp.gmail.com"  # Change if using another provider
port = 465
SENDER_EMAIL ="pythonsendsmail8@gmail.com"
SENDER_PASSWORD = os.getenv("PYTHONEMAILPASS")

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email: str, ot: str):
    sslcontext = ssl.create_default_context()
    m = f"Your OTP for CleanIt Login is: {ot}. Valid for 5 minutes."
    message = f"""From: CleanIt <{SENDER_EMAIL}>
To: {email}
Subject: OTP for CleanIt Login

{m}
Regards,
CleanIt Team
"""
    try:
        with smtplib.SMTP_SSL(host, port, context=sslcontext) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, message)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    otp = generate_otp()
    print(send_otp_email("mayank.kapoor2607@gmail.com",otp))