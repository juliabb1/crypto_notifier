from app.main import list_cryptos
from scripts.init_db import init_db
from scripts.seed_data import seed


def test_list_cryptos():
    init_db()
    seed()
    cryptos = list_cryptos()
    print(cryptos)
    assert any(c.symbol == "BTC" for c in cryptos)


if __name__ == '__main__':
    test_list_cryptos()