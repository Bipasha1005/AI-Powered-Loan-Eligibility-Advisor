from pdf_report import generate_pdf_report

user_input = {
    "No of Dependents": 2,
    "Education": "Graduate",
    "Self Employed": "No",
    "Income (Annual)": 600000,
    "Loan Amount": 200000,
    "Loan Term (Months)": 12,
    "CIBIL Score": 750
}

generate_pdf_report(
    user_data=user_input,
    probability=0.87,
    decision="APPROVED",
    output_path="reports/sample_report.pdf"
)

print("PDF generated successfully")
