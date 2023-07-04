import pandas as pd
import numpy as np


df = pd.read_csv('non_extreme_params_yearly_90.csv')
mu = np.log(np.array(df['mu']).astype('float'))
sig = np.log(np.array(df['sigma']).astype('float'))
# get skewness (exp(std*std)+2)sqrt(exp(std*std)-1)

skewness = (np.exp(sig*sig)+2)*np.sqrt(np.exp(sig*sig)-1)
df['skew'] = skewness

# get mean (exp(mu + sig*sig/2))
mean = np.exp(mu + sig*sig/2)
# get variane (exp(sig*sig)-1)*exp(2*mu+sig*sig)
var = (np.exp(sig*sig)-1)*np.exp(2*mu+sig*sig)
df['mu'] = mu
df['sigma'] = sig
df['mean'] = mean
df['var'] = var
df['mode'] = np.exp(mu - sig*sig)

df.to_csv('non_extreme_params_yearly_90_.csv')