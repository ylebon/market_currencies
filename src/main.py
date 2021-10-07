from typing import List

import crud
import models
import schemas
import updater
from config import settings
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from instruments import binance, oanda, bitstamp, cex, okex, poloniex
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Blincks Referencedata', openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# ASSET
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    updater.start()


@app.post("/assets/", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = crud.get_asset_by_name(db, name=asset.name)
    if db_asset:
        raise HTTPException(status_code=400, detail="Asset already registered")
    return crud.create_asset(db=db, asset=asset)


@app.get("/assets/", response_model=List[schemas.Asset])
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    assets = crud.get_assets(db, skip=skip, limit=limit)
    return assets


@app.get("/assets/{asset_id}", response_model=schemas.Asset)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset


# EXCHANGE

@app.post("/exchanges/", response_model=schemas.Exchange)
def create_exchange(exchange: schemas.ExchangeCreate, db: Session = Depends(get_db)):
    db_exchange = crud.get_exchange_by_name(db, name=exchange.name)
    if db_exchange:
        raise HTTPException(status_code=400, detail="Exchange already registered")
    return crud.create_exchange(db=db, exchange=exchange)


@app.get("/exchanges/", response_model=List[schemas.Exchange])
def read_exchanges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    exchanges = crud.get_exchanges(db, skip=skip, limit=limit)
    return exchanges


@app.get("/exchanges/{exchange_id}", response_model=schemas.Exchange)
def read_exchange(exchange_id: int, db: Session = Depends(get_db)):
    db_exchange = crud.get_exchange(db, exchange_id=exchange_id)
    if db_exchange is None:
        raise HTTPException(status_code=404, detail="Exchange not found")
    return db_exchange


# Instrument
@app.post("/instruments/", response_model=schemas.Instrument)
def create_instrument(instrument: schemas.InstrumentCreate, db: Session = Depends(get_db)):
    db_instrument = crud.get_instrument_by_symbol(db, symbol=instrument.symbol)
    if db_instrument:
        raise HTTPException(status_code=400, detail="Instrument already registered")

    base, quote = instrument.symbol.upper().split("_")

    # create asset
    db_base = crud.get_asset_by_name(db, name=base)
    if not db_base:
        db_base = crud.create_asset(db=db, asset=schemas.AssetCreate(name=base))

    # quote
    db_quote = crud.get_asset_by_name(db, name=quote)
    if not db_quote:
        db_quote = crud.create_asset(db=db, asset=schemas.AssetCreate(name=quote))

    return crud.create_instrument(db=db, instrument=instrument, base_id=db_base.id, quote_id=db_quote.id)


@app.post("/exchanges/{exchange}/instruments", response_model=List[schemas.ExchangeInstrument])
def create_exchange_instrument(exchange: str, db: Session = Depends(get_db)):
    # db exchange
    db_exchange = crud.get_exchange_by_name(db, name=exchange.upper())
    if not db_exchange:
        db_exchange = crud.create_exchange(db=db, exchange=schemas.ExchangeCreate(name=exchange))

    if exchange.upper() == 'BINANCE':
        instruments = binance.load()
    elif exchange.upper() == 'OANDA':
        instruments = oanda.load()
    elif exchange.upper() == 'BITSTAMP':
        instruments = bitstamp.load()
    elif exchange.upper() == 'CEX':
        instruments = cex.load()
    elif exchange.upper() == 'OKEX':
        instruments = okex.load()
    elif exchange.upper() == 'POLONIEX':
        instruments = poloniex.load()
    else:
        raise HTTPException(status_code=400, detail="Exchange instruments script not implemented")

    response = list()
    for instrument in instruments:
        db_instrument = crud.get_instrument_by_symbol(db, symbol=instrument['symbol'])
        if not db_instrument:
            base, quote = instrument['symbol'].upper().split("_")

            # create base asset
            db_base = crud.get_asset_by_name(db, name=base)
            if not db_base:
                db_base = crud.create_asset(db=db, asset=schemas.AssetCreate(name=base))

            # create quote asset
            db_quote = crud.get_asset_by_name(db, name=quote)
            if not db_quote:
                db_quote = crud.create_asset(db=db, asset=schemas.AssetCreate(name=quote))

            db_instrument = crud.create_instrument(db=db,
                                                   instrument=schemas.InstrumentCreate(symbol=instrument['symbol']),
                                                   base_id=db_base.id, quote_id=db_quote.id)

        r = crud.create_exchange_instrument(
            db=db,
            instrument=schemas.ExchangeInstrumentCreate(**instrument),
            exchange_id=db_exchange.id,
            instrument_id=db_instrument.id
        )

        response.append(r)

    return response


@app.get("/exchanges/{exchange}/instruments", response_model=List[schemas.ExchangeInstrument])
def read_exchanges(exchange: str, skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    # db exchange
    db_exchange = crud.get_exchange_by_name(db, name=exchange.upper())
    if not db_exchange:
        raise HTTPException(status_code=400, detail="Exchange not found")
    exchange_instruments = crud.get_exchange_instruments(db, exchange_id=db_exchange.id, skip=skip, limit=limit)
    return exchange_instruments
