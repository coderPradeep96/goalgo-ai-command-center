import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os

def send_email(recipient_email, subject, body, attachment_path=None):
    try:
        sender_email = st.secrets["EMAIL_SENDER"]
        recipient_email = st.secrets["EMAIL_RECIEVER"]
        sender_password = st.secrets["EMAIL_PASS"]

        # Setup the MIME
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        # Body content
        message.attach(MIMEText(body, "plain"))

        # Attachment (if provided)
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                message.attach(part)

        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)

        return True, f"📧 Email sent successfully to {recipient_email}"
    
    except Exception as e:
        return False, f"❌ Failed to send email: {str(e)}"
