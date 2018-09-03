# 
# Copyright (c) 2018 Andera del Monaco
#
# The following example shows how to import the Yahoo Finance Python Interface
# into your own script, and how to use it.
# 
# In particular, we will download the timeseries of APPLE stock splits since January, 1st 1980
# via the api 'download'.
#

import yahoo_finance_pynterface as yahoo

if __name__ == '__main__':

    r = yahoo.Get.Splits("AAPL", period=['1980-1-1','2018-08-31'], using_api=yahoo.api.AccessMode.DOWNLOAD);
    print(r if len(r)>0 else "something odd happened o.O");



