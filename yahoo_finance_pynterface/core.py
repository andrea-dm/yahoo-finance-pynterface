from aenum          import Enum
from collections    import namedtuple
from typing         import Tuple, Dict, List, Union, ClassVar, Any, Optional, Callable


class API(Enum):
    # Base class for enumeration
    def __repr__(self):
        return f"<YahooFinancePynterface.core {self.__name__} : '{self.value}'>";
    def __str__(self):
        return self.value;

class ProcessingMode(API):
    # Enumeration class to list available processing modes.
    SERIAL = 'serial';
    PARALLEL = 'parallel';
    AUTO = 'auto';


def parser(d:Any, tuplename='YahooFinanceDataTuple') -> Any:
    # A simple recursive parser to return a more 'readable' namedtuple.
    if d is "null":
        return None
    elif isinstance(d,dict):
        return namedtuple(tuplename, d.keys())(*[parser(v) for v in d.values()]);
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
