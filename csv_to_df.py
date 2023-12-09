import pandas as pd
pd.set_option('display.max_columns', None)

def csv_to_df(file_path):
    '''convert csv file to a pandas dataframe'''
    with open(file_path, 'r', encoding="utf-8") as f:
        cars_df = pd.read_csv(f)

    # covert price_rub to integer
    cars_df['price_rub'] = cars_df['price_rub'].astype('int32')

    # convert mileage to integer
    cars_df['mileage_kms'] = cars_df['mileage_kms'].astype('int32')

    # convert buid_year to datetime
    cars_df['build_year'] = pd.to_datetime(cars_df['build_year'], format='%Y')
    cars_df['build_year'] = cars_df['build_year'].dt.year

    # convert horse power to integer
    cars_df['horse_pwr'] = cars_df['horse_pwr'].astype('int32')

    # convert to categorical dtype
    cars_df['gas'] = cars_df['gas'].astype('category')
    cars_df['drive'] = cars_df['drive'].astype('category')
    cars_df['trans'] = cars_df['trans'].astype('category')
    cars_df['brand'] = cars_df['brand'].astype('category')
    cars_df['model'] = cars_df['model'].astype('category')
    cars_df['engine'] = cars_df['engine'].astype('category')

    # convert date to datetime
    cars_df['date'] = pd.to_datetime(cars_df['date'])

    return cars_df