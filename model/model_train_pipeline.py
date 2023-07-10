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

pipeline = Pipeline([("scaler", StandardScaler()), ("xgb", XGBRegressor())])
pipeline.fit(X_train, y_train)
train_pred = pipeline.predict(X_train)
train_mse = mean_squared_error(y_true=y_train, y_pred=train_pred)
train_rmse = np.sqrt(train_mse)

print("Model train RMSE : %f" %train_rmse)

# save scaler & model
joblib.dump(pipeline[0], "scaler.joblib")
joblib.dump(pipeline[1], "xgb.joblib")
joblib.dump(pipeline, "pipeline.joblib")