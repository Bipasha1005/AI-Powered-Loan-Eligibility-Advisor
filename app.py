import streamlit as st
import pandas as pd
import os
from src.predict import predict_loan
from src.pdf_report import generate_pdf_report

st.set_page_config(
    page_title="AI-Powered Loan Eligibility Advisor",
    layout="centered"
)

st.title("🏦 AI-Powered Loan Eligibility Advisor")
st.write("Enter your financial details to check loan eligibility instantly.")

# -----------------------
# USER INPUT FORM
# -----------------------
with st.form("loan_form"):
    no_of_dependents = st.number_input("Number of Dependents", min_value=0, max_value=10, value=1)
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    income_annum = st.number_input("Annual Income", min_value=0, value=500000)
    loan_amount = st.number_input("Loan Amount", min_value=0, value=200000)
    loan_term = st.number_input("Loan Term (months)", min_value=6, value=12)
    cibil_score = st.number_input("CIBIL Score", min_value=300, max_value=900, value=750)
    residential_assets_value = st.number_input("Residential Asset Value", min_value=0, value=0)
    commercial_assets_value = st.number_input("Commercial Asset Value", min_value=0, value=0)
    luxury_assets_value = st.number_input("Luxury Asset Value", min_value=0, value=0)
    bank_asset_value = st.number_input("Bank Asset Value", min_value=0, value=100000)

    submit = st.form_submit_button("Check Eligibility")

# -----------------------
# PREDICTION
# -----------------------
if submit:
    user_df = pd.DataFrame([{
        "no_of_dependents": no_of_dependents,
        "education": education,
        "self_employed": self_employed,
        "income_annum": income_annum,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "cibil_score": cibil_score,
        "residential_assets_value": residential_assets_value,
        "commercial_assets_value": commercial_assets_value,
        "luxury_assets_value": luxury_assets_value,
        "bank_asset_value": bank_asset_value
    }])

    probability, decision = predict_loan(user_df)

    st.subheader("📊 Prediction Result")
    st.metric("Approval Probability", f"{probability:.2%}")

    if decision == "APPROVED":
        st.success("✅ Loan Approved")
    elif decision == "REVIEW":
        st.warning("⚠️ Loan Under Review")
    else:
        st.error("❌ Loan Rejected")

    # -----------------------
    # PDF GENERATION
    # -----------------------
    if not os.path.exists("reports"):
        os.makedirs("reports")

    pdf_path = "reports/loan_report.pdf"

    generate_pdf_report(
        user_data=user_df.iloc[0].to_dict(),
        probability=probability,
        decision=decision,
        output_path=pdf_path
    )

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📄 Download Loan Report (PDF)",
            data=f,
            file_name="Loan_Eligibility_Report.pdf",
            mime="application/pdf"
        )

# =========================
# 🤖 AI FINANCIAL CHATBOT
# =========================
from src.advanced_chatbot import financial_chatbot

st.divider()
st.subheader("💬 AI Financial Guidance Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "llm_context" not in st.session_state:
    st.session_state.llm_context = []

user_query = st.text_input("Ask me about loans, EMI, credit score, or finance")

if st.button("Send"):
    if user_query.strip():
        bot_reply, st.session_state.llm_context = financial_chatbot(
            user_query,
            st.session_state.llm_context
        )

        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Bot", bot_reply))

# Display conversation
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
