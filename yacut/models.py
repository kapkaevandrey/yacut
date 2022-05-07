import random
from datetime import datetime

from settings import (
    DEFAULT_LENGTH_SHORT_PATH, GENERATION_ATTEMPTS, PATH_MATCHING_PATTERN,
    PATH_SYMBOLS, MAX_LENGTH_SHORT_PATH, MAX_LENGTH_URL
)
from . import db
from .error_handlers import InvalidAPIUsageError


class URL_map(db.Model):  # Именно такое имя заложено в тесте test_database.py
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_URL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_PATH), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    @classmethod
    def create(cls, **data):
        if not data['short']:
            data['short'] = URL_map.get_unique_short()
        url_map = URL_map(**data)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @classmethod
    def get_unique_short(cls):
        for _ in range(GENERATION_ATTEMPTS):
            short_link = ''.join(
                random.choices(PATH_SYMBOLS, k=DEFAULT_LENGTH_SHORT_PATH)
            )
            if URL_map.is_valid_short(short_link, "in"):
                return short_link
        raise ValueError("Не удалось сгенерировать ссылку")

    @classmethod
    def is_valid_short(
            cls, short: str,
            rules='re in max',
            exception=False
    ):
        if 'max' in rules and len(short) > MAX_LENGTH_SHORT_PATH:
            if exception:
                raise InvalidAPIUsageError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            return False
        if 're' in rules and not PATH_MATCHING_PATTERN.match(short):
            if exception:
                raise InvalidAPIUsageError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            return False
        if ('in' in rules and
                cls.query.filter_by(short=short).first() is not None):
            if exception:
                raise InvalidAPIUsageError(f'Имя "{short}" уже занято.')
            return False
        return True
