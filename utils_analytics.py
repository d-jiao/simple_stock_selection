import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings("ignore")

clf = linear_model.Ridge(alpha=0.01)
linreg = linear_model.LinearRegression()
pca = PCA(n_components=1)

def select_stock(stock_is):
    stock_is['ret'] = stock_is.groupby('ticker')['close'].pct_change()
    stock_is = stock_is.replace([np.inf, -np.inf], np.nan)
    stock_is = stock_is.dropna()
    stock_is['fwd_ret'] = stock_is.groupby('ticker')['ret'].shift(-20)

    tickers = stock_is.groupby('ticker').tail(20)['ticker']
    x_ = stock_is.groupby('ticker').tail(20).drop(['ticker', 'date', 'fwd_ret'], axis=1)
    x = stock_is.dropna().drop(['ticker', 'date', 'fwd_ret'], axis=1)

    pca.fit(x.append(x_))
    x_pca = pca.fit_transform(x)
    clf.fit(x_pca, stock_is['fwd_ret'].dropna())
    x_pca_ = pca.fit_transform(x_)

    pred_ret = pd.concat([pd.Series(tickers.values), pd.Series(clf.predict(x_pca_))], axis=1, ignore_index=True)
    pred_ret.columns = ['ticker', 'ret']
    pred_ret.ret += 1

    pred_ret_agg = pd.concat([pred_ret.drop('ret', axis=1), pred_ret.groupby('ticker').agg('cumprod')], axis=1)
    pred_ret_agg = pred_ret_agg.groupby('ticker').tail(1).sort_values('ret')
    tickers = pred_ret_agg.ticker[-100:].values
    return tickers


def get_beta(stock_is, hs300_is, zz500_is, tickers):
    stock_is['ret'] = stock_is.groupby('ticker')['close'].pct_change()
    stock_is = stock_is.replace([np.inf, -np.inf], np.nan)
    stock_is = stock_is.dropna()

    ret_is = stock_is.pivot(index='ticker', columns='date', values='ret').fillna(0)
    ret_is = ret_is.loc[ret_is.index.isin(tickers)]

    hs300_is['ret'] = hs300_is.close.pct_change()
    zz500_is['ret'] = zz500_is.close.pct_change()
    hs300_is = hs300_is.set_index('date')
    zz500_is = zz500_is.set_index('date')
    ret_is = ret_is.append(hs300_is.ret)
    ret_is = ret_is.append(zz500_is.ret)
    ret_is = ret_is.replace([np.inf, -np.inf], np.nan)
    ret_is = ret_is.dropna(axis=1)

    y = ret_is.iloc[:-2, :].mean().values
    x = ret_is.iloc[-2:, :].values
    linreg.fit(x.T, y)
    beta = linreg.coef_
    return beta