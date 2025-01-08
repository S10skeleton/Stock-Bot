"""
app.py
------
Local Flask server to serve the web interface and provide REST endpoints.
"""
from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'historical_data.db')

def get_portfolio_data():
    # For demonstration, let's just return some placeholders.
    # In a real app, you'd query your portfolio table in the DB.
    portfolio = [
        {"symbol": "AAPL", "shares": 10, "avg_price": 150.00},
        {"symbol": "TSLA", "shares": 5, "avg_price": 700.00}
    ]
    return portfolio

@app.route('/')
def index():
    # This will render `templates/index.html`
    return render_template('index.html')

@app.route('/api/portfolio', methods=['GET'])
def api_portfolio():
    # Return the portfolio JSON
    return jsonify(get_portfolio_data())

@app.route('/api/performance', methods=['GET'])
def api_performance():
    # Sample data
    data = {
        "totalValue": 120_000.0,  # example
        "unrealizedPnL": 5_000.0
    }
    return jsonify(data)

if __name__ == "__main__":
    # Debug mode for local development
    app.run(debug=True)
