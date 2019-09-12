# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ns_web_crawler import settings
from ns_web_crawler.models.game_model import GameModel

# 創建基礎連結類型:
Base = declarative_base()

# 初始化資料庫連結:
engine = create_engine(settings.DATABASE_URL)

GameModel.metadata.create_all(engine)
# GameEPriceModel.metadata.create_all(engine)
# CountryCurrencyModel.metadata.create_all(engine)

# 建立資料庫連線
def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()

    # session. create extension uuid-ossp
    return session