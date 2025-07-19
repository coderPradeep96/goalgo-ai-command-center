import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

def simugpt_ui():
    st.title("📈 SimuGPT - Portfolio Backtest Engine")

    if 'quantgpt_portfolio' not in st.session_state:
        st.warning("⚠️ No portfolio found. Please build one using QuantGPT first.")
        return

    portfolio_df = st.session_state['quantgpt_portfolio']
    tickers = portfolio_df['Stock'].tolist()
    weights = portfolio_df['Weight'].values

    st.subheader("🗓 Select Simulation Time Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
    with col2:
        end_date = st.date_input("End Date", value=pd.to_datetime("2025-01-01"))

    if st.button("🚀 Run Simulation"):
        # Fetch data
        price_data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        if price_data.empty:
            st.error("❌ Failed to fetch historical data.")
            return

        price_data = price_data.fillna(method='ffill').dropna()
        daily_returns = price_data.pct_change().dropna()

        # NAV Simulation
        weighted_returns = daily_returns @ weights
        nav_series = (1 + weighted_returns).cumprod() * 100  # base = 100

        st.subheader("📊 Simulated NAV Timeline")
        st.line_chart(nav_series)

        total_return = nav_series.iloc[-1] / nav_series.iloc[0] - 1
        annualized_return = (1 + total_return) ** (252 / len(nav_series)) - 1
        volatility = weighted_returns.std() * np.sqrt(252)
        sharpe = annualized_return / volatility

        st.markdown(f"""
        ### 📈 Portfolio Simulation Summary
        - **Total Return:** {total_return:.2%}
        - **Annualized Return:** {annualized_return:.2%}
        - **Annualized Volatility:** {volatility:.2%}
        - **Sharpe Ratio (rf=0):** {sharpe:.2f}
        """)

        # Save for export/email
        st.session_state['simugpt_nav'] = nav_series
        st.session_state['simugpt_stats'] = {
            'Total Return': total_return,
            'Annualized Return': annualized_return,
            'Volatility': volatility,
            'Sharpe': sharpe
        }
