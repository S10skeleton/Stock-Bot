# Stock-Bot

## Overview
This project is a Python-based **Stock Trading Bot** designed to analyze historical stock data, calculate technical indicators, and simulate trading strategies. The bot fetches real-time stock data, evaluates buy/sell signals, and can be extended for automated trading using broker APIs. This project is aimed at creating a robust trading model that can monitor and evaluate a large number of stocks programmatically.

## Features
- **Fetch Historical Data**: Retrieves historical stock data for analysis.
- **Technical Indicators**: Calculates indicators like SMA (Simple Moving Average), RSI, and more.
- **Simulated Trading**: Simulates trades based on defined strategies and tracks profits/losses.
- **Dynamic Stock Monitoring**: Supports monitoring individual stocks or multiple stocks from a predefined list.
- **Real-time Data**: Integrates with APIs like `yfinance` for real-time stock price updates.
- **Extensibility**: Easily integrate broker APIs (e.g., Alpaca, Interactive Brokers) for automated trading.

## Installation
### Clone the Repository:
```bash
git clone https://github.com/your-username/stock-trading-bot.git
cd stock-trading-bot
```

### Set Up the Environment:
- Create a virtual environment (optional but recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate   # On Windows: venv\Scriptsctivate
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Install Additional Tools (if using Anaconda):
```bash
conda activate base
conda install pandas matplotlib yfinance
```

## Usage
### Prepare Stock List:
Add stock tickers to `tickers.csv` for analysis. Example:
```csv
Symbol
AAPL
MSFT
GOOGL
AMZN
TSLA
```

### Run the Bot:
Execute the main script to fetch data and simulate trading:
```bash
python fetch_stock_data.py
```

### Results:
- View simulated trading performance in the console.
- Visualize stock trends, indicators, and buy/sell signals.

## Project Structure
```
Stock-Bot/
├── fetch_stock_data.py    # Main script to fetch data and simulate trading
├── tickers.csv            # List of stock tickers to analyze
├── requirements.txt       # Dependencies for the project
├── README.md              # Project documentation
└── data/                  # Folder for saving fetched stock data (optional)
```

## Key Components
- **Technical Indicators**:
  - **SMA**: Simple Moving Averages to identify trends.
  - **Signals**: Buy/Sell signals based on SMA crossovers.
- **Simulated Trading**:
  - Tracks cash balance, portfolio value, and trade history.
  - Evaluates strategy performance (e.g., win rate, profit/loss).
- **Data Visualization**:
  - Uses `matplotlib` to plot stock prices, indicators, and signals.

## Future Enhancements
- **Expand Indicators**: Add RSI, MACD, Bollinger Bands, and others.
- **Backtesting Framework**: Evaluate strategies across various timeframes.
- **Real-time Trading**: Integrate with broker APIs for automated trading.
- **Portfolio Management**: Monitor multiple stocks and manage capital allocation.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- **Libraries Used**:
  - [yfinance](https://github.com/ranaroussi/yfinance) for stock data.
  - [matplotlib](https://matplotlib.org/) for data visualization.
  - [pandas](https://pandas.pydata.org/) for data manipulation.
- **Inspirations**:
  - Financial trading strategies and algorithmic trading concepts.

## Disclaimer
This project is for educational purposes only. Trading stocks involves substantial risk, and past performance does not guarantee future results. Use at your own risk.
