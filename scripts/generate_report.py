# scripts/generate_report.py

import datetime
from backtest import run_strategy
from emailer import send_report_email

if __name__ == "__main__":
    today = datetime.date.today()
    print(f"[INFO] Running strategy for {today}")

    result_path = run_strategy(save_to="reports/")
    
    if result_path:
        print(f"[INFO] Report saved to: {result_path}")
        send_report_email(result_path)
    else:
        print("[ERROR] Strategy failed or no report generated.")
