import os
import csv
import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Adjust path if your CSV is in application/tickers.csv
TICKERS_CSV = os.path.join(BASE_DIR, '..', 'tickers.csv')

DATABASE_PATH = os.path.join(BASE_DIR, '..', 'data', 'historical_data.db')

def update_stock_data(symbol='AAPL'):
    """Fetch and insert data for a single symbol into market_data table."""
    ticker = yf.Ticker(symbol)
    # For a daily granularity, you could do period='1y', interval='1d' 
    # or whatever timeframe you want
    data = ticker.history(period='1d', interval='1m')

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

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

    # Insert fetched data
    for index, row in data.iterrows():
        date_str = index.strftime('%Y-%m-%d %H:%M:%S')
        volume_val = int(row['Volume']) if not pd.isna(row['Volume']) else 0

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
            volume_val
        ))

    conn.commit()
    conn.close()

def update_multiple_stocks():
    """Loop through tickers.csv and call update_stock_data for each."""
    if not os.path.exists(TICKERS_CSV):
        print(f"ERROR: {TICKERS_CSV} does not exist.")
        return

    with open(TICKERS_CSV, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            symbol = row['Symbol'].strip()
            if symbol:
                print(f"Fetching data for: {symbol}")
                update_stock_data(symbol)
    print("Done updating multiple stocks.")

if __name__ == "__main__":
    # You can call update_multiple_stocks() to read from CSV 
    # or a single call to update_stock_data('TSLA') for one ticker.
    update_multiple_stocks()
