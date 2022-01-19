# Funding rate arbitrage strategy trading code.
#! Author: Cholian Li
# Contact: 
#! cholianli970518@gmail.com
# Created at 20220118

'''
############################## logging ##########################################


########################################################################
'''


import pandas as pd
import numpy as np

import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

from pandas import json_normalize

import datetime as dt

import numpy as np
import math

# ============================ api module =====================================
''' ======  begin of functions, you don't need to touch ====== '''
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

''' ======  end of functions ====== '''


# =========================== time module =====================================
def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else:
        return False
    
def obtain_tp(start = True):
    # start
    if start:
        starting_time = dt.datetime(2020,1,2,23,54,0)
        time_point = starting_time + pd.to_timedelta([0,8,16], unit = 'h')
        return time_point
    
    # end
    starting_time = dt.datetime(2020,1,2,0,0,0)
    time_point = starting_time + pd.to_timedelta([0,8,16], unit = 'h')
    return time_point

def obtain_time_pair(time_point):
    tm_pair = []
    for i in range(len(time_point)):
        time_ed = time_point[i] + pd.Timedelta(minutes=5)
        tm_pair.append((time_point[i].time(),time_ed.time()))
        
    return tm_pair

def inPeriod(utcNow,prior = True):

    if prior:
        for i in range(len(time_pair_prior)):
            if isNowInTimePeriod(time_pair_prior[i][0],time_pair_prior[i][1],utcNow):
                return True
        return False
    
    elif not prior:
        for i in range(len(time_pair_after)):
            if isNowInTimePeriod(time_pair_after[i][0],time_pair_after[i][1],utcNow):              
                return True
        return False

    return False


# =========================== symbol selection module ======================================
def obatin_all_current():

    BASE_URL = 'https://fapi.binance.com' # production base url
    url_path = '/fapi/v1/premiumIndex'

    response = send_public_request(url_path, params)
    df = json_normalize(response)
    df = df.merge(perpetual_token,left_on='symbol',right_on='symbol')
    
    return df
        
        
def select_symbol(bound = 0.0028):

    fundingrate_df['lastFundingRate'] = fundingrate_df['lastFundingRate'].astype(float)
    sorted_fr = fundingrate_df.sort_values(key = abs,by = 'lastFundingRate',ascending=False)
    sorted_fr = sorted_fr.reset_index(drop=True)

    # 0.0004*2 手续费 + 0.002 95%的置信区间波动
    target_smb_ls = sorted_fr[abs(sorted_fr['lastFundingRate']) >= bound]['symbol']
    
    if target_smb_ls.empty:
        return None

    else:
        target_smb = sorted_fr['symbol'][0]
        return target_smb


# ============================= trading module ====================================
def currentFR(target_smb):
    FR = fundingrate_df.loc[fundingrate_df.symbol == target_smb,'lastFundingRate'].tolist()[0]
    # print(FR)
    return float(FR)

def currentPosAmt(target_smb):
    BASE_URL = 'https://fapi.binance.com' # production base url
    url_path = '/fapi/v2/account'
    
    response = send_signed_request('GET', url_path)
    
    account_positions = json_normalize(response['positions'])
    account_positions['positionAmt'] = account_positions['positionAmt'].astype(float)
    
    posAmt = account_positions.loc[account_positions.symbol == target_smb,'positionAmt'].values[0]
    
    return posAmt


def Order_BUY_Market(symbol,quantity):
    
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': quantity,
    }
    response = send_signed_request('POST', '/fapi/v1/order',params)
    return response


def Order_SELL_Market(symbol,quantity):
    
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'MARKET',
        'quantity': quantity,
    }

    response = send_signed_request('POST', '/fapi/v1/order',params)
    return response
    
    
def change_leverage(symbol,leverage = 1):
    params = {
        'symbol': symbol,
        'leverage': leverage,
        # 'origClientOrderId':"wWtnnmizY3xq2Cji8oaidM"
    }
    response = send_signed_request('POST', '/fapi/v1/leverage',params)
    print(response)
    
    
def trading_quantity(target_smb,trading_amount):
 
    # obtain the current price
    current_price = fundingrate_df[fundingrate_df['symbol'] == target_smb]['markPrice'].values[0]
    current_price = float(current_price)
    
    # calculate the quantity with the trading amount
    quantity = trading_amount / current_price
    
    # calculate the round number
    round_num = np.log10(current_price /trading_amount)
    round_num = math.ceil(round_num)
    
    # round the quantity
    quantity = round(quantity,round_num)
    
    return quantity




