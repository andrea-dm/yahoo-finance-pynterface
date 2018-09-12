# Yahoo Finance Python Interface
![PyPI - Python Version](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg?longCache=true&style=flat) ![PyPI - Package Version](https://img.shields.io/badge/pypi-1.0.2-blue.svg?longCache=true&style=flat) ![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg) ![Status - Stable](https://img.shields.io/badge/status-stable-brightgreen.svg?longCache=true&style=flat)

**yahoo-finance-pynterface** is a Python package that provides a new interface to the Yahoo Finance API.

<br />

## Motivation
 [Yahoo Finance](https://finance.yahoo.com/) is by far the most popular (_and free!_) resource for financial data. 

Many packages have been distributed to provide access to such a resource in the recent past.<br />
However, most of such projects were aiming at filling the gap that the changes made in May, 2017 by the Yahoo Team left behind.

**yahoo-finance-pynterface** has been intended to provide a completely new interface to Yahoo Finance,<br />
and it is meant to offer effective methods to interact with its API. 

<br />

## About
**yahoo-finance-pynterface** makes an extensive use of [pandas](https://pandas.pydata.org/).<br />
As a consequence, most of the data retrieved are returned as `pandas.DataFrame` objects. 

Even if a stable release is available, the project has yet to be considered "complete" and many other features has yet to come!
Please, drop me an email if any comment/suggestion/remark pops up in your mind :)

<br />

## Requirements
**yahoo-finance-pynterface** is currently working on `Python >= 3.5` only. <br />
Any help to add support for `Python == 2.x` is welcome and encouraged as well as very much appreciated!

Furthermore, the following packages are required:

- `requests >= 2.19.1`
- `pandas >= 0.23.4`
- `numpy >= 1.15.1`
- `pytz >= 2018.5`
- `dateutil >= 2.7.3`
- `aenum >= 2.1.2`

<br />

## Installation
Use `pip` to install **yahoo_finance_pynterface**:

```python
   pip install yahoo-finance-pynterface
```

<br />

## Documentation
For a quick reference, navigate to the [Wiki Page](https://github.com/andrea-dm/yahoo-finance-pynterface/wiki).<br />
And do not forget to check the [examples](https://github.com/andrea-dm/yahoo-finance-pynterface/tree/master/examples)!

<br />

## Change Log
 _September 12, 2018_ <br />
&nbsp;&nbsp; **Version 1.0.2** <br />
&nbsp;&nbsp;&nbsp;&nbsp; Fixed type hints

 _August 31, 2018_ <br />
&nbsp;&nbsp; **Version 1.0.1** <br />
&nbsp;&nbsp;&nbsp;&nbsp; First stable release

<br />

## Thanks
Seriously, thanks!<br />
-- andrea-dm
