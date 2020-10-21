# RossmanSalesPrediction
ML Engineering Project

Currently deployed w AWS:
http://18.141.207.232:8888/predict

### Data (/data)
train.csv - training data
store.csv - store data 

### Jupyter Notebook (/notebooks)
`docker-compose up`
Compared 3 Regression algorithms (sklearn library):
- Random Forest Regression - used in flaskapp
- Ridge Regression
- Gradiant Boosting Regressor

Running the notebook creates 2 files: `RFR.pkl` and `preprocessor.joblib`
**RFR.pkl** - RandomForestRegression model used for prediction (uploaded as git lfs file)
**preprocessor.joblib** - ColumnTransformer(OneHotEncoder,StandardScaler) used to preprocess data for prediction in webapp
!!!These files must be manually moved from "/notebooks" to main directory "/" prior to running flask app.!!!

### Flask app (/app)
**api.py** - contains the api endpoint `/predict`
**processing.py** - contains the logic for processing the POST json into data usable for prediction
**validate.py** - contains the validator for the json file recieved by the api


## How to run flask app locally
`docker build -t flask-app:latest .`
`docker run -d --publish 8888:5000 flask-app`
http://localhost:8888/predict
