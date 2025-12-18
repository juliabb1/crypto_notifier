import httpx
import json
from app.models import Coin


class DataService:
    BASE_URL = "https://api.coingecko.com/api/v3/coins"

    @staticmethod
    async def list_top_crypto_currencies(amount: int) -> list[Coin]:
        params = {
                'vs_currency': 'eur',
                'order': 'market_cap',
                'per_page': amount,
                'page': 1
        }
        url = f"{DataService.BASE_URL}/markets"
        async with httpx.AsyncClient() as client:
            r = await client.get(url, params=params)
        json_obj = json.loads(r.text)
        coins = [
            Coin(**coin_data)
            for coin_data in json_obj
        ]
        return coins
    
    @staticmethod
    async def get_index(fullName: str) -> float:
        # Use full ID if short code is provided, otherwise use the input as-is
        # CHeck if index = short or long, if short, get fullName
        #  i guess i needthe short one
        # coin_id = SYMBOL_TO_ID.get(index.lower(), index.lower())
        coin_id = "btc"
        params = {
            'vs_currency': 'eur'
        }
        url = f"{DataService.BASE_URL}/{coin_id}"
        async with httpx.AsyncClient() as client:
            r = await client.get(url, params=params)
        json_obj = json.loads(r.text)
        result = json_obj.get('market_data', {}).get('current_price', {}).get('eur')
        return result