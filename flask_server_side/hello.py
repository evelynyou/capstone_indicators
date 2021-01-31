from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    print("Received request")
    return 'Best Trading Indicators Ever!'
