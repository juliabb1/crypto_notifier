# app/models.py
from app.db import Base
from sqlalchemy import Column, Float, Integer, String


class CryptoPrice(Base):
    __tablename__ = "crypto_price"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
