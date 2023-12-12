from url_to_csv import url_to_csv
from classes import Car

with open("config.txt", "r", encoding="utf-8") as file:
    config = file.read().splitlines()

car = Car('skoda', 'octavia')

url_to_csv(config, car, 4)