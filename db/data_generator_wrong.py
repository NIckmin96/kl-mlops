import json
import psycopg2
import requests
import pandas as pd
from sklearn.datasets import fetch_california_housing
from argparse import ArgumentParser

def load_data():
    # load dataset (carlifornia housing)
    X,y = fetch_california_housing(return_X_y = True, as_frame = True)
    df = pd.concat([X,y], axis = 'columns')
    return df

def create_table(query):
    # send query
    with db_connect.cursor() as cur:
        cur.execute(query)
        db_connect.commit()
        
def insert_data(data):
    # data insertion query
    # wrong data insertion(on-purpose)
    query = f"""
    insert into california_housing (
        timestamp,
        MedInc,
        HouseAge,
        AveRooms,
        AveBedrms,
        Population,
        AveOccup,
        Latitude,
        Longitude,
        MedHouseVal
    )
    values (
        now(),
        {data.AveRooms},
        {data.MedInc},
        {data.Population},
        {data.HouseAge},
        {data.Latitude},
        {data.AveBedrms},
        {data.Longitude},
        {data.AveOccup},
        {data.MedHouseVal}
    );
    """
    # print(query)
    with db_connect.cursor() as cur:
        cur.execute(query)
        db_connect.commit()
        
def loop_insertion(df):
    for i in range(len(df)):
        data = df.iloc[i].squeeze()
        insert_data(data)

# slack alarm function
def alarm(msg):
    payload = {"text":msg}
    url = ${{secrets.WEBHOOK_URL}}
    headers = {'Content-type':'application/json'}
    requests.post(url=url, headers=headers, data=json.dumps(payload))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--db-host", dest="db_host", type=str, default="localhost")
    args = parser.parse_args()
    
    db_connect = psycopg2.connect(
        user='myuser',
        password='mypassword',
        host=args.db_host,
        port=5432,
        database="mydatabase"
    )
    
    try:
        df = load_data().sample(frac=0.1)
        
        loop_insertion(df)
        alarm("Data insertion success")
    except Exception as e:
        msg = e.__class__.__name__ + ":" + e.__str__()
        alarm(msg)
