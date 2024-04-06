import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'database', 'inventory.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

