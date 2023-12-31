import os
from argparse import ArgumentParser

import mlflow
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# 0. set mlflow environments
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000'
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5001'
os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'miniostorage'

# 1. load model from mlflow
parser = ArgumentParser()
parser.add_argument("--model-name", dest='model_name', type=str, default='sk_model')
parser.add_argument("--run-id", dest='run_id', type=str)
args = parser.parse_args()

model_pipeline = mlflow.sklearn.load_model(f"runs:/{args.run_id}/{args.model_name}")

# 2. get data
df = pd.read_csv("../model/data.csv")
X = df.drop(['id','timestamp','medhouseval'], axis='columns')
y = df['medhouseval']
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.2, random_state=2023)

# 3. predict results
train_pred = model_pipeline.predict(X_train)
valid_pred = model_pipeline.predict(X_valid)

train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
valid_rmse = np.sqrt(mean_squared_error(y_valid, valid_pred))

print("Train RMSE :", train_rmse)
print("Valid RMSE :", valid_rmse)