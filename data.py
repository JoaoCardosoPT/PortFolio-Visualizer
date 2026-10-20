import requests
import pandas as pd

def data(symbol):
    url = f"https://api.diadata.org/v1/quotation/{symbol.upper()}"

    try:
        response = requests.get(url, timeout=4)

        if response.status_code == 200:
           data = response.json()

           symbol = data.get("Symbol")
           price = data.get("Price")
           time = data.get("Time")

           return data
        elif response.status_code == 404:
            print(f"Error: The Symbol {symbol} is not available")
            return None
        else:
            print(f"Error")
            return None
    except requests.exceptions.RequestException as e:
        print("Connection Error")
        return None

def fetch_candles(symbol, interval='1h', limit=100):
    response = requests.get("https://data-api.binane.vision/api/v3/klines", params={"symbol": f"{symbol.strip().upper()}USDT", "interval": interval, "limit": limit,}, timeout=10,)

    response.raise_for_status()
    rows = response.json()
    if not rows:
        raise ValueError("No history Available")

    candles = pd.DataFrame([row[:6] for row in row], columns=["Date", "Open", "High"]
