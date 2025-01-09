
# Stock Bot

A local, self-contained stock trading AI bot that:

- Collects Historical & Real-Time Data via Python scripts (using yfinance or any other API).
- Computes Technical Indicators (50- & 200-day Moving Averages, RSI, MACD, Bollinger Bands).
- Stores all data and indicators in a local SQLite database.
- Presents a local dashboard (HTML/CSS/JS + Flask) where you can select symbols and see relevant price + indicator info.
- *(Planned)* Performs Sentiment Analysis from multiple sources (Twitter/X, Reddit, StockTwits, Finnhub, etc.) to gauge market sentiment.
- *(Planned)* Trains/Uses an AI Model to generate buy/sell signals or forecasts, integrating technical + sentiment data.

![StockPage](application/web/assets/Screenshot.png)

## Table of Contents

- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Features](#features)
  - [Data Collection](#data-collection)
  - [Technical Indicators](#technical-indicators)
  - [Local Web Interface](#local-web-interface)
  - [Sentiment Analysis (Planned)](#sentiment-analysis-planned)
  - [AI Model (Planned)](#ai-model-planned)
- [Dependencies](#dependencies)
- [Future Plans](#future-plans)
- [License](#license)

## Project Structure

A possible layout (simplified):

```
Stock-Bot/
├── application/
│   ├── scripts/
│   │   └── data_fetch.py
│   │   └── sentiment_fetch.py (planned)
│   ├── web/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   └── js/
│   │   │       └── script.js
│   │   ├── templates/
│   │   │   └── index.html
│   │   └── app.py (Flask server)
│   ├── data/
│   │   └── historical_data.db (SQLite DB)
│   ├── aggregator/ (planned aggregator for multi-source sentiment/data)
│   └── README.md (this file)
├── tickers.csv
├── .env (for API keys, ignored by Git)
├── requirements.txt
└── ...
```

## Setup & Installation

1. Clone this repository (or download it).
2. Create/Activate a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or .\venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Prepare your `.env` file (if you plan to use external APIs). Example:
   ```makefile
   TWITTER_BEARER_TOKEN="YOUR_TOKEN_HERE"
   NEWSAPI_KEY="YOUR_NEWSAPI_KEY"
   ```
   Ensure `.env` is in `.gitignore`.

## Usage

1. Add your symbols to `tickers.csv` in the format:
   ```csv
   Symbol
   AAPL
   TSLA
   MSFT
   ...
   ```

2. Fetch & Store Data:
   ```bash
   cd application
   python scripts/data_fetch.py
   ```
   This will pull daily price data for each symbol and store rows in `historical_data.db`. It will also compute indicators like `MA_50`, `MA_200`, `RSI_14`, `MACD`, etc.

3. Run the Flask App:
   ```bash
   python web/app.py
   ```
   Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser. A dropdown lets you pick a symbol; a table displays price and indicator columns (MA, RSI, MACD, Bollinger, etc.).

## Features

### Data Collection
- **yfinance** for daily stock data.
- `tickers.csv` as your watchlist.
- SQLite DB (`historical_data.db`) for persistent storage.

### Technical Indicators
- **Moving Averages**: 50-day (`ma_50`) and 200-day (`ma_200`).
- **RSI**: 14-period Relative Strength Index.
- **MACD**: (12,26,9) plus MACD signal line.
- **Bollinger Bands**: (20-day SMA ± 2 std).

### Local Web Interface
- Flask backend serving JSON endpoints:
  - `/api/symbols`: Returns a list of stock tickers in DB.
  - `/api/market-data/<symbol>`: Returns the latest rows + indicator columns.
- HTML/JS/CSS front-end:
  - A dropdown to select symbol.
  - A table showing date, open, high, low, close, volume, and computed indicators.

### Sentiment Analysis *(Planned)*
- Fetch and combine sentiment data from multiple sources:
  - Twitter/X (if rate limits allow)
  - Reddit (via PRAW or direct API)
  - News (NewsAPI, RSS)
  - Finnhub or other aggregator
- Store in the DB, possibly in a `sentiment_data` table with fields like `(symbol, source, text, sentiment_score, created_at)`.
- Combine with price data for advanced signals.

### AI Model *(Planned)*
- Incorporate a machine learning or deep learning model that:
  - Ingests technical indicators + sentiment features.
  - Outputs a trading signal (buy/sell/hold) or price forecast.
- Backtest performance before going live.

## Dependencies

- Python 3.8+ (recommended)
- Flask for the web server
- `requests` / `python-dotenv` for API integration
- `yfinance` for stock data
- `pandas` for data manipulation & indicator calculations
- `sqlite3` (built into Python)
- *(Planned)* `nltk` for sentiment analysis, or libraries like `praw` (Reddit) / `tweepy` (Twitter).

Install required dependencies:
```bash
pip install flask requests python-dotenv yfinance pandas
```

## Future Plans

- **Automated Scheduling**:
  Use `schedule` or OS-level Task Scheduler to fetch data periodically.
- **Advanced Sentiment**:
  Possibly use FinBERT or another specialized NLP model for financial text.
- **Portfolio & Transactions**:
  Create a portfolio or transactions table to track buy/sell orders.
  Integrate a broker API (e.g., Alpaca, Interactive Brokers) for live or paper trading.
- **Refined AI**:
  Train a model offline with historical data & sentiment.
  Evaluate performance.
  Integrate with the local dashboard to see predicted signals.

## License

This project is for educational purposes. You can adapt it to your own needs. If sharing publicly, consider adding an open-source license (e.g., MIT) or your own terms.
