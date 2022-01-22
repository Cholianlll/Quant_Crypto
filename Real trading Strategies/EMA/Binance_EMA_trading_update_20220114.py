# Binance trading system, refer to the backtrader framework
####################### Github Version #####################


#! Author: Cholian Li
# Contact: 
#! cholianli970518@gmail.com
# Created at 20220101


import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

from pandas import json_normalize
import random

import pandas as pd
import talib as ta
import datetime





''' ======  Module: Requesting - start ====== '''
def hashing(query_string):
    return hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json;charset=utf-8',
        'X-MBX-APIKEY': KEY
    })
    return {
        'GET': session.get,
        'DELETE': session.delete,
        'PUT': session.put,
        'POST': session.post,
    }.get(http_method, 'GET')

# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    url = BASE_URL + url_path + '?' + query_string + '&signature=' + hashing(query_string)
    # print("{} {}".format(http_method, url))
    params = {'url': url, 'params': {}}
    response = dispatch_request(http_method)(**params)
    return response.json()

# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + '?' + query_string
    # print("{}".format(url))
    response = dispatch_request('GET')(url=url)
    return response.json()

''' ======  Module: Requesting - end ====== '''


''' ======  Module: Current position - start ====== '''

def find(lst, value):
    # find the corresponding symbol info from the respond dict
    for i, dic in enumerate(lst):
        if dic['symbol'] == value:
            return lst[i]
    raise ValueError('No such a symbol')


def position(pos_amt):
    # judge the current position
    if pos_amt > 0:
        return "BUY"
    elif pos_amt < 0:
        return "SELL"
    else:
        return "Empty"
    
    
def Holding_info(symbol):
    
    # obtain the current account info
    response = send_signed_request('GET', '/fapi/v2/account')
    account_positions = json_normalize(response['positions'])

    # append the current position to the symbol holding information
    # short position of "SELL", long position for "BUY","Empty"
    symbol_info = find(response['positions'],symbol)
    symbol_pos_amt = float(symbol_info['positionAmt'])
    symbol_info['position'] = position(symbol_pos_amt)
    
    return symbol_info


def Current_position(symbol):
    hold_pos = Holding_info(symbol)['position']
    hold_amt = Holding_info(symbol)['positionAmt']
    
    return hold_pos,hold_amt
   
''' ======  Module: Current position - end ====== ''' 



''' ======  Module: Order status - start ====== ''' 

def Order_status(symbol:str,orderId:int):
    
    params = {
    'symbol': symbol,
    'orderId': orderId,
    # 'origClientOrderId':"zb0BWGDa0g1CTYEBYJiHtf"
    }
    
    response = send_signed_request('GET', '/fapi/v1/order',params)
    return response['status']


''' ======  Module: Order status - end ====== ''' 



''' ======  Module: data obtain and indicator - start ====== ''' 

def future_data(pair,interval,contractType = 'PERPETUAL'):
    
    url_path = '/fapi/v1/continuousKlines'
    params = {
    'pair': pair,
    'contractType': contractType,
    'interval': interval,
    'limit':1500
    }

    response = send_public_request(url_path, params)

    col = ['Open time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades',
        'Taker buy volume','Taker buy quote asset volume','Ignore']
    data = pd.DataFrame(response,columns=col)

    # adjust the datetime type
    data['Open time'] = pd.to_datetime(data['Open time'],unit='ms',utc=True)
    data['Close time'] = pd.to_datetime(data['Close time'],unit='ms',utc=True)

    # transfer the object to float
    data.iloc[:,1:6] = data.iloc[:,1:6].astype(float)
    
    return data


def ema_indicator(data,ema_a_period = 36,ema_b_period = 60):
    
    close = data['Close']
    ema_a = ta.EMA(close,timeperiod=ema_a_period).tolist()
    ema_b = ta.EMA(close,timeperiod=ema_b_period).tolist()

    return ema_a,ema_b

