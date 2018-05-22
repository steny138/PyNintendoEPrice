# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ns_web_crawler.models.game_eprice_model import GameEPriceModel
from ns_web_crawler.models.country_mapping_currency_model import CountryCurrencyModel

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('postgresql://admin:1qaz2wsx@localhost/')
# engine = create_engine('postgres://yjvykvqlwlrmsn:9bd81b536b37f210a5387d64767b3db664f05f396c61b1f986b0ecbb4b2bd703@ec2-54-243-213-188.compute-1.amazonaws.com:5432/d58g9qj3e7kf68')

GameEPriceModel.metadata.create_all(engine)
CountryCurrencyModel.metadata.create_all(engine)

#返回数据库会话
def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()

    # session. create extension uuid-ossp
    return session