# =============================== main module ==============================================

def runstart():

    # out of loop
    # parameters

    in_order = False
    leverage = 1
    trading_amount = 100 # e.g 100 -> $100
    funding_rate_bound = 0.0008

    # inside of loop
    
    # i = 0
    while 1 > 0:
             
        # time module
        # i += 1
        # utcNow = dt.datetime(2022,1,2,7,51,0) + pd.Timedelta(i,unit="minutes")
        utcNow = dt.datetime.utcnow()

        print(utcNow)
        utcNowTime = utcNow.time()

        # prior
        if inPeriod(utcNowTime,prior = True):
            print('=======================================================')
            print('Prior period: Starting at', utcNow)

            if not in_order:
                print('Prior period: No order existed before')

                #! obtain usefull information, this will be used for the whole loop
                global fundingrate_df
                fundingrate_df = obatin_all_current()
                target_smb = select_symbol(bound = funding_rate_bound)
                print('Prior period: Selecting target Symbol:',target_smb)
                
                # if there is a target smb that satisfies the band, for example, funding rate <= -0.28%
                if target_smb:
                    
                    # no position currently
                    if currentPosAmt(target_smb) == 0:
                        print('Prior period: Current Funding rate:',currentFR(target_smb))
                        
                        # Negative Funding Rate
                        if currentFR(target_smb) < 0:
                            
                            print('Prior period: Change the leverage')                        
                            change_leverage(target_smb,leverage)

                            # orderLong()
                            quantity = trading_quantity(target_smb,trading_amount)
                            response = Order_BUY_Market(target_smb,quantity)
                            
                            # avoid the failed order
                            if len(response) > 10:
                                print(f'Prior period: Placed a Long position,{target_smb},{quantity}')
                                print(response)
                                in_order = True # loop indicator
                            
                        # Positive Funding Rate
                        elif currentFR(target_smb) > 0:
                            
                            print('Prior period: Change the leverage')                        
                            change_leverage(target_smb,leverage)
                            
                            # orderShort()
                            quantity = trading_quantity(target_smb,trading_amount)
                            response = Order_SELL_Market(target_smb,quantity)
                            
                            # avoid the failed order
                            if len(response) > 10:
                                print(f'Prior period: Placed a Short position,{target_smb},{quantity}')   
                                print(response)
                                in_order = True # loop indicator
                    else:
                        print('Prior period: Current position is not clear, BREAK!')
                        break
                        
                else: 
                    print('Prior period: No satisfied symbol')
            else:
                print('Prior period: Waiting for closing position')
            
        elif inPeriod(utcNowTime,prior = False):
            
            print('////////////////////////////////////////////////')
            print('After period: Starting at',utcNow)
            
            if in_order:
                print('After period: Entering the after period for the order')

                if utcNowTime.minute == 0 :
                    print('After period: Waiting for funding rate settlement......')
                    time.sleep(60) # sleep for funding rate settlement
            
                # long position
                if currentPosAmt(target_smb) > 0:
                    
                    # Sell()
                    Order_SELL_Market(target_smb,quantity)
                    print('After period: Long position Closed')
                    in_order = False
                    
                # short postion 
                elif currentPosAmt(target_smb) < 0:
                    
                    # BUY()
                    Order_BUY_Market(target_smb,quantity)
                    print('After period: Short position Closed')   
                    in_order = False
                
                else:
                    print('After period: Error! No position was closed')
                    in_order = False
                    
                print('Order finished')
                print('==================================================')
                
            else:  
                # Sleep time for each order operation
                time.sleep(60)
                
        # Sleep time for each loop
        time.sleep(20)
        
        
if __name__ == '__main__':
    
# =================================================================================================    
    #! 这个apikey是链接future 账户的，可以进行实盘交易的
    #! 谨慎！

    KEY = ''
    SECRET = ''
    
# =================================================================================================

    # obtain the exchange_info
    BASE_URL = 'https://fapi.binance.com' # production base url
    url_path = '/fapi/v1/exchangeInfo'
    params = {}
    response = send_public_request(url_path, params)
    exchange_info = json_normalize(response['symbols'])
    perpetual_token = exchange_info[exchange_info['contractType'] == 'PERPETUAL']
    
    # prepare the time interval
    time_point_prior = obtain_tp()
    time_point_after = obtain_tp(start=False)
    time_pair_prior = obtain_time_pair(time_point_prior)
    time_pair_after = obtain_time_pair(time_point_after)
    
# =================================================================================================    
    runstart()