''' ======  Module: data obtain and indicator - end ====== ''' 

''' ======  Module: Trading Operation - start ====== ''' 

def Order_BUY_Market(symbol,quantity):
    
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': quantity,
    }
    response = send_signed_request('POST', '/fapi/v1/order',params)
    # print(response)

def Order_SELL_Market(symbol,quantity = 0.002):
    
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'MARKET',
        'quantity': quantity,
    }

    response = send_signed_request('POST', '/fapi/v1/order',params)
    # print(response)

''' ======  Module: Trading Operation - end ====== ''' 

''' ======  Module: Runing - start ====== ''' 
def run_start(symbol,interval='8h',quantity = 0.002):
    # param
    # symbol = 'ETHUSDT'
    # interval = '8h'
    # quantity = 0.002
    
    # order and position info
    current_position,current_amt = Current_position(symbol)
    print(f'Current holding position : {current_position}, quantity: {current_amt}')

    # data and indicator
    data = future_data(symbol,interval)
    ema_a,ema_b = ema_indicator(data)
    print(f"Ema_a indicator: {ema_a[-1]}, Ema_b indicator: {ema_b[-1]}")

    # 36 > 60, we should hold a buy position
    if ema_a[-1] > ema_b[-1]:
        # if it exists an buy order, nothing to do
        if current_position in ['BUY']:
            print('Already in //BUY// position, no order needed to execute')
            return 
        
        elif current_position in ['SELL']:
            Order_BUY_Market(symbol, quantity)
            print('Close the previous //SELL// order')
            time.sleep(5)
            Order_BUY_Market(symbol, quantity)
            print('Place a //BUY// order')
            return

        elif current_position in ['Empty']:
            Order_BUY_Market(symbol, quantity)
            print('Place a //BUY// order')
            return
        
    elif ema_a[-1] < ema_b[-1]:
        # reverse to the above the operation
        if current_position in ['SELL']:
            print('Already in //SELL// position, no order needed to execute')
            return 
        
        elif current_position in ['BUY']:
            print('Close the previous //BUY// order')
            Order_SELL_Market(symbol,quantity)
            
            print('Place a //SELL// order')
            Order_SELL_Market(symbol,quantity)
            return
        elif current_position in ['Empty']:
            print('Place a //SELL// order')
            Order_SELL_Market(symbol,quantity)
            return
            

def account_P_L():
    # ## USER_DATA endpoints, call send_signed_request #####
    response = send_signed_request('GET', '/fapi/v2/account')
    account_assets = json_normalize(response['assets'])
    account_assets = account_assets.set_index('asset')
    asset = ['USDT']
    
    Balance = account_assets.loc[asset]['walletBalance'].values[0]
    UnrealizedProfit = account_assets.loc[asset]['unrealizedProfit'].values[0]
    
    return float(Balance),float(UnrealizedProfit)
''' ======  Module: Runing - end ====== ''' 




if __name__ == '__main__':
    
# =============== Parameters =========================
    symbol = 'BTCUSDT'
    quantity = 0.037
    interval = '6h'
    
    ema_a_period = 36
    ema_b_period = 60
# =============== API keys ==========================
    #! Input your key and secret from Binance, then run directly.

    KEY = ''
    SECRET = ''

# ========= Main body ================================
    # for spot market
    # BASE_URL = 'https://api.binance.com' # production base url

    # for future market
    BASE_URL = 'https://fapi.binance.com' # production base url
    t = random.randint(5,20)
    
    while 1 != 0:
        Balance,UnrealizedProfit = account_P_L()
        cur_time = datetime.datetime.now()
        
        print('========================================')
        print(f'Time: {cur_time}')
        print(f"Current account balance is: {Balance}")
        print(f"Unrealized Profit is: {UnrealizedProfit}")
        print()
        print('////////////////////////////////////////')
        run_start(symbol,interval,quantity)
        print('========================================')
        print()
        time.sleep(60)