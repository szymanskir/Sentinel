#!/bin/sh

#for testing
docker run -p 8000:80 -e 'API_ENDPOINT=http://localhost:5000'  sentinel-web:latest