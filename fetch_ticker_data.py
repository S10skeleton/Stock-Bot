import pandas as pd

# Load the ticker symbols from a CSV file
tickers_df = pd.read_csv("tickers.csv")
tickers = tickers_df['Symbol'].tolist()
print(tickers)  # List of tickers

import yfinance as yf



stock_data = {}  # Dictionary to store all stock data

# Fetch data for all tickers
for ticker in tickers:
    data = yf.download(ticker, start="2020-01-01", end="2023-01-01")
    print(f"{ticker} data fetched successfully!")

    # Add indicators and signals
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['Signal'] = 0  # Default to hold
    data.loc[data['SMA_20'] > data['SMA_50'], 'Signal'] = 1  # Buy
    data.loc[data['SMA_20'] < data['SMA_50'], 'Signal'] = -1  # Sell

    # Store the data
    stock_data[ticker] = data

    print()

