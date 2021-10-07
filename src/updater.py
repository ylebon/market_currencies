import os

import requests
from apscheduler.schedulers.background import BackgroundScheduler


def run_tasks():
    print("Running referencedata update")
    # poloniex exclude
    exchanges = ["binance", "bitstamp", "cex", "okex", "oanda", "poloniex"]
    for exchange in exchanges:
        try:
            print(f"Updating exchange '{exchange.upper()}' referencedata ...")
            url = f"http://localhost:8000/exchanges/{exchange}/instruments"
            with requests.Session() as session:
                session.post(url)
        except Exception as error:
            print(f"ERROR: failed to update exchange '{exchange.upper()}' referencedata.")
            print(error)


def start():
    # run tasks
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_tasks, 'date')
    scheduler.add_job(run_tasks, 'interval', hours=int(os.environ.get('UPDATE_INTERVAL', 24)))
    scheduler.start()
