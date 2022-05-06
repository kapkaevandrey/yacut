from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import LINK_MATCHING_PATTERN, MAX_LENGTH_LINK, MAX_LENGTH_URL


class UrlMapForm(FlaskForm):
    original = URLField(
        'Ссылка для сокращения',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, MAX_LENGTH_URL, message='Недопустимая длинна ссылки'),
            URL(message='Не корректный адрес'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                1,
                MAX_LENGTH_LINK,
                message='Длинна сслыки не должна превышать 16 символов'
            ),
            Regexp(
                LINK_MATCHING_PATTERN,
                message='Ссылка должна содержать только цифры и'
                        'символы латинского алфавита'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
