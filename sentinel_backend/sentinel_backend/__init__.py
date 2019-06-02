import os
from flask import Flask
from flask_cors import CORS
from flask_cognito import CognitoAuth

app = Flask(__name__)
app.config.from_object("sentinel_backend.default_settings")
app.config.from_envvar("SENTINEL_BACKEND_SETTINGS")
app.config["COGNITO_REGION"] = os.environ.get("COGNITO_REGION")
app.config["COGNITO_USERPOOL_ID"] = os.environ.get("COGNITO_USERPOOL_ID")
app.config["COGNITO_APP_CLIENT_ID"] = os.environ.get("COGNITO_APP_CLIENT_ID")

CORS(app)
cogauth = CognitoAuth(app)


@cogauth.identity_handler
def lookup_cognito_user(payload):
    return payload["username"]


if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler

    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(
        os.path.join(app.config["LOG_DIR"], "sentinel_backend.log"), "midnight"
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter("<%(asctime)s> <%(levelname)s> %(message)s")
    )
    app.logger.addHandler(file_handler)

import sentinel_backend.views  # noqa: E402,F401
