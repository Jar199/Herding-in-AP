import pandas as pd
import numpy as np
import os


months = os.listdir('./raw_data_month/pt')
years = os.listdir('./raw_data_year/pt')
flag = True

for file in months:
    print(file)
    if flag:
        flag = False
        df1 = pd.read_csv('./raw_data_month/pt/' + file, encoding='ms949')
    else:
        df2 = pd.read_csv('./raw_data_month/pt/' + file, encoding='ms949')
        try: df1 = df1.drop(columns=['Unnamed: 0'])
        except: pass
        try: df2 = df2.drop(columns=['Unnamed: 0'])
        except: pass
        df1['building_code'] = df1['building_code'].astype('str')
        df2['building_code'] = df2['building_code'].astype('str')
        df1 = pd.merge(df1, df2, how='outer', on='building_code')

df1.to_csv('./raw_data_month/dm2016-2022.csv', encoding='ms949')

flag = True

for file in years:
    print(file)
    if flag:
        flag = False
        df1 = pd.read_csv('./raw_data_year/pt/' + file, encoding='ms949')
    else:
        df2 = pd.read_csv('./raw_data_year/pt/' + file, encoding='ms949')
        try: df1 = df1.drop(columns=['Unnamed: 0'])
        except: pass
        df2 = df2.drop(columns=['Unnamed: 0'])
        df1['building_code'] = df1['building_code'].astype('str')
        df2['building_code'] = df2['building_code'].astype('str')
        df1 = pd.merge(df1, df2, how='outer', on='building_code')

df1.to_csv('./raw_data_year/dy2016-2022.csv', encoding='ms949')