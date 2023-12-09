from sqlmodel import Field, Session, SQLModel, create_engine, select
from csv_to_df import csv_to_df
import pandas as pd


class Cars(SQLModel, table=True):  
    id: int | None = Field(default=None, primary_key=True)
    brand_id: int
    model_id: int
    engine_id: int
    horse_pwr: int
    trans_id: int
    gas_id: int
    deive_id: int
    build_year: int
    mileage_kms: int
    price_rub: int
    pud_date: str


# Set up the connection URL
host = '127.0.0.1'
port = '5432'
username = 'postgres'
password = '1986'
database_name = 'avito_cars'

# connection url
url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'

engine = create_engine(url, echo=True)


def create_car(df: pd.Series):
    car = Cars(
        brand_id=
        model_id=
        engine_id=
        horse_pwr=horse_pwr
        trans_id: int
        gas_id: int
        deive_id: int
        build_year: int
        mileage_kms: int
        price_rub: int
        pud_date: str)  

    with Session(engine) as session:  
        session.add(car)
        session.commit()


def select_heroes():
    with Session(engine) as session:  
        statement = select(Hero)  
        results = session.exec(statement)  
        for hero in results:  
            print(hero)  
    

def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()  


if __name__ == "__main__":
    main()