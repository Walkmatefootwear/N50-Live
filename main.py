from fastapi import FastAPI
import yfinance as yf
import time

app = FastAPI()

ticker = yf.Ticker("^NSEI")
last_candle_fetch = 0
cached_candles = []

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/nifty/price")
def nifty_price():
    info = ticker.fast_info
    price = info["last_price"]
    prev = info["previous_close"]

    return {
        "price": round(price, 2),
        "change": round(price - prev, 2),
        "percent": round(((price - prev) / prev) * 100, 2)
    }

@app.get("/nifty/candles")
def nifty_candles():
    global last_candle_fetch, cached_candles

    now = time.time()

    # Cache candles for 60 seconds
    if now - last_candle_fetch < 60 and cached_candles:
        return {"candles": cached_candles}

    hist = ticker.history(period="7d", interval="1d")

    candles = []
    for _, r in hist.iterrows():
        candles.append({
            "o": round(float(r["Open"]), 2),
            "h": round(float(r["High"]), 2),
            "l": round(float(r["Low"]), 2),
            "c": round(float(r["Close"]), 2)
        })

    cached_candles = candles
    last_candle_fetch = now

    return {"candles": candles}
