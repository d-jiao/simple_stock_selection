import pandas as pd
import numpy as np
import warnings
from utils_data import *
from utils_analytics import *
warnings.filterwarnings("ignore")

def pnl_calc(stock_oos, hs300_oos, zz500_oos, tickers, beta):
    stock_oos['ret'] = stock_oos.groupby('ticker')['close'].pct_change()
    stock_oos = stock_oos.replace([np.inf, -np.inf], np.nan)
    ret_oos = stock_oos.pivot(index='ticker', columns='date', values='ret').fillna(0)
    tickers_ = np.setdiff1d(tickers, ret_oos.index)
    for ticker_ in tickers_:
        ret_oos.loc[ticker_] = 0

    hs300_oos['ret'] = hs300_oos.close.pct_change()
    zz500_oos['ret'] = zz500_oos.close.pct_change()
    ret_mkt_oos = pd.concat([hs300_oos.ret, zz500_oos.ret], axis=1)
    ret_mkt_oos = ret_mkt_oos.replace([np.inf, -np.inf], np.nan)
    ret_mkt_oos = ret_mkt_oos.fillna(0)

    ret_portfolio = ret_oos.mean().values
    ret_hedged = np.dot(ret_mkt_oos, beta)
    ret_ = ret_portfolio - ret_hedged
    return ret_


def back_test(years, stock_df, hs300, zz500):
    dates = np.array([])
    dates_all = np.array([])
    ret = np.array([])
    pos = pd.DataFrame(columns=np.append(['HS300', 'ZZ500'], stock_df.ticker.unique()))

    lookback = 12
    i = 0
    end = stock_df.date.max()

    for year in years:
        print('Doing Year', year)
        for month in range(1, 13):
            i += 1
            dates = np.append(dates, year * 1e4 + month * 1e2 + 1)

            if dates[-1] >= end:
                break

            if i <= lookback:
                continue

            is_start = dates[-lookback - 1]
            is_end = dates[-1]
            oos_start = is_end
            oos_end = is_end + 31

            # get in-sample data
            stock_is = stock_df.loc[find_dates(is_start, is_end, stock_df.date)]
            hs300_is = hs300.loc[find_dates(is_start, is_end, hs300.date)]
            zz500_is = zz500.loc[find_dates(is_start, is_end, zz500.date)]

            # get out-of-sample data
            stock_oos = stock_df.loc[find_dates(oos_start, oos_end, stock_df.date)]
            hs300_oos = hs300.loc[find_dates(oos_start, oos_end, hs300.date)]
            zz500_oos = zz500.loc[find_dates(oos_start, oos_end, zz500.date)]

            # do stock selection
            tickers = select_stock(stock_is)

            # do beta calculation
            beta = get_beta(stock_is, hs300_is, zz500_is, tickers)

            # do oos back-testing
            ret_ = pnl_calc(stock_oos, hs300_oos, zz500_oos, tickers, beta)
            ret = np.append(ret, ret_)

            # document the positions
            pos.loc[int(dates[-1]), tickers] = 1
            pos.loc[int(dates[-1]), ['HS300', 'ZZ500']] = beta
            dates_all = np.append(dates_all, hs300_oos.date)

        if dates[-1] >= end:
            break

    return pos, ret, dates_all