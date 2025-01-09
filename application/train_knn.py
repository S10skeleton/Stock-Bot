import os
import sqlite3
import pandas as pd
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATABASE_PATH = 'data/historical_data.db'  # Adjust as needed
TICKERS_CSV = 'tickers.csv'  # Path to your tickers.csv
MODEL_DIR = 'models'  # Directory to save the models

# Ensure the model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data(symbol):
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query(f"""
        SELECT date, close, volume,
               ema_8, ema_13, ema_21, ema_34, ema_55, ema_89, ema_144, ema_200,
               rsi_14, macd, macd_signal
        FROM market_data
        WHERE symbol='{symbol}'
        ORDER BY date ASC
    """, conn)
    conn.close()

    if df.empty:
        return df

    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Create the target label with "hold" logic
    # Buy (1) if price is expected to rise significantly
    # Sell (-1) if price is expected to fall significantly
    # Hold (0) otherwise
    df['future_close'] = df['close'].shift(-1)
    df.dropna(inplace=True)  # Remove last row with no future_close

    # Define a threshold for significant change (e.g., 1% of current price)
    threshold = 0.01
    df['label'] = 0  # Default to hold
    df.loc[(df['future_close'] > df['close'] * (1 + threshold)), 'label'] = 1  # Buy
    df.loc[(df['future_close'] < df['close'] * (1 - threshold)), 'label'] = -1  # Sell

    return df

def train_knn_for_symbol(symbol):
    df = load_data(symbol)
    if len(df) < 50:
        print(f"Not enough data to train KNN for {symbol}. Skipping...")
        return None

    # Define features and labels
    feature_cols = [
        'close', 'volume',
        'ema_8', 'ema_13', 'ema_21', 'ema_34', 'ema_55', 'ema_89', 'ema_144', 'ema_200',
        'rsi_14', 'macd', 'macd_signal'
    ]
    X = df[feature_cols].fillna(0)  # Fill NaN with 0
    y = df['label']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Train KNN
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)

    # Evaluate accuracy
    y_pred = knn.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"KNN Accuracy for {symbol}: {acc * 100:.2f}%")

    # Save the model to file
    model_path = os.path.join(MODEL_DIR, f"{symbol}_knn.pkl")
    with open(model_path, 'wb') as model_file:
        pickle.dump(knn, model_file)

    return knn

def train_knn_for_all_tickers():
    # Load tickers from CSV
    if not os.path.exists(TICKERS_CSV):
        print(f"ERROR: {TICKERS_CSV} does not exist.")
        return

    tickers = pd.read_csv(TICKERS_CSV)['Symbol'].dropna().tolist()
    for symbol in tickers:
        print(f"Training KNN for {symbol}...")
        train_knn_for_symbol(symbol)

if __name__ == "__main__":
    train_knn_for_all_tickers()
