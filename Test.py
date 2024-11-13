import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Page 1: Risk Aversion Questionnaire
st.set_page_config(page_title="Investment Portfolio App", layout="wide")

# Function for Page 1: Risk Aversion Questionnaire
def risk_aversion_page():
    st.title("Investor Risk Aversion Questionnaire")
    st.write("Answer the following questions to determine your risk aversion level:")

    # Question 1: What is your investment horizon?
    horizon = st.selectbox(
        "What is your investment horizon?",
        ["Less than 1 year", "1-3 years", "3-5 years", "More than 5 years"]
    )

    # Question 2: How do you feel about the possibility of losing money in the short term?
    short_term_loss = st.radio(
        "How do you feel about the possibility of losing money in the short term?",
        ["I cannot tolerate any loss", "I can tolerate some loss", "I am comfortable with significant loss"]
    )

    # Question 3: What type of returns are you expecting from your investments?
    returns_expectation = st.selectbox(
        "What type of returns are you expecting from your investments?",
        ["Low (2-5%)", "Moderate (5-10%)", "High (10%+)"]
    )

    # Question 4: How much time are you willing to spend managing your investments?
    time_investment = st.selectbox(
        "How much time are you willing to spend managing your investments?",
        ["Minimal (I prefer a hands-off approach)", "Moderate (I can manage periodically)", "High (I want to be actively involved)"]
    )

    # Question 5: What is your primary investment goal?
    investment_goal = st.radio(
        "What is your primary investment goal?",
        ["Capital preservation", "Balanced growth", "Aggressive growth"]
    )

    # Risk level determination based on answers
    if horizon == "Less than 1 year":
        risk_score = 1
    elif horizon == "1-3 years":
        risk_score = 2
    elif horizon == "3-5 years":
        risk_score = 3
    else:
        risk_score = 4

    if short_term_loss == "I cannot tolerate any loss":
        risk_score += 1
    elif short_term_loss == "I can tolerate some loss":
        risk_score += 2
    else:
        risk_score += 3

    if returns_expectation == "Low (2-5%)":
        risk_score += 1
    elif returns_expectation == "Moderate (5-10%)":
        risk_score += 2
    else:
        risk_score += 3

    if time_investment == "Minimal (I prefer a hands-off approach)":
        risk_score += 1
    elif time_investment == "Moderate (I can manage periodically)":
        risk_score += 2
    else:
        risk_score += 3

    if investment_goal == "Capital preservation":
        risk_score += 1
    elif investment_goal == "Balanced growth":
        risk_score += 2
    else:
        risk_score += 3

    # Determine risk level based on total score
    if risk_score <= 7:
        st.session_state['risk_level'] = "Low"
    elif risk_score <= 12:
        st.session_state['risk_level'] = "Medium"
    else:
        st.session_state['risk_level'] = "High"

    # Display the risk level
    st.write(f"Your selected risk tolerance level: {st.session_state['risk_level']}")

    # "Next" button to navigate to Page 2
    if st.button("Next"):
        st.session_state.page = "Stock Classification"  # Move to the next page

# Page 2: Stock Classification and Comparison
def stock_classification_page():
    st.title("Stock Classification Based on Risk Tolerance")
    
    # Display stock classification based on risk level
    if 'risk_level' in st.session_state:
        risk_level = st.session_state['risk_level']
        if risk_level == "Low":
            st.write("Low-Risk Stocks (Beta < 1):")
            stocks = {
                "JNJ": 0.52, "PG": 0.41, "KO": 0.62, "WM": 0.75, 
                "AEP": 0.54, "MCD": 0.74, "DUK": 0.46, "T": 0.73,
                "PFE": 0.62, "MSFT": 0.9, "SBUX": 0.96, "TXN": 0.98, "SNOW": 0.83
            }
        elif risk_level == "Medium":
            st.write("Medium-Risk Stocks (Beta 1-1.5):")
            stocks = {
                "NKE": 1.03, "MMM": 1.0, "CURLF": 1.49, "LUMN": 1.2, 
                "RYA.IR": 1.38, "ABNB": 1.16
            }
        else:
            st.write("High-Risk Stocks (Beta > 1.5):")
            stocks = {
                "TSLA": 2.3, "SQ": 2.48, "SHOP": 2.37, "ROKU": 2.07, 
                "NVDA": 1.6
            }
        
        # Display stocks and their beta values
        for stock, beta in stocks.items():
            st.write(f"{stock} - {beta} Beta")

    # Risk-Free Assets
    st.write("Risk-Free Assets:")
    st.write("- Bonds\n- T-bills")
    
    # Comparison of two companies' stock prices and volumes
    st.subheader("Compare Two Companies")
    stock1 = st.text_input("Enter first stock ticker (e.g., TSLA):", "TSLA")
    stock2 = st.text_input("Enter second stock ticker (e.g., AAPL):", "AAPL")
    
    # Fetch and plot data if both tickers are entered
    if stock1 and stock2:
        # Download data from Yahoo Finance
        data1 = yf.download(stock1, period="1y")
        data2 = yf.download(stock2, period="1y")
        
        # Align both dataframes to the same index
        combined_index = data1.index.union(data2.index)
        data1 = data1.reindex(combined_index).fillna(method="ffill").fillna(0)
        data2 = data2.reindex(combined_index).fillna(method="ffill").fillna(0)
        
        # Plot price history and volume as line charts
        st.write(f"Price and Volume History for {stock1} and {stock2}")
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Plot close price for both stocks
        ax1.plot(data1.index, data1['Close'], label=f"{stock1} Close Price")
        ax1.plot(data2.index, data2['Close'], label=f"{stock2} Close Price")
        ax1.set_title("Stock Price History")
        ax1.legend()
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

        # Plot volume for both stocks as line charts
        ax2.plot(data1.index, data1['Volume'], label=f"{stock1} Volume", color="blue")
        ax2.plot(data2.index, data2['Volume'], label=f"{stock2} Volume", color="orange")
        ax2.set_title("Volume History")
        ax2.legend()
        ax2.xaxis.set_major_locator(mdates.MonthLocator())
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

        # Display the plots
        plt.tight_layout()
        st.pyplot(fig)

    # "Next" button to navigate to Page 3
    if st.button("Next"):
        st.session_state.page = "Portfolio Builder"  # Move to the next page

# Page 3: Portfolio Builder and Optimization
def portfolio_builder_page():
    st.title("Portfolio Builder")
    
    # Input for stock selection and investment amount
    st.write("Enter the stocks and investment amount to build your portfolio.")
    selected_stocks = st.multiselect("Choose stocks:", ["JNJ", "PG", "KO", "WM", "AEP", "TSLA", "SQ", "SHOP", "ROKU", "NVDA"])
    investment_amount = st.number_input("Total Investment Amount:", min_value=100.0, value=1000.0)
    
    # Placeholder for portfolio optimization logic (e.g., to minimize risk)
    st.write("Calculating optimal portfolio weights to minimize risk...")
    
    # Example weights and returns (placeholder calculations)
    weights = np.random.dirichlet(np.ones(len(selected_stocks)), size=1)[0]
    expected_return = np.round(np.dot(weights, np.random.uniform(0.05, 0.15, len(selected_stocks))), 4)
    portfolio_variance = np.round(np.dot(weights.T, weights) * np.var(weights), 4)
    
    st.write("Optimal Portfolio Weights:")
    for stock, weight in zip(selected_stocks, weights):
        st.write(f"{stock}: {weight:.2%}")
    
    st.write(f"Expected Portfolio Return: {expected_return * 100:.2f}%")
    st.write(f"Portfolio Risk (Variance): {portfolio_variance:.4f}")
    
    # Display pie chart for portfolio composition
    fig, ax = plt.subplots()
    ax.pie(weights, labels=selected_stocks, autopct='%1.1f%%')
    ax.set_title("Portfolio Composition")
    st.pyplot(fig)

# Sidebar for page navigation
st.sidebar.title("Navigation")
if 'page' not in st.session_state:
    st.session_state.page = "Risk Aversion"  # Default page

# Page routing based on the session state
if st.session_state.page == "Risk Aversion":
    risk_aversion_page()
elif st.session_state.page == "Stock Classification":
    stock_classification_page()
elif st.session_state.page == "Portfolio Builder":
    portfolio_builder_page()
