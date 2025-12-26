from pytest import Session
from app.repository.account_repository import AccountRepository
from app.repository.cryptocurrency_repository import CryptocurrencyRepository
from app.repository.favorite_repository import FavoriteRepository
from sqlalchemy.orm import sessionmaker


class BotService():

    def __init__(
            self,
            session_factory: sessionmaker[Session],
            account_repository: AccountRepository,
            favorite_repository: FavoriteRepository,
            cryptocurrency_repository: CryptocurrencyRepository,
    ):
        self._session_factory = session_factory
        self._account_repository = account_repository
        self._favorite_repository = favorite_repository
        self._cryptocurrency_repository = cryptocurrency_repository

        
    def is_crypto_empty(self) -> bool:
        with self._session_factory.get_session() as db:
            return self._cryptocurrency_repository.is_empty_wo_session(db)
        