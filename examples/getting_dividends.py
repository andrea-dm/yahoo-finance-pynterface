# 
# Copyright (c) 2018 Andera del Monaco
#
# The following example shows how to import the Yahoo Finance Python Interface
# into your own script, and how to use it.
# 
# In particular, we will download the timeseries of APPLE close daily price from 2017-09-1 to 2018-08-31,
# and then will plot them using the matplotlib package.
# In order to illustrate the implementation of pandas.DataFrame within the YahooFinancePynterface, 
# we will plot the 20-periods simple moving avarege on the same figure.
#

import yahoo_finance_pynterface as yahoo
import datetime                 as dt
import matplotlib.pyplot        as plt
import matplotlib.ticker        as mticker

if __name__ == '__main__':
    fig, ax = plt.subplots(1)

    ticker = "AAPL";
    r,_ = yahoo.Get.Dividends(ticker, period=['1998-09-1','2018-08-31']);
    if len(r)>0:
        r.plot(kind='bar', ax=ax);
        ticklabels = [item.strftime('%Y-%m-%d') for item in r.index];
        ax.grid(True, alpha=0.2)
        ax.xaxis.set_major_formatter(mticker.FixedFormatter(ticklabels));
        print(r)
    else:
        print("something odd happened o.O")
    
    plt.gcf().autofmt_xdate()
    plt.show();


