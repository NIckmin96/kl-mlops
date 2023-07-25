# kl-mlops

> Demo version of mlops(especially, *Model Pipeline* part)

# Dir
├── API_serving
│   ├── Dockerfile
│   ├── app.py
│   ├── docker-compose.yaml
│   ├── download_model.py
│   ├── schemas.py
│   └── sk_model
├── README.md
├── db
│   ├── Dockerfile
│   ├── README.md
│   ├── data_generator.py
│   ├── data_generator_wrong.py
│   ├── data_generator_wrong_2.py
│   ├── db.ipynb
│   ├── db_server
│   └── docker-compose.yaml
├── model
│   ├── data.csv
│   ├── mlruns
│   ├── model_train_pipeline.py
│   ├── model_validation.py
│   ├── pipeline.joblib
│   ├── scaler.joblib
│   └── xgb.joblib
├── model-registry
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   ├── load_model_from_registry.py
│   ├── prometheus.yml
│   └── save_model_to_registry.py
├── poetry.lock
└── pyproject.toml

## db/
    - create database(postgres) server
    - create table & insert data(sklearn - California Housing Dataset)
## model/
    - create model pipeline(Xgboost Regressor)
## model-registry/
    - create model tracking server(MLflow)
        - show model tracking metrics **from model backend server**
    - create model artifact server(minio)
        - save model artifacts(e.g. model.pt)
    - create model backend server(postgres)
        - save model metrics(e.g. rmse, acc ...)
    - **Send monitoring message** using `Slack Webhook`
## API_serving/
    - create API server(for deployment)
    - set input&output schemas(BaseModel)