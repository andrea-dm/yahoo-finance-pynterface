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
import matplotlib.pyplot        as plt
import matplotlib.dates         as mdates

if __name__ == '__main__':
    fig, ax = plt.subplots(1);
    
    r,_ = yahoo.Get.Prices("AAPL", period=['2017-09-1','2018-08-31']);
    if len(r)>0:
        plt.plot(r.index.values, r['Close']);
        plt.plot(r.index.values, r['Close'].rolling(20).mean());
        ax.grid(True, alpha=0.5);
        ax.set_yticklabels([f"{i*20}.00 $" for i in range(6,15)]);
        ax.xaxis.set_major_locator(mdates.MonthLocator());
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'));
        print(r['Close']);
    else:
        print("something odd happened o.O");
    
    fig.autofmt_xdate();
    plt.show();

