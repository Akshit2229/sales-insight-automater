import os
import smtplib
from email.message import EmailMessage

def send_email(to_email: str, subject: str, body: str) -> tuple[bool, str]:
    """
    Sends an email using the configured SMTP server.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    
    if not all([smtp_server, smtp_user, smtp_pass]) or smtp_user == "your_email@gmail.com":
        print("SMTP is not fully configured in environment. Skipping email.")
        return False, "Email skipped: SMTP credentials not configured in .env file."
        
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"Email successfully sent to {to_email}")
        return True, f"Success! Summary sent to {to_email}"
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False, f"Failed to send email: {str(e)}"
