# Initialize variables
initial_balance = 10000  # Starting cash in dollars
balance = initial_balance
position = 0  # Number of shares held
trade_log = []  # To store trade details

# Simulate trades
for index, row in data.iterrows():
    if row['Signal'] == 1 and balance >= row['Close']:  # Buy
        position += 1
        balance -= row['Close']
        trade_log.append({'Date': index, 'Action': 'Buy', 'Price': row['Close'], 'Balance': balance})
    elif row['Signal'] == -1 and position > 0:  # Sell
        balance += row['Close']
        position -= 1
        trade_log.append({'Date': index, 'Action': 'Sell', 'Price': row['Close'], 'Balance': balance})

# Final portfolio value
final_balance = balance + (position * data.iloc[-1]['Close'])
print(f"Initial Balance: ${initial_balance:.2f}")
print(f"Final Balance: ${final_balance:.2f}")
print(f"Net Profit: ${final_balance - initial_balance:.2f}")
