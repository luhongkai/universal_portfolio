import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests


def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    return tickers

tickers = save_sp500_tickers()
print(tickers)



def get_data_from_yahoo(reload_sp500=False):
    ticker_count = 0
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("Users/jennyhung/MathfreakData/Research/MyResearch/UniversalPortfolio/Code/universal_portfolio/universal_portfolio/util/sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('Users/jennyhung/MathfreakData/Research/MyResearch/UniversalPortfolio/Code/universal_portfolio/universal_portfolio/util/stock_dfs'):
        os.makedirs('Users/jennyhung/MathfreakData/Research/MyResearch/UniversalPortfolio/Code/universal_portfolio/universal_portfolio/util/stock_dfs')

    start = dt.datetime(2008, 1, 1)
    end = dt.datetime(2016, 12, 31)

    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('Users/jennyhung/MathfreakData/Research/MyResearch/UniversalPortfolio/Code/universal_portfolio/universal_portfolio/util/stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker, "yahoo", start, end)
                df.to_csv('Users/jennyhung/MathfreakData/Research/MyResearch/UniversalPortfolio/Code/universal_portfolio/universal_portfolio/util/stock_dfs/{}.csv'.format(ticker))
                ticker_count += 1
            except:
                continue
        else:
            print('Already have {}'.format(ticker))

    print('Total number of tickers (S&P500): ' + str(len(tickers)))
    print('Total number of processed tickers (S&P500): ' + ticker_count)


get_data_from_yahoo(True)
