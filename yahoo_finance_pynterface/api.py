import core

import io
import re  
import requests
import pytz       
import time
import datetime         as dt
import numpy            as np
import pandas           as pd

from typing             import Tuple, Dict, List, Union, ClassVar, Any, Optional, Type, NoReturn, NewType
from dateutil.parser    import parse as dt_p

import types


class AccessModeInQuery(core.API):
    # Enumeration class to list available API access modes.
    NONE = 'n/a';
    DOWNLOAD = 'download';
    CHART = 'chart';
    DEFAULT = 'download';


class EventsInQuery(core.API):
    # Enumeration class to list the 'events' that is possible to request.
    NONE = '';
    HISTORY = 'history';
    DIVIDENDS = 'div';
    SPLITS = 'split';


class Query():
    # Class that encodes the request parameters into a query.
    # It provides methods to set such parameters 
    # as well as to validate them in accordance to the Yahoo Finance API expected arguments.

    __events__:ClassVar[List[str]]             = ["history", "split", "div"];
    __chart_range__:ClassVar[List[str]]        = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"];
    __chart_interval__:ClassVar[List[str]]     = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"];
    __download_frequency__:ClassVar[List[str]] = ["1d", "1wk", "1mo"];
    
    def __init__(self, using_api:Type[AccessModeInQuery]):
        self.query:Dict[str,Optional[str]] = {};
        self.__api__:AccessModeInQuery = using_api;

    def __str__(self):
        return "&".join([f"{param}={value}" for param, value in self.query.items() if value is not None]) if len(self.query)>0 else "";

    def __len__(self):
        return len(self.query);

    def __bool__(self):
        return True if len(self.query)>0 else False;

    def SetEvents(self, events:Type[EventsInQuery]) -> Optional[NoReturn]:
        if not isinstance(events, EventsInQuery):
            self.query['events'] = None;
            raise TypeError(f"invalid type for the argument 'events'; <class 'EventsInQuery'> expected, got {type(events)}");
        else:
            if self.__api__ is AccessModeInQuery.CHART:
                self.query['events'] = events if events not in [EventsInQuery.HISTORY, EventsInQuery.NONE] else None;
            elif self.__api__ is AccessModeInQuery.DOWNLOAD:
                self.query['events'] = events if events is not EventsInQuery.NONE else str(EventsInQuery.HISTORY);
            else:
                self.query['events'] = None;
                raise ValueError(f"value of argument 'events' is not compatible with the given API '{str(self.__api__)}'");

    def SetInterval(self, interval:str) -> Optional[NoReturn]:
        if not isinstance(interval, str):
            self.query['interval'] = None;
            raise TypeError(f"invalid type for the argument 'interval'; {type(str)} expected, got {type(interval)}");
        else:
            if (self.__api__ is AccessModeInQuery.CHART and interval in self.__chart_interval__) \
            or (self.__api__ is AccessModeInQuery.DOWNLOAD and interval in self.__download_frequency__):
                self.query['interval'] = interval;
            else:
                self.query['interval'] = None;
                raise ValueError(f"value of argument 'interval' is not compatible with the given API '{str(self.__api__)}'");

    def SetPeriod(self, period:Union[str,dt.datetime,List[Union[int,dt.datetime]]]) -> Optional[NoReturn]:
        if isinstance(period,list) and len(period) is 2 and all(lambda p: isinstance(p,int) or isinstance(p,dt.datetime) or isinstance(p,str) for p in period):
            self.query['period1'], self.query['period2'] = self.__parse_periods__(*(period));
        elif isinstance(period,str):
            if self.__api__ is AccessModeInQuery.CHART and period in self.__chart_range__:
                self.query['range'] = period;
            else:
                raise ValueError(f"value of argument 'period' is not compatible with the given API '{str(self.__api__)}'");
        elif isinstance(period,dt.datetime):
            self.query['period1'], self.query['period2'] = self.__parse_periods__(period,period);
        else:
            self.query['period1'], self.query['period2'], self.query['range'] = None, None, None;
            raise TypeError(f"invalid type for the argument 'period'; {type(str)} or {type(dt.datetime)} or a list of either {type(int)} or {type(dt.datetime)} expected, got {type(period)}");

    @classmethod
    def __parse_periods__(cls, value1:Union[dt.datetime,int,str], value2:Union[dt.datetime,int,str]) -> Tuple[int,int]:
        # Note that the earliest date that is possible to take into consideration is platform-dependent.
        # For compatibility reasons, we do not accept timestamps prior to epoch time 0.
        if isinstance(value1,str):
            try:
                period1 = int(dt_p(value1).timestamp());
            except (OSError,OverflowError):
                period1 = 0; 
        else:
            period1 = max(0,(int(time.mktime(value1.timetuple())))) if isinstance(value1, dt.datetime) else max(0,value1);

        if value1==value2:
            period2 = period2;
        elif isinstance(value2,str):
            try:
                period2 = int(dt_p(value2).timestamp());
            except OSError:
                period2 = dt.datetime.now().timestamp();
        else:
            period2 = max(period1,int(time.mktime(value2.timetuple()))) if isinstance(value2, dt.datetime) else max(period1,value2);

        return period1, period2


