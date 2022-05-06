import random
from datetime import datetime

from settings import (
    DEFAULT_LENGTH, LINK_MATCHING_PATTERN,
    LINK_SYMBOLS, MAX_LENGTH_SHORT_URL, MAX_LENGTH_URL,
)

from .error_handlers import InvalidAPIUsageError
from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_URL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_URL), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']

    @classmethod
    def is_valid_short_id(cls, short_id: str, rules='re max in', exception=False):
        if 'max' in rules and len(short_id) > MAX_LENGTH_SHORT_URL:
            if exception:
                raise InvalidAPIUsageError(
                    f'Указано недопустимое имя для короткой ссылки'
                )
            return False
        if 're' in rules and not LINK_MATCHING_PATTERN.match(short_id):
            if exception:
                raise InvalidAPIUsageError(
                    f'Указано недопустимое имя для короткой ссылки'
                )
            return False
        if 'in' in rules and cls.query.filter_by(short=short_id).first() is not None:
            if exception:
                raise InvalidAPIUsageError(f'Имя "{short_id}" уже занято.')
            return False
        return True

    @classmethod
    def get_unique_short_id(cls):
        short_link = ''.join(
                random.choices(LINK_SYMBOLS, k=DEFAULT_LENGTH)
            )
        while not cls.is_valid_short_id(short_link, 'in'):
            short_link = ''.join(
                random.choices(LINK_SYMBOLS, k=DEFAULT_LENGTH)
            )
        return short_link
