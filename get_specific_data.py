

import pandas as pd
from datetime import datetime, timedelta
import sys
sys.path.append('F:\\Bot')
import config 
import asyncio
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
import numpy as np
import ta
import pyotp
from logzero import logger

from SmartApi import SmartConnect

#smart api angel one login
api_key = config.api_key_smartapi
username = config.angel_one_username
pwd = config.angel_one_pin
smartApi = SmartConnect(api_key)



import requests
import pandas as pd

scrip_details = None

try:
    scrip_details = pd.read_csv('scrip.csv')
except:
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = requests.get(url)
    data = response.json()

    # Filter out stocks with symbol name ending with -EQ and exchange_seq is NSE
    filtered_data = [entry for entry in data if entry["exch_seg"] == "NSE" and entry["symbol"].endswith("-EQ")]

    scrip_details = pd.DataFrame(filtered_data)



try:
    token = config.qr_smartApi
    totp = pyotp.TOTP(token).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

data = smartApi.generateSession(username, pwd, totp)
if data['status'] == False:
    logger.error(data)
    


#getting data from angel one smart api

async def historical_fetch_data(symbol_token, interval, from_date, to_date): 
    df = await asyncio.to_thread(
        smartApi.getCandleData,
        {
            "exchange": 'NSE',
            "symboltoken": symbol_token,
            "interval": interval,
            "fromdate": from_date,
            "todate": to_date
        }
    )
    
    return df


def calculate_vwap(data):
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    volume = data['volume']
    
    # Calculate the cumulative totals
    cum_typical_price_volume = (typical_price * volume).cumsum()
    cum_volume = volume.cumsum()
    
    # Calculate VWAP
    vwap_value = cum_typical_price_volume / cum_volume

    return {'vwap': vwap_value}


def calculate_sma(data, window):
    close_prices = data['close']
    sma_values = close_prices.rolling(window=window, min_periods=window).mean()
    return sma_values



def calculate_rsi(df, window = 14):
    
    rsi = ta.momentum.RSIIndicator(df['close'], window=window)
    
    return rsi.rsi()


def calculate_atr(df, window=14):
    atr = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=window)
    # Calculate RMA manually
    rma_atr = atr.average_true_range().ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    return rma_atr


async def fetch_data(symbol, interval, end_date = datetime.now()-timedelta(days = 1), num_periods = 0, ):
    
    try:
        start_date = end_date - timedelta(days=num_periods)

        # Format start date and end date strings with specific times
        start_date_str = start_date.strftime('%Y-%m-%d 09:15')  # Ensure leading zero for single-digit hour
        end_date_str = end_date.strftime('%Y-%m-%d 15:30')

        try:
            symbol_token = scrip_details.loc[scrip_details['name'] == (symbol), 'token'].values[0]
        except Exception as e:
            print('Scrip Not found in angel one', symbol)
            return 

        #getting data
        response = await historical_fetch_data(
            symbol_token=symbol_token,
            interval = interval,
            from_date=start_date_str,
            to_date=end_date_str
        )
        
        df = pd.DataFrame(response['data'], columns=['Date', 'open', 'high', 'low', 'close', 'volume'])
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index)
        
        
        #df['sma_50'] = calculate_sma(df, 50)
        #df['sma_200'] = calculate_sma(df, 200)
        #df['rsi'] = calculate_rsi(df, 14)
        df['atr_20'] = calculate_atr(df, 20)


        #df['EMA_7'] = calculate_ema(df, 7)
        
        #df = df.loc[df.index.date == datetime.today().date()]

        #df['vwap'] = calculate_vwap(df)['vwap']
        df.dropna(inplace=True)
        
        return (symbol, df)
        
    except Exception as e:
        print(e)






    







