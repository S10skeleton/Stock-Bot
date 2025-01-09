from flask import Flask, jsonify, request, render_template
import os
import pickle
import sqlite3
import pandas as pd

app = Flask(__name__)
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'historical_data.db')
MODEL_DIR = 'models'


@app.route('/')
def index():
    return render_template('index.html')

def load_model(symbol):
    model_path = os.path.join(MODEL_DIR, f"{symbol}_knn.pkl")
    if not os.path.exists(model_path):
        return None
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

@app.route('/api/knn-signals/<symbol>', methods=['GET'])
def get_knn_signals(symbol):
    """Return predicted buy/sell signals using the KNN model for the selected symbol."""
    model = load_model(symbol)
    if model is None:
        return jsonify({"error": f"No model found for {symbol}"}), 404

    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query(f"""
        SELECT date, close, volume,
               ema_8, ema_13, ema_21, ema_34, ema_55, ema_89, ema_144, ema_200,
               rsi_14, macd, macd_signal
        FROM market_data
        WHERE symbol = ?
        ORDER BY date ASC
    """, conn, params=(symbol,))
    conn.close()

    if df.empty:
        return jsonify({"error": f"No data found for {symbol}"}), 404

    feature_cols = [
        "close", "volume",
        "ema_8", "ema_13", "ema_21", "ema_34", "ema_55", "ema_89", "ema_144", "ema_200",
        "rsi_14", "macd", "macd_signal"
    ]
    df["prediction"] = model.predict(df[feature_cols].fillna(0))

    # Filter out "hold" signals (label == 0)
    signals = []
    for _, row in df.iterrows():
        if row["prediction"] == 1:  # Buy
            signals.append({"date": row["date"], "price": row["close"], "type": "buy"})
        elif row["prediction"] == -1:  # Sell
            signals.append({"date": row["date"], "price": row["close"], "type": "sell"})

    return jsonify(signals)



@app.route('/api/symbols')
def get_symbols():
    """Return distinct symbols in the DB."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT symbol FROM market_data ORDER BY symbol ASC;")
    rows = cursor.fetchall()
    conn.close()
    symbols = [r[0] for r in rows]
    return jsonify(symbols)

@app.route('/api/market-data/<symbol>')
def get_market_data(symbol):
    """Return date, close, and the new indicator columns (multi-EMA) for the selected symbol."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    # SELECT the columns you want, including the new EMAs
    cursor.execute("""
        SELECT date,
            open, high, low, close, volume,
            ma_50, ma_200, rsi_14, macd, macd_signal,
            bb_upper, bb_mid, bb_lower,
            ema_8, ema_13, ema_21, ema_34, ema_55, ema_89, ema_144, ema_200
        FROM market_data
        WHERE symbol = ?
        ORDER BY date ASC
    """, (symbol,))
    rows = cursor.fetchall()
    conn.close()

    data_list = []
    for row in rows:
        data_list.append({
            "date": row[0],
            "open": row[1],
            "high": row[2],
            "low": row[3],
            "close": row[4],
            "volume": row[5],
            "ma_50": row[6],
            "ma_200": row[7],
            "rsi_14": row[8],
            "macd": row[9],
            "macd_signal": row[10],
            "bb_upper": row[11],
            "bb_mid": row[12],
            "bb_lower": row[13],
            "ema_8": row[14],
            "ema_13": row[15],
            "ema_21": row[16],
            "ema_34": row[17],
            "ema_55": row[18],
            "ema_89": row[19],
            "ema_144": row[20],
            "ema_200": row[21]
        })

    return jsonify(data_list)

if __name__ == '__main__':
    # Run your Flask dev server
    app.run(debug=True)
