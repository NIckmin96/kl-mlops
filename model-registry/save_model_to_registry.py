import os
import json
import joblib
import mlflow
import psycopg2
import requests
import numpy as np
import pandas as pd
from argparse import ArgumentParser
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# slack alarm function
def alarm(msg):
    payload = {"text":msg}
    url = ${{secrets.WEBHOOK_URL}}
    headers = {'Content-type':'application/json'}
    requests.post(url=url, headers=headers, data=json.dumps(payload))

# 0. set mlflow environments
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000'
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5001'
os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'miniostorage'

# 1. load data
db_connect = psycopg2.connect(host='localhost', user='myuser', database='mydatabase', password='mypassword', port=5432)
df = pd.read_sql("select * from california_housing", db_connect)
X = df.drop(['id','timestamp','medhouseval'], axis='columns')
y = df['medhouseval']
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.2, random_state=2023)

# 2. model development and train(pipeline)
pipeline = Pipeline([("scaler", StandardScaler()), ("xgb", XGBRegressor())])
pipeline.fit(X_train, y_train)
train_pred = pipeline.predict(X_train)
valid_pred = pipeline.predict(X_valid)

train_mse = mean_squared_error(y_true=y_train, y_pred=train_pred)
train_rmse = np.sqrt(train_mse)
valid_mse = mean_squared_error(y_true=y_valid, y_pred=valid_pred)
valid_rmse = np.sqrt(valid_mse)

print("Model TRAIN RMSE : %f" %train_rmse)
print("Model VALID RMSE : %f" %valid_rmse)

# 3. save scaler & model
parser = ArgumentParser()
parser.add_argument("--model-name", dest="model_name", type=str, default="sk_model")
args = parser.parse_args()

mlflow.set_experiment("new-exp")
mlflow.set_tracking_uri("http://localhost:5001")

signature = mlflow.models.signature.infer_signature(model_input=X_train, model_output=train_pred)
input_sample = X_train.iloc[:10]

with mlflow.start_run():
    mlflow.log_metrics({"train_rmse":train_rmse, "valid_rmse":valid_rmse})
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        artifact_path=args.model_name,
        signature=signature,
        input_example=input_sample
    )

# send slack message
metrics = mlflow.search_runs(['1'])['metrics.valid_rmse'].values # experiment_id = 1
mean_val_rmse = np.mean(metrics)
diff = valid_rmse - mean_val_rmse
if mean_val_rmse <= valid_rmse:
    alarm("model validation score dropped by %f" %diff)

# 4. save data
df.to_csv("data.csv", index=False)
