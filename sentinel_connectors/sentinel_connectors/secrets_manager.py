import boto3
from botocore.exceptions import ClientError
from abc import ABC
import logging
import json


class SecretsManager(ABC):
    def __init__(self, secret_id: str):
        self._secret_id = secret_id
        self._logger = logging.getLogger(SecretsManager.__name__)

    def get_secrets(self):
        region_name = "eu-central-1"
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self._secret_id
            )
        except ClientError as e:

            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text
                # using the provided KMS key. Deal with the exception here,
                # and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the
                # current state of the resource. Deal with the exception here,
                # and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        except Exception as e:
            self._logger.error(e)

        else:
            # Decrypts secret using the associated KMS CMK.
            if 'SecretString' in get_secret_value_response:
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
