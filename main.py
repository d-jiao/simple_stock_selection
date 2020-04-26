import pandas as pd
from utils_test import *
from utils_visual import *

def main():
    years = range(2012, 2019)
    # stock_df, hs300, zz500 = get_data()
    hs300 = pd.read_csv('./data/000300_index.csv')
    zz500 = pd.read_csv('./data/000905_index.csv')
    stock_df = pd.read_csv('stock_df.csv', index_col=0)
    stock_df = stock_df.drop('est_pb_fttm', axis=1)

    pos, ret, dates = back_test(years, stock_df, hs300, zz500)
    pos = pos.fillna(1)
    pos.to_csv('positions.csv')
    dates = get_dates(dates)
    plot_pnl(ret, dates)

    print('The average annual return is %.2f%%' % (ret.mean() * 252 * 100))
    print('The average annual volatility is %.2f%%' % (ret.std() * np.sqrt(252) * 100))
    print('The maximum drawdown is %.2f%%' % (mmd(ret) * 100))
    print('The annualized Sharpe ratio is %.4f' % sharpe(ret))
    print('The annualized Sortino ratio is %.4f' % sortino(ret))
    print('The Sterling ratio is %.4f' % sterling(ret))

if __name__ == '__main__':
    main()