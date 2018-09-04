# 
# Copyright (c) 2018 Andera del Monaco
#
# The following example shows how to import the Yahoo Finance Python Interface
# into your own script, and how to use it.
# 
# In particular, we will download the timeseries of APPLE close daily price from 2017-09-1 to 2018-08-31,
# and then will plot them using the matplotlib package.
# In order to illustrate the implementation of pandas.DataFrame within the YahooFinancePynterface, 
# we will plot the 20-periods Bollinger bands on the same figure.
#

import yahoo_finance_pynterface as yahoo
import matplotlib.pyplot        as plt
import matplotlib.dates         as mdates
import matplotlib.ticker        as mticker

if __name__ == '__main__':

    fig, ax = plt.subplots(1);
    
    r = yahoo.Get.Prices("AAPL", period=['2017-09-1','2018-08-31']);
    if r is not None:
        mu = r.Close.rolling(20).mean()
        sigma = r.Close.rolling(20).std()
        plt.fill_between(r.index.values,mu+2*sigma,mu-2*sigma, color='moccasin');
        plt.plot(r.index.values, mu, color='orange');
        plt.plot(r.index.values, r.Close, color='dodgerblue');
        ax.grid(True, alpha=0.5);
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1));
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'));     
        ax.yaxis.set_major_locator(mticker.FixedLocator(range(100,300,10)))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,pos: f"{x}.00 $"))
        print(r.Close);
    else:
        print("something odd happened o.O");
    
    plt.gcf().autofmt_xdate();
    plt.show();

