import requests
import pandas
import numpy
import pytz
import dateutil.parser
import aenum #2.1.2

if __name__ == '__main__':

    f = open('version.txt', 'w')

    f.writelines("- `{} >= {}`\n".format(requests.__name__,requests.__version__));
    
    f.write("- `{} >= {}`\n".format(pandas.__name__,pandas.__version__));
    
    f.write("- `{} >= {}`\n".format(numpy.__name__,numpy.__version__));
    
    f.write("- `{} >= {}`\n".format(pytz.__name__,pytz.__version__));
    
    f.write("- `{} >= {}`\n".format(dateutil.__name__,dateutil.__version__));
    
    f.write("- `{} >= {}`\n".format(aenum,'2.1.2'));

    f.close()