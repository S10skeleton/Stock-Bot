import time
import schedule
import os
from data_fetch import update_multiple_stocks  # or update_stock_data, etc.

def job():
    print("Running data fetch job...")
    update_multiple_stocks()  # or call your function that updates all tickers
    print("Data fetch complete.")

# Schedule the job every 30 minutes
schedule.every(10).minutes.do(job)

if __name__ == "__main__":
    print("Scheduler started. Will update every 10 minutes.")
    # Run the scheduler indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)
