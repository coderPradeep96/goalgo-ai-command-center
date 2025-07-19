import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def quantgpt_ui():
    st.title("🧠 QuantGPT - Smart Portfolio Builder")

    st.subheader("📊 Step 1: Portfolio Configuration")
    investment = st.number_input("💰 Total investment amount (₹)", min_value=10000, value=500000)
    num_stocks = st.slider("📌 Number of stocks to include", 5, 20, 10)
    strategy = st.selectbox("📈 Weighting strategy", ["Equal Weight", "Volatility Weighted"])

    st.subheader("📦 Step 2: Choose Stock Universe")
    nifty_100 = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
                 'ITC.NS', 'LT.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'BAJFINANCE.NS',
                 'HCLTECH.NS', 'ADANIENT.NS', 'SUNPHARMA.NS', 'MARUTI.NS', 'TITAN.NS']

    selected_stocks = st.multiselect("📍 Select from NIFTY 100", nifty_100, default=nifty_100[:15])
    days = st.slider("🕒 Historical data window (days)", 90, 365, 180)

    if st.button("🚀 Build Portfolio"):
        end = datetime.today()
        start = end - timedelta(days=days)
        prices = yf.download(selected_stocks, start=start, end=end)['Adj Close']

        if prices.empty:
            st.error("⚠️ Unable to fetch stock data. Please check your internet or stock list.")
            return

        returns = prices.pct_change().dropna()
        mean_returns = returns.mean() * 252
        volatilities = returns.std() * np.sqrt(252)

        if strategy == "Equal Weight":
            weights = np.repeat(1 / num_stocks, num_stocks)
            selected = mean_returns.nlargest(num_stocks).index.tolist()
            explanation = "📘 Equal Weight Strategy: Each selected stock is assigned the same proportion of the portfolio."
        else:
            inv_vol = 1 / volatilities
            inv_vol = inv_vol / inv_vol.sum()
            selected = inv_vol.nlargest(num_stocks).index.tolist()
            weights = inv_vol.loc[selected].values
            explanation = "📘 Volatility Weighted Strategy: Stocks with lower volatility receive higher weight to reduce risk."

        # Fetch latest prices
        latest_prices = yf.download(selected, period="1d")['Adj Close'].iloc[-1]
        portfolio = pd.DataFrame({
            'Stock': selected,
            'Weight': weights,
            'Price': latest_prices.values
        })

        portfolio['Allocation (₹)'] = portfolio['Weight'] * investment
        portfolio['Qty to Buy'] = (portfolio['Allocation (₹)'] / portfolio['Price']).astype(int)
        portfolio['Expected Return'] = mean_returns.loc[selected].values
        portfolio['Volatility'] = volatilities.loc[selected].values

        # Portfolio metrics
        expected_portfolio_return = np.dot(weights, mean_returns.loc[selected])
        expected_portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(returns[selected].cov() * 252, weights)))

        st.markdown("### 🧾 Portfolio Recommendation")
        st.write(explanation)
        st.dataframe(portfolio[['Stock', 'Weight', 'Price', 'Qty to Buy', 'Allocation (₹)', 'Expected Return', 'Volatility']])

        st.markdown(f"""
        #### 📊 Portfolio Summary
        - **Expected Annual Return:** {expected_portfolio_return:.2%}
        - **Expected Annual Volatility:** {expected_portfolio_vol:.2%}
        - **Sharpe (assumed RF=0):** {(expected_portfolio_return / expected_portfolio_vol):.2f}
        """)

        # Save to session for SimuGPT / EmailGPT
        st.session_state['quantgpt_portfolio'] = portfolio
        st.session_state['quantgpt_summary'] = {
            'Expected Return': expected_portfolio_return,
            'Volatility': expected_portfolio_vol,
            'Sharpe': expected_portfolio_return / expected_portfolio_vol
        }
