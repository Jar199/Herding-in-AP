import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import math 

class MLE():
    def __init__(self, samples, m, std, learning_rate, epochs, verbose=False):
        """
        :param samples: samples for get MLE
        :param learning_rate: alpha on weight update
        :param epochs: training epochs
        :param verbose: print status
        """
        self._samples = samples
        self._m = m
        self._std = std
        self._learning_rate = learning_rate
        self._epochs = epochs
        self._verbose = verbose


    def likelihood(self, x, M):
        """
        Probability Density Function is Normal distribution
        PDF's y is same as likelihood

        :param x:
        :return: likelihood of input x (likelihood of input x is same as y of pdf)
        """

        #return  1/(x * self._std * math.sqrt(2*math.pi)) * np.exp( -(np.log(x) - M)**2/(2*self._std **2))
        return M * (x/self._std)**(M-1) * np.exp(-(x/self._std)**M)

    def fit(self):
        """
        training estimator
        M, which minimizes Likelihood, is obtained by the gradient descent method.
        M is the MLE of the samples
        """

        # init M
        self._estimator = np.random.normal(self._m, self._std, 1)

        # train while epochs
        self._training_process = []
        for epoch in range(self._epochs):
            likelihood = np.prod(self.likelihood(self._samples, self._m))
            prediction = np.prod(self.likelihood(self._samples, self._estimator))
            cost = self.cost(likelihood, prediction)
            self._training_process.append((epoch, cost))
            self.update(self._samples, self._estimator)

            # print status
            #if self._verbose == True and ((epoch + 1) % 10 == 0):
            #    print("Iteration: %d ; cost = %.4f" % (epoch + 1, cost))


    def cost(self, likelihood, prediction):
        """
        cost function
        :param likelihood: likelihood of population
        :param prediction: likelihood in samples
        :return: the cost of optimizing the parameters
        """
        return math.sqrt(likelihood - prediction)


    def update(self, x, M):
        """
        update in gradient descent
        gradient is approximated
        :param x: samples
        :param M: estimator
        """
        gradient = np.sum(np.exp(-(np.power(x - M, 2) / (2*math.pow(self._std, 2)))))
        if self._m > self._estimator:
            self._estimator += self._learning_rate * gradient
        else:
            self._estimator -= self._learning_rate * gradient


    def get_mle(self):
        """
        parameter getter
        :return: estimator of MLE
        """
        return self._estimator

df = pd.read_csv('./dm2016-2022.csv', encoding='ms949')
result_df = pd.DataFrame()
cut = 0.9
alpha = []
mean = []
sig = []
cut_off = []

for date in df.columns:
    try : int(date)
    except: continue
    print(date)
    nbins = 45
    prices = df[date].dropna().tolist()
    prices.sort()
    data = prices[:int(len(prices) * cut)]
    cut_off.append(prices[int(len(prices) * cut) - 1])
    
    shape, loc , scale = scipy.stats.lognorm.fit(data, floc = 0)
    counts, bin_edges  = np.histogram(data, nbins, normed=True) 
    sample = np.linspace(0, np.max(np.array(data)), nbins)
    fitted = scipy.stats.lognorm.pdf(sample, shape, loc=loc, scale=scale)\
    
    
    plt.figure(figsize=(12, 9)) 
    estimator = MLE(data, scale, shape, learning_rate=0.1, epochs=30, verbose=True)
    estimator.fit()
    result = estimator.get_mle()
    mu = round(estimator._m, 2)
    std = round(estimator._std, 2)
    mean.append(mu)
    sig.append(std)
    plt.title(date, size=30)
    plt.yticks(fontsize=18)
    #plt.xlim([0, 1500])
    #plt.ylim([0, 0.004])
    plt.plot(bin_edges[:-1], counts, color='b', marker='o', linestyle='None', markersize=5, markeredgecolor='b', label='non-extreme data')
    #plt.plot(sample, counts, color='b', marker='o', linestyle='None', markersize=5, markeredgecolor='b', label='non-extreme data')
    plt.plot(sample, fitted, linewidth=5, color='r', label=f'log-normal \n(mu, sig)=({mu}, {std})')
    #Mean = math.exp(mu + std*std/2)
    plt.axvline(mu, 0, 1, color='lightgray', linestyle='--')
    plt.legend()

    plt.show()
    #plt.savefig(f'./fig_log_normal_month/fig_{date}')
    
"""result_df['date'] = df.columns[1:]
result_df['mean'] = mean
result_df['sigma'] = sig
result_df['cut_off'] = cut_off

result_df.to_csv('./non_extreme_params_monthly_90.csv', encoding='ms949', index=False)"""