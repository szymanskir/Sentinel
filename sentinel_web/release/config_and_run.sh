#!/bin/sh

envsubst '$API_ENDPOINT' < /app/config.js.tmpl > usr/share/nginx/html/config.js
echo "Starting app"
nginx -g "daemon off;"