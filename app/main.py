from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.models import Cryptocurrency
from app.db import SessionLocal
from scripts.init_db import init_db

def list_cryptocurrencies():
    db = SessionLocal()
    crypto_currencies = db.query(Cryptocurrency).all()
    for c in crypto_currencies:
       print(f"{c.fullName}: ({c.symbol})")
    db.close()
    return crypto_currencies

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to DB...")
    init_db()
    print("=== Crypto Prices ===")
    cryptos = list_cryptocurrencies()
    print(f"Loaded {len(cryptos)} cryptos from DB.")

    yield

    # Clean up the ML models and release the resources
    print("Closing DB connection...")
app = FastAPI(lifespan=lifespan)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}