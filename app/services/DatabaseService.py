import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Account, Cryptocurrency, Notification, PlatformType, Coin
from app.services.DataService import DataService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')


class AccountService:
    
    @staticmethod
    def get_or_create_account(platform: PlatformType, platform_id: str) -> Account:
        db = SessionLocal()
        try:
            # Check if account already exists
            existing_account = db.query(Account).filter(
                Account.platform == platform,
                Account.platformId == str(platform_id)
            ).first()
            
            if existing_account:
                logging.info(f"Found existing {platform.value} account for {platform_id}")
                return existing_account
            
            # Create new account if it doesn't exist, userId is created by db
            new_account = Account(
                platform=platform,
                platformId=str(platform_id),
                created_at=datetime.now()
            )
            db.add(new_account)
            db.commit()
            logging.info(f"Created new {platform.value} account for {platform_id}")
            return new_account
        except Exception as e:
            logging.error(f"Error getting/creating account: {e}")
            db.rollback()
            raise
        finally:
            db.close()


class FavoriteService:
    
    @staticmethod
    def add_favorite(platform: PlatformType, platform_id: str, symbol: str, full_name: str = None) -> bool:
  
        db = SessionLocal()
        try:
            account = db.query(Account).filter(
                Account.platform == platform,
                Account.platformId == str(platform_id)
            ).first()
            
            if not account:
                logging.error(f"Account not found for {platform_id}")
                return False
            
            # Get or create cryptocurrency - search by uppercase symbol
            crypto = db.query(Cryptocurrency).filter(
                Cryptocurrency.symbol == symbol.upper()
            ).first()
            
            if not crypto:
                raise ValueError(f"Cryptocurrency {symbol} not found in database")
            
            logging.info(f"crypto not in account.favorite_cryptos")
            # Check if already in favorites
            if crypto not in account.favorite_cryptos:
                logging.info(f"!222")
                account.favorite_cryptos.append(crypto)
                db.commit()
                logging.info(f"Added {symbol} to favorites for {platform_id}")
                return True
            
            return False
        except Exception as e:
            logging.error(f"Error adding favorite: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @staticmethod
    def remove_favorite(platform: PlatformType, platform_id: str, symbol: str) -> bool:
        """Remove a cryptocurrency from user's favorites."""
        db = SessionLocal()
        try:
            account = db.query(Account).filter(
                Account.platform == platform,
                Account.platformId == str(platform_id)
            ).first()
            
            if not account:
                return False
            
            crypto = db.query(Cryptocurrency).filter(
                Cryptocurrency.symbol == symbol.upper()
            ).first()
            
            if not crypto:
                return False
            
            if crypto in account.favorite_cryptos:
                account.favorite_cryptos.remove(crypto)
                db.commit()
                return True
            
            return False
        except Exception as e:
            logging.error(f"Error removing favorite: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @staticmethod
    def get_favorites(platform: PlatformType, platform_id: str) -> list:
        """Get user's favorite cryptocurrencies."""
        db = SessionLocal()
        try:
            account = db.query(Account).filter(
                Account.platform == platform,
                Account.platformId == str(platform_id)
            ).first()
            
            if not account:
                return []
            
            return account.favorite_cryptos
        except Exception as e:
            logging.error(f"Error getting favorites: {e}")
            return []
        finally:
            db.close()


class CryptocurrencyService:
    
    @staticmethod
    def cryptocurrencies_exist() -> bool:
        db = SessionLocal()
        try:
            count = db.query(Cryptocurrency).count()
            return count > 0
        except Exception as e:
            logging.error(f"Error checking if cryptocurrencies exist: {e}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def crypto_exists(identifier: str) -> bool:
        db = SessionLocal()
        try:
            crypto = db.query(Cryptocurrency).filter(
                (Cryptocurrency.symbol == identifier.upper()) |
                (Cryptocurrency.fullName == identifier)
            ).first()
            exists = crypto is not None         
            return exists
        except Exception as e:
            logging.error(f"Error checking if cryptocurrency exists: {e}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def store_cryptocurrencies(crypto_currencies: list[Coin]) -> bool:
        db = SessionLocal()
        try:
            added_count = 0
            for crypto in crypto_currencies:
                # TODO: Improve efficiency
                existing_crypto = db.query(Cryptocurrency).filter(
                    Cryptocurrency.symbol == crypto.symbol.upper()
                ).first()
                if not existing_crypto:
                    crypto = Cryptocurrency(
                        symbol=crypto.symbol.upper(),
                        fullName=crypto.name
                    )
                    db.add(crypto)
                    added_count += 1
            
            if added_count > 0:
                db.commit()
                logging.info(f"Successfully stored {added_count} new cryptocurrencies in database")
                return True
            else:
                logging.info("All cryptocurrencies already exist in database")
                return True
                
        except Exception as e:
            logging.error(f"Error storing cryptocurrencies: {e}")
            db.rollback()
            return False
        finally:
            db.close()
