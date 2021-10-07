import requests

URL = "https://poloniex.com/public?command=returnTicker"
EXCHANGE = "POLONIEX"

STATIC_INSTRUMENTS = [
    "USDT_LINKBEAR",
    "USDT_LINKBULL"
]


def load():
    """
    Load POLONIEX instruments

    """

    instruments = list()

    for x in STATIC_INSTRUMENTS:
        instrument = dict(exchange=EXCHANGE.lower())
        instrument['exchange_code'] = x
        instrument['symbol'] = x.split("_")[1] + "_" + x.split("_")[0]
        instrument['min_qty'] = None
        instrument['max_qty'] = None
        instrument['step_qty'] = None

        instrument['min_price'] = None
        instrument['max_price'] = None
        instrument['step_price'] = None

        instruments.append(instrument)

    response = requests.get(URL).json()
    for x in response:
        instrument = dict(exchange=EXCHANGE.lower())
        instrument['exchange_code'] = x
        instrument['symbol'] = x.split("_")[1] + "_" + x.split("_")[0]

        instrument['min_qty'] = None
        instrument['max_qty'] = None
        instrument['step_qty'] = None

        instrument['min_price'] = None
        instrument['max_price'] = None
        instrument['step_price'] = None

        instruments.append(instrument)

    return instruments


if __name__ == "__main__":
    print(load())
