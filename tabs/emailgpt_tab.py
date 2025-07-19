import streamlit as st
import pandas as pd
from utils.emailer import generate_pdf_from_html, send_email_with_pdf

def emailgpt_ui():
    st.title("📤 EmailGPT - Generate & Send Portfolio Report")

    if 'quantgpt_portfolio' not in st.session_state or 'simugpt_stats' not in st.session_state:
        st.warning("⚠️ Please run QuantGPT and SimuGPT first.")
        return

    email = st.text_input("Enter CEO Email Address")
    if st.button("📄 Generate Report & Send"):
        portfolio = st.session_state['quantgpt_portfolio']
        stats = st.session_state['simugpt_stats']

        # Convert to list of dicts for Jinja
        portfolio_dict = portfolio.to_dict(orient="records")
        pdf_path = generate_pdf_from_html({"portfolio": portfolio_dict, "summary": stats})

        send_email_with_pdf("GoAlgo Portfolio Report", "Attached is the strategy report.", email, pdf_path)
        st.success(f"📨 Report sent to {email}")
