from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsageError
from .models import URL_map


@app.route('/api/id/<string:custom_id>/', methods=['GET'])
def get_origin_url(custom_id):
    url_map = URL_map.query.filter_by(short=custom_id).first()
    if url_map is None:
        raise InvalidAPIUsageError(
            'Указанный id не найден', HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsageError('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsageError('"url" является обязательным полем!')
    if 'custom_id' in data and data['custom_id']:
        URL_map.is_valid_short(data['custom_id'], exception=True)
    url_map = URL_map.create(original=data['url'], short=data.get('custom_id'))
    return jsonify(
        {'url': url_map.original,
         'short_link': url_for(
             'short_id_view',
             custom_id=url_map.short,
             _external=True
         )}
    ), HTTPStatus.CREATED
