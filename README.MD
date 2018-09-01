# Yahoo Finance Python Interface


**yahoo-finance-pynterface** is a Python package that provide a new interface to the Yahoo Finance API.

Check the [Wiki Page](https://github.com/andrea-dm/yahoo-finance-pynterface/wiki) for a quick reference.


### Motivation
 [Yahoo Finance](https://finance.yahoo.com/) is by far the most popular (_and free!_) resource for financial data. 

Many packages have been distributed to provide access to such a resource in the recent past.
However, most of such projects were aiming at filling the gap that the changes made in May, 2017 by the Yahoo Team left behind.

**yahoo-finance-pynterface** has been intended to provide a completely new interface to Yahoo Finance,
and it is meant to offer effective methods to interact with its API. 


### About
**yahoo-finance-pynterface** is based on [pandas](https://pandas.pydata.org/).
| Hence, most of the data retrieved are returned as _pandas_.**DataFrame** object. 

Even if a stable release is available, the project has yet to be considered "complete" and many other features has yet to come!
Please, drop me an email if any comment/suggestion/remark pops up in your mind :)


### Requirements
**yahoo-finance-pynterface** is currently working on `Python >= 3.6` only. 
| Any help to add support for `Python == 2.x` is welcome and encouraged as well as very much appreciated! `<addr>`

Furthermore, the following packages are required:

- `requests >= 2.19.1`
- `pandas >= 0.23.4`
- `numpy >= 1.15.1`
- `pytz >= 2018.5`
- `dateutil >= 2.7.3`
- `aenum >= 2.1.2`


### Change Log

**Version 1.0.1** (_August 31, 2018_)
	First stable release
