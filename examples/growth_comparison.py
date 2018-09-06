# 
# Copyright (c) 2018 Andera del Monaco
#
# The following example shows how to import the Yahoo Finance Python Interface
# into your own script, and how to use it together with pandas.
# 
# In particular, we will download the timeseries of three different stocks close daily price from 2008-01-01 to 2018-08-31,
# and then will plot their growth evolution in a line chart using matplotlib.
#

import yahoo_finance_pynterface as yahoo
import pandas                   as pd

import matplotlib.pyplot        as plt
import matplotlib.dates         as mdates
import matplotlib.ticker        as mticker

if __name__ == '__main__':
    
    fig, ax = plt.subplots(1);

    tickers = ["AAPL", "GOOGL", "AMZN"];    
    
    data = yahoo.Get.Prices(tickers, interval="1mo", period=['2008-1-1','2018-08-31']);

    assets = pd.DataFrame({ticker:(df['Adj Close'].pct_change()+1).cumprod() for ticker,df in data.items()});
    assets.index.name = "";
    assets.plot(ax=ax, title="A growth comparison since January, 2008");

    ax.grid(True, alpha=0.5);    
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6));
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'));
    ax.yaxis.set_major_locator(mticker.FixedLocator(range(1,36,5)));
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,pos: f"{x-1} %" if x>1 else "0 %" if x==1 else ""));

    plt.legend();
    plt.gcf().autofmt_xdate();
    plt.show()

