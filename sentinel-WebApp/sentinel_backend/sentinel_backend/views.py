from flask import jsonify, request, render_template
from datetime import datetime
from sentinel_backend import app
from .repository import MockRepository

_REPOSITORY = MockRepository('../mock-data')


@app.route('/')
def index():
    app.logger.warning('sample message')
    return render_template('index.html')


@app.route('/mentions')
def get_mentions():
    since = datetime.strptime(request.args.get('from'), '%Y-%m-%d')
    until = datetime.strptime(request.args.get('to'), '%Y-%m-%d')
    keywords = request.args.get('keywords').split(',')
    mentions = _REPOSITORY.get_mentions(since, until, keywords)
    return jsonify(mentions)


@app.route('/my-keywords')
def get_my_keywords():
    user = request.args.get('user')
    return jsonify(_REPOSITORY.get_keywords(user=user))


@app.route('/all-keywords')
def get_all_keywords():
    return jsonify(_REPOSITORY.get_keywords())
