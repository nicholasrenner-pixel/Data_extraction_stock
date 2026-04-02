import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Stock Data Extraction App", layout="wide")

st.title("Stock Data Extraction App")
st.write("Extract stock market prices from Yahoo Finance using a ticker symbol")

# Sidebar inputs
st.sidebar.header("User Input")

ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Download button
if st.sidebar.button("Download Data"):
    
    # Create ticker object
    stock = yf.Ticker(ticker)

    # Fetch historical data
    df = stock.history(start=start_date, end=end_date)

    if df.empty:
        st.error("No data found. Please check the ticker symbol or date range.")
    else:
        st.success("Data downloaded successfully")

        # Company info
        st.subheader("Company Information")
        info = stock.info

        company_name = info.get("longName", "N/A")
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        market_cap = info.get("marketCap", "N/A")
        website = info.get("website", "N/A")

        st.write(f"**Company Name:** {company_name}")
        st.write(f"**Sector:** {sector}")
        st.write(f"**Industry:** {industry}")
        st.write(f"**Market Cap:** {market_cap}")
        st.write(f"**Website:** {website}")

        # Display data
        st.subheader("Historical Stock Data")
        st.dataframe(df)

        # Plot closing price
        st.subheader("Closing Price Chart")
        fig, ax = plt.subplots()
        ax.plot(df.index, df["Close"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price")
        ax.set_title(f"{company_name} Closing Price")
        st.pyplot(fig)

        # Convert to CSV
        csv = df.to_csv().encode("utf-8")

        # Download button
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name=f"{ticker}_stock_data.csv",
            mime="text/csv"
        )
