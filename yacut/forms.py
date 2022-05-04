from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import (
    Length, DataRequired, Optional, Regexp, URL,
)
from settings import LINK_MATCHING_PATTERN, MAX_LENGTH_LINK, MAX_LENGTH_URL


class UrlMapForm(FlaskForm):
    original_link = URLField(
        'Ссылка для сокращения',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(2, MAX_LENGTH_URL),
            URL(message='Не корректный адрес'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, MAX_LENGTH_LINK),
            Regexp(
                LINK_MATCHING_PATTERN,
                message='Ссылка должна содержать только цифры и'
                        'символы латинского алфавита'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Создать')

