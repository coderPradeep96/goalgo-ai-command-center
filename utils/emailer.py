import smtplib
import pdfkit
from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

def generate_pdf_from_html(template_vars, output_pdf="report.pdf"):
    env = Environment(loader=FileSystemLoader("utils/templates"))
    template = env.get_template("report_template.html")
    html_out = template.render(**template_vars)

    pdfkit.from_string(html_out, output_pdf)
    return output_pdf

def send_email_with_pdf(subject, body, receiver_email, attachment_path):
    sender_email = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with open(attachment_path, "rb") as f:
        part = MIMEApplication(f.read(), _subtype="pdf")
        part.add_header("Content-Disposition", "attachment", filename=os.path.basename(attachment_path))
        message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(message)
