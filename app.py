#import librabries 
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
#setting configuration of the page such as title and sub title 
st.set_page_config(page_title = "Stock Data Extraction App",layout ="wide")
st.title('Stock Data extraction app')
#description
st.write('Extract stock market prices from Yahoo finance using ticker')
#creating a side bar
st.sidebar.header('User input')
#create an input box 
ticker = st.sidebar.text_input('Enter Stock ticker','AAPL')
#input for a start date
start_date = st.sidebar.date_input('Start date',pd.to_datetime('2023-01-01'))
#input for an end date 
end_date = st.sidebar.date_input('End date',pd.to_datetime('today'))
#Download data buttion 
if st.sidebar.button('Download data'):
    stock  = yf.download(ticker,start=start_date,end=end_date)
    df = stock.history(start=start_date,end=end_date)
    if df.empty:
      st.error('No data found. Please check the ticker symbol or data range')
    else:
      st.success('Data downloaded successfully')
      st.write(df)
    #display company header
    st.subheader('Company header')
    info = stock.info
#getting company names and information and writing it down within steam lit
    company_name = info.get('longName','N/A')
    sector = info.get('sector','N/A')
    industry = info.get('industry','N/A')
    market_cap = info.get('marketCap','N/A')
    website = info.get('website','N/A')

    st.write(f'Company Name: {company_name}')
    st.write(f'Sector: {sector}')
    st.write(f'Industry: {industry}')
    st.write(f'Market Cap: {market_cap}')

    st.subheader('Historical stock data')
    st.dataframe(df)
#making and plotting the prices 
    st.subheader('Cloing price chart')
    fig,ax = plt.subplots()
    ax.plot(df.index,df['Close'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Close price')
    ax.set_title(f'{company_name} closing price')
    st.pyplot(fig)
#convert df to csv for download 
    csv = df.to_csv.encode('utf-8')
    #download button for csv
    st.download_button(Label='Download data as CSV',
                       data=csv,
                       file_name=f'{ticker}_stock_data_.csv',
                       mime='text/csv')


