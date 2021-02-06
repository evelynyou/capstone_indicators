#!/bin/bash
set -x

# Kill running Flask
killall flask

# Export main app
export FLASK_APP=trade.py

# Now restart it, the logs will be in flask_logs.
nohup flask run --host=0.0.0.0 --port=8080 > flask_logs 2>&1 &
set +x
