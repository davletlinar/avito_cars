from datetime import datetime
import os
import random
from icecream import ic
from bs4 import BeautifulSoup
from classes import Car

import pandas as pd

from get_html import get_html

car = Car('volkswagen', 'amarok')

def parse_car(car: object, car_counter: int, len_car_objects: int) -> None:
    '''scrape a car object and return time left'''
    global total_time

    url = f"https://www.avito.ru/all/avtomobili/{car.brand}/{car.model}"
    html_content = get_html(url)

    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        pages = soup.find_all("span", class_="styles-module-text-InivV")
        pages_num = int(pages[-1].text) # find number of pages of a car.model
        pages_lst = list(range(1, pages_num + 1)) # create list of pages
        random.shuffle(pages_lst) # shuffle list of pages
        ic(pages_num)

parse_car(car, 1, 1)