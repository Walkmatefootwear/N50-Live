from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # safe for read-only price API
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/nifty")
def nifty():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()

    q = data["quoteResponse"]["result"][0]

    return {
        "price": q["regularMarketPrice"],
        "change": q["regularMarketChange"],
        "percent": q["regularMarketChangePercent"]
    }
