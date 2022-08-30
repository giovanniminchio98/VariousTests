import gate_api
from gate_api.exceptions import ApiException, GateApiException
import pandas as pd
import time
import datetime as dt
import numpy as np

import time

# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(host = "https://api.gateio.ws/api/v4")
api_client = gate_api.ApiClient(configuration)

# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)

# this function starts calling the Gate.io API
# the response will contains price data for multiple cryptocurrencies
# the price information of each cryptocurrency will be stored in its own dataframe
def request_data(runs, currency_pair, s):
    currency_dfs = {}
    for t in range(runs):

        try:
            api_response = api_instance.list_tickers(currency_pair=currency_pair)
        except GateApiException as ex:
            print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
        except ApiException as e:
            print("Exception when calling SpotApi->list_tickers: %s\n" % e)

        ts = dt.datetime.now()
        currency_response_dict = {resp.currency_pair: resp for resp in api_response
                                if "USDT" in resp.currency_pair and "BEAR" not in resp.currency_pair}
                  
        for currency_name, response in currency_response_dict.items():
            try:
                currency_dfs[currency_name]
            except KeyError:
                # Create new dataframe if currency does not have one yet
                currency_dfs[currency_name] = pd.DataFrame(columns=[
                    'Symbol', 
                    'Timestamp', 
                    'Volume', 
                    'Price', 
                    'Price_Delta', 
                    'Price_Delta_Percent'])
            
            # get the price of the currency at the last price point
            if len(currency_dfs[currency_name]) > 1:
                #print(currency_dfs[currency_name])
                price_before = currency_dfs[currency_name]['Price'].iloc[-1]
            else:
                price_before = 0
            
            # append a new record the dataframe of this currency
            new_data_as_dict = append_data_to_df(price_before, response, ts)
            
            # add this dataframe to the list of currency_dataframe. there are separate dfs per currency.
            currency_dfs[currency_name] = currency_dfs[currency_name].append(new_data_as_dict, ignore_index=True)
                
        # wait s seconds until the next request
        time.sleep(s)
    return currency_dfs

# this function is called for each cryptocurrency and everytime the gate.io API returns price data
# the function extracts price information from a single API response and adds it to a dataframe 
# example: the API response contains data for 270 cryptocurrency price pairs -> the function is called 270 time per API response
def append_data_to_df(price_before, data, ts):
    volume = data.base_volume
    price = pd.to_numeric(data.last)
    price_delta = price - price_before
    
    if price > 0:
        price_delta_p = price_delta / price 
    else:
        price_delta_p = 0
    
    new_record = {
                  'Symbol': data.currency_pair, 
                  'Timestamp': ts, 
                  'Volume': volume, 
                  'Price': price,
                  'Price_Delta': price_delta,
                  'Price_Delta_Percent': price_delta_p
                 }
    return new_record


s = 0 # API request interval in seconds
currency_pair = '' # currency pair (optional)
runs = 1 # number of data points to fetch
lista_mia = {}
lista_volume = {}


for i in range(1):
    start_time = time.time()
    df_list = request_data(runs, currency_pair, s)
    end = time.time() - start_time

    print('Tempo(s): ' + str(end))
    a=1

    for pair in df_list.keys():
        try:
            lista_mia[pair] = lista_mia[pair] + [float(df_list[pair]['Price'][0])]
            lista_volume[pair] = lista_volume[pair] + [float(df_list[pair]['Volume'][0])]
        except:
            lista_mia[pair] = [float(df_list[pair]['Price'][0])]
            lista_volume[pair] = [float(df_list[pair]['Volume'][0])]

for i in range(30):
    start_time = time.time()
    df_list = request_data(runs, currency_pair, s)
    end = time.time() - start_time

    print('Tempo(s): ' + str(end))
    a=1

    for pair in df_list.keys():
        try:
            lista_mia[pair] = lista_mia[pair] + [float(df_list[pair]['Price'][0])]
            lista_volume[pair] = lista_volume[pair] + [float(df_list[pair]['Volume'][0])]
        except:
            lista_mia[pair] = [float(df_list[pair]['Price'][0])]
            lista_volume[pair] = [float(df_list[pair]['Volume'][0])]

a=1

print('STARTING  the analysis of prices...')

while True:
    # get data
    df_list = request_data(runs, currency_pair, s)
    # save new values
    for pair in df_list.keys():
        try:
            lista_mia[pair] = lista_mia[pair] + [float(df_list[pair]['Price'][0])]
            lista_volume[pair] = lista_volume[pair] + [float(df_list[pair]['Volume'][0])]
        except:
            lista_mia[pair] = [float(df_list[pair]['Price'][0])]
            lista_volume[pair] = [float(df_list[pair]['Volume'][0])]

        try:
            # check prices variations
            chiude = lista_mia[pair][-1]
            apre = lista_mia[pair][-30]

            try:
                variation = (float(((chiude-apre)/chiude)*100)) 
            except:
                variation = 0
            # check volume to be all good 
            min_volume = min(lista_volume[pair][-20:])

            if variation > 9 and min_volume > 1 and chiude > max(lista_mia[pair][-10:]):
                print('PUMP IN ', pair)
        except:
            print('\tERROR with ', pair)


    a=1
