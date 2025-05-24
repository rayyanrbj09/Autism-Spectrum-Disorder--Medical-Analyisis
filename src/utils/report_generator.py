# report.py
from fpdf import FPDF
import os
import logging

# Configure logging
logging.basicConfig(filename="asd_app.log", level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_pdf_report(data):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="ASD Prediction Report", ln=1, align='C')
        pdf.ln(10)

        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key.capitalize()}: {value}", ln=1, align='L')

        # Safely handle filename (email may be missing)
        raw_email = data.get('email', 'unknown_user')
        safe_email_part = raw_email.replace('@', '_').replace('/', '_').replace('\\', '_').replace(':', '_')
        if not safe_email_part or safe_email_part.lower() == "n/a":
            safe_email_part = "anonymous"
        filename = f"asd_report_{safe_email_part}.pdf"

        output_dir = "reports"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        pdf.output(filepath)
        logging.info(f"Report generated: {filepath}")
        return filepath

    except Exception as e:
        logging.error(f"Error generating PDF report: {e}", exc_info=True)
        return None
