import pandas as pd
import os
from icecream import ic
from sqlmodel import Field, SQLModel, Session, create_engine, select
from classes import Cars


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
    
    # convert pub_date to datetime
    main_df['pub_date'] = pd.to_datetime(main_df['pub_date'], format='%Y-%m-%d')

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
        #os.remove(f"csv_files/{file}") # delete file
    return refactor_df(main_df)


def create_rows(main_df) -> None:
    # Set up the connection URL
    host = '127.0.0.1'
    port = '5432'
    username = 'postgres'
    password = '1986'
    database_name = 'car-prices'

    # connection url
    url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'

    engine = create_engine(url, echo=False)
    with Session(engine) as session:
        for row in main_df.itertuples(index=False):
            car = Cars(brand=row.brand,
                    model=row.model,
                    engine=row.engine,
                    horse_pwr=row.horse_pwr,
                    trans=row.trans,
                    gas=row.gas,
                    drive=row.drive,
                    build_year=row.build_year,
                    mileage_kms=row.mileage_kms,
                    price_rub=row.price_rub,
                    pub_date=row.pub_date)
            session.add(car)
        session.commit()


ic(merge_csv().info())
create_rows(merge_csv())
