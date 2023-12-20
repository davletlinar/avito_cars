from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
from csv_to_df import csv_to_df
import pandas as pd


class Cars(SQLModel, table=True):  
    id: Optional[int] = Field(default=None, primary_key=True)
    brand_id: int
    modl_id: int
    engine_id: int
    horse_pwr: int
    trans_id: int
    gas_id: int
    drive_id: int
    build_year: int
    mileage_kms: int
    price_rub: int
    pub_date: str


# Set up the connection URL
host = '127.0.0.1'
port = '5432'
username = 'postgres'
password = '1986'
database_name = 'avito_cars'

# connection url
url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'

engine = create_engine(url, echo=True)


def create_car(df: pd.Series) -> None:
    car = Cars(brand_id = df.brand_id,
        modl_id = df.model_id,
        engine_id = df.engine_id,
        horse_pwr = df.horse_pwr,
        trans_id = df.trans_id,
        gas_id = df.gas_id,
        drive_id = df.drive_id,
        build_year = df.build_year,
        mileage_kms = df.mileage_kms,
        price_rub = df.price_rub,
        pub_date = df.pub_date)

    with Session(engine) as session:  
        session.add(car)
        session.commit()


def select_heroes() -> None:
    with Session(engine) as session:  
        statement = select(Hero)  
        results = session.exec(statement)  
        for hero in results:  
            print(hero)  
    

def main() -> None:
    create_car()
    select_heroes()  


if __name__ == "__main__":
    pass