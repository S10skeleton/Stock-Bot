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

    # Basic columns for MAs, RSI, MACD, Bollinger
    base_columns = [
        ('ma_50', 'REAL'),
        ('ma_200', 'REAL'),
        ('rsi_14', 'REAL'),
        ('macd', 'REAL'),
        ('macd_signal', 'REAL'),
        ('bb_upper', 'REAL'),
        ('bb_mid', 'REAL'),
        ('bb_lower', 'REAL')
    ]

    # Additional columns for multi-EMA ribbon
    ema_columns = [
        ('ema_8',   'REAL'),
        ('ema_13',  'REAL'),
        ('ema_21',  'REAL'),
        ('ema_34',  'REAL'),
        ('ema_55',  'REAL'),
        ('ema_89',  'REAL'),
        ('ema_144', 'REAL'),
        ('ema_200', 'REAL')
    ]

    columns = base_columns + ema_columns

    for col_name, col_type in columns:
        try:
            cursor.execute(f"ALTER TABLE market_data ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            # Column likely exists already
            pass

    conn.commit()
    conn.close()

def update_stock_data(symbol):
    """
    Fetch daily data for 'symbol' and insert into market_data table (if not already present).
    Then compute indicators (MA, RSI, MACD, Bollinger, multi-EMA) and update the rows.
    """
    # 1) Fetch daily historical data, e.g. 1 year
    #    If you want more data for the long-term (say 2 or 5 years), adjust 'period'
    data = yf.Ticker(symbol).history(period='1y', interval='1d')

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 2) Create the table if it doesn't exist yet (without indicator columns)
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

    # 3) Insert or IGNORE daily rows
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
    # Ensure columns for indicators & EMAs exist
    ensure_indicator_columns()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 1) Load data from DB into a DataFrame
    df = pd.read_sql_query(f"""
        SELECT *
        FROM market_data
        WHERE symbol='{symbol}'
        ORDER BY date ASC
    """, conn)

    if df.empty:
        conn.close()
        return  # No data to process

    # Convert 'date' to datetime, in case it’s string
    df['date'] = pd.to_datetime(df['date'])

    # 2) Sort and compute indicators in pandas
    df.sort_values('date', inplace=True)

    # --- 50 & 200 Moving Averages ---
    df['ma_50']  = df['close'].rolling(window=50).mean()
    df['ma_200'] = df['close'].rolling(window=200).mean()

    # --- RSI (14) ---
    df['rsi_14'] = compute_rsi(df['close'], window=14)

    # --- MACD (12,26,9) ---
    df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema_12'] - df['ema_26']
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()

    # --- Additional EMAs for the "ribbon" ---
    df['ema_8']   = df['close'].ewm(span=8,   adjust=False).mean()
    df['ema_13']  = df['close'].ewm(span=13,  adjust=False).mean()
    df['ema_21']  = df['close'].ewm(span=21,  adjust=False).mean()
    df['ema_34']  = df['close'].ewm(span=34,  adjust=False).mean()
    df['ema_55']  = df['close'].ewm(span=55,  adjust=False).mean()
    df['ema_89']  = df['close'].ewm(span=89,  adjust=False).mean()
    df['ema_144'] = df['close'].ewm(span=144, adjust=False).mean()
    df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()  # you also have an ma_200; this is an EMA_200

    # --- Bollinger Bands (20, 2 std) ---
    df['bb_mid'] = df['close'].rolling(window=20).mean()
    df['bb_std'] = df['close'].rolling(window=20).std()
    df['bb_upper'] = df['bb_mid'] + (2 * df['bb_std'])
    df['bb_lower'] = df['bb_mid'] - (2 * df['bb_std'])

    # 3) Update each row in the DB with indicator values
    for idx, row in df.iterrows():
        date_str = row['date'].strftime('%Y-%m-%d')
        
        # Convert to float or None if NaN (some early rows might not have enough data for a 50/200/EMA_200)
        values = {
            'ma_50':       float(row['ma_50'])       if pd.notna(row['ma_50'])       else None,
            'ma_200':      float(row['ma_200'])      if pd.notna(row['ma_200'])      else None,
            'rsi_14':      float(row['rsi_14'])      if pd.notna(row['rsi_14'])      else None,
            'macd':        float(row['macd'])        if pd.notna(row['macd'])        else None,
            'macd_signal': float(row['macd_signal']) if pd.notna(row['macd_signal']) else None,
            'bb_upper':    float(row['bb_upper'])    if pd.notna(row['bb_upper'])    else None,
            'bb_mid':      float(row['bb_mid'])      if pd.notna(row['bb_mid'])      else None,
            'bb_lower':    float(row['bb_lower'])    if pd.notna(row['bb_lower'])    else None,
            'ema_8':       float(row['ema_8'])       if pd.notna(row['ema_8'])       else None,
            'ema_13':      float(row['ema_13'])      if pd.notna(row['ema_13'])      else None,
            'ema_21':      float(row['ema_21'])      if pd.notna(row['ema_21'])      else None,
            'ema_34':      float(row['ema_34'])      if pd.notna(row['ema_34'])      else None,
            'ema_55':      float(row['ema_55'])      if pd.notna(row['ema_55'])      else None,
            'ema_89':      float(row['ema_89'])      if pd.notna(row['ema_89'])      else None,
            'ema_144':     float(row['ema_144'])     if pd.notna(row['ema_144'])     else None,
            'ema_200':     float(row['ema_200'])     if pd.notna(row['ema_200'])     else None,
        }

        cursor.execute(f"""
            UPDATE market_data
            SET 
                ma_50       = :ma_50,
                ma_200      = :ma_200,
                rsi_14      = :rsi_14,
                macd        = :macd,
                macd_signal = :macd_signal,
                bb_upper    = :bb_upper,
                bb_mid      = :bb_mid,
                bb_lower    = :bb_lower,
                ema_8       = :ema_8,
                ema_13      = :ema_13,
                ema_21      = :ema_21,
                ema_34      = :ema_34,
                ema_55      = :ema_55,
                ema_89      = :ema_89,
                ema_144     = :ema_144,
                ema_200     = :ema_200
            WHERE symbol = '{symbol}' AND date = '{date_str}'
        """, values)

    conn.commit()
    conn.close()

def compute_rsi(series, window=14):
    """
    Basic RSI calculation (14-day).
    RSI = 100 - (100 / (1 + RS)), where RS = avg_gain / avg_loss.
    This is a simplified approach, not exactly Wilder's smoothing.
    """
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def update_multiple_stocks():
    """Loop through tickers.csv and call update_stock_data for each symbol."""
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
    # You can call update_multiple_stocks() to process everything in tickers.csv
    # or call update_stock_data('TSLA') for a single ticker.
    update_multiple_stocks()
