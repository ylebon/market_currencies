import requests

URL = "https://www.okex.com/api/spot/v3/instruments"
EXCHANGE = "OKEX"


def load():
    """
    Load OKEX instruments

    """

    instruments = list()
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}).json()

    for x in response:
        instrument = dict(exchange=EXCHANGE.lower())
        instrument['exchange_code'] = x['instrument_id']
        instrument['symbol'] = x["base_currency"] + "_" + x["quote_currency"]

        instrument['min_qty'] = x['min_size']
        instrument['max_qty'] = None
        instrument['step_qty'] = x['size_increment']

        instrument['min_price'] = None
        instrument['max_price'] = None
        instrument['step_price'] = x['tick_size']

        instruments.append(instrument)

    return instruments


if __name__ == "__main__":
    print(load())
