from flask import Flask
app = Flask(__name__)

from app import api

if __name__ == 'app':
    app.run(host="0.0.0.0", port=5000)
