import os
import re
import string

DEFAULT_LENGTH_SHORT_PATH = 6
PATH_SYMBOLS = (string.ascii_uppercase +
                string.ascii_lowercase +
                string.digits)
PATH_MATCHING_PATTERN = re.compile(rf'^[{PATH_SYMBOLS}]+$')
MAX_LENGTH_SHORT_PATH = 16
MAX_LENGTH_URL = 2048


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 'sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
