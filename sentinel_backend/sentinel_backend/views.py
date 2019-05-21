from flask import jsonify, request, render_template
from flask_cognito import cognito_auth_required
from sentinel_backend import app
from .repository import DynamoDbRepository
from .visualization import create_mentions_count_plot, create_sentiment_scores_plot

from dateutil.parser import parse as parse_utc

# _REPOSITORY = MockRepository("../mock-data")
_REPOSITORY = DynamoDbRepository()


@app.route("/")
def index():
    app.logger.warning("sample message")
    return render_template("index.html")


@app.route("/mentions")
@cognito_auth_required
def get_mentions():
    since = parse_utc(request.args.get("from"), ignoretz=True)
    until = parse_utc(request.args.get("to"), ignoretz=True)

    keywords = request.args.getlist("keywords")

    mentions = _REPOSITORY.get_mentions("users0", since, until, keywords)
    mentions.origin_date = [str(x) for x in mentions["origin_date"]]
    return mentions.to_json(orient="records")


@app.route("/mentions-count")
@cognito_auth_required
def get_mentions_count():
    since = parse_utc(request.args.get("from"), ignoretz=True)
    until = parse_utc(request.args.get("to"), ignoretz=True)

    keywords = request.args.getlist("keywords")

    mentions = _REPOSITORY.get_mentions("users0", since, until, keywords)
    plot_data = create_mentions_count_plot(mentions)
    return jsonify(plot_data)


@app.route("/sentiment")
@cognito_auth_required
def get_tions():
    since = parse_utc(request.args.get("from"), ignoretz=True)
    until = parse_utc(request.args.get("to"), ignoretz=True)

    keywords = request.args.getlist("keywords")

    mentions = _REPOSITORY.get_mentions("users0", since, until, keywords)
    plot_data = create_sentiment_scores_plot(mentions)
    return jsonify(plot_data)


@app.route("/my-keywords")
@cognito_auth_required
def get_my_keywords():
    return jsonify(_REPOSITORY.get_keywords("users0"))


@app.route("/all-keywords")
def get_all_keywords():
    return jsonify(_REPOSITORY.get_all_keywords())
