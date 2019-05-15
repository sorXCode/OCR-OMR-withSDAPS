import pandas as pd
from copy import deepcopy

df = pd.read_csv('project4/data_1.csv')
data = deepcopy(df)

print(df.tail())
print(df.head())
df.