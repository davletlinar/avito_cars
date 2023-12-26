from sqlmodel import Field, SQLModel, Session, create_engine, select
import pandas as pd
from icecream import ic
from classes import Cars
    

def create_rows(main_df) -> None:
    # Set up the connection URL
    host = '172.17.0.1'
    # host = '0.0.0.0'
    port = '5432'
    username = 'postgres'
    password = '1986'
    database_name = 'car-prices'

    # connection url
    url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'

    engine = create_engine(url, echo=False)
    with Session(engine) as session:
        for row in main_df.itertuples(index=False):
            car = Cars(brand=row.brand,
                    model=row.model,
                    engine=row.engine,
                    horse_pwr=row.horse_pwr,
                    trans=row.trans,
                    gas=row.gas,
                    drive=row.drive,
                    build_year=row.build_year,
                    mileage_kms=row.mileage_kms,
                    price_rub=row.price_rub,
                    pub_date=row.date)
            session.add(car)
        session.commit()