import random

from flask import render_template, url_for, redirect, flash, abort

from .forms import UrlMapForm
from . import app, db
from .models import URL_map
from settings import DEFAULT_LENGTH_LINK, LINK_SYMBOLS


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if form.validate_on_submit():
        short_url = form.custom_id.data
        if URL_map.query.filter_by(short=short_url).first() is not None:
            flash('Эта ссылка уже занята', 'validation')
            return render_template('get_short_url.html', form=form)
        short_url = get_unique_short_id() if not short_url else short_url
        url_map = URL_map(
            original=form.original_link.data,
            short=short_url
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template(
            'get_short_url.html',
            form=form,
            url_map=url_map
        )
    return render_template('get_short_url.html', form=form)


# @app.route('/<string:custom_id>', methods=['GET'])
# def short_id_view(custom_id):
#     url_map = 1
#     return "Типа того"


def get_unique_short_id(length=DEFAULT_LENGTH_LINK):
    short_link = random.choices(LINK_SYMBOLS, k=DEFAULT_LENGTH_LINK)
    if URL_map.query.filter_by(short=short_link).first() is None:
        return short_link
    return get_unique_short_id(length=length)
