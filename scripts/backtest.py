# scripts/backtest.py

import os
import datetime
from fpdf import FPDF

def run_strategy(save_to="reports/"):
    # 🧠 Simulate a basic strategy result
    today = datetime.date.today().strftime("%Y-%m-%d")
    report_path = os.path.join(save_to, f"report_{today}.pdf")

    os.makedirs(save_to, exist_ok=True)

    # 📝 Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Strategy Report: {today}", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="📈 Performance Summary\n\n- Strategy Return: 12.7%\n- Benchmark Return: 9.3%\n- Sharpe Ratio: 1.45\n- Trades Executed: 18\n- Win Rate: 61.1%\n")
    
    pdf.output(report_path)
    return report_path
