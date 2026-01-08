from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
import os

def generate_pdf_report(user_data, probability, decision, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1 * inch, height - 1 * inch, "Loan Eligibility Evaluation Report")

    # Date
    c.setFont("Helvetica", 10)
    c.drawString(1 * inch, height - 1.3 * inch,
                 f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

    # Section: Applicant Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, height - 2 * inch, "Applicant Information")

    y = height - 2.4 * inch
    c.setFont("Helvetica", 11)

    for key, value in user_data.items():
        c.drawString(1 * inch, y, f"{key.replace('_', ' ').title()}: {value}")
        y -= 0.25 * inch

    # Section: Decision
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, y - 0.2 * inch, "Loan Decision Summary")

    c.setFont("Helvetica", 12)
    c.drawString(1 * inch, y - 0.6 * inch, f"Decision Status: {decision}")
    c.drawString(1 * inch, y - 1.0 * inch, f"Approval Probability: {probability:.2%}")

    # Interpretation
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, y - 1.6 * inch, "Interpretation")

    c.setFont("Helvetica", 11)
    explanation_text = (
        "This decision is generated using a machine learning model trained on "
        "historical loan approval data. Key factors influencing the outcome "
        "include credit score, income level, requested loan amount, and asset values."
    )

    text_obj = c.beginText(1 * inch, y - 2.0 * inch)
    for line in explanation_text.split(". "):
        text_obj.textLine(line.strip())
    c.drawText(text_obj)

    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(1 * inch, 0.75 * inch,
                 "Disclaimer: This report is AI-generated and intended for informational purposes only.")

    c.showPage()
    c.save()
