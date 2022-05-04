import random
import re
from datetime import datetime

from settings import (
    DEFAULT_LENGTH_LINK, LINK_MATCHING_PATTERN,
    LINK_SYMBOLS, MAX_LENGTH_LINK,
)

from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(2048), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_LINK), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']

    @classmethod
    def is_valid_short_id(cls, short_id: str):
        if not (len(short_id) <= MAX_LENGTH_LINK and
                re.match(LINK_MATCHING_PATTERN, short_id)):
            return False, 'Указано недопустимое имя для короткой ссылки'
        if cls.query.filter_by(short=short_id).first() is not None:
            return False, f'Имя "{short_id}" уже занято.'
        return True, ""

    @classmethod
    def get_unique_short_id(cls, length=DEFAULT_LENGTH_LINK):
        short_link = ''.join(
            random.choices(LINK_SYMBOLS, k=DEFAULT_LENGTH_LINK)
        )
        if cls.query.filter_by(short=short_link).first() is None:
            return short_link
        return cls.get_unique_short_id(length=length)
