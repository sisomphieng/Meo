import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

# Set the title and layout for the app
st.title("Investment Portfolio Advisor")

# Step 1: Risk Aversion Questionnaire
st.header("Investor Risk Aversion")
risk_aversion = st.radio("Select your risk aversion level:", ["High", "Middle", "Low"])

# Step 2: Portfolio Allocation Based on Risk Aversion
st.header("Suggested Portfolio Allocation")
if risk_aversion == "High":
    st.write("50% T-Bills, 30% Corporate Bonds, 10% S&P 500, 10% Small Stocks")
elif risk_aversion == "Middle":
    st.write("40% S&P 500, 30% Corporate Bonds, 20% Small Stocks, 10% T-Bills")
else:
    st.write("60% Small Stocks, 30% S&P 500, 10% Corporate Bonds")

# Step 3: Select Stocks Based on Risk Aversion
st.header("Stock Selection Based on Risk Aversion")
stocks = []
if risk_aversion == "High":
    stocks = ["JNJ", "PG", "KO", "PEP", "MSFT"]
elif risk_aversion == "Middle":
    stocks = ["AAPL", "MSFT", "CSCO", "HD", "V"]
else:
    stocks = ["TSLA", "NVDA", "PLTR", "ROKU", "DKNG"]

st.write("Selected Stocks:", ", ".join(stocks))

# Step 4: Input Investment Amount
investment_amount = st.number_input("Enter the amount you want to invest:", min_value=100, value=1000)

# Step 5: Calculate and Display Portfolio Risk and Return
st.header("Portfolio Risk and Return")

# Fetch stock data and calculate expected return and variance (risk)
# Note: You would typically include more logic to compute this from historical data
if st.button("Calculate"):
    # Dummy risk/return calculation (replace with actual calculations)
    expected_return = round(np.random.uniform(5, 15), 2)  # Placeholder for expected return %
    risk = round(np.random.uniform(1, 10), 2)  # Placeholder for portfolio variance %

    st.write(f"Expected Portfolio Return: {expected_return}%")
    st.write(f"Portfolio Risk (Variance): {risk}%")
