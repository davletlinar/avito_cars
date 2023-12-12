from datetime import datetime
import os
from classes import Car

import pandas as pd


def merge_csv_files(car: Car) -> None:
    '''merge parsed csv files into one'''
    folder = 'exports_csv'
    filenames = []

    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        filenames.append(filename)

    filenames.sort()

    dfs = []

    for filename in filenames:
        df = pd.read_csv(f'exports_csv/{filename}')
        dfs.append(df)

    merged_df = pd.concat(dfs)
    merged_df.drop_duplicates(inplace=True)
    date = datetime.now().strftime("%Y-%m-%d")
    merged_df.to_csv(f'merged_csv/{date}_{car.brand}_{car.model}.csv', index=False)

    for filename in filenames:
        os.remove(f'exports_csv/{filename}')

    print('✅ Merging complete\n')