from flask import Flask, render_template
from flask import request
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__)

# NOTE: disable this after launch.
CORS(app)

@app.route('/')
def hello_world():
    print("Received request")
    #return 'Best Trading Indicators Ever!'

    return render_template("index.html")
