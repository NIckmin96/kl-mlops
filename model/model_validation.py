import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# load data used in training
df = pd.read_csv('data.csv')
X = df.drop(['id','timestamp','medhouseval'], axis='columns')
y = df['medhouseval']
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.2, random_state=2023)

# load model(pipeline) used in training
pipeline = joblib.load("pipeline.joblib")

train_pred = pipeline.predict(X_train)
valid_pred = pipeline.predict(X_valid)

train_mse = mean_squared_error(y_true=y_train, y_pred=train_pred)
train_rmse = np.sqrt(train_mse)
valid_mse = mean_squared_error(y_true=y_valid, y_pred=valid_pred)
valid_rmse = np.sqrt(valid_mse)

print("Load Model TRAIN RMSE : %f" %train_rmse)
print("Load Model VALID RMSE : %f" %valid_rmse)
