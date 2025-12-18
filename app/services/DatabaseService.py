"""
DEPRECATED: This file is kept for backward compatibility.
Use the new service modules instead:
- app.services.account_service.AccountService
- app.services.favorite_service.FavoriteService
- app.services.cryptocurrency_service.CryptocurrencyService
"""

# Re-export for backward compatibility
from app.services.account_service import AccountService
from app.services.favorite_service import FavoriteService
from app.services.cryptocurrency_service import CryptocurrencyService

__all__ = ['AccountService', 'FavoriteService', 'CryptocurrencyService']
