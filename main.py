from bs4 import BeautifulSoup
import time
import json
import random
from icecream import ic
from urllib.request import HTTPError


from url_to_csv import url_to_csv, get_html
from time_diff import time_diff
from merge_csv_files import merge_csv_files
from csv_to_df import csv_to_df
from classes import Car


def sleep_time(secs: int) -> None:
    """sleep for random time with countdown"""
    for _ in range(secs):
        time.sleep(1)
        print('-', end='', flush=True)
    print(f' {secs}', end='', flush=True)
    print('\n', end='')


def create_car_objects() -> list:
    """read json file with brand and model names
    create list with car objects with brand and model names"""
    with open("cars.json", "r", encoding="utf-8") as file:
        car_models = json.load(file)

    car_objects = [Car(brand, model) for brand, models in car_models.items() for model in models]
    return car_objects


def parse_pages(car: object, car_counter: int, len_car_objects: int, pages_lst: list, total_time: int) -> None:
    '''parse each page of a car'''
    
    # read config file with avito css classes
    with open("config.txt", "r", encoding="utf-8") as file:
        config = file.read().splitlines()
    
    pages_num = len(pages_lst) # number of pages of a car.model
    page_counter = 1 # count current page
    retry_lst = [] # list of pages that were not parsed due to an error
    
    for page in pages_lst:
        time_a = time.time()
        
        try:
            url_to_csv(config, car, page)
            print(f"Car {car_counter}/{len_car_objects}, page {page_counter}/{pages_num} processed")

            sleep_time(random.randint(60, 90))  # sleep and back to work
            time_b = time.time()
            
            # calculate remaining time
            time_per_page = int(time_b - time_a)
            total_time = total_time - time_per_page
            if total_time//60 > 59:
                print(f"Estimated time remaining: {total_time//3600} h {total_time%3600//60} min\n")
            else:
                print(f"Estimated time remaining: {total_time//60} min\n")
            page_counter += 1
        except Exception as e:
            print(f"❌ {e}")
            retry_lst.append((car, page))
            sleep_time(random.randint(60, 90))  # sleep and back to work
    
    # retry pages that were not parsed due to an error
    for car, page in retry_lst:
        try:
            print(f"Retry processing page {page}")
            url_to_csv(config, car, page)
            sleep_time(random.randint(60, 90))  # sleep and back to work
        except KeyError as e:
            print(f"❌ {e}")
            sleep_time(random.randint(60, 90))  # sleep and back to work


def parse_car(car: object, car_counter: int, len_car_objects: int, total_time: int) -> None:
    """scrape a car object"""

    url = f"https://www.avito.ru/all/avtomobili/{car.brand}/{car.model}"
    html_content = get_html(url)

    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        pages = soup.find_all("span", class_="styles-module-text-InivV")
        pages_num = int(pages[-1].text) # find number of pages of a car.model
        pages_lst = list(range(1, pages_num + 1)) # create list of pages
        random.shuffle(pages_lst) # shuffle list of pages
    
    sleep_time(random.randint(60, 90))  # sleep and back to work
    parse_pages(car, car_counter, len_car_objects, pages_lst, total_time) # scrape each page
    merge_csv_files(car) # merge exported csv files into one


def main(car_objects) -> None:
    objects_counter = 0

    # load json file for storing timing
    with open("cars.json", "r", encoding="utf-8") as file:
        timing_data = json.load(file)

    # calculate total time to execute loop
    total_time = sum(map(lambda x: sum(x), (list(car.values()) for car in timing_data.values())))

    for car_object in car_objects:
        try:
            time_a = time.time() # start timing
            objects_counter += 1
            parse_car(car_object, objects_counter, len(car_objects), total_time)
            time_b = time.time()
            elapsed_time = int(time_b - time_a)

            # calculate remaining time
            time_diff_sec, timing_data = time_diff(car_object, elapsed_time, timing_data)
            total_time += time_diff_sec

            # update cars.json
            with open("cars.json", "w", encoding="utf-8") as file:
                json.dump(timing_data, file, indent=4)
        except HTTPError as e:
            print(f"❌  {e}")
            exit()
            #sleep_time(60)
            #main(car_objects)
    print("Well done!")


if __name__ == "__main__":
    main(create_car_objects())
