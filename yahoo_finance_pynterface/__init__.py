#!/usr/bin/env python
#
# Yahoo Finance Python Interface
# https://github.com/andrea-dm/yahoo-finance-pynterface
#
# Copyright (c) 2018 Andera del Monaco
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__name__    = "yahoo_finance_pynterface";
__version__ = "1.0.1";
__author__  = "Andrea del Monaco";
__all__     = ['Get'];

import api
import core
import requests
import datetime             as dt
import concurrent.futures   as cf
import pandas               as pd

from typing                 import Tuple, Dict, List, Union, ClassVar, Any, Optional, Type, NoReturn


class Get():
    # Class container that exposes the methods available
    # to interact with the Yahoo Finance API.
    #
    # Such methods are:
    #
    # - With(...) :                 to enable/disable parallel calculations;
    # - CurrentProcessingMode() :   to get the current processing mode;
    # - Info(...) :                 to retrieve basic informations about the ticker such as trading periods, base currency, ...;
    # - Prices(...) :               to get the time series of OHLC prices together with Volumes (and adjusted close prices, when available);
    # - Dividends(...) :            to get the time series of dividends;
    # - Splits(...) :               to get the time series of splits;
    #
    # The above methods should be sufficient for any standard usage.
    # To gain much more control over the data sent back by Yahoo, the following method is implemented:
    #
    # - Data(...) :                 the basic method that is actually pushing the request for data.
    #
    # All the other methods are somewhat relying on it.
   
    __processing_mode__:Type[core.ProcessingMode] = core.ProcessingMode.AUTO;

    @classmethod
    def With(cls, mode:Type[core.ProcessingMode]) -> Optional[NoReturn]:
        if not isinstance(mode,core.ProcessingMode):
            raise TypeError(f"invalid type for the argument 'mode'! <class 'core.ProcessingMode'> expected; got '{type(mode)}'");
        else:
            cls.__processing_mode__ = mode;

    @classmethod
    def CurrentProcessingMode(cls) -> str:
        return str(cls.__processing_mode__);

    @classmethod
    def Info(cls, tickers:Union[str, List[str]]) -> Tuple[Optional[Dict[str,Any]],Optional[List[str]]]: # Union[str,int,float]
        r,f = cls.Data(tickers, "1d", "1y", using_api=api.AccessMode.CHART);
        if len(r)>0:
            unnecessary_infos = ['dataGranularity', 'validRanges'];
            for ticker, data in r.items():
                r[ticker] = core.parser({k:v for k,v in data['meta'].items() if k not in unnecessary_infos});
            return r, f;
        else:
            return None, f;

    @classmethod
    def Prices(cls, tickers:Union[str, List[str]],
            interval:str="1d",
            period:Optional[Union[str,List[Union[str,dt.datetime]]]]=None,
            using_api:Type[api.AccessMode]=api.AccessMode.CHART) -> Tuple[Optional[Union[dict, pd.DataFrame]],Optional[list]]:
        r,f = cls.Data(tickers, interval, period, events=api.EventsInQuery.HISTORY, using_api=using_api);
        if len(r)>0:
            k = 'quotes' if using_api is api.AccessMode.CHART else 'data';
            return ({ticker:data[k] for ticker,data in r.items()}, f) if isinstance(tickers,list) else (r[tickers][k],f);
        else:
            return None, f;

    @classmethod
    def Dividends(cls, tickers:Union[str, List[str]],
            interval:str="1d",
            period:Optional[Union[str,List[Union[str,dt.datetime]]]]=None,
            using_api:Type[api.AccessMode]=api.AccessMode.CHART) -> Tuple[Optional[dict],Optional[list]]:
        r,f = cls.Data(tickers, interval, period, events=api.EventsInQuery.DIVIDENDS, using_api=using_api);
        if len(r)>0:
            k = 'events' if using_api is api.AccessMode.CHART else 'data';
            return ({ticker:data[k] for ticker,data in r.items()}, f) if isinstance(tickers,list) else (r[tickers][k],f);
        else:
            return None, f;

    @classmethod
    def Splits(cls, tickers:Union[str, List[str]],
            interval:str="1d",
            period:Optional[Union[str,List[Union[str,dt.datetime]]]]=None,
            using_api:Type[api.AccessMode]=api.AccessMode.CHART) -> Tuple[Optional[dict],Optional[list]]:
        r,f = cls.Data(tickers, interval, period, events=api.EventsInQuery.SPLITS, using_api=using_api);
        if len(r)>0:
            k = 'events' if using_api is api.AccessMode.CHART else 'data';
            return ({ticker:data[k] for ticker,data in r.items()}, f) if isinstance(tickers,list) else (r[tickers][k],f);
        else:
            return None, f;

    @classmethod
    def Data(cls, tickers:Union[str, List[str]],
             interval:str="1d",
             period:Optional[Union[str,dt.datetime,List[Union[str,dt.datetime]]]]=None,
             events:Type[api.EventsInQuery]=api.EventsInQuery.HISTORY,
             using_api:Type[api.AccessMode]=api.AccessMode.DEFAULT) -> Tuple[Optional[dict],Optional[List[str]]]:
        
        if isinstance(tickers,str) or (isinstance(tickers,list) and all(isinstance(ticker,str) for ticker in tickers)):
            tickers = tickers if isinstance(tickers, list) else list([tickers]);
            tickers = [x.upper() for x in tickers];
        else:
            raise TypeError(f"invalid type for the argument 'tickers'! {type(str)} or a list of {type(str)} expected; got {type(tickers)}");
        
        if period is None:
            t = dt.datetime.now();
            period = [t-dt.timedelta(weeks=52),t] if using_api is api.AccessMode.DOWNLOAD else "1y";

        params = api.Query(using_api);
        params.SetPeriod(period);
        params.SetInterval(interval);
        params.SetEvents(events);
        if not isinstance(using_api,api.AccessMode):
            raise TypeError(f"invalid type for the argument 'using_api'! <class 'api.AccessMode'> expected; got {type(api)}");
        else:
            if cls.__processing_mode__ is core.ProcessingMode.PARALLEL:
                get = cls.__parallel__;
            elif cls.__processing_mode__ is core.ProcessingMode.SERIAL:
                get = cls.__serial__;
            else:
                get = cls.__serial__ if len(tickers)==1 else cls.__parallel__;
            return get(tickers, params, using_api);

    @classmethod
    def __serial__(cls, tickers:list, params:Type[api.Query], using_api:Type[api.AccessMode]) -> Tuple[dict,Optional[List[str]]]:
        data = dict();
        failed = list();
        for ticker in tickers:
            response = cls.__get__(ticker, params, using_api, timeout=2);
            if response:
                data[ticker] = response;
            else:
                failed.append(ticker);
        return data, failed;

    @classmethod
    def __parallel__(cls, tickers:list, params:Type[api.Query], using_api:Type[api.AccessMode]) -> Tuple[dict,Optional[List[str]]]:
        data = dict();
        failed = list();
        with cf.ProcessPoolExecutor(max_workers=len(tickers)) as executor:
            results = { executor.submit(cls.__get__, ticker, params, using_api, timeout=2) : ticker for ticker in tickers};
            for result in cf.as_completed(results):
                if result.result():
                    data[results[result]] = result.result();
                else:
                    failed.append(results[result]);
        return data, failed;
    
    @staticmethod
    def __get__(ticker:str, params:Type[api.Query], this_api:Type[api.AccessMode], timeout:int=5) -> Optional[dict]:
        err, res = api.Session.With(this_api).Get(ticker, params, timeout=timeout);
        if err:
            err_msg = "*ERROR: {0:s}.\n{1:s}";
            if res['code']=='Unprocessable Entity':
                print(err_msg.format(res['code'], res['description']));
                print("please, check whether the parameters you have set are correct!");
            elif res['code']=="-1":
                print(err_msg.format("A request exception occured", res['description']));
            elif res['code']=="-2":
                print(err_msg.format(res['description'], "Aborting the task..."));
            else:
                print(err_msg.format(res['code'], res['description']));
            return None;
        else:
            return res;