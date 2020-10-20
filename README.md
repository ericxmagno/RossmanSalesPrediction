# RossmanSalesPrediction
ML Engineering Project

### Data (/data)
train.csv - training data
store.csv - store data 

### Jupyter Notebook (/notebooks)
`docker-compose up`
Compared 3 Regression algorithms (sklearn library):
- Random Forest Regression - used in flaskapp
- Ridge Regression
- Gradiant Boosting Regressor

Running the notebook creates 2 files: `RFR.joblib` and `preprocessor.joblib`
**RFR.joblib** - RandomForestRegression model used for prediction
**preprocessor.joblib** - ColumnTransformer(OneHotEncoder,StandardScaler) used to preprocess data for prediction in webapp
These files must be manually moved from "/notebooks" to main directory prior to running flask app.

### Flask app (/app)
`docker build -t flaskapp:latest .`
`docker run -d -p 5000:5000 flaskapp`
**api.py** - contains the api endpoint `/predict`
**processing.py** - contains the logic for processing the POST json into data usable for prediction