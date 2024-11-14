import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Sidebar navigation for the multi-page app
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Risk Tolerance Quiz", "Company Comparison", "Portfolio Builder"])

# Page 1: Risk Tolerance Quiz
if page == "Risk Tolerance Quiz":
    st.title('Investment Risk Tolerance Quiz')

    # Define quiz questions and options with scores
    questions = {
           "1. In general, how would your best friend describe you as a risk taker?": {
        "options": ["A real gambler", "Willing to take risks after completing adequate research", "Cautious", "A real risk avoider"],
        "scores": [4, 3, 2, 1]  # Score for each option
    },
    "2. You are on a TV game show and can choose one of the following.  Which would you take?": {
        "options": ["$1,000 in cash", "A 50% chance at winning $5,000", "A 25% chance at winning $10,000", "A 5% chance at winning $100,000"],
        "scores": [1, 2, 3, 4]  # Score for each option
    },
    "3. You have just finished saving for a “once-in-a-lifetime” vacation.  Three weeks before you plan to leave, you lose your job.  You would:": {
        "options": ["Cancel the vacation", "Take a much more modest vacation", "Go as scheduled, reasoning that you need the time to prepare for a job search", "Extend your vacation, because this might be your last chance to go first-class"],
        "scores": [1, 2, 3, 4]  # Score for each option
    },
    "4. If you unexpectedly received $20,000 to invest, what would you do?": {
        "options": ["Deposit it in a bank account, money market account, or an insured CD", "Invest it in safe high quality bonds or bond mutual funds", "Invest it in stocks or stock mutual funds"],
        "scores": [1, 2, 3]  # Score for each option
    },
    "5. In terms of experience, how comfortable are you investing in stocks or stock mutual funds?": {
        "options": ["Not at all comfortable", "Somewhat comfortable", "Very comfortable"],
        "scores": [1, 2, 3]  # Score for each option
    },
    "6. When you think of the word “risk” which of the following words comes to mind first? ": {
        "options": ["Loss", "Uncertainty", "Opportunity", "Thrill"],
        "scores": [1, 2, 3,4]  # Score for each option
    },
    "7. Some experts are predicting prices of assets such as gold, jewels, collectibles, and real estate (hard assets) to increase in value; bond prices may fall, however, experts tend to agree that government bonds are relatively safe. Most of your investment assets are now in high interest government bonds. What would you do?": {
        "options": ["Hold the bonds", "Sell the bonds, put half the proceeds into money market accounts, and the other half into hard assets", "Sell the bonds and put the total proceeds into hard assets", "Sell the bonds, put all the money into hard assets, and borrow additional money to buy more"],
        "scores": [1, 2, 3,4]  # Score for each option
    },
    "8. Given the best and worst case returns of the four investment choices below, which would you prefer?": {
        "options": ["$200 gain best case; $0 gain/loss worst case", "$800 gain best case; $200 loss worst case", "$2,600 gain best case; $800 loss worst case", "$4,800 gain best case; $2,400 loss worst case"],
        "scores": [1, 2, 3,4]  # Score for each option
    },
    "9. In addition to whatever you own, you have been given $1,000.  You are now asked to choose between:": {
        "options": ["A sure gain of $500", "A 50% chance to gain $1,000 and a 50% chance to gain nothing"],
        "scores": [1, 3]  # Score for each option
    },
    "10. In addition to whatever you own, you have been given $2,000.  You are now asked to choose between:": {
        "options": ["A sure loss of $500", "A 50% chance to lose $1,000 and a 50% chance to lose nothing"],
        "scores": [1, 3]  # Score for each option
    },
    "11. Suppose a relative left you an inheritance of $100,000, stipulating in the will that you invest ALL the money in ONE of the following choices.  Which one would you select?": {
        "options": ["A savings account or money market mutual fund", "A mutual fund that owns stocks and bonds", "A portfolio of 15 common stocks", "Commodities like gold, silver, and oil"],
        "scores": [1, 2, 3, 4]  # Score for each option
    },
    "12. If you had to invest $20,000, which of the following investment choices would you find most appealing?": {
        "options": ["60% in low-risk investments 30% in medium-risk investments 10% in high-risk investments", "30% in low-risk investments 40% in medium-risk investments 30% in high-risk investments", "10% in low-risk investments 40% in medium-risk investments 50% in high-risk investments"],
        "scores": [1, 2, 3]  # Score for each option
    },
    "13. Your trusted friend and neighbor, an experienced geologist, is putting together a group of investors to fund an exploratory gold mining venture. The venture could pay back 50 to 100 times the investment if successful.  If the mine is a bust, the entire investment is worthless.  Your friend estimates the chance of success is only 20%.  If you had the money, how much would you invest? ": {
        "options": ["Nothing", "One month’s salary", "Three month’s salary", "Six month’s salary"],
        "scores": [1, 2, 3,4]  # Score for each option
    }
}

    # Store user's responses
    user_answers = {}
    for question, data in questions.items():
        st.subheader(question)
        user_answers[question] = st.radio("Select your answer:", data["options"])

    if st.button("Submit"):
        # Calculate total score
        score = sum([data["scores"][data["options"].index(user_answers[q])] for q, data in questions.items()])
        st.write("Thank you for taking the quiz!")
        st.write(f"Your score: {score}")

        # Determine risk tolerance level
        risk_tolerance_categories = {
            (0, 18): "Low risk tolerance (conservative)",
            (19, 22): "Below-average risk tolerance",
            (23, 28): "Average/moderate risk tolerance",
            (29, 32): "Above-average risk tolerance",
            (33, float('inf')): "High risk tolerance (aggressive)"
        }
        for score_range, tolerance in risk_tolerance_categories.items():
            if score_range[0] <= score <= score_range[1]:
                st.write(f"Your risk tolerance level: {tolerance}")
                st.session_state.risk_tolerance_level = tolerance
                break

