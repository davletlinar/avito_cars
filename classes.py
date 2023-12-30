from typing import Optional
from sqlmodel import Field, SQLModel


class Car:
    '''car objects for scraping'''
    def __init__(self, brand: str, model: str) -> None:
        self.brand = brand
        self.model = model
        

class Page(Car):
    '''page objects for scraping'''
    def __init__(self, page_num: int) -> None:
        self.page_num = page_num
        
        
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