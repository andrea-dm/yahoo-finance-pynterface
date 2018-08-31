**Yahoo Finance Python Interface**
===================

 [Yahoo Finance](https://finance.yahoo.com/) is by far the most popular (_and free!_) resource for financial data. 

Many packages have been distributed to provide access to such a resource lately.
The most recent projects among them were actually addressing the changes that the Yahoo Team made in May, 2017. 

**yahoo-finance-pynterface** has been intended to provide a completely new interface to Yahoo Finance,
and it is meant to offer effective methods to interact with its API. 

Even if a stable release is available, the project has yet to be considered "complete" and many other features has yet to come!
Please, drop me an email if any comment/suggestion/remark pops up in your mind :)


Getting Started
-------------

Basic usage:

```python
    import yahoo_finance_pynterface as yfi
    
    data = yfi.Get.Prices("AAPL")
```
