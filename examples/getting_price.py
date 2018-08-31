import yahoo_finance_pynterface as yahoo
import matplotlib.pyplot        as plt
import matplotlib.dates         as mdates

if __name__ == '__main__':

    fig, ax = plt.subplots(1);
    fig.fmt_xdata = mdates.DateFormatter('%Y-%m-%d');
    ax.grid(True);

    ticker = "AAPL";
    r,_ = yahoo.Get.Prices(ticker);
    if len(r)>0:
        plt.plot(r.index.values, r['Close']);
        print(r['Close'])
    else:
        print("something odd happened o.O")
    
    fig.autofmt_xdate()
    plt.show();

