from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

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
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()

        result = data.get("quoteResponse", {}).get("result", [])

        if not result:
            return {
                "error": "No data from Yahoo",
                "source": "yahoo"
            }

        q = result[0]

        return {
            "price": q.get("regularMarketPrice"),
            "change": q.get("regularMarketChange"),
            "percent": q.get("regularMarketChangePercent"),
            "source": "yahoo"
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": "Request failed",
            "details": str(e),
            "source": "yahoo"
        }

    except Exception as e:
        return {
            "error": "Unexpected error",
            "details": str(e)
        }
