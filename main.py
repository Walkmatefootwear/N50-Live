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

        # Use history instead of fast_info (more reliable)
        hist = ticker.history(period="2d", interval="1d")

        if hist.empty or len(hist) < 2:
            return {
                "error": "Insufficient data",
                "source": "yfinance"
            }

        prev_close = float(hist["Close"].iloc[-2])
        last_price = float(hist["Close"].iloc[-1])

        change = last_price - prev_close
        percent = (change / prev_close) * 100

        return {
            "price": round(last_price, 2),
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
