import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
#lo troverai

if __name__=='__main__':

    done = ['FB', 'TSLA', 'NVDA', 'AMD',  'MSFT', 'NFLX', 'BABA', 'TCS','AMZN', 'BTC-USD','QCOM']
    stocks = ['AAPL', 'ABNB']

    for stock in stocks:
        print('starting...')

        period = 7

        ticker = yf.Ticker(stock)
        aapl_df = ticker.history(period=str(period)+'y')

        plt.title(stock+" stock price")
        plt.plot(aapl_df['Close'])
        plt.show(block=False)

        a=1

        # Download stock data then export as CSV
        aapl_df.to_csv(stock + '.csv')

        data = pd.read_csv(stock+'.csv')
        first_date = data['Date'][0]

        starting_year = first_date[:4]
        starting_month = first_date[5:7]

        ' init variable for info about ROI for each month of each year'
        ' for the last 5 years'

        years=[]
        months=[0]*(int(starting_month)-1)

        single_values = []

        'init some temp variables'
        starting_price = 0
        ending_price=0
        var_perc = 0 # float(((end_price-start_price)/start_price)*100)

        year = int(starting_year)
        month = int(starting_month)

        start=1

        for i in range(start, len(data)-1):
            # get various data
            temp_data = data['Date'][i]
            temp_open = data['Open'][i]
            temp_close = data['Close'][i]

            temp_div = data['Dividends'][i]

            # use data
            mean_price = (float(temp_open) + float(temp_close))/2
            
            # month check
            this_month = data['Date'][i][5:7]
            this_year = data['Date'][i][:4]
            
            if i==start or int(data['Date'][i-1][5:7])!=int(data['Date'][i][5:7]):
                starting_price = mean_price

            try:
                # last month day
                if  i==len(data)-start-1 or int(this_month)!=int(data['Date'][i+1][5:7]):
                    ending_price = mean_price

                    var = float(((ending_price-starting_price)/starting_price)*100)

                    months.append(var)
                    single_values.append(var)
            except:
                continue

            try:
                # finito anno
                if int(data['Date'][i-1][:4])!=int(data['Date'][i][:4]):
                    years.append(months)
                    months=[]
            except:
                continue

        # last current year
        for k in range(len(months)+1,13):
            months.append(0)
        years.append(months)
        a=1

        # plot the results
        # prepare the labels
        labels = []
        for i in range(year, year+period+1):
            labels.append(str(i))

        months = ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec']
        
        xss = np.arange(0,12*(period+2),period+2)

        # plot each year monthly ROI
        plt.figure(2)
        plt.title(stock+" stock ROi monthly")
        plt.xticks(xss,months)
        for j in range(period+1):
            try:
                # plt.plot(months, years[j], label=labels[j])
                xs = np.arange(j,j+12*(period+2),(period+2))
                plt.bar(xs,years[j], label=labels[j])
            
                plt.xticks(xs,months)
            except:
                continue

        # HERE tell pyplot which labels correspond to which x values
        

        plt.legend()
        plt.show()
        a=1
    

