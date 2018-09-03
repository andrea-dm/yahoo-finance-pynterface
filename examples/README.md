# Yahoo Finance Python Interface


In this folder you may find several examples (and many other have yet to come!) showing how the **yahoo-finance-pynterface** works.


<br />


## `getting_prices.py`
This script will download the timeseries of Apple Inc. close daily price from September, 1st 2017 to August, 31st 2018,<br />
and then it will plot it in a line chart using the `matplotlib` package.<br />
In order to illustrate the implementation of `pandas.DataFrame` within the **yahoo-finance-pynterface**,<br />
the 20-periods simple moving avarege will be plotted on the same figure as well, as the picture below is showing.
![result](resources/getting_prices.png)


<br />


## `getting_dividends.py`
This script will download the timeseries of Apple Inc. dividends of the last 10 years.<br />
The result will be then plotted as bar chart using pandas' internal plotting system, as the picture below shows.
![result](resources/getting_dividends.png)


<br />


## `getting_stock_splits.py`
This script will download the timeseries of Apple Inc. stock splits since January, 1st 1980 via the api 'download',<br />
and then it will print the data on screen.<br />
<br />
![result](resources/getting_splits.png)
