import yfinance as yf
import streamlit as st

# Streamlit App Layout
st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Function for deep debt analysis
def deep_debt_analysis(stock_ticker):
    stock = yf.Ticker(stock_ticker)
    balance_sheet = stock.balance_sheet.T
    income_statement = stock.financials.T
    cash_flow = stock.cashflow.T
    
    debt_analysis = {
        "Debt-to-Equity Ratio": None,
        "Interest Coverage Ratio": None,
        "Debt-to-EBITDA Ratio": None,
        "Cash Flow to Debt Ratio": None,
        "Total Debt Trend": [],
        "Debt Growth Status": None,
        "Zero Debt Potential": None,
        "Buy Opportunity": None,  # Adding the buy opportunity metric
    }

    # Debt-to-Equity Ratio
    if 'Total Debt' in balance_sheet.columns and 'Stockholders Equity' in balance_sheet.columns:
        total_debt = balance_sheet['Total Debt'].iloc[0]
        equity = balance_sheet['Stockholders Equity'].iloc[0]
        debt_analysis["Debt-to-Equity Ratio"] = total_debt / equity if equity != 0 else None

    # Interest Coverage Ratio
    if 'EBIT' in income_statement.columns and 'Interest Expense' in income_statement.columns:
        ebit = income_statement['EBIT'].iloc[0]
        interest_expense = income_statement['Interest Expense'].iloc[0]
        debt_analysis["Interest Coverage Ratio"] = ebit / interest_expense if interest_expense != 0 else None

    # Debt-to-EBITDA Ratio
    if 'EBITDA' in income_statement.columns:
        ebitda = income_statement['EBITDA'].iloc[0]
        debt_analysis["Debt-to-EBITDA Ratio"] = total_debt / ebitda if ebitda != 0 else None

    # Cash Flow to Debt Ratio
    if 'Operating Cash Flow' in cash_flow.columns:
        operating_cash_flow = cash_flow['Operating Cash Flow'].iloc[0]
        debt_analysis["Cash Flow to Debt Ratio"] = operating_cash_flow / total_debt if total_debt != 0 else None

    # Total Debt Trend
    if 'Total Debt' in balance_sheet.columns:
        debt_analysis["Total Debt Trend"] = balance_sheet['Total Debt'].dropna().tolist()

    # Debt Growth Status
    if len(debt_analysis["Total Debt Trend"]) > 1:
        initial_debt = debt_analysis["Total Debt Trend"][0]
        latest_debt = debt_analysis["Total Debt Trend"][-1]
        if latest_debt > initial_debt:
            debt_analysis["Debt Growth Status"] = "Debt is increasing"
        elif latest_debt < initial_debt:
            debt_analysis["Debt Growth Status"] = "Debt is decreasing"
        else:
            debt_analysis["Debt Growth Status"] = "No change in debt"

    # Zero Debt Potential
    if len(debt_analysis["Total Debt Trend"]) > 0:
        peak_debt = max(debt_analysis["Total Debt Trend"])
        latest_debt = debt_analysis["Total Debt Trend"][-1]
        debt_analysis["Zero Debt Potential"] = (
            "Company is nearing zero debt" if latest_debt < 0.1 * peak_debt else "Debt reduction is steady"
        )

    # Buy Opportunity Teller
    if debt_analysis["Zero Debt Potential"] == "Company is nearing zero debt":
        debt_analysis["Buy Opportunity"] = "Big Buy Opportunity! Company is reducing debt aggressively."
    elif debt_analysis["Debt Growth Status"] == "Debt is decreasing":
        debt_analysis["Buy Opportunity"] = "Potential Buy! Debt is decreasing consistently."
    else:
        debt_analysis["Buy Opportunity"] = "Not a Buy Signal. Monitor for debt trends."

    return debt_analysis

# Streamlit App Layout
st.title("Deep Debt Analysis with Buy Opportunity Teller")
st.write("Analyze the debt metrics of any publicly listed company and determine if it's a buy opportunity.")

# Input for Stock Ticker
stock_ticker = st.text_input("Enter Stock Ticker (e.g., ZOMATO.NS):", value="ZOMATO.NS")

# Perform Analysis
if st.button("Analyze"):
    try:
        analysis_result = deep_debt_analysis(stock_ticker)
        st.subheader(f"Debt Analysis for {stock_ticker}")
        for metric, value in analysis_result.items():
            st.write(f"**{metric}:** {value}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
