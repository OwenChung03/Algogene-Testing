import matplotlib.pyplot as plt
import yfinance as yf
import datetime
import pandas as pd
import statsmodels.tsa.stattools as ts
from scipy.stats import linregress
# Attributes to change
year_start = 2020
year_end = 2020
cryptocurrencies = ['BTC-USD', 'ETH-USD', 'XRP-USD','DOGE-USD']
data_lst = ['BTC', 'ETH', 'XRP', 'DOGE']
choice1 = cryptocurrencies[0]
choice2 = cryptocurrencies[1]

# Functions
def download_data(crypto, start, end):
    crypto_data = {}
    ticker = yf.download(crypto, start, end)
    crypto_data['price'] = ticker['Adj Close']
    return pd.DataFrame(crypto_data)

def plot_pairs(data1, data2):
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle(f'{choice1} and {choice2} graph')
    ax1.plot(data1)
    ax2.plot(data2)
    plt.show()
    
def scatter_plot(data1, data2):
    plt.scatter(data1.values, data2.values)
    plt.xlabel(choice1)
    plt.ylabel(choice2)
    plt.show()

if __name__ == '__main__':
    start_date = datetime.datetime(year_start, 1, 1)
    end_date = datetime.datetime(year_end, 12, 31)
    pair1 = download_data(choice1, start_date, end_date)
    pair2 = download_data(choice2, start_date, end_date)

    plot_pairs(pair1, pair2)
    scatter_plot(pair1, pair2)

    # Linear Regression
    result = linregress(pair1.values[:, 0], pair2.values[:, 0]) # [:, 0] can turn 2D array to 1D array

    # Create the residual series
    residuals = pair1 - result.slope * pair2 
    # We can find a constant Beta such that y - (Beta)x = I(0) is a stationary process
    # If we can find a Beta Parameter then x(t) and y(t) are cointergrated so there may be a true long term relationship between these variables

    # Conduct Augmented-Dickey-Fuller Test (tests null hypothesis that a unit root is present in a time series sample)
    adf = ts.adfuller(residuals)
    print(adf)
    
    # Set Critical Values to be 95% confidence interval
    confidence = adf[0]
    confidence_level = adf[1]
    pct1_z = adf[4]['1%']
    pct5_z = adf[4]['5%']
    pct10_z = adf[4]['10%']
    if pct10_z < confidence:
        print(f'low confidence level at {adf[1]}, {choice1} and {choice2} are not cointegrated.')
    elif pct5_z < confidence:
        print(f'It is 90% confident that {choice1} and {choice2} are cointegrated. ')
    elif pct1_z < confidence:
        print(f'It is 95% confident that {choice1} and {choice2} are cointegrated. ')
    else:
        print(f'It is 99% confident that {choice1} and {choice2} are cointegrated. ')

