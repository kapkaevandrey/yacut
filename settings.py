import os
import string

LINK_SYMBOLS = (string.ascii_uppercase +
                string.ascii_lowercase +
                string.digits)
DEFAULT_LENGTH_LINK = 6


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
