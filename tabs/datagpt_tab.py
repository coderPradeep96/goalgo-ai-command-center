import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def datagpt_ui():
    st.title("📈 DataGPT - Market Data & Indicators")

    st.subheader("Select NIFTY 100 Stocks")

    # Example stock list — replace with dynamic NIFTY 100 list if needed
    nifty_100 = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS']
    selected_stocks = st.multiselect("Select stock(s)", nifty_100, default=nifty_100[:3])

    days = st.slider("Number of past days", 30, 365, 180)

    if st.button("🔍 Fetch & Analyze"):
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)

        for ticker in selected_stocks:
            st.markdown(f"### 📊 {ticker}")
            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty:
                st.warning(f"No data found for {ticker}")
                continue

            # Compute indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
            data['RSI'] = compute_rsi(data['Close'])

            st.line_chart(data[['Close', 'SMA_20', 'EMA_20']])
            st.line_chart(data[['RSI']])

            st.dataframe(data.tail(10))

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
