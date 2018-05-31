# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ns_web_crawler.models.game_eprice_model import GameEPriceModel
from ns_web_crawler.models.country_mapping_currency_model import CountryCurrencyModel
from ns_web_crawler import settings

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine(settings.DATABASE_URL)

GameEPriceModel.metadata.create_all(engine)
CountryCurrencyModel.metadata.create_all(engine)

#返回数据库会话
def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()

    # session. create extension uuid-ossp
    return session