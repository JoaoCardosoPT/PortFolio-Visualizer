from fastapi import FastAPI, HTTPException, Query, status
from data import data, fetch_candles

app = FastAPI(title="Crypto API")
# define our route
@app.get("/api/quote")

def get_quote(symbol: str = Query(..., description="Crypto Symbol")):
    symbol_normalized = symbol.strip().upper()

    if not symbol_normalized:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No Symbol")

    result = data(symbol_normalized)
    
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Not possible to obtain data")
    return {"data": result} 

@app.get("/api/candles")
def get_candles(symbol: str = Query(...), interval: str = "1h", limit: int = Query(24, ge=1, le=1000), ):
    candles = fetch_candles(symbol, interval, limit)
    return {"data": candles}
