import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

MONTHLY = True

if MONTHLY : df = pd.read_csv('./non_extreme_params_monthly_90.csv', encoding='ms949')
else : df = pd.read_csv('./non_extreme_params_yearly_90.csv', encoding='ms949')

df['date'] = df['date'].astype('str')
date = []
for i in range(len(df)):
    date.append(df['date'][i][4:])
param = 'sigma'
if MONTHLY: 
    s, e = 0, 12
    for year in range(2016, 2023):
        m = np.mean(df[param][s:e])
        std = np.std(df[param][s:e])
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.figure(figsize=(14, 10))
        plt.title(year, size=45, pad=15)
        plt.axhspan(m-std, m+std, alpha=0.5, color='yellowgreen')
        plt.plot(date[s:e], np.ones(12)*m, linewidth=7, color='orange')
        plt.plot(date[s:e], df[param][s:e], marker='o', linewidth=3, markersize=8)
        plt.xlabel('date(month)', fontsize=35, labelpad=10)
        plt.ylabel(param, fontsize=35, labelpad=10)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.show()
        #plt.savefig(f"./fig/fig_non_param_/{param}_{year}")
        s = e
        e += 12
        
else :
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.figure(figsize=(14, 10))
    plt.title('2016-2022', size=45, pad=15)
    plt.plot(df['date'], df[param], marker='o', linewidth=3, markersize=8)
    plt.xlabel('date(year)', fontsize=35, labelpad=10)
    plt.ylabel(param, fontsize=35, labelpad=10)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    #plt.show()
    plt.savefig(f"./fig_non_param_/{param}_yearly")