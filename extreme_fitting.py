import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func_powerlaw(x, Alpha, C):
    return x**(-Alpha) * C


#df = pd.read_csv('./dy2016-2022.csv', encoding='ms949')
df = pd.read_csv('./dm2016-2022.csv', encoding='ms949')
result = pd.DataFrame()
cut = 0.9
alpha = []
for date in df.columns:
    try : int(date)
    except: continue
    print(date)
    nbins = 60
    prices = df[date].dropna().tolist()
    prices.sort()
    data = prices[int(len(prices) * cut):]
    
    counts, bin_edges  = np.histogram(data, nbins, normed=True) 
        
    popt, pcov = curve_fit(func_powerlaw, bin_edges[:-1], counts, maxfev = 50000)
    # popt = [Alpha, C]
    # pconv = [popt[0]의 covariance, popt[1]의 covariance]
    alpha.append(popt[0])
    
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.figure(figsize=(12, 10))
    plt.title(date, size=30)
    plt.xlabel('apartment price', size=22, labelpad=15) # fontdict = 폰트 지정
    plt.ylabel('alpha', size=22, labelpad=15)
    plt.xticks(fontsize=18)
    #plt.xlim([700, 5500])
    #plt.ylim([0, 0.0045])
    plt.yticks(fontsize=18)
    plt.plot(bin_edges[:-1], counts, color='b', marker='o', linestyle='None', markersize=5, markeredgecolor='b', label='extreme data')
    plt.plot(bin_edges[:-1], func_powerlaw(bin_edges[:-1], popt[0], popt[1]), linewidth=2, color='r', label=f'power-law \nalpha={round(popt[0], 3)}')
    plt.legend(fontsize=18)
    #plt.savefig(f'./fig_year/fig_{date}')
    #plt.savefig(f'./fig_month/fig_{date}')
    #plt.clf() # clear figure
    plt.show()
    


"""
# estimate parameters for extreme data
result['date'] = df.columns[2:]
result['alpha'] = alpha
result.set_index('date', inplace=True)
result.to_csv(f'./extreme_param_yearly_{str(int(cut*100))}.csv', encoding='ms949')
#result.to_csv(f'./extreme_param_monthly_{str(int(cut*100))}.csv', encoding='ms949')"""