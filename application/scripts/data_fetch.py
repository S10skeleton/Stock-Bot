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

def ensure_indicator_columns():
    """
    Add columns for technical indicators if they don't already exist.
    This modifies the existing market_data table.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # List of columns to add, if they don't exist
    columns = [
        ('ma_50', 'REAL'),
        ('ma_200', 'REAL'),
        ('rsi_14', 'REAL'),
        ('macd', 'REAL'),
        ('macd_signal', 'REAL'),
        ('bb_upper', 'REAL'),
        ('bb_mid', 'REAL'),
        ('bb_lower', 'REAL')
    ]

    for col_name, col_type in columns:
        try:
            cursor.execute(f"ALTER TABLE market_data ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError as e:
            # Likely the column already exists
            pass

    conn.commit()
    conn.close()

def update_stock_data(symbol):
    """
    Fetch daily data for 'symbol' and insert into market_data table (if not already present).
    Then compute indicators (MA, RSI, MACD, Bollinger) and update the rows.
    """
    # 1) Fetch daily historical data, e.g. 1 year
    #    If you want more data for the long-term (say 2 or 5 years), adjust 'period'
    data = yf.Ticker(symbol).history(period='1y', interval='1d')

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 2) Create the table if needed (without indicator columns here)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            UNIQUE(symbol, date)
        )
    """)

    # 3) Insert or ignore daily rows
    for index, row in data.iterrows():
        date_str = index.strftime('%Y-%m-%d')  # daily date
        volume_val = int(row['Volume']) if not pd.isna(row['Volume']) else 0

        cursor.execute("""
            INSERT OR IGNORE INTO market_data (symbol, date, open, high, low, close, volume)
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

    # 4) Now compute and update indicators
    compute_and_update_indicators(symbol)

def compute_and_update_indicators(symbol):
    """
    Loads daily rows for 'symbol' from the DB into a DataFrame,
    computes indicators, then updates each row in the DB.
    """
    # Ensure columns for indicators exist
    ensure_indicator_columns()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 4.1) Load data from DB into a DataFrame
    df = pd.read_sql_query(f"""
        SELECT * FROM market_data
        WHERE symbol='{symbol}'
        ORDER BY date ASC
    """, conn)

    if df.empty:
        conn.close()
        return  # No data to process

    # Convert 'date' to datetime, in case it’s string
    df['date'] = pd.to_datetime(df['date'])

    # 4.2) Compute indicators in pandas
    df = df.sort_values('date')  # ensure chronological order

    # --- Moving Averages ---
    df['ma_50'] = df['close'].rolling(window=50).mean()
    df['ma_200'] = df['close'].rolling(window=200).mean()

    # --- RSI (14) ---
    # We'll do a quick RSI implementation using pandas
    # Alternatively, you can use a library like pandas_ta or talib
    df['rsi_14'] = compute_rsi(df['close'], window=14)

    # --- MACD (12,26,9) ---
    # MACD = EMA(12) - EMA(26), Signal = EMA(9) of that MACD
    df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema_12'] - df['ema_26']
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()

    # --- Bollinger Bands (20, 2 std) ---
    # Typical usage: 20-day moving average & +/- 2 std dev
    df['bb_mid'] = df['close'].rolling(window=20).mean()
    df['bb_std'] = df['close'].rolling(window=20).std()
    df['bb_upper'] = df['bb_mid'] + (2 * df['bb_std'])
    df['bb_lower'] = df['bb_mid'] - (2 * df['bb_std'])

    # 4.3) Update each row in the DB with the computed values
    for idx, row in df.iterrows():
        # Some rows (early ones) might be NaN if not enough data to compute
        values = {
            'ma_50':       float(row['ma_50'])       if pd.notna(row['ma_50']) else None,
            'ma_200':      float(row['ma_200'])      if pd.notna(row['ma_200']) else None,
            'rsi_14':      float(row['rsi_14'])      if pd.notna(row['rsi_14']) else None,
            'macd':        float(row['macd'])        if pd.notna(row['macd']) else None,
            'macd_signal': float(row['macd_signal']) if pd.notna(row['macd_signal']) else None,
            'bb_upper':    float(row['bb_upper'])    if pd.notna(row['bb_upper']) else None,
            'bb_mid':      float(row['bb_mid'])      if pd.notna(row['bb_mid']) else None,
            'bb_lower':    float(row['bb_lower'])    if pd.notna(row['bb_lower']) else None
        }

        date_str = row['date'].strftime('%Y-%m-%d')
        cursor.execute(f"""
            UPDATE market_data
            SET ma_50 = :ma_50,
                ma_200 = :ma_200,
                rsi_14 = :rsi_14,
                macd = :macd,
                macd_signal = :macd_signal,
                bb_upper = :bb_upper,
                bb_mid = :bb_mid,
                bb_lower = :bb_lower
            WHERE symbol = '{symbol}' AND date = '{date_str}'
        """, values)

    conn.commit()
    conn.close()

def compute_rsi(series, window=14):
    """
    Basic RSI calculation (14-day default).
    RSI = 100 - (100 / (1 + RS))
    where RS = avg_gain / avg_loss
    This is a simplified version, not exactly matching Wilder's smoothing approach,
    but good for demonstration. 
    """
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

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
                print(f"Fetching + computing indicators for: {symbol}")
                update_stock_data(symbol)
    print("Done updating multiple stocks.")

if __name__ == "__main__":
    # Or a single call to update_stock_data('TSLA') for one ticker:
    update_multiple_stocks()
