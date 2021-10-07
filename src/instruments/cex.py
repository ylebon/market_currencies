import requests

URL = "https://cex.io/api/currency_limits"
EXCHANGE = "CEX"


def load():
    """
    Load CEX instruments

    """

    instruments = list()
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}).json()

    for x in response["data"]["pairs"]:
        instrument = dict(exchange=EXCHANGE.lower())
        instrument['exchange_code'] = x["symbol1"] + "_" + x["symbol2"]
        instrument['symbol'] = x["symbol1"] + "_" + x["symbol2"]

        instrument['min_qty'] = x['minLotSize']
        instrument['max_qty'] = x['maxLotSize']
        instrument['step_qty'] = None

        instrument['min_price'] = x['minPrice']
        instrument['max_price'] = x['maxPrice']
        instrument['step_price'] = None

        instruments.append(instrument)

    return instruments


if __name__ == "__main__":
    print(load())
