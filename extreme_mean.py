import pandas as pd
import numpy as np


MONTHLY = False

if MONTHLY:
    df = pd.read_csv('./dm2016-2022.csv', encoding='ms949') 
    alphas = pd.read_csv('./extreme_alpha_monthly_90.csv', encoding='ms949')
else: 
    df = pd.read_csv('./dy2016-2022.csv', encoding='ms949') 
    alphas = pd.read_csv('./extreme_alpha_yearly_90.csv', encoding='ms949')

means = []

cols = df.columns
for i in range(1, len(cols)):
    x_min = df[cols[i]].dropna().astype(float).min()
    alpha = alphas['alpha'][i-1]
    means.append((alpha - 1) / (alpha - 2) * x_min)

alphas['mean'] = means

if MONTHLY: alphas.to_csv('./extreme_params_monthly_90.csv', encoding='ms949')
else: alphas.to_csv('./extreme_params_yearly_90.csv', encoding='ms949')