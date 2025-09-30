# main.py
from fastapi import FastAPI

app = FastAPI(title="Minimal Trader Bot API")

@app.get("/")
def read_root():
    return {"status": "Service is running!", "version": "1.0.0"}

@app.get("/coin/price/{coin_id}")
def get_coin_price(coin_id: str):
    return {"coin_id": coin_id, "price": 100.0}