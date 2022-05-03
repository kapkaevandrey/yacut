from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import (
    Length, DataRequired, Optional, Regexp, URL,
)


class UrlMapForm(FlaskForm):
    original_link = URLField(
        'Ссылка для сокращения',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(2, 2048),
            URL(message='Не корректный адрес'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16),
            Regexp(
                r'^[A-Za-z1-9]+$',
                message='Ссылка должна содержать только цифры и'
                        'символы латинского алфавита'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Создать')

