from flask import jsonify, request, render_template
from flask_cognito import cognito_auth_required, current_user
from sentinel_backend import app
from .repository import KeywordRepository, MentionRepository
from .visualization import create_mentions_count_plot, create_sentiment_scores_plot

from dateutil.parser import parse as parse_utc

_KEYWORD_REPOSITORY = KeywordRepository()
_MENTION_REPOSITORY = MentionRepository()


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

    mentions = _MENTION_REPOSITORY.get_mentions(
        str(current_user), since, until, keywords
    )
    if not mentions.empty:
        mentions.origin_date = [str(x) for x in mentions.origin_date]
    return mentions.to_json(orient="records")


@app.route("/mentions-count")
@cognito_auth_required
def get_mentions_count():
    since = parse_utc(request.args.get("from"), ignoretz=True)
    until = parse_utc(request.args.get("to"), ignoretz=True)

    keywords = request.args.getlist("keywords")

    mentions = _MENTION_REPOSITORY.get_mentions(
        str(current_user), since, until, keywords
    )
    plot_data = create_mentions_count_plot(mentions)
    return jsonify(plot_data)


@app.route("/sentiment")
@cognito_auth_required
def get_sentiment():
    since = parse_utc(request.args.get("from"), ignoretz=True)
    until = parse_utc(request.args.get("to"), ignoretz=True)

    keywords = request.args.getlist("keywords")

    mentions = _MENTION_REPOSITORY.get_mentions(
        str(current_user), since, until, keywords
    )
    plot_data = create_sentiment_scores_plot(mentions)
    return jsonify(plot_data)


@app.route("/keywords/add")
@cognito_auth_required
def add_keyword():
    keyword = request.args.get("keyword")
    _KEYWORD_REPOSITORY.add(keyword, str(current_user))
    return jsonify(success=True)


@app.route("/keywords/delete")
@cognito_auth_required
def delete_keyword():
    keyword = request.args.get("keyword")
    _KEYWORD_REPOSITORY.delete(keyword, str(current_user))
    return jsonify(success=True)


@app.route("/keywords/update")
@cognito_auth_required
def update_keyword():
    old_keyword = request.args.get("old_keyword")
    current_keyword = request.args.get("current_keyword")
    _KEYWORD_REPOSITORY.update(old_keyword, current_keyword, str(current_user))
    return jsonify(success=True)


@app.route("/my-keywords")
@cognito_auth_required
def get_my_keywords():
    return jsonify(_KEYWORD_REPOSITORY.get_by_user(str(current_user)))
