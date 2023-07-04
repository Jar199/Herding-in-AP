import pandas as pd
import numpy as np


df = pd.read_csv('./raw_data_year/dy2016-2022.csv', encoding='ms949')

cols = df.columns
for i in range(len(df)):
    end = 2
    for j in range(1, len(df.columns)):
        if not pd.isnull(df[cols[j]][i]):
            end = j
            
    for j in range(2, end + 1):
        if pd.isnull(df[cols[j]][i]) and not pd.isnull(df[cols[j-1]][i]):
            df[cols[j]][i] = df[cols[j-1]][i]
            

#df = df.drop(columns=['Unnamed: 0'])
df.to_csv('./raw_data_year/dy2016-2022_filled.csv', encoding='ms949')

"""


df = pd.read_csv('./raw_data_year/dy2016-2022.csv', encoding='ms949')

cols = df.columns
for i in range(len(df)):
    flag = True
    s = 2
    for j in range(2, len(df.columns)-1):
        if flag: 
            if pd.isnull(df[cols[j]][i]): continue
            else: 
                flag = False
                j -= 1
        else:
            if not pd.isnull(df[cols[j]][i]):
                s = j
                if pd.isnull(df[cols[s+1]][i]):
                    for k in range(s+1, len(df.columns)):
                        if not pd.isnull(df[cols[k]][i]):
                            e = k
                            break
                    fill_num = np.linspace(df[cols[s]][i], df[cols[e]][i], (e - s + 1), endpoint=False)
                    j += 1 
                    for k in range(1, len(fill_num)):
                        df[cols[j]][i] = fill_num[k]
                        j += 1
                    

            

#df = df.drop(columns=['Unnamed: 0'])
df.to_csv('./raw_data_year/dy2016-2022_filled.csv', encoding='ms949')"""