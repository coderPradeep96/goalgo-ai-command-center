import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def quantgpt_ui():
    st.title("🧠 QuantGPT - Smart Portfolio Builder")

    st.subheader("Step 1: Portfolio Configuration")
    investment = st.number_input("Enter total investment amount (₹)", min_value=10000, value=500000)
    num_stocks = st.slider("Number of stocks to include", 5, 20, 10)
    strategy = st.selectbox("Weighting strategy", ["Equal Weight", "Volatility Weighted"])

    st.subheader("Step 2: Stock Universe")
    nifty_100 = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
                 'ITC.NS', 'LT.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'BAJFINANCE.NS',
                 'HCLTECH.NS', 'ADANIENT.NS', 'SUNPHARMA.NS', 'MARUTI.NS', 'TITAN.NS']

    selected_stocks = st.multiselect("Select stock universe", nifty_100, default=nifty_100[:15])
    days = st.slider("Historical data window (days)", 90, 365, 180)

    if st.button("🚀 Build Portfolio"):
        end = datetime.today()
        start = end - timedelta(days=days)
        prices = yf.download(selected_stocks, start=start, end=end)['Adj Close']

        returns = prices.pct_change().dropna()
        mean_returns = returns.mean()
        volatilities = returns.std()

        if strategy == "Equal Weight":
            weights = np.repeat(1/num_stocks, num_stocks)
            selected = mean_returns.nlargest(num_stocks).index.tolist()
        elif strategy == "Volatility Weighted":
            inv_vol = 1 / volatilities
            inv_vol = inv_vol / inv_vol.sum()
            selected = inv_vol.nlargest(num_stocks).index.tolist()
            weights = inv_vol.loc[selected].values

        portfolio = pd.DataFrame({
            'Stock': selected,
            'Weight': weights,
            'Price': yf.download(selected, period="1d")['Adj Close'].iloc[-1].values
        })
        portfolio['Allocation (₹)'] = portfolio['Weight'] * investment
        portfolio['Qty to Buy'] = (portfolio['Allocation (₹)'] / portfolio['Price']).astype(int)

        st.success("✅ Portfolio Constructed")
        st.dataframe(portfolio[['Stock', 'Weight', 'Price', 'Qty to Buy', 'Allocation (₹)']])
