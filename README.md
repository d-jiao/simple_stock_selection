# simple_stock_selection
A simple stock selection and back testing model using ridge regression and principle component analysis.

## Code Structure
- main.py: the entry of the back-test analytics which runs all the functions of interest;
- utils_analytics.py: the functions to conduct data analysis on top of the cleaned dataset;
- utils_data.py: the functions to fetch and clean the data;
- utils_test.py: the functions to run the back test;
- utils_visual.py: the functions to visualize the results. 

## Work Flow
- As a first step, we read the data and do some preprocessing. In this step, the column of "est_pb_fttm", with all values being NaN's, is dropped. We also calculate the daily return of the stocks using close price to run the analysis afterwards;
- In this stock selection strategy, we use a look-back window of 1 year (12 months, this number can be tuned if necessary with cross validation) and do monthly rebalancing;
- During each look-back period, we drop NaN's from the training set. The rationale here is after dropping the empty values, we still get a pool of over 1,000 stocks, which are adequate for diversification. We run a panel ridge regression for the 1-month forward return on the first principle component of the features. The model from the training set can predict the future 1-month daily returns of each stock;
- Based on the predicted returns, we select the top 100 (again this number could be tuned if necessary) stocks with maximum 1-month cummulative return, and construct an equal-weighted portfolio. We do not choose a, say, mimimum-vol portfolio for simplicity;
- After the portfolio is constructed, we hedge the portfolio from market betas to chase the return from alpha. To hedge the portfolio, we use the OLS betas on HS300 and ZZ500 from the training set.
- The back-test runs from 2012-01-01 to 2017-08-14.

## Summary of Back-Test
### The cumulative PnL
![image](https://github.com/d-jiao/simple_stock_selection/blob/master/pnl.png)
### Performance Metrics
- The average annual return is 16.19%
- The average annual volatility is 16.73%
- The maximum drawdown is 51.57%
- The annualized Sharpe ratio is 0.9675
- The annualized Sortino ratio is 1.0541
- The Sterling ratio is 0.0012
### Conclusion and Outlook
This simple stock seletion model achieves decent out-of-sample performance in the back-testing period. The model does not require a great number of parameters to be tuned and is thus free of data mining / over-fitting.   
We believe with a good estimation for the covariance matrix using factor models, the performance would be enhanced be constructing a minimum-vol portfolio. 
