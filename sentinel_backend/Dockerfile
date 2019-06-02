FROM python:3.6

COPY sentinel_backend /sentinel/sentinel_backend
COPY sentinel_common /sentinel/sentinel_common

WORKDIR /sentinel/sentinel_backend

RUN pip3 install -r requirements.txt

ENV AWS_DEFAULT_REGION eu-central-1
ENV DYNAMO_DB_REGION eu-central-1

ENTRYPOINT [ "make", "prod" ]