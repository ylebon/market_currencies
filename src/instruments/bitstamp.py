import requests

URL = "https://www.bitstamp.net/api/v2/trading-pairs-info"
EXCHANGE = "BITSTAMP"


def load():
    """
    Load BITSTAMP instruments

    """

    instruments = list()
    response = requests.get(URL).json()

    for x in response:
        instrument = dict(exchange=EXCHANGE.lower())
        instrument['exchange_code'] = x['name']
        instrument['symbol'] = x['name'].replace('/', '_')
        instrument['min_qty'] = float(x['minimum_order'].split(' ')[0])
        instrument['max_qty'] = 0
        instrument['step_qty'] = float(float(1) / float(10 ** float(x['counter_decimals'])))
        instruments.append(instrument)

    return instruments


if __name__ == "__main__":
    print(load())
