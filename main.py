from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "service": "NIFTY 50 Live API",
        "status": "running",
        "endpoint": "/nifty"
    }

@app.get("/nifty")
def nifty():
    try:
        ticker = yf.Ticker("^NSEI")
        data = ticker.fast_info

        price = data.get("last_price")
        prev = data.get("previous_close")

        if price is None or prev is None:
            return {
                "error": "Yahoo data unavailable",
                "source": "yfinance"
            }

        change = price - prev
        percent = (change / prev) * 100

        return {
            "price": round(price, 2),
            "change": round(change, 2),
            "percent": round(percent, 2),
            "source": "yfinance"
        }

    except Exception as e:
        return {
            "error": "Fetch failed",
            "details": str(e),
            "source": "yfinance"
        }
