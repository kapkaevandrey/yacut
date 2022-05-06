from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import UrlMapForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if not form.validate_on_submit():
        return render_template('index_short_url.html', form=form)
    short_url = form.custom_id.data
    if (short_url and
            URL_map.query.filter_by(short=short_url).first() is not None):
        flash(f'Имя {short_url} уже занято!', 'validation')
        return render_template('index_short_url.html', form=form)
    short_url = URL_map.get_unique_short_id() if not short_url else short_url
    url_map = URL_map(original=form.original.data, short=short_url)
    db.session.add(url_map)
    db.session.commit()
    return render_template('index_short_url.html', form=form, url_map=url_map)


@app.route('/<string:custom_id>', methods=['GET'])
def short_id_view(custom_id):
    url_map = URL_map.query.filter_by(short=custom_id).first()
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
