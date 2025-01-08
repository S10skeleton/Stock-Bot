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

# 2) Provide an API endpoint for market data
@app.route('/api/market-data')
def get_market_data():
    """ Return some rows from the market_data table as JSON. """
    # Connect to the DB
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Query up to the first 10 rows for demo (or whatever you like)
    cursor.execute("""
        SELECT symbol, date, open, high, low, close, volume
        FROM market_data
        ORDER BY date ASC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()

    # Convert to a list of dicts for easy JSON serialization
    data_list = [
        {
            "symbol": row[0],
            "date": row[1],
            "open": row[2],
            "high": row[3],
            "low": row[4],
            "close": row[5],
            "volume": row[6]
        }
        for row in rows
    ]

    return jsonify(data_list)

if __name__ == '__main__':
    # For local dev, enable debug mode
    app.run(debug=True)
