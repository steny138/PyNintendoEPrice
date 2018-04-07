import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String,Integer,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

import datetime
class GameEPriceModel(Base):
    __tablename__ = 'eprices'

    id          =   Column(UUID(as_uuid=True),
                        primary_key=True)
    name        =   Column(String(100),nullable=True)
    name_tw     =   Column(String(100),nullable=True)
    country     =   Column(String(10),nullable=False)
    eprice      =   Column(Float,nullable=False)
    create_time =   Column(String(500), nullable=False)
    update_time =   Column(DateTime,nullable=False)

    def __init__(self,id,name,country,eprice,name_tw=None,create_time=None,update_time=None):
        self.id             =   id
        self.name           =   name
        self.country        =   country
        self.eprice         =   eprice
        self.name_tw        =   name_tw
        self.create_time    =   create_time
        self.update_time    =   update_time

        if self.create_time is None:
            self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.update_time is None:
            self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
