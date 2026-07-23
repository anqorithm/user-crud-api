import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_email(to: str, subject: str, body: str, html: bool = False):
    if not settings.email_enabled:
        return {"status": "disabled"}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from
    msg["To"] = to

    if html:
        part = MIMEText(body, "html")
    else:
        part = MIMEText(body, "plain")

    msg.attach(part)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        if settings.smtp_user and settings.smtp_password:
            server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.smtp_from, [to], msg.as_string())

    return {"status": "sent", "to": to}


def send_welcome_email(email: str, name: str):
    send_email(
        to=email,
        subject="Welcome to our platform!",
        body=f"Hi {name}, welcome! Your account has been created successfully.",
    )


def send_password_reset_email(email: str, reset_token: str):
    reset_link = f"https://example.com/reset-password?token={reset_token}"
    send_email(
        to=email,
        subject="Password Reset Request",
        body=f"Click the link to reset your password: {reset_link}",
    )