# import time
# import datetime
# import pandas as pd
# import yfinance as yf
# ticker = 'AAPL'
# # # time.mktime converts the datetime to second value
# # start_date = int(time.mktime(datetime.datetime(2020, 1, 1 ,23 , 59).timetuple()))
# # end_date = int(time.mktime(datetime.datetime(2020, 12, 31 ,23 , 59).timetuple()))
# # interval = '1d'
# # url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_date}&period2={end_date}&interval={interval}&events=history&includeAdjustedClose=true'
# # df = pd.read_csv(url)
# start_date = '2020-01-01'
# end_date = '2020-12-31'
# cryptocurrencies = ['BTC-USD', 'ETH-USD', 'XRP-USD','DOGE-USD']
# for i in range(4):
#     tickerData = yf.Ticker(cryptocurrencies[i])
#     tickerDf = tickerData.history(period = '1d', start = start_date, end = end_date)
import datetime
import numpy as np
import pandas.io as web
from scipy.stats import norm
import pandas as pd
import yfinance as yf



def var_cov_var(P, c, mu, sigma):
    """
    Variance-Covariance calculation of daily Value-at-Risk
    using confidence level c, with mean of returns mu
    and standard deviation of returns sigma, on a portfolio
    of value P.
    """
    alpha = norm.ppf(1-c, mu, sigma)
    return P - P*(alpha + 1)

if __name__ == "__main__":
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2014, 1, 1)

    citi = web.DataReader("C", 'yahoo', start, end)
    citi["rets"] = citi["Adj Close"].pct_change()

    P = 1e6   # 1,000,000 USD
    c = 0.99  # 99% confidence interval
    mu = np.mean(citi["rets"])
    sigma = np.std(citi["rets"])

    var = var_cov_var(P, c, mu, sigma)
    print("Value-at-Risk: $%0.2f" % var)