import pandas as pd
import numpy as np


data = pd.read_csv('datasets/Lesson_04_Working_With_Pandas/Dataset/housing_data.csv')

print(data.tail())
print('shape', data.shape)
print('coloumns', data.columns.to_list())

print('some cols ')
print(data[['SalePrice', 'Alley']].tail())

print('loc iloc')
print(data.loc[0])
print(data.iloc[0])
print(data.loc[0, ['SalePrice', 'Alley']])
# print(data.iloc[0, 'price'])


print(len(data[data['SalePrice'] > 900000]))

print(data.isnull().sum() / len(data)* 100 )

print()


print('shape', data.shape)
data.drop_duplicates(inplace=True)
print('shape', data.shape)

print()


group  = data.groupby('SaleCondition')
print(group.tail().sort_index())
print('describe')
print(data.describe())

df = pd.DataFrame(data)
print(df['SaleCondition'].str.capitalize())

