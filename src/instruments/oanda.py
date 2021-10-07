import json
import os

# instruments file
INSTRUMENTS_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'oanda_instruments.json')
)

EXCHANGE = "OANDA"


def load():
    """
    Load OANDA instruments

    """

    instruments = list()

    # open instruments file
    with open(INSTRUMENTS_FILE) as f:
        response = json.load(f)
        for x in response['instruments']:
            instrument = dict(exchange=EXCHANGE.lower())
            instrument['exchange_code'] = x["instrument"]
            instrument['symbol'] = x["instrument"]

            instrument['min_qty'] = float(0)
            instrument['max_qty'] = float(x.get('maxTradeUnits', 0))
            instrument['step_qty'] = float(0)
            instrument['pip'] = float(x['pip'])

            instruments.append(instrument)

    return instruments


if __name__ == "__main__":
    print(load())
