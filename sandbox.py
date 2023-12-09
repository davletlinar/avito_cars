from url_to_csv import url_to_csv

with open('config.txt', 'r', encoding="utf-8") as file:
        config = file.read().splitlines()
        

from classes import Car

car = Car('volkswagen', 'golf')

if __name__ == '__main__':
    url_to_csv(config, car, input('page: '))