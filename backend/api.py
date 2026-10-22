from fastapi import FastAPI, HTTPException, Query, status
from data import data

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
