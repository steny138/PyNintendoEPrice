# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ns_web_crawler.models.game_eprice_model import GameEPriceModel

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('postgresql://admin:1qaz2wsx@localhost/')

GameEPriceModel.metadata.create_all(engine)

#返回数据库会话
def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session