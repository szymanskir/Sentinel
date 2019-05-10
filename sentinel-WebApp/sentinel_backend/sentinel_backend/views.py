from flask import jsonify, request, render_template
from sentinel_backend import app
from .repository import MockRepository
from dateutil.parser import parse as parse_utc

_REPOSITORY = MockRepository('../mock-data')


@app.route('/')
def index():
    app.logger.warning('sample message')
    return render_template('index.html')


@app.route('/mentions')
def get_mentions():
    since = parse_utc(request.args.get('from'), ignoretz=True)
    until = parse_utc(request.args.get('to'), ignoretz=True)

    keywords = request.args.get('keywords')
    if keywords is None:
        keywords = _REPOSITORY.get_keywords(user=request.args.get('user'))
    else:
        keywords = keywords.split(',')

    mentions = _REPOSITORY.get_mentions(since, until, keywords)
    return jsonify(mentions)


@app.route('/my-keywords')
def get_my_keywords():
    user = request.args.get('user')
    return jsonify(_REPOSITORY.get_keywords(user=user))


@app.route('/all-keywords')
def get_all_keywords():
    return jsonify(_REPOSITORY.get_keywords())
