from bs4 import BeautifulSoup
import time
import json
import random
from icecream import ic


from get_html import get_html
from time_diff import time_diff
from url_to_df import url_to_df, df_refactor
from df_to_db_sqlmodel import create_rows
from classes import Car


def read_config() -> list[str]:
    '''read config file with avito css classes'''
    with open("config.txt", "r", encoding="utf-8") as file:
        return file.read().splitlines()
    

def sleep_time() -> None:
    '''sleep for random time with seconds status bar'''
    secs = random.randint(60, 90)
    for _ in range(secs):
        time.sleep(1)
        print('-', end='', flush=True)
    print(f' {secs}', end='', flush=True)
    print('\n', end='')


def create_car_objects() -> list:
    '''read json file with brand and model names
    create list with car objects with brand and model names'''
    with open("cars.json", "r", encoding="utf-8") as file:
        car_models = json.load(file)

    car_objects = [Car(brand, model) for brand, models in car_models.items() for model in models]
    return car_objects


def calculate_remaining_time(time_a: int) -> None:
    '''calculate remaining time after every processed page'''
    global total_time
    time_b = int(time.time())
    time_per_page = time_b - time_a
    total_time -= time_per_page
    if total_time//60 > 59:
        print(f"Estimated time remaining: {total_time//3600} h {total_time%3600//60} min\n")
    else:
        print(f"Estimated time remaining: {total_time//60} min\n")


def url_to_db(config: list[str], car: Car, page: int) -> None:
    df = url_to_df(config, car, page)
    df = df_refactor(df)
    create_rows(df)


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
    
    sleep_time()  # waiting
    # scrape each page and return total time left for calculation
    parse_pages(car, car_counter, len_car_objects, pages_lst)


def parse_pages(car: object, car_counter: int, len_car_objects: int, pages_lst: list) -> None:
    '''parse each page of a car and return time left as total_time'''
    global total_time
    
    config = read_config()
    
    pages_num = len(pages_lst) # number of pages of a car.model
    page_counter = 1 # count current page
    retry_lst = [] # list of pages that were not parsed due to an error
    
    for page in pages_lst:
        time_a = int(time.time())
        
        try:
            url_to_db(config, car, page)
            print(f"Car {car_counter}/{len_car_objects}, page {page_counter}/{pages_num} processed")

            sleep_time()  # waiting
            
            page_counter += 1
        except Exception as e:
            print(f"❌ {e}")
            retry_lst.append((car, page))
            sleep_time()  # waiting

        # calculate remaining time
        calculate_remaining_time(time_a)
    
    retry_parse_pages(retry_lst) # retry pages that were not parsed due to an error
    
    
def retry_parse_pages(retry_lst: list) -> None:
    '''retry pages that were not parsed due to an error'''
    global total_time
    internal_retry_lst = [] # copy list of pages that were not parsed due to an error
    config = read_config()
    for car, page in retry_lst:
        time_a = int(time.time())
        try:
            print(f"Retry processing page {page}")
            url_to_db(config, car, page)
            sleep_time()  # waiting
        except Exception as e:
            print(f"❌ {e}")
            internal_retry_lst.append((car, page))
            sleep_time()  # waiting
        calculate_remaining_time(time_a) # calculate remaining time
        
    if internal_retry_lst:
        retry_parse_pages(internal_retry_lst)


def main() -> None:
    objects_counter = 0
    global total_time
    car_objects = create_car_objects()

    # load json file for storing timing
    with open("cars.json", "r", encoding="utf-8") as file:
        timing_data = json.load(file)

    # calculate total time to execute loop
    total_time = sum(map(lambda x: sum(x), (list(car.values()) for car in timing_data.values())))

    for car_object in car_objects:
        time_a = int(time.time()) # start timing
        objects_counter += 1
        parse_car(car_object, objects_counter, len(car_objects)) #total_time)
        time_b = int(time.time())
        elapsed_time = time_b - time_a

        # calculate remaining time
        time_diff_sec, timing_data = time_diff(car_object, elapsed_time, timing_data)
        total_time += time_diff_sec

        # update cars.json
        with open("cars.json", "w", encoding="utf-8") as file:
            json.dump(timing_data, file, indent=4)
    print("Well done!")


if __name__ == "__main__":
    main()
