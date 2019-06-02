#!/bin/sh

envsubst '$API_ENDPOINT $AWS_REGION $COGNITO_USER_POOL_ID $COGNITO_WEB_CLIENT_ID' < /app/config.js.tmpl > usr/share/nginx/html/config.js
echo "Starting app"
nginx -g "daemon off;"