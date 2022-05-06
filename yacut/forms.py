from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import (
    MAX_LENGTH_SHORT_PATH, MAX_LENGTH_URL, PATH_MATCHING_PATTERN,
)


class UrlMapForm(FlaskForm):
    original_link = URLField(
        'Ссылка для сокращения',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, MAX_LENGTH_URL, 'Недопустимая длинна URL'),
            URL(message='Не корректный адрес'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, MAX_LENGTH_SHORT_PATH, 'Недопустимая длинна URL'),
            Regexp(
                PATH_MATCHING_PATTERN,
                message='Ссылка должна содержать только цифры и'
                        'символы латинского алфавита'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
