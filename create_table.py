from sqlmodel import SQLModel, create_engine, Field
from typing import Optional
from datetime import date


host = '193.104.57.46'
# host = '127.0.0.1'
port = '5432'
username = 'postgres'
password = '1986'
database_name = 'car-prices'

    # connection url
url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'
engine = create_engine(url, echo=True)

class Cars(SQLModel, table=True):
    '''cars table model'''
    id: Optional[int] = Field(default=None, primary_key=True)
    brand: str
    model: str
    engine: float
    horse_pwr: int
    trans: str
    gas: str
    drive: str
    build_year: date
    mileage_kms: int
    price_rub: int
    pub_date: date
    
def create_table():
    '''create cars table'''
    SQLModel.metadata.create_all(engine)
    
if __name__ == '__main__':
    create_table()