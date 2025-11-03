from app.db import SessionLocal
from app.models import CryptoPrice
from scripts.init_db import init_db


def list_cryptos():
    db = SessionLocal()
    cryptos = db.query(CryptoPrice).all()
    for c in cryptos:
        print(f"{c.symbol}: {c.price}")
    db.close()
    return cryptos  # Add this line to return the cryptos list


if __name__ == "__main__":
    init_db()
    print("=== Crypto Prices ===")
    cryptos = list_cryptos()
    print(f"Loaded {len(cryptos)} cryptos from DB.")