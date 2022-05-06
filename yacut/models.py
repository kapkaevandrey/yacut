import random
import re
from datetime import datetime

from settings import (
    DEFAULT_LENGTH, LINK_MATCHING_PATTERN,
    LINK_SYMBOLS, MAX_LENGTH_LINK, MAX_LENGTH_URL,
)

from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_URL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_LINK), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['custom_id']

    @classmethod
    def is_valid_short_id(cls, short_id: str, *rules):
        if 'max' in rules and len(short_id) > MAX_LENGTH_LINK:
            return (
                False,
                f'Указано недопустимое имя для короткой ссылки - {short_id}'
                f'Максимальная длинна ссылки {MAX_LENGTH_LINK}.'
            )
        if 're' in rules and not LINK_MATCHING_PATTERN.match(short_id):
            return (
                False,
                f'Указано недопустимое имя для короткой ссылки - {short_id}'
                f'Используйте только цифры и буквы латинского алфавита.'
            )
        if 'is' in rules and cls.query.filter_by(short=short_id).first() is not None:
            return False, f'Имя "{short_id}" уже занято.'
        return True, ""

    @classmethod
    def get_unique_short_id(cls):
        short_link = ''
        while cls.query.filter_by(short=short_link).first() is not None:
            short_link = ''.join(
                random.choices(LINK_SYMBOLS, k=DEFAULT_LENGTH)
            )
        return short_link
