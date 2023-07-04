import pandas as pd
import numpy as np
import os


months = os.listdir('./raw_data_month')
years = os.listdir('./raw_data_year')

for file in months:
    if '_raw' in file:
        print(file)
        month = str(file.split('_')[0])
        df = pd.read_csv('./raw_data_month/' + file, encoding='ms949')
        
        dict1 = {}

        # 건물명코드 별로 아파트 가격 값 저장
        for i in range(len(df)):
            key = str(df['building_code'][i])
            if key in dict1:
                list_ = dict1[key]
            else:
                list_ = []
            list_.append(df['price'][i])
            dict1[key] = list_

        buildings = list(set(list(df['building_code'])))
        dict2 = dict()
        # 계약된 아파트 가격들의 평균값 하나를 해당 건물의 대표가격으로 사용
        for i in range(len(buildings)):
            #key = str(df['building_code'][i])
            key = buildings[i]
            dict2[key] = np.mean(np.array(dict1[key]))
            
        # 건물별 해당 기간동안의 아파트 가격 dataframe으로 저장
        result = pd.DataFrame(columns=['building_code', month])
        for i in dict2:
            result.loc[len(result)] = [i, dict2[i]]
        result.to_csv(f'./raw_data_month/pt/pt_{month}.csv', encoding='ms949')


for file in years:
    if '_raw' in file:
        print(file)
        df2 = pd.read_csv('./raw_data_year/' + file, encoding='ms949')
        year = str(file.split('_')[0])
        
        dict3 = {}

        # 건물명코드 별로 아파트 가격 값 저장
        for i in range(len(df2)):
            key = str(df2['building_code'][i])
            if key in dict3:
                list_ = dict3[key]
            else:
                list_ = []
            list_.append(df2['price'][i])
            dict3[key] = list_

        buildings = list(set(list(df2['building_code'])))
        dict4 = dict()
        # 계약된 아파트 가격들의 평균값 하나를 해당 건물의 대표가격으로 사용
        for i in range(len(buildings)):
            #key = str(df['building_code'][i])
            key = buildings[i]
            dict4[key] = np.mean(np.array(dict3[key]))
            
        # 건물별 해당 기간동안의 아파트 가격 dataframe으로 저장
        result2 = pd.DataFrame(columns=['building_code', year])
        for i in dict4:
            result2.loc[len(result2)] = [i, dict4[i]]

        result2.to_csv(f'./raw_data_year/pt/pt_{year}.csv', encoding='ms949')
