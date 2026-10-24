import requests

def data(symbol, interval="1h", limit=100):
    response = requests.get(f"https://api.diadata.org/v1/quotation/{symbol.strip().upper()}", timeout=10,)

    response.raise_for_status()
    return response.json()

def fetch_candles(symbol, interval="1h", limit=100):
    response = requests.get(
        "https://data-api.binance.vision/api/v3/klines",
        params={
            "symbol": symbol.strip().upper(),
            "interval": interval,
            "limit": limit,
        },
        timeout=10,
    )

    response.raise_for_status()
    raw_candles = response.json()

    candles = []

    for candle in raw_candles:
        candles.append({
            "time": candle[0] // 1000,
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
        })

    return candles
