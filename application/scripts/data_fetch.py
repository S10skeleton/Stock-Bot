"""
data_fetch.py
------------
Pulls stock data (historical & real-time) and stores/updates it in the local DB.
"""
import yfinance as yf
import sqlite3
from datetime import datetime

DATABASE_PATH = '../data/historical_data.db'

def update_stock_data(symbol='AAPL'):
    """Fetch latest data from Yahoo Finance and store it in the SQLite DB."""
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='1d', interval='1m')  # last trading day, 1-min intervals

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Example table: market_data (id, symbol, date, open, high, low, close, volume)
    # Create table if not exists:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER
        )
    """)

    for index, row in data.iterrows():
        date_str = index.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO market_data (symbol, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            symbol,
            date_str,
            row['Open'],
            row['High'],
            row['Low'],
            row['Close'],
            int(row['Volume']) if not pd.isna(row['Volume']) else 0
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_stock_data()
