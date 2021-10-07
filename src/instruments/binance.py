import requests

URL = "https://api.binance.com/api/v1/exchangeInfo"
EXCHANGE = "BINANCE"


def load():
    """
    Load BINANCE instruments

    """

    instruments = list()
    response = requests.get('https://api.binance.com/api/v1/exchangeInfo').json()

    for x in response['symbols']:
        instrument = dict(exchange=EXCHANGE.lower())
        instrument['exchange_code'] = x["symbol"]
        instrument['symbol'] = x["baseAsset"] + "_" + x["quoteAsset"]

        for filter in x['filters']:
            if filter['filterType'] == 'LOT_SIZE':
                instrument['min_qty'] = float(filter['minQty'])
                instrument['max_qty'] = float(filter['maxQty'])
                instrument['step_qty'] = float(filter['stepSize'])
            elif filter['filterType'] == 'PRICE_FILTER':
                instrument['min_price'] = float(filter['minPrice'])
                instrument['max_price'] = float(filter['maxPrice'])
                instrument['step_price'] = float(filter['tickSize'])
        instruments.append(instrument)

    return instruments


if __name__ == "__main__":
    print(load())
