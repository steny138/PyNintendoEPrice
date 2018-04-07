import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String,Integer,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

import datetime

class CountryCurrencyModel(Base):
    __tablename__ = 'country_currency'

    id              =   Column(UUID(as_uuid=True),
                            primary_key=True)
    country         =   Column(String(10),nullable=False)
    country_name    =   Column(String(100),nullable=True)
    currency        =   Column(String(10),nullable=False)
    currency_name   =   Column(String(100),nullable=True)
    symbol          =   Column(String(30),nullable=True)
    unit            =   Column(String(30),nullable=True)
    digit           =   Column(String(30),nullable=True)
    last_updated    =   Column(DateTime,nullable=False)

    def __init__(self,
                    id,
                    country,
                    currency,
                    country_name=None,
                    currency_name=None,
                    symbol=None,
                    unit=None,
                    digit=None,
                    last_updated=None):
        self.id             =   id
        self.country        =   country
        self.currency       =   currency
        self.country_name   =   country_name
        self.currency_name  =   currency_name
        self.symbol         =   symbol
        self.unit           =   unit
        self.digit          =   digit
        self.last_updated   =   last_updated

        if self.last_updated is None:
            self.last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")