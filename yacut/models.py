from datetime import datetime
import random

from . import db
from settings import LINK_SYMBOLS


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(2048), nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    @classmethod
    def get_short_url(cls, length=6):
        short_url = ''.join(random.choices(LINK_SYMBOLS, k=length))
        return short_url
