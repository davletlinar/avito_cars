import pandas as pd
from csv_to_df import csv_to_df
import sqlalchemy as db


pd.set_option('display.max_columns', None)


# Set up the connection URL
host = '127.0.0.1'
port = '5432'
username = 'postgres'
password = '1986'
database_name = 'avito_cars'

# Create the connection URL
url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'

# Create the engine and connect to the database
engine = db.create_engine(url)
con = engine.connect()

df = csv_to_df('merged_csv/merged_data_1.csv')

rs = con.execute(db.text('select brand from brands'))
if df.iloc[0, 0] not in rs.all():
    stmt = db.insert(db.Table('brands')).values(brand=df.iloc[0, 0])
    con.execute(stmt)
    con.commit()

rs = con.execute(db.text('select model from models'))
if df.iloc[0, 1] not in rs.all():
    stmt = db.insert(db.Table('models')).values(model=df.iloc[0, 1])
    con.execute(stmt)
    con.commit()