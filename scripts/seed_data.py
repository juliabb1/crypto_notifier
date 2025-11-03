# scripts/seed_data.py
from app.db import SessionLocal, engine
from app.models import Base, CryptoPrice
from sqlalchemy import inspect


def create_tables_if_not_exist():
    """Create tables if they don't exist"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    if 'cryptoprice' not in existing_tables:
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created")
    else:
        print("✓ Tables already exist")


def seed():
    db = SessionLocal()
    
    # First, create tables if they don't exist
    create_tables_if_not_exist()
    
    # Check if data already exists to avoid duplicates
    existing_count = db.query(CryptoPrice).count()
    if existing_count > 0:
        print(f"✓ Database already contains {existing_count} records")
        db.close()
        return
    
    # Insert seed data
    cryptos = [
        CryptoPrice(symbol="BTC", price=30000),
        CryptoPrice(symbol="ETH", price=2000),
        CryptoPrice(symbol="XRP", price=0.5)
    ]
    db.add_all(cryptos)
    db.commit()
    db.close()
    print("✓ Seed data inserted")


if __name__ == "__main__":
    seed()