class Response:   
    # Class to parse and process responses sent back by the Yahoo Finance API.
    # Use the 'Parse()' method to correctly retrieve data structures in accordance to the chosen 'AccessModeInQuery' API.

    def __init__(self, input:Type[requests.models.Response]): 
        self.__format__:str = ""; 
        self.__error__:Optional[Dict[str, str]] = None;
        self.__meta__:Optional[Dict[str, Union[str, int, float]]] = None;
        self.__timestamps__:Optional[List[dt.datetime]] = None;
        self.__quotes__:Optional[pd.DataFrame] = None;
        self.__events__:Optional[pd.DataFrame] = None;
        self.__data__:Optional[Union[pd.DataFrame,dict]] = None;

        def is_json() -> bool:
            nonlocal input;
            try:
                input = input.json(parse_float=float, parse_int=int);
            except ValueError :
                return False
            else:
                return True

        if is_json():

            if'chart' in input.keys():
                self.__format__ = 'chart';
                if 'error' in input['chart'].keys():
                    self.__error__ = self.__response_parser__(input['chart']['error']);
                if self.__error__ is None:
                    data = input['chart']['result'][0];
                    self.__error__ = {'code':"ok", 'description':"success!"};
                    self.__meta__ = self.__response_parser__(data['meta']);

                    self.__timestamps__ = pd.DatetimeIndex(list( map(dt.datetime.utcfromtimestamp, sorted(data['timestamp']))), name=f"Date ({pytz.utc})");

                    self.__quotes__ = pd.DataFrame({
                        'Open'     : np.array(data['indicators']['quote'][0]['open']),
                        'High'     : np.array(data['indicators']['quote'][0]['high']),
                        'Low'      : np.array(data['indicators']['quote'][0]['low']),
                        'Close'    : np.array(data['indicators']['quote'][0]['close']),
                        'Adj Close': np.array(data['indicators']['adjclose'][0]['adjclose'])
                                        if 'adjclose' in data['indicators'].keys()
                                        else np.full(len(data['indicators']['quote'][0]['close']),np.NaN),
                        'Volume'   : np.array(data['indicators']['quote'][0]['volume'])},
                        index=self.__timestamps__);

                    if 'events' in data.keys():
                        index = list();
                        entries = list();
                        columns = list();
                        if 'splits' in data['events'].keys():
                            for split in data['events']['splits'].values():
                                index.append(split['date']);
                                entries.append([split['numerator'], split['denominator'], split['denominator']/split['numerator']]);
                            columns=['From', 'To', 'Split Ratio'];
                        elif 'dividends' in data['events'].keys():
                            for dividend in data['events']['dividends'].values():
                                index.append(dividend['date']);
                                entries.append(dividend['amount']);
                            columns=['Dividends'];
                        index = pd.DatetimeIndex(list(map(lambda ts: dt.datetime.utcfromtimestamp(ts).date(),sorted(index))), name=f"Date ({pytz.utc})");
                        self.__events__ = pd.DataFrame(entries,index=index,columns=columns);

            elif 'finance' in input.keys():
                self.__format__ = 'finance';
                if 'error' in input['finance'].keys():
                    self.__error__ = self.__response_parser__(input['finance']['error']);
                if self.__error__ is None:
                    self.__data__ = self.__response_parser__(input['finance']);
        else:
            self.__format__ = 'finance';
            self.__error__ = {'code':"ok", 'description':"success!"};
            self.__data__ = pd.read_csv(io.StringIO(input.text),index_col=0,parse_dates=True).sort_index();


    def Parse(self) -> Dict[str,Any]:
        if self.__format__ == 'chart':
            return {'api':'chart', 'meta':self.__meta__, 'quotes':self.__quotes__, 'events':self.__events__, 'error':self.__error__};
        elif self.__format__ == 'finance':
            return {'api':'download', 'data':self.__data__, 'error':self.__error__};
        else:
            return {'api': 'unknown', 'error':{'code':"0", 'description':"invalid API"} };

    @classmethod
    def __response_parser__(cls, d:Any) -> Any:
        if d is "null":
            return None
        elif isinstance(d,dict):
            return {key:cls.__response_parser__(value) for key, value in d.items()};
        elif isinstance(d,list):
            try:
                return list(map(float, d));
            except :
                return d;
        elif isinstance(d,str):
            try:
                return float(d);
            except:
                return d;
        else:
            return d


