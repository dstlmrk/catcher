#!/usr/bin/env bash

# start at localhost:9090
python -m uwsgi --http :9092 --wsgi-file ../restapi.py --callable app