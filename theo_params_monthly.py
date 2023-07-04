import pandas as pd
import numpy as np
import math

df = pd.read_csv('dm2016-2022.csv', encoding='ms949')
# yearly data에 대한 theo_params를 구하려면
# df = pd.read_csv('dy2016-2022.csv', encoding='ms949')

df_ = pd.DataFrame()


b_month = []
###################### extract extreme prices ######################
COLS = df.columns
mask = np.zeros(len(df))
MASK = pd.DataFrame()
for month in range(1, len(COLS)):
    prices = df[COLS[month]].dropna().tolist()
    prices.sort()
    cut = prices[int(len(prices) * 0.9)]
    for i in range(len(df)):
        if df[COLS[month]][i] >= cut:
            mask[i] = 1
MASK['mask'] = mask 


for i in range(len(mask)):
    if mask[i] == 0:
        MASK['mask'][i] = np.nan
for month in range(1, len(COLS)):    
    df[COLS[month]] = MASK['mask']*df[COLS[month]]



###################### compute b ######################

for month in range(2, len(df.columns)):
    x_ = df[df.columns[month]].astype('float')
    x = df[df.columns[month-1]].astype('float')
    b = np.mean(((x_ - x) / x))
    b_month.append(b)
df_['b'] = b_month

###################### compute r ######################
DF = pd.read_csv('dm2016-2022.csv')
R = []

#### r -> extreme data 사용하여 계산 ####
"""for month in range(2, len(df.columns)):
    new_build = np.count_nonzero(df[df.columns[month-1]].isnull() & df[df.columns[month]].notnull()) # 새로 건축된 아파트 단지 수
    R.append(new_build)
df_['r'] = R
total = np.sum(R)
df_['r'] = df_['r'] / total"""

#### r -> total data 사용하여 계산 #### --> 이 방법 사용.
for month in range(2, len(DF.columns)):
    new_build = np.count_nonzero(DF[DF.columns[month-1]].isnull() & DF[DF.columns[month]].notnull()) # 새로 건축된 아파트 단지 수
    R.append(new_build)
df_['r'] = R
total = np.sum(R)
df_['r'] = df_['r'] / total



###################### compute λ ######################

df_raw = pd.read_csv('./raw_data_month/dm2016-2022_RAW.csv', encoding='ms949')
LAMBDA = []

#### λ -> extreme data 사용하여 계산 ####
for month in range(2, len(df_raw.columns)):
    total = len(df[df.columns[month]].dropna()) # 건축 완료된 모든 아파트 단지 수
    df_raw[df_raw.columns[month]] = MASK['mask'] * df_raw[df_raw.columns[month]]
    trade = len(df_raw[df_raw.columns[month]].dropna()) # 건축된 아파트 중 매매거래가 이루어진 아파트 수
    print(trade, total)
    LAMBDA.append(trade / total)
print(len(df_), len(LAMBDA))
df_['lambda'] = LAMBDA
lam = np.mean(np.array(LAMBDA))



###################### compute c per apartments ######################
# c = (z[i+1] - (1+b)z[i])/(z.mean - z[i])
C = []
c = []

means = pd.read_csv('dmean_total.csv')

c_df = pd.DataFrame()
means = means['mean of price']

b = np.mean(df_['b'])


for i in range(1, len(COLS)): df[COLS[i]] = df[COLS[i]].astype('float')
for i in range(2, len(COLS)):
    mon = str(COLS[i])[4:]
    # 1. z.mean 해당 아파트의 연도별 가격 평균값 사용 --> 이 방법 사용
    c_df[COLS[i-1]] = (df[COLS[i]] - (1 + (b[i-2])) * df[COLS[i-1]]) / (np.mean(df[COLS[i-1]]) - df[COLS[i-1]])
    
    # 2. z.mean 해당 아파트의 모든 기간의 가격 평균값 사용
    #c_df[COLS[i-1]] = (df[COLS[i]] - (1 + float(b)) * df[COLS[i-1]]) / (means - df[COLS[i-1]])



###################### compute c per month  ######################

c_month = pd.DataFrame()
sum_ = []
cmonth = []
date = []
for i in range(len(c_df.columns)):
    tmp = c_df.iloc[:, i].dropna()
    cmonth.append(np.mean(tmp))
    date.append(c_df.columns[i])
        
c_month['date'] = date
c_month['monthly'] = cmonth
df_['c'] = cmonth


###################### compute alpha not including c ######################
# alpha = log(1 + r/lambda) / log(1 + b)
b = np.mean(list(df_['b']))
df_['alpha'] = np.log(1+ df_['r']/df_['lambda']) / np.log(1 + df_['b'])


###################### compute alpha including c ######################
c = np.mean(list(c_month['monthly']))
df_['alpha_c'] = (np.log(1 - c*c/2) + np.log(1 + df_['r']/df_['lambda'])) / np.log(1 + df_['b'])

df_.to_csv('theo_monthly.csv') 
