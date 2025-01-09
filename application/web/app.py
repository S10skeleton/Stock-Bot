import os
import sqlite3

from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Build a robust absolute path to your database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '..', 'data', 'historical_data.db')

# 1) Serve Your Main Dashboard (index.html)
@app.route('/')
def index():
    """ Render the main HTML page. """
    return render_template('index.html')  # This looks in /templates by default

@app.route('/api/symbols')
def get_symbols():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT symbol FROM market_data ORDER BY symbol ASC")
    rows = cursor.fetchall()
    conn.close()

    symbols = [r[0] for r in rows]
    return jsonify(symbols)


@app.route('/api/market-data/<symbol>')
def get_market_data(symbol):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date,
               open, high, low, close, volume,
               ma_50, ma_200, rsi_14, macd, macd_signal,
               bb_upper, bb_mid, bb_lower
        FROM market_data
        WHERE symbol = ?
        ORDER BY date DESC
        LIMIT 100
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
            "bb_lower": row[13]
        })

    return jsonify(data_list)




if __name__ == '__main__':
    # For local dev, enable debug mode
    app.run(debug=True)

    
