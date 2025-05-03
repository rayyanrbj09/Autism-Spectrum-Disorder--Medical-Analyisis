# report.py
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

def generate_pdf_report(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="ASD Prediction Report", ln=1, align='C')
    pdf.ln(10)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key.capitalize()}: {value}", ln=1, align='L')

    filename = f"asd_report_{data['email'].split('@')[0]}.pdf"
    filepath = os.path.join("reports", filename)
    os.makedirs("reports", exist_ok=True)
    pdf.output(filepath)

    return filepath

def send_email_with_report(recipient_email, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = 'Your ASD Prediction Report'
    msg['From'] = "your_email@example.com"
    msg['To'] = recipient_email
    msg.set_content("Attached is your ASD prediction report.")

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(pdf_path)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    # Setup your email credentials
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "your_email@example.com"
    smtp_pass = "your_app_password"  # Use App Password (2FA)

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_user, smtp_pass)
        smtp.send_message(msg)