# Page 2: Company Financial Comparison & Golden/Death Cross Visualization
elif page == "Company Comparison":
    st.title("Financial Comparison of Two Companies")

    # User inputs for company symbols
    st.subheader("Compare Two Companies")
    company1 = st.text_input("Enter first stock ticker (e.g., TSLA):", "TSLA")
    company2 = st.text_input("Enter second stock ticker (e.g., TSLA):", "TSLA")

    if company1 and company2:
        # Fetch and display financial metrics for both companies
        def get_financial_metrics(symbol):
            stock = yf.Ticker(symbol)
            balance_sheet = stock.balance_sheet
            income_statement = stock.financials

            # Debt-to-Equity Ratio
            debt_to_equity = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0] / balance_sheet.loc['Stockholders Equity'].iloc[0]

            # Revenue Growth
            revenue_growth = ((income_statement.loc['Total Revenue'].iloc[0] - income_statement.loc['Total Revenue'].iloc[1]) /
                              income_statement.loc['Total Revenue'].iloc[1]) * 100

            # Return on Equity (ROE)
            roe = (income_statement.loc['Net Income'].iloc[0] / balance_sheet.loc['Stockholders Equity'].iloc[0]) * 100

            return {"Debt-to-Equity": debt_to_equity, "Revenue Growth": revenue_growth, "ROE": roe}

        # Display metrics for each company
        metrics1 = get_financial_metrics(company1)
        metrics2 = get_financial_metrics(company2)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Metrics for {company1}")
            for metric, value in metrics1.items():
                st.write(f"**{metric}:** {value:.2f}")

        with col2:
            st.subheader(f"Metrics for {company2}")
            for metric, value in metrics2.items():
                st.write(f"**{metric}:** {value:.2f}")

        # Plot Golden/Death Cross
        def plot_golden_death_cross(symbol):
            data = yf.download(symbol, start="2022-01-01")['Adj Close']
            short_ma = data.rolling(window=50).mean()
            long_ma = data.rolling(window=200).mean()

            plt.figure(figsize=(12, 6))
            plt.plot(data, label="Price")
            plt.plot(short_ma, label="50-day MA (Golden Cross)", linestyle="--")
            plt.plot(long_ma, label="200-day MA (Death Cross)", linestyle="--")
            plt.legend()
            plt.title(f"Golden/Death Cross for {symbol}")
            st.pyplot(plt)

        st.write("**Golden/Death Cross for Selected Stocks**")
        plot_golden_death_cross(company1)
        plot_golden_death_cross(company2)

        try:
            # Compare stock price movements
            data1 = yf.download(company1, start="2023-01-01")['Adj Close']
            data2 = yf.download(company2, start="2023-01-01")['Adj Close']

            plt.figure(figsize=(12, 6))
            plt.plot(data1, label=company1)
            plt.plot(data2, label=company2)
            plt.xlabel("Date")
            plt.ylabel("Adjusted Close Price")
            plt.title(f"Price Comparison: {company1} vs {company2}")
            plt.legend()
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.error("Please enter both company symbols for comparison.")
# Portfolio Optimization function (Mean-Variance Optimization)
def optimize_portfolio(returns, risk_free_rate=0.0):
    # Objective function: Minimize portfolio variance (risk)
    def objective(weights):
        return np.dot(weights.T, np.dot(returns.cov(), weights))

    # Constraints: Weights must sum to 1 (fully invested)
    def constraint(weights):
        return np.sum(weights) - 1

    # Bounds for each weight: between 0 and 1
    bounds = [(0, 1) for _ in range(len(returns.columns))]

    # Initial guess (equal distribution)
    initial_guess = [1. / len(returns.columns)] * len(returns.columns)

    # Solve the optimization problem
    result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints={'type': 'eq', 'fun': constraint})

    return result.x  # Optimal weights
