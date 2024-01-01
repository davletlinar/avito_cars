from url_to_df import url_to_df
from classes import Car
from icecream import ic


car = Car('volkswagen', 'arteon')

ic(url_to_df(car, 3))