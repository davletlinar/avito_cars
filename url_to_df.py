from bs4 import BeautifulSoup
from classes import Car
import pandas as pd
import datetime as dt
from icecream import ic
import re

from get_html import get_html

import logging
logging.basicConfig(filename='description.log', encoding='utf-8', level=logging.INFO)


def url_to_df(config: list, car: Car, page: int) -> 0 | 1:
    url = f'https://www.avito.ru/all/avtomobili/{car.brand}/{car.model}?p={page}'
    ic(url)

    html = get_html(url)
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except TypeError as e:
        print(e)
        print(f'Page {page} was not parsed due to an error')
        soup = None
        
    main_df = pd.DataFrame() # create main dataframe
    
    # parse headers
    if soup:
        headers = soup.find_all('h3')
    else:
        return 0
    
    headers_list = list(map(lambda x: x.text, headers))
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
    prices = soup.find_all('strong', class_=config[7])
    prices_list = list(map(lambda x: x.text[:-2], prices))
    prices_list = prices_list[1:]
   
    # remove 'от ' from a price
    prices_list = list(map(lambda x: x.replace('от ', '').replace('\xa0', ''), prices_list))
    
    # create price_rub column
    main_df['price_rub'] = prices_list
    
    # add date column
    main_df['date'] = dt.datetime.today().strftime("%Y/%m/%d")
    main_df['date'] = pd.to_datetime(main_df['date'])

    # parse descriptions
    descriptions = soup.find_all('p', class_=config[4])
    descriptions_list = []
    for description in descriptions:
        if (description.text[0].isnumeric() or description.text.split(', ')[0] == 'Битый')\
        and description.text.split(', ')[-1] != 'электро':
            descriptions_list.append(description.text.replace('\xa0', ''))
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

def df_refactor(main_df: pd.DataFrame) -> pd.DataFrame:
    # remove invalid data
    main_df = main_df[~(main_df['engine'].astype(str).str.len() > 3)]
    main_df = main_df[~(main_df['horse_pwr'].isna())]
    main_df.drop_duplicates(inplace=True)
    
    # covert price_rub to integer
    main_df['price_rub'] = main_df['price_rub'].astype('int32')

    # convert mileage to integer
    main_df['mileage_kms'] = main_df['mileage_kms'].astype('int32')

    # convert buid_year to datetime
    main_df['build_year'] = pd.to_datetime(main_df['build_year'], format='%Y')
    main_df['build_year'] = main_df['build_year'].dt.year
    
    # convert pub_date to datetime
    main_df['date'] = pd.to_datetime(main_df['date'], format='%Y-%m-%d')
    main_df['date'] = main_df['date'].dt.date

    # convert horse power to integer
    main_df['horse_pwr'] = main_df['horse_pwr'].astype('int32')

    # convert to categorical dtype
    main_df['gas'] = main_df['gas'].astype('category')
    main_df['drive'] = main_df['drive'].astype('category')
    main_df['trans'] = main_df['trans'].astype('category')
    main_df['brand'] = main_df['brand'].astype('category')
    main_df['model'] = main_df['model'].astype('category')
    main_df['engine'] = main_df['engine'].astype('float')

    return main_df