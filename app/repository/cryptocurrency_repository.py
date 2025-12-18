import logging
from sqlalchemy.orm import Session
from app.models import Cryptocurrency, Coin
from app.repository.base_repository import BaseRepository

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')


class CryptocurrencyRepository(BaseRepository):
    
    def cryptocurrencies_exist(self) -> bool:
        with self.get_session() as db:
            count = db.query(Cryptocurrency).count()
            return count > 0
    
    def crypto_exists(self, identifier: str) -> bool:
        with self.get_session() as db:
            crypto = db.query(Cryptocurrency).filter(
                (Cryptocurrency.symbol == identifier.upper()) |
                (Cryptocurrency.fullName == identifier)
            ).first()
            return crypto is not None
    
    def get_crypto_by_symbol(self, symbol: str) -> Cryptocurrency | None:
        with self.get_session() as db:
            return db.query(Cryptocurrency).filter(
                Cryptocurrency.symbol == symbol.upper()
            ).first()
    
    def get_all_cryptocurrencies(self) -> list[Cryptocurrency]:
        with self.get_session() as db:
            return db.query(Cryptocurrency).all()
    
    def store_cryptocurrencies(self, crypto_currencies: list[Coin]) -> bool:
        with self.get_session() as db:
            added_count = 0
            updated_count = 0
            
            for crypto in crypto_currencies:
                existing_crypto = db.query(Cryptocurrency).filter(
                    Cryptocurrency.symbol == crypto.symbol.upper()
                ).first()
                
                if not existing_crypto:
                    new_crypto = Cryptocurrency(
                        symbol=crypto.symbol.upper(),
                        fullName=crypto.name
                    )
                    db.add(new_crypto)
                    added_count += 1
                elif existing_crypto.fullName != crypto.name:
                    # Update name if changed
                    existing_crypto.fullName = crypto.name
                    updated_count += 1
            
            if added_count > 0:
                logging.info(f"Successfully stored {added_count} new cryptocurrencies")
            if updated_count > 0:
                logging.info(f"Updated {updated_count} cryptocurrency names")
            if added_count == 0 and updated_count == 0:
                logging.info("All cryptocurrencies already up to date")
            
            return True
    
    def store_cryptocurrency(self, symbol: str, full_name: str) -> Cryptocurrency:
        with self.get_session() as db:
            existing_crypto = db.query(Cryptocurrency).filter(
                Cryptocurrency.symbol == symbol.upper()
            ).first()
            
            if existing_crypto:
                logging.info(f"Cryptocurrency {symbol} already exists")
                return existing_crypto
            
            new_crypto = Cryptocurrency(
                symbol=symbol.upper(),
                fullName=full_name
            )
            db.add(new_crypto)
            db.flush()
            logging.info(f"Stored new cryptocurrency: {symbol}")
            return new_crypto
