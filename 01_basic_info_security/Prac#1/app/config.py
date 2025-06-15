import os


class Config:
    # Строка подключения к базе напрямую, без .env
    SQLALCHEMY_DATABASE_URI = 'postgresql://bookvault:secret@db:5432/bookvault_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-secret-key'
