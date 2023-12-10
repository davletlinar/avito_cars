from url_to_csv import url_to_csv
from classes import Car

car = Car('volkswagen', 'jetta')

# read config file with avito css classes
with open("config.txt", "r", encoding="utf-8") as file:
    config = file.read().splitlines()

url_to_csv(config, car, 24)