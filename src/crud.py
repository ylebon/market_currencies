import models
import schemas
from sqlalchemy.orm import Session


def get_asset(db: Session, asset_id: int):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()


def get_asset_by_name(db: Session, name: str):
    return db.query(models.Asset).filter(models.Asset.name == name).first()


def get_assets(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Asset).offset(skip).limit(limit).all()


def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(name=asset.name.upper(), description=asset.description)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def get_exchange(db: Session, exchange_id: int):
    return db.query(models.Exchange).filter(models.Exchange.id == exchange_id).first()


def get_exchange_by_name(db: Session, name: str):
    return db.query(models.Exchange).filter(models.Exchange.name == name).first()


def get_exchanges(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Exchange).offset(skip).limit(limit).all()


def create_exchange(db: Session, exchange: schemas.ExchangeCreate):
    db_exchange = models.Exchange(name=exchange.name.upper(), description=exchange.description)
    db.add(db_exchange)
    db.commit()
    db.refresh(db_exchange)
    return db_exchange


def create_instrument(db: Session, instrument: schemas.InstrumentCreate, base_id: int, quote_id: int):
    db_instrument = models.Instrument(symbol=instrument.symbol.upper(), base_id=base_id, quote_id=quote_id)
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument


def create_exchange_instrument(db: Session, exchange_id: int, instrument_id: int,
                               instrument: schemas.ExchangeInstrumentCreate):
    db_exchange_instrument = models.ExchangeInstrument(
        exchange_id=exchange_id,
        instrument_id=instrument_id,
        exchange_code=instrument.exchange_code,
        min_qty=instrument.min_qty,
        max_qty=instrument.max_qty,
        step_qty=instrument.step_qty,
        min_price=instrument.min_price,
        max_price=instrument.max_price,
        step_price=instrument.step_price,
        pip=instrument.pip
    )
    db.add(db_exchange_instrument)
    db.commit()
    db.refresh(db_exchange_instrument)
    return db_exchange_instrument


def get_instrument_by_symbol(db: Session, symbol: str):
    return db.query(models.Instrument).filter(models.Instrument.symbol == symbol).first()


def get_exchange_instrument_by_symbol(db: Session, exchange: str, symbol: str):
    return db.query(models.ExchangeInstrument).filter(models.ExchangeInstrument.symbol == symbol).first()


def get_exchange_instruments(db: Session, exchange_id: int, skip: int = 0, limit: int = 1000):
    results = db.query(models.ExchangeInstrument).filter(models.ExchangeInstrument.exchange_id == exchange_id).offset(
        skip).limit(limit).all()
    return results
