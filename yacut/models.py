import random
from datetime import datetime

from settings import (
    DEFAULT_LENGTH_SHORT_PATH, GENERATION_ATTEMPTS, PATH_MATCHING_PATTERN,
    PATH_SYMBOLS, MAX_LENGTH_SHORT_PATH, MAX_LENGTH_URL
)
from . import db
from .error_handlers import InvalidAPIUsageError


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_URL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_PATH), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def from_dict(self, data):
        self.original = data['original']
        self.short = data['short']

    @classmethod
    def is_valid_short_id(
            cls, short_id: str,
            rules='re in max',
            exception=False
    ):
        if 'max' in rules and len(short_id) > MAX_LENGTH_SHORT_PATH:
            if exception:
                raise InvalidAPIUsageError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            return False
        if 're' in rules and not PATH_MATCHING_PATTERN.match(short_id):
            if exception:
                raise InvalidAPIUsageError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            return False
        if ('in' in rules and
                cls.query.filter_by(short=short_id).first() is not None):
            if exception:
                raise InvalidAPIUsageError(f'Имя "{short_id}" уже занято.')
            return False
        return True

    @classmethod
    def get_unique_short_id(cls):
        counter = 0
        while counter <= GENERATION_ATTEMPTS:
            short_link = ''.join(
                random.choices(PATH_SYMBOLS, k=DEFAULT_LENGTH_SHORT_PATH)
            )
            if URL_map.is_valid_short_id(short_link, "in"):
                return short_link
            counter += 1
        raise ValueError("Не удалось сгенерировать ссылку")

    @classmethod
    def create_and_commit(cls, **data):
        if not data['short']:
            data['short'] = URL_map.get_unique_short_id()
        url_map = URL_map()
        url_map.from_dict(data)
        db.session.add(url_map)
        db.session.commit()
        return url_map
