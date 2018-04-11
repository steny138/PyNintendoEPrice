# coding: utf-8
from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql.base import UUID
from flask_sqlalchemy import SQLAlchemy
from settings import db


class CountryCurrency(db.Model):
    __tablename__ = 'country_currency'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    country = db.Column(db.String(10), nullable=False)
    country_name = db.Column(db.String(100))
    currency = db.Column(db.String(10), nullable=False)
    currency_name = db.Column(db.String(100))
    symbol = db.Column(db.String(30))
    unit = db.Column(db.String(30))
    digit = db.Column(db.String(30))
    last_updated = db.Column(db.DateTime, nullable=False)


class Eprice(db.Model):
    __tablename__ = 'eprices'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(100))
    name_tw = db.Column(db.String(100))
    country = db.Column(db.String(10), nullable=False)
    eprice = db.Column(db.Float(53), nullable=False)
    create_time = db.Column(db.String(500), nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)


class Rate(db.Model):
    __tablename__ = 'rates'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    key = db.Column(db.String(10), nullable=False)
    base_currency = db.Column(db.String(10), nullable=False)
    target_currency = db.Column(db.String(10), nullable=False)
    rate = db.Column(db.Float(53), nullable=False)
    use_date = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
