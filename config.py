import os

class Config:
    # QUART_DB_DATABASE_URL = 'sqlite:///../database/inventory2.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super_secret_key'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True