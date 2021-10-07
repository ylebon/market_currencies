from typing import Optional

from pydantic import BaseModel, constr


class AssetBase(BaseModel):
    name: str
    description: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class Asset(AssetBase):
    id: int

    class Config:
        orm_mode = True


class ExchangeBase(BaseModel):
    name: str
    description: Optional[str] = None


class ExchangeCreate(ExchangeBase):
    pass


class Exchange(ExchangeBase):
    id: int

    class Config:
        orm_mode = True


class InstrumentBase(BaseModel):
    symbol: constr(regex=r"^.*_.*$")


class InstrumentCreate(InstrumentBase):
    pass


class Instrument(InstrumentBase):
    id: int
    base_id: int
    quote_id: int

    class Config:
        orm_mode = True


class ExchangeInstrumentBase(BaseModel):
    symbol: str
    exchange: str
    exchange_code: str
    min_qty: Optional[float] = None
    max_qty: Optional[float] = None
    step_qty: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    step_price: Optional[float] = None
    pip: Optional[float] = None


class ExchangeInstrumentCreate(ExchangeInstrumentBase):
    pass


class ExchangeInstrument(ExchangeInstrumentBase):
    id: int
    exchange_id: int
    instrument_id: int
    exchange_code: str
    base: str
    quote: str

    class Config:
        orm_mode = True
