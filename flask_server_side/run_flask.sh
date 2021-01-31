#!/bin/bash
set -x
export FLASK_APP=hello.py
nohup flask run --host=0.0.0.0 --port=8080 &
set +x
