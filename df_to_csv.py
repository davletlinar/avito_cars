import pandas as pd
from classes import Car
import time
import os

def df_to_csv(df: pd.DataFrame, car: Car, page: int) -> None:
    date_y_m_d = time.strftime("%Y-%m-%d")
    df.to_csv(f"csv_files/{date_y_m_d}_{car.brand}_{car.model}_{page}.csv", index=False)
    
    
def refactor_df(main_df: pd.DataFrame) -> pd.DataFrame:
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
    main_df['pub_date'] = pd.to_datetime(main_df['date'], format='%Y-%m-%d')
    main_df['pub_date'] = main_df['date'].dt.date

    # convert horse power to integer
    main_df['horse_pwr'] = main_df['horse_pwr'].astype('int32')

    # convert to categorical dtype
    main_df['gas'] = main_df['gas'].astype('category')
    main_df['drive'] = main_df['drive'].astype('category')
    main_df['trans'] = main_df['trans'].astype('category')
    main_df['brand'] = main_df['brand'].astype('category')
    main_df['model'] = main_df['model'].astype('category')
    main_df['engine'] = main_df['engine'].astype('float')
    
    # remove incorrect data
    main_df = main_df[main_df['horse_pwr'] < 1000]
    main_df = main_df[main_df['engine'] < 10]

    return main_df
    

def merge_csv() -> pd.DataFrame:
    # make a list of all csv files in the folder
    csv_files = [file for file in os.listdir("csv_files") if file.endswith(".csv")]
    main_df = pd.DataFrame()
    for file in csv_files:
        df = pd.read_csv(f"csv_files/{file}")
        main_df = pd.concat([main_df, df])
    return refactor_df(main_df)

def remove_csv() -> None:
    # remove all csv files in the folder
    for file in os.listdir("csv_files"):
        if file.endswith(".csv"):
            os.remove(f"csv_files/{file}")
    