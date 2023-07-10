import joblib
import psycopg2
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# from sklearn.datasets import fetch_california_housing

# load data
db_connect = psycopg2.connect(host='localhost', user='myuser', database='mydatabase', password='mypassword')
df = pd.read_sql("select * from california_housing order by id desc limit 100", db_connect)
X = df.drop(['id','timestamp','medhouseval'], axis='columns')
y = df['medhouseval']
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.2, random_state=2023)

# model development and train(pipeline)
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

# save scaler & model
joblib.dump(pipeline[0], "scaler.joblib")
joblib.dump(pipeline[1], "xgb.joblib")
joblib.dump(pipeline, "pipeline.joblib")

# save data
df.to_csv("data.csv", index=False)