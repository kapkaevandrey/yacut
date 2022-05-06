import os
import string
import re

DEFAULT_LENGTH = 6
LINK_SYMBOLS = (string.ascii_uppercase +
                string.ascii_lowercase +
                string.digits + '\]\[')
LINK_MATCHING_PATTERN = re.compile(rf'^[{LINK_SYMBOLS}]+$')
MAX_LENGTH_LINK = 16
MAX_LENGTH_URL = 2048


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 'sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
