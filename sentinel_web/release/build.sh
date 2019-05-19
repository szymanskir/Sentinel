#!/bin/sh

export VERSION=${1:-0.0.1-dev}
docker build -f Dockerfile -t balindwalinstalin/sentinel-web:$VERSION ..