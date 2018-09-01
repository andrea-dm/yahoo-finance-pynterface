import requests
import pandas
import numpy
import pytz
import dateutil.parser
import aenum #2.1.2

if __name__ == '__main__':

    print("Package:\t{} {}".format(requests.__name__,requests.__version__));
    
    print("Package:\t{} {}".format(pandas.__name__,pandas.__version__));
    
    print("Package:\t{} {}".format(numpy.__name__,numpy.__version__));
    
    print("Package:\t{} {}".format(pytz.__name__,pytz.__version__));
    
    print("Package:\t{} {}".format(dateutil.__name__,dateutil.__version__));
    
    print("Package:\t{}".format(aenum));