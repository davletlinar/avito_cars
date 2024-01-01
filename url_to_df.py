from selectolax.lexbor import LexborHTMLParser
from classes import Car
import pandas as pd
import datetime as dt
from icecream import ic
import re

from get_html import get_html

import logging
logging.basicConfig(filename='description.log', encoding='utf-8', level=logging.INFO)


def read_config() -> list[str]:
    '''read config file with avito css classes'''
    with open("config.txt", "r", encoding="utf-8") as file:
        return file.read().splitlines()
    

def url_to_df(car: Car, page: int) -> pd.DataFrame:
    config = read_config()
    url = f'https://www.avito.ru/all/avtomobili/{car.brand}/{car.model}?p={page}'
    ic(url)

    html = get_html(url)
    parser = LexborHTMLParser(html)
        
    main_df = pd.DataFrame() # create main dataframe
    
    # parse headers
    headers = parser.css('h3')
    headers_list = list(map(lambda x: x.text(), headers))
    headers_list = headers_list[1:-1]
    headers_list = list(map(lambda x: x.replace('\xa0', '').replace(' ', ''), headers_list))
    
    # create build_year column
    main_df['build_year'] = list(map(lambda x: re.search(r',(\d{4})($|,)', x).group(1), headers_list))

    # create mileage_kms column
    for i in range(len(headers_list)):
        if headers_list[i][-2:] != 'км':
            headers_list[i] += ', 0км'
        
    main_df['mileage_kms'] = list(map(lambda x: re.search(r'(\d+)км', x).group(1), headers_list))

    # parse prices
    prices = parser.css(f'strong.{config[7]}')
    prices_list = list(map(lambda x: x.text()[:-2], prices))
    prices_list = prices_list[1:]
   
    # remove 'от ' from a price
    prices_list = list(map(lambda x: x.replace('от ', '').replace('\xa0', ''), prices_list))
    
    # create price_rub column
    main_df['price_rub'] = prices_list
    
    # add date column
    main_df['date'] = dt.datetime.today().strftime("%Y/%m/%d")
    main_df['date'] = pd.to_datetime(main_df['date'])

    # parse descriptions
    descriptions = parser.css(f'p[class="{config[4]}"]')
    descriptions_list = []
    for description in descriptions:
        ic(description.text())
        if (description.text()[0].isnumeric() or description.text().split(', ')[0] == 'Битый')\
        and description.text().split(', ')[-1] != 'электро':
            descriptions_list.append(description.text().replace('\xa0', ''))
    prepandas_descriptions_list = list(map(lambda x: x.split(), descriptions_list))
    
    # insert 0 kms mileage to new cars
    for i in prepandas_descriptions_list:
        if len(i) == 6:
            i.insert(0, '0')
        if len(i[1]) == 1:
            i[1] +='.0'

    # add battered data
    prepandas_descriptions_list = list(map(lambda x: x if x[0] == 'Битый,' else [0] + x, prepandas_descriptions_list))
    
    # create descriptions temp dataframe
    descriptions_temp = pd.DataFrame(prepandas_descriptions_list)
    descriptions_temp = descriptions_temp[[2, 3, 4, 6, 7, 0]]
    descriptions_temp[4] = descriptions_temp[4].str.extract(r'(\d+)')
    descriptions_temp[6] = descriptions_temp[6].str.rstrip(',')
    
    # add descriptions temp dataframe to dataframe
    main_df[['engine', 'trans', 'horse_pwr', 'drive', 'gas', 'battered']] = descriptions_temp
    
    # add brand and model columns
    main_df['brand'] = car.brand.title()
    main_df['model'] = car.model.title().replace('_', ' ')
    
    # remove battered cars
    main_df = main_df[main_df['battered'] == 0]

    # rearranging columns order
    main_df= main_df[['brand', 'model', 'engine', 'horse_pwr', 'trans', 'gas', 'drive',
                        'build_year', 'mileage_kms', 'price_rub', 'date']]
    return main_df