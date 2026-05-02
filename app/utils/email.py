import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp_email(email, code):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    html = f"""
    <html>
      <body style="font-family: Arial; text-align:center;">
        <h2>🔐 Verifikasi Email</h2>
        <p>Kode OTP kamu:</p>
        <h1 style="letter-spacing:5px;">{code}</h1>
        <p>Berlaku 5 menit</p>
      </body>
    </html>
    """

    msg = MIMEText(html, "html")
    msg["Subject"] = "Kode Verifikasi"
    msg["From"] = sender
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, email, msg.as_string())

        print("EMAIL TERKIRIM")
    except Exception as e:
        print("ERROR:", e)