# Page 3: Portfolio Builder
if page == "Portfolio Builder":
    st.title("Portfolio Builder")

    # Investment amount input
    investment_amount = st.number_input("Enter total investment amount:", min_value=0.0, step=1000.0)

    # Risk Tolerance-Based Stock Selection
    if "risk_tolerance_level" in st.session_state:
        risk_tolerance = st.session_state.risk_tolerance_level
        if risk_tolerance == "Low risk tolerance (conservative)":
            stock_options = ["VTI", "BND", "AGG", "XLP", "VZ"]  # Examples of low-risk stocks (broad market, bonds)
            st.write("Based on your low risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "Below-average risk tolerance":
            stock_options = ["VUG", "VO", "VEA", "KO", "PG"]  # Examples of below-average risk stocks (growth, value)
            st.write("Based on your below-average risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "Average/moderate risk tolerance":
            stock_options = ["QQQ", "SPY", "IVV", "MSFT", "JNJ"]  # Examples of moderate risk stocks (tech, S&P 500)
            st.write("Based on your average risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "Above-average risk tolerance":
            stock_options = ["ARKK", "TQQQ", "XLK", "TSLA", "NVDA"]  # Examples of above-average risk stocks (innovation, tech)
            st.write("Based on your above-average risk tolerance, we recommend considering the following stocks:")
        elif risk_tolerance == "High risk tolerance (aggressive)":
            stock_options = ["FDN", "SPYD", "XLY", "AMZN", "BABA"]  # Examples of high-risk stocks (high-dividend, retail)
            st.write("Based on your high risk tolerance, we recommend considering the following stocks:")
        else:
            st.warning("Please complete the Risk Tolerance Quiz first to get stock suggestions.")

        # Input for stock selection (multiselect)
        selected_stocks = st.multiselect("Select Stocks:", stock_options)

        # Input for investment amount for each selected stock
        stock_allocations = {}
        for stock in selected_stocks:
            allocation = st.number_input(f"Investment amount for {stock}:", min_value=0.0)
            stock_allocations[stock] = allocation

        if selected_stocks and stock_allocations:
            try:
                # Fetch historical adjusted close price data for selected stocks
                stock_data = yf.download(selected_stocks, start="2023-01-01")['Adj Close']

                # Calculate daily returns (percentage change)
                returns = stock_data.pct_change().dropna()

                # Optimize portfolio weights (minimize risk)
                optimal_weights = optimize_portfolio(returns)

                # Calculate portfolio composition (weight allocation)
                portfolio_composition = {selected_stocks[i]: optimal_weights[i] for i in range(len(selected_stocks))}

                # Display portfolio composition
                st.write("**Optimal Portfolio Weights (Minimized Risk):**")
                for stock, weight in portfolio_composition.items():
                    st.write(f"{stock}: {weight * 100:.2f}%")

                # Display Pie Chart of Portfolio Composition
                fig, ax = plt.subplots()
                ax.pie(optimal_weights, labels=selected_stocks, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error building portfolio: {e}")

    else:
        st.warning("Please complete the Risk Tolerance Quiz first to get stock suggestions.")
