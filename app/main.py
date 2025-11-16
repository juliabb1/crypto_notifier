from app.db import SessionLocal
# from app.models import CryptoPrice
from app.models import Cryptocurrency
from scripts.init_db import init_db


def list_cryptocurrencies():
    db = SessionLocal()
    crypto_currencies = db.query(Cryptocurrency).all()
    for c in crypto_currencies:
       print(f"{c.fullName}: ({c.symbol})")
    db.close()
    return crypto_currencies


if __name__ == "__main__":
    init_db()
    print("=== Crypto Prices ===")
    cryptos = list_cryptocurrencies()
    print(f"Loaded {len(cryptos)} cryptos from DB.")