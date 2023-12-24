from typing import Optional
from sqlmodel import Field, SQLModel


class Car:
    '''car objects for scraping'''
    def __init__(self, brand: str, model: str):
        self.brand = brand
        self.model = model
        
        
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
    build_year: int
    mileage_kms: int
    price_rub: int
    pub_date: str