import pandas as pd
import numpy as np
import warnings
import datetime
warnings.filterwarnings("ignore")

def find_dates(start, end, date_full):
    ind = np.logical_and((date_full - start) >= 0, (date_full - end) < 0)
    return ind

def get_dates(dates):
    dates_all = np.array([])
    for i in range(len(dates)):
        year = int(dates[i] / 10000)
        month = int(dates[i] / 100) % 100
        day = int(dates[i] % 100)
        dates_all = np.append(dates_all, datetime.date(year, month, day))
    return dates_all

def get_data(root='z:/share/data/test_data/'):
    dates = pd.read_csv(root + './data/calendar.csv')
    hs300 = pd.read_csv(root + './data/000300_index.csv')
    zz500 = pd.read_csv(root + './data/000905_index.csv')
    st_stock = pd.read_csv(root + './data/st_stock.csv')
    all_stock = pd.read_csv(root + './data/summary.csv')

    stock_df = pd.DataFrame()
    for ticker in all_stock.symbol:
        if ticker in st_stock.symbol.values:
            continue
        stock_df_ = pd.read_csv('./data/' + ticker + '.csv')
        stock_df_['ticker'] = ticker
        stock_df = stock_df.append(stock_df_)

    stock_df = stock_df.reset_index().drop('index', axis=1)
    stock_df = stock_df.drop('est_pb_fttm', axis=1)

    return stock_df, hs300, zz500

def sharpe(ret):
    sharpe = ret.mean() / ret.std() * np.sqrt(252)
    return sharpe

def sortino(ret, thresh = 0):
    sortino = ret.mean() / ret[ret < thresh].std() * np.sqrt(252)
    return sortino

def mmd(ret):
    cumret = (ret + 1).cumprod()
    mmd = max(pd.Series(cumret).cummax() - cumret)
    return mmd

def sterling(ret):
    m = mmd(ret)
    sterling = ret.mean()/m
    return sterling