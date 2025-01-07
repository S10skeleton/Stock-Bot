import yfinance as yf
import pandas as pd

# Fetch historical data for multiple stocks
stocks = ["AAPL", "MSFT", "GOOGL"]
stock_data = {}  # Dictionary to store data for each stock

for stock in stocks:
    data = yf.download(stock, start="2020-01-01", end="2023-01-01")
    print(f"{stock} data fetched successfully!")
    
    # Add Simple Moving Averages (SMA)
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    # Generate buy and sell signals
    data['Signal'] = 0  # Default to hold
    data.loc[data['SMA_20'] > data['SMA_50'], 'Signal'] = 1  # Buy
    data.loc[data['SMA_20'] < data['SMA_50'], 'Signal'] = -1  # Sell
    
    # Store the data in the dictionary
    stock_data[stock] = data

# Example: Access and print the last 5 rows of data for AAPL
print("\nAAPL Data:")
print(stock_data["AAPL"][['Close', 'SMA_20', 'SMA_50', 'Signal']].tail())

# Example: Print the last 5 rows of data for MSFT
print("\nMSFT Data:")
print(stock_data["MSFT"][['Close', 'SMA_20', 'SMA_50', 'Signal']].tail())

# Example: Print the last 5 rows of data for GOOGL
print("\nGOOGL Data:")
print(stock_data["MSFT"][['Close', 'SMA_20', 'SMA_50', 'Signal']].tail())