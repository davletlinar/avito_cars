from datetime import datetime
import os
from classes import Car

import pandas as pd

car = Car('Audi', 'A3')

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
print(merged_df.info())
merged_df = merged_df[~(merged_df['engine'].astype(str).str.len() > 3)]
merged_df.drop_duplicates(inplace=True)
date = datetime.now().strftime("%Y-%m-%d")
merged_df.to_csv(f'merged_csv/{date}_{car.brand}_{car.model}.csv', index=False)

'''for filename in filenames:
    os.remove(f'exports_csv/{filename}')'''

print('✅ Merging complete\n')