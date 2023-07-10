import joblib
import numpy as np
import pandas as dp
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import fetch_california_housing

X,y = fetch_california_housing(return_X_y=True, as_frame=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.2, random_state=2023)

pipeline = joblib.load("pipeline.joblib")

valid_pred = pipeline.predict(X_valid)
valid_mse = mean_squared_error(y_true=y_valid, y_pred=valid_pred)
valid_rmse = np.sqrt(valid_mse)

print("Model valid RMSE : %f" %valid_rmse)