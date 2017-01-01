#!/usr/bin/env bash

# start at localhost:9999
uwsgi --http :9999 --wsgi-file ../catcher/restapi.py --callable api