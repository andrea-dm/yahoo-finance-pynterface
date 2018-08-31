Yahoo Finance Python Interface
===================

 [Yahoo Finance](https://finance.yahoo.com/) is by far the most popular (_and free!_) resource for financial data. 

Many packages have been distributed to provide access to such a resource in the recent past.
However, most of such projects were addressing the problem that arose within the community after the changes made in May, 2017 by the Yahoo Team.

**yahoo-finance-pynterface** has been intended to provide a completely new interface to Yahoo Finance,
and it is meant to offer effective methods to interact with its API. 

Even if a stable release is available, the project has yet to be considered "complete" and many other features has yet to come!
Please, drop me an email if any comment/suggestion/remark pops up in your mind :)


About
-------------------

**yahoo-finance-pynterface** is based on [pandas](https://pandas.pydata.org/).
Hence, most of the data returned are stored in a _pandas_.**DataFrame**.



Getting Started
-------------------

Basic usage:

```python
    import yahoo_finance_pynterface as yahoo
    
    data = yahoo.Get.Prices("AAPL")
```

Check the "examples" folder for further _examples_!
