
from scripts.emailer import send_email
import streamlit as st
import os
from utils.generate_pdf import generate_sample_pdf




st.set_page_config(page_title="GoAlgo AI Command Center", layout="wide")

st.title("📈 GoAlgo AI Command Center")
st.markdown("Welcome, CEO. Your AI Team is standing by for commands.")

selected_tab = st.sidebar.radio("GoAlgo AI Command Center", ["InfraGPT", "DataGPT", "QuantGPT", "SimuGPT", "EmailGPT"])


if selected_tab == "InfraGPT":
    from tabs import infra_tab
    infra_tab.infragpt_ui()
if selected_tab == "DataGPT":
    from tabs import datagpt_tab
    datagpt_tab.datagpt_ui()


if selected_tab == "EmailGPT":
    st.header("📤 Export & Email Reports")
    st.write("EmailGPT handles all exports and communications.")
    st.subheader("📬 Email Insight Report")

    email_input = st.text_input("Enter your email address", placeholder="you@example.com")
    
    if st.button("Send Report"):
        if not email_input:
            st.warning("Please enter a valid email address.")
        else:
            # Make sure the report file exists
            report_path = "reports/insight_report.pdf"
    
            if not os.path.exists(report_path):
                st.error("⚠️ Report file not found.")
            else:
                success, message = send_email(
                    recipient_email=email_input,
                    subject="📈 GoAlgo Insight Report",
                    body="Hi,\n\nPlease find attached your daily GoAlgo insight report.\n\nBest,\nTeam GoAlgo",
                    attachment_path=report_path
                )
                st.success(message) if success else st.error(message)




