# config do banco de dados
import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://adminautocert:craniovaldo1@localhost:5432/autocert')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
