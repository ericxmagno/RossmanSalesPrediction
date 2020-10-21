from app import app
from flask import Flask,jsonify,request
from joblib import load
import pickle
import pandas as pd
import os
from app.processing import preprocess

@app.route("/")
def home():
   return "Flask running."

@app.route("/predict", methods=['POST'])
def index():
   data = request.get_json()
   sales = predict_sales(data)
   return jsonify({"sales": sales[0]})

def predict_sales(data):
   df = pd.DataFrame(data, index=[0])
   if df["Open"].iloc[0] == 0:
      return [0]
   else:
      X = preprocess(df, preprocessor)
      return model.predict(X)

if __name__ == 'app.api':
   model = load("rfr.pkl") # Load model
   print ('Model loaded')
   preprocessor = load("preprocessor.joblib") # Load preprocessor
   print("Preprocessor loaded")
   app.run(host="0.0.0.0", port=5000)