class Session:
    # A lower level class that explicitly requests data to Yahoo Finance via HTTP.
    # I provides two 'public' methods:
    #
    # - With(...):  to set the favorite access mode;
    # - Get(...):   to explicitly push request to Yahoo.
    #
    # It implements a recursive call to the HTTP 'GET' method in case of failure.
    # The maximum number of attempts has been hardcodedly set to 10.

    __yahoo_finance_url__:str = "";
    __yahoo_finance_api__:Type[AccessModeInQuery] = AccessModeInQuery.NONE;

    def __init__(self):
        self.__last_time_checked__ : dt.datetime;
        self.__cookies__ : Type[requests.cookies.RequestsCookieJar];
        self.__crumb__ : str;

    @classmethod
    def With(cls, this_api:Type[AccessModeInQuery]) -> Union['Session',NoReturn]:
        if not isinstance(this_api,AccessModeInQuery):
            raise TypeError(f"invalid type for the argument 'this_api'; <class 'AccessModeInQuery'> expected, got {type(this_api)}.");
        else:
            cls.__set_api__(this_api);
            cls.__set_url__();
            session = cls();
            session.__start__();
            return session;

    @classmethod
    def __set_url__(cls) -> Optional[NoReturn]:
        if cls.__yahoo_finance_api__ is not AccessModeInQuery.NONE:
            cls.__yahoo_finance_url__ = f"https://query1.finance.yahoo.com/v7/finance/{cls.__yahoo_finance_api__}/";
        else:
            raise UnboundLocalError("session's api has not been set yet");

    @classmethod
    def __set_api__(cls, input_api:Type[AccessModeInQuery]=AccessModeInQuery.DEFAULT) -> None:
        if cls.__yahoo_finance_api__ is not input_api:
            cls.__yahoo_finance_api__ = input_api if input_api is not AccessModeInQuery.NONE else AccessModeInQuery.DEFAULT;
        #else:
        #    print(f"*INFO: the session 'api' was already '{input_api}'.");

    def __start__(self) -> None:
        r = requests.get('https://finance.yahoo.com/quote/SPY/history');
        self.__cookies__ = requests.cookies.cookiejar_from_dict({'B': r.cookies['B']});
        pattern = re.compile(r'.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}');
        for line in r.text.splitlines():
            crumb_match = pattern.match(line)
            if crumb_match is not None:
                self.__crumb__ = crumb_match.groupdict()['crumb'];
                break;
        self.__last_time_checked__ = dt.datetime.now();

    def __restart__(self) -> None:
        self.__abandon__();
        self.__start__();
    
    def __refresh__(self, force:bool=False) -> None:
        if force:
            self.__restart__();
        else:
            if self.__last_time_checked__ is not None:
                current_time = dt.datetime.now()
                delta_secs = (current_time - self.__last_time_checked__).total_seconds()
                if delta_secs > 300: # 300 = 5 minutes
                    self.__restart__();

    def __abandon__(self) -> None:
        self.__cookies__ = None;
        self.__crumb__ = "";
        self.__last_time_checked__ = None;

    def Get(self, ticker:str, params:Type[Query], attempt:int=0, timeout:int=10, last_error:str="") -> Union[Tuple[bool, dict],NoReturn]:
        if not isinstance(ticker,str):
            raise TypeError(f"invalid type for the argument 'ticker'! {type(str)} expected; got {type(ticker)}");
        if not isinstance(params, Query):
            raise TypeError(f"invalid type for the argument 'params'! <class 'Query'> expected; got {type(params)}");
        if attempt<10:
            query = f"?{str(params)}&crumb={self.__crumb__}" if params else f"?crumb={self.__crumb__}";
            url = self.__yahoo_finance_url__ + ticker + query;
            try:
                response = requests.get(url, cookies=self.__cookies__)
                response.raise_for_status();
            except requests.HTTPError as e:
                if response.status_code in [408, 409, 429]:
                    time.sleep(timeout);
                    self.__refresh__();
                    return self.Get(ticker,params,attempt=attempt+1,timeout=timeout+1,last_error=str(e))
                elif response.status_code in [401, 404, 422]:
                    r = Response(response).Parse();
                    if r['error']['description'] == "Invalid cookie":
                        self.__refresh__(force=True);
                        return self.Get(ticker,params,attempt=attempt+1,timeout=timeout+5,last_error=r['error']['description'])
                    else:
                        return True, dict({'code': r['error']['code'], 'description': f"{r['error']['description']} (attempt: {attempt})"});
                else :
                    m = re.match(r'^(?P<code>\d{3})\s?\w*\s?Error\s?:\s?(?P<description>.+)$', str(e));
                    return True, dict({'code': m['code'], 'description': f"{m['description']} (attempt: {attempt})"});
            except requests.Timeout as e:
                time.sleep(timeout);
                self.__refresh__();
                return self.Get(ticker,params,attempt=attempt+1,timeout=timeout+1,last_error=str(e))
            except requests.RequestException as e:
                if re.search(r"^\s*Invalid\s?URL", str(e)):
                    time.sleep(timeout);
                    self.__refresh__();
                    return self.Get(ticker,params,attempt=attempt+1,timeout=timeout+1,last_error=str(e));
                else:
                    return True, dict({'code': "-1", 'description': f"{str(e)} (attempt: {attempt})"});
            else:
                r = Response(response).Parse();
                if r['error'] is not None and r['error']['code'] is not "ok":
                    return True, dict({'code': r['error']['code'], 'description': f"{r['error']['description']} (attempt: {attempt})"});
                else:
                   return False, r;
        else:
            return True, dict({'code': "-2", 'description': "{}\nThe maximum number of attempts has been exceeded!".format(last_error)}); 
