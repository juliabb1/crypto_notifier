from app.repository.cryptocurrency_repository import CryptocurrencyRepository
from app.repository.account_repository import AccountRepository
from app.repository.favorite_repository import FavoriteRepository

class DataService:
    def __init__(
            self, 
            account_repository: AccountRepository, 
            favorite_repository: FavoriteRepository, 
            cryptocurrency_repository: CryptocurrencyRepository):
        self.account_repository = account_repository
        self.favorite_repository = favorite_repository
        self.cryptocurrency_repository = cryptocurrency_repository

    