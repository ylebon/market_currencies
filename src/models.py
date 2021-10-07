from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class Asset(Base):
    __tablename__ = "Assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, unique=True, index=True)


class Exchange(Base):
    __tablename__ = "Exchanges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, unique=True, index=True)
    instruments = relationship("ExchangeInstrument", order_by="ExchangeInstrument.id")


class Instrument(Base):
    __tablename__ = "Instruments"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    base_id = Column(Integer, ForeignKey('Assets.id'))
    quote_id = Column(Integer, ForeignKey('Assets.id'))

    base_rel = relationship('Asset', foreign_keys=base_id)
    quote_rel = relationship('Asset', foreign_keys=quote_id)

    @property
    def base(self):
        return self.base_rel.name

    @property
    def quote(self):
        return self.quote_rel.name


class ExchangeInstrument(Base):
    __tablename__ = "ExchangeInstruments"

    id = Column(Integer, primary_key=True, index=True)
    exchange_id = Column(Integer, ForeignKey('Exchanges.id'), nullable=False)
    instrument_id = Column(Integer, ForeignKey('Instruments.id'), nullable=False)
    exchange_code = Column(String, unique=False, nullable=False)
    min_qty = Column(Float)
    max_qty = Column(Float)
    step_qty = Column(Float)
    min_price = Column(Float)
    max_price = Column(Float)
    step_price = Column(Float)
    pip = Column(Float)

    exchange_rel = relationship('Exchange', foreign_keys=exchange_id)
    instrument_rel = relationship('Instrument', foreign_keys=instrument_id)

    @property
    def symbol(self):
        return self.instrument_rel.symbol

    @property
    def exchange(self):
        return self.exchange_rel.name

    @property
    def base(self):
        return self.instrument_rel.base

    @property
    def quote(self):
        return self.instrument_rel.quote
