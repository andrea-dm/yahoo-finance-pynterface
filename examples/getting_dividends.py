# 
# Copyright (c) 2018 Andera del Monaco
#
# The following example shows how to import the Yahoo Finance Python Interface
# into your own script, and how to use it.
# 
# In particular, we will download the timeseries of APPLE dividends of the last 10 years.
# The result wil be plotted as bar chart using matplotlib together with seaborn.
#

import yahoo_finance_pynterface as yahoo
import matplotlib.pyplot        as plt
import matplotlib.ticker        as mticker
import seaborn                  as sns

sns.set_style('darkgrid')
sns.set_palette('pastel')

if __name__ == '__main__':
    fig, ax = plt.subplots(1)
    
    r = yahoo.Get.Dividends("AAPL", period=['1998-09-1','2018-08-31']);
    if r is not None:
        r.index.name = "";
        r.plot(kind='bar', ax=ax, color='orange', zorder=100);
        ax.xaxis.set_major_formatter(mticker.FixedFormatter([item.strftime('%Y-%m-%d') for item in r.index]));
        ax.grid(axis='x')
        print(r);
    else:
        print("something odd happened o.O");
    
    plt.title("Apple Inc.: Dividends")
    plt.gcf().autofmt_xdate();
    plt.show();


