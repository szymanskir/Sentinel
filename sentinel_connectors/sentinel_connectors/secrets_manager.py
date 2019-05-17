# https://docs.aws.amazon.com/code-samples/latest/catalog/python-secretsmanager-secrets_manager.py.html
import boto3
from abc import ABC
import logging
import json


class SecretsManager(ABC):
    def __init__(self, secret_id: str):
        self._secret_id = secret_id
        self._logger = logging.getLogger(SecretsManager.__name__)

    def get_secrets(self):
        session = boto3.session.Session()
        region_name = session.region_name
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self._secret_id
            )
        except Exception as e:
            self._logger.error(e)
            raise e

        self._logger.info(
            f"Secret with id: {self._secret_id} recovered successfully"
        )
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)


class TwitterSecretsManager(SecretsManager):
    def __init__(self):
        super().__init__("sentinel/api_keys/twitter")


class RedditSecretsManager(SecretsManager):
    def __init__(self):
        super().__init__("sentinel/api_keys/reddit")


class GoogleNewsSecretsManager(SecretsManager):
    def __init__(self):
        super().__init__("sentinel/api_keys/google_news")
