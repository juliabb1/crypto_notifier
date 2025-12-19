import logging
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from app.models import PlatformType
from app.repository.cryptocurrency_repository import CryptocurrencyRepository
from app.repository.account_repository import AccountRepository
from app.repository.favorite_repository import FavoriteRepository

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

class DataService:
    
    def __init__(
            self, 
            account_repository: AccountRepository, 
            favorite_repository: FavoriteRepository, 
            cryptocurrency_repository: CryptocurrencyRepository):
        self._account_repository = account_repository
        self._favorite_repository = favorite_repository
        self._cryptocurrency_repository = cryptocurrency_repository
    
    def check_account_and_crypto(self, platform: PlatformType, platform_id: str, input_crypto: str) -> bool:
        account = self._account_repository.find_by_platform_and_id(platform, platform_id)
        if account is None:
            account = self._account_repository.create(
                platform=platform,
                platformId=str(platform_id)
            )
        cryptocurrency = self._cryptocurrency_repository.find_by_name_or_symbol(input_crypto)
        if cryptocurrency is None:
            return False
        return True

        

        