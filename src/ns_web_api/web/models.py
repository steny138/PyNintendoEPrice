# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql.base import UUID
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    nsuid = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    name_tw = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    name_jp = db.Column(db.String(100))
    category = db.Column(db.String(100))
    cover = db.Column(db.String(300))
    players = db.Column(db.String(30))
    onsale_jp = db.Column(db.Boolean)
    currency_jp = db.Column(db.String(10))
    eprice_jp = db.Column(db.Float(53))
    onsale_us = db.Column(db.Boolean)
    currency_us = db.Column(db.String(10))
    eprice_us = db.Column(db.Float(53))
    onsale_ca = db.Column(db.Boolean)
    currency_ca = db.Column(db.String(10))
    eprice_ca = db.Column(db.Float(53))
    onsale_za = db.Column(db.Boolean)
    currency_za = db.Column(db.String(10))
    eprice_za = db.Column(db.Float(53))
    onsale_nz = db.Column(db.Boolean)
    currency_nz = db.Column(db.String(10))
    eprice_nz = db.Column(db.Float(53))
    onsale_nl = db.Column(db.Boolean)
    currency_nl = db.Column(db.String(10))
    eprice_nl = db.Column(db.Float(53))
    onsale_mx = db.Column(db.Boolean)
    currency_mx = db.Column(db.String(10))
    eprice_mx = db.Column(db.Float(53))
    onsale_it = db.Column(db.Boolean)
    currency_it = db.Column(db.String(10))
    eprice_it = db.Column(db.Float(53))
    onsale_ch = db.Column(db.Boolean)
    currency_ch = db.Column(db.String(10))
    eprice_ch = db.Column(db.Float(53))
    onsale_au = db.Column(db.Boolean)
    currency_au = db.Column(db.String(10))
    eprice_au = db.Column(db.Float(53))
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
