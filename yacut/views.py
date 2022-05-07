from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import UrlMapForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if not form.validate_on_submit():
        return render_template('index_short_url.html', form=form)
    custom_id = form.custom_id.data
    if not URL_map.is_valid_short(custom_id, "in"):
        flash(f'Имя {custom_id} уже занято!', 'validation')
        return render_template('index_short_url.html', form=form)
    url_map = URL_map.create(
        original=form.original_link.data,
        short=custom_id
    )
    return render_template('index_short_url.html', form=form, url_map=url_map)


@app.route('/<string:custom_id>', methods=['GET'])
def short_id_view(custom_id):
    url_map = URL_map.query.filter_by(short=custom_id).first()
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
