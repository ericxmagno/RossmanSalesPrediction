import pandas as pd
import sys
from flask import Flask, jsonify, request
from joblib import load

from app import app
from app.processing import preprocess
from app.validate import validateJson


@app.route("/")
def home():
   return "Flask running."

@app.route("/predict", methods=['POST'])
def index():
   try:
      data = request.get_json()
      if validateJson(data):
         sales = predict_sales(data)
         return jsonify({"sales": sales[0]})
      else:
         return jsonify({"error": "invalid json"})
   except Exception as e:
      return jsonify({"error": str(e)})

def predict_sales(data):
   df = pd.DataFrame(data, index=[0])
   if df["Open"].iloc[0] == 0:
      return [0]
   else:
      X = preprocess(df, preprocessor)
      return model.predict(X)

if __name__ == 'app.api':
   print("--- Starting Flask ----")
   model = load("rfr.pkl") # Load model
   print ('###### Model loaded #####')
   preprocessor = load("preprocessor.joblib") # Load preprocessor
   print("##### Preprocessor loaded #####")
   import os
   if not os.environ.get('TEST_RUNNING', '') == 'True':
      app.run(host="0.0.0.0", port=5000)
