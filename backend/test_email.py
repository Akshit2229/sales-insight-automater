import os
from dotenv import load_dotenv
from services.email_service import send_email

load_dotenv(dotenv_path="../.env")

success, msg = send_email(
    to_email=os.getenv("SMTP_USER"), 
    subject="Test from Sales Insight", 
    body="This is a test message to ensure SMTP is working!"
)

print(f"Success: {success}")
print(f"Message: {msg}")
