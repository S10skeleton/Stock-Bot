import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '..', 'data', 'historical_data.db')

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM market_data LIMIT 5;")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
