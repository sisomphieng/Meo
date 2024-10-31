import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go
import appdirs as ad
import yfinance as yf
!pip -q install streamlit appdirs

ad.user_cache_dir = lambda *args: "/tmp"

# Specify title and logo for the webpage.
# Set up your web app
st.set_page_config(layout="wide", page_title="WebApp_Demo")

# Sidebar
st.sidebar.title("Input")
symbol = st.sidebar.text_input('Please enter the stock symbol: ', 'NVDA').upper()
# Selection for a specific time frame.
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date',value=datetime.date(2024,1,1))
with col2:
    edate = st.date_input('End Date',value=datetime.date.today())

st.title(f"{symbol}")

stock = yf.Ticker(symbol)
if stock is not None:
  # Display company's basics
  st.write(f"# Sector : {stock.info['sector']}")
  st.write(f"# Company Beta : {stock.info['beta']}")
else:
  st.error("Failed to fetch historical data.")

data = yf.download(symbol,start=sdate,end=edate)
if data is not None:
  # Create a candlestick chart using Plotly
  fig = go.Figure(data=[go.Candlestick(x=data.index,
                                      open=data['Open'],
                                      high=data['High'],
                                      low=data['Low'],
                                      close=data['Close'])])
  fig.update_layout(title=f"{symbol} Candlestick Chart",
                    xaxis_title="Date",
                    yaxis_title="Price")
  st.plotly_chart(fig)

  st.line_chart(data['Close'],x_label="Date",y_label="Close")
else:
    st.error("Failed to fetch historical data.")

  st.line_chart(data['Close'],x_label="Date",y_label="Close")
else:
    st.error("Failed to fetch historical data.")
