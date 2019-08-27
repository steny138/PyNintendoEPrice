import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String,Integer,DateTime,Float,Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

import datetime
class GameModel(Base):
    __tablename__ = 'games'
    """
    eprice: 基準的遊戲價格
    country: 基準的遊戲區域
    currency: 基準的遊戲幣別

    onsale_[country]: 該遊戲在該國家是否特價
    currency_[country]: 該遊戲在該國家的與基準遊戲幣別
    eprice_[country]: 該遊戲在該國家的售價

    countries : ['AU', 'CA', 'CH', 'IT', 'MX', 'NL', 'NZ', 'US', 'ZA']
    """
    id                  =   Column(UUID(as_uuid=True),primary_key=True)
    name                =   Column(String(100),nullable=True)
    name_tw             =   Column(String(100),nullable=True)
    name_en             =   Column(String(100),nullable=True)
    name_jp             =   Column(String(100),nullable=True)

    eprice              =   Column(Float,nullable=False)
    country             =   Column(String(10),nullable=False)
    currency            =   Column(String(10),nullable=False)

    onsale_jp           =   Column(Boolean, default=False)
    currency_jp         =   Column(String(10), nullable=False)
    eprice_jp           =   Column(Float, nullable=False)

    onsale_us           =   Column(Boolean,default=False)
    currency_us         =   Column(String(10),nullable=False)
    eprice_us           =   Column(Float,nullable=False)

    onsale_ca           =   Column(Boolean,default=False)
    currency_ca         =   Column(String(10),nullable=False)
    eprice_ca           =   Column(Float,nullable=False)

    onsale_za           =   Column(Boolean,default=False)
    currency_za         =   Column(String(10),nullable=False)
    eprice_za           =   Column(Float,nullable=False)

    onsale_nz           =   Column(Boolean,default=False)
    currency_nz         =   Column(String(10),nullable=False)
    eprice_nz           =   Column(Float,nullable=False)

    onsale_nl           =   Column(Boolean,default=False)
    currency_nl         =   Column(String(10),nullable=False)
    eprice_nl           =   Column(Float,nullable=False)

    onsale_mx           =   Column(Boolean,default=False)
    currency_mx         =   Column(String(10),nullable=False)
    eprice_mx           =   Column(Float,nullable=False)

    onsale_it           =   Column(Boolean,default=False)
    currency_it         =   Column(String(10),nullable=False)
    eprice_it           =   Column(Float,nullable=False)

    onsale_ch           =   Column(Boolean,default=False)
    currency_ch         =   Column(String(10),nullable=False)
    eprice_ch           =   Column(Float,nullable=False)

    onsale_au           =   Column(Boolean,default=False)
    currency_au         =   Column(String(10),nullable=False)
    eprice_au           =   Column(Float,nullable=False)

    create_time         =   Column(String(500), nullable=False)
    update_time         =   Column(DateTime,nullable=False)

    def __init__(self,id,name,country,eprice,currency=None,name_tw=None,create_time=None,update_time=None):
        self.id                     =   id
        self.name                   =   name
        self.name_tw                =   name_tw
        self.country                =   country
        self.eprice                 =   eprice
        self.currency               =   currency
        self.create_time            =   create_time
        self.update_time            =   update_time

        if self.create_time is None:
            self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.update_time is None:
            self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
