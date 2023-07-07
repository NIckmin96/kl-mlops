import time
import psycopg2
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
    query = f"""
    insert into carlifornia_housing (
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
        {data.MedInc},
        {data.HouseAge},
        {data.AveRooms},
        {data.AveBedrms},
        {data.Population},
        {data.AveOccup},
        {data.Latitude},
        {data.Longitude},
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

# table creation query
creation_query = """create table if not exists carlifornia_housing (
    id serial primary key,
    timestamp timestamp,
    MedInc float8,
    HouseAge float8,
    AveRooms float8,
    AveBedrms float8,
    Population float8,
    AveOccup float8,
    Latitude float8,
    Longitude float8,
    MedHouseVal float8
    );"""

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
    
    df = load_data()
    create_table(creation_query)
    loop_insertion(df)