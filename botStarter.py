# Disclaimer!
# This bot is designed to be informational and educational only and do not constitute investment advice.
# Use at your own risk. 
import config
import csv
import numpy
import math
import talib
import time
from datetime import datetime
from numpy import genfromtxt
from binance.client import Client
from requests.exceptions import ConnectionError
from binance.exceptions import BinanceAPIException

def priceUpdaterBTC():
    
    #Connect the Binance API
    client = Client(config.API_KEY, config.API_SECRET)

    #Open CSV file
    csvfile = open('BTC_LATEST.csv', 'w+', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    #Get candles for BTC 15 mins
    candles = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "7 days ago UTC")
    
    #Write to CSV file
    for candlestick in candles:
        candlestick_writer.writerow(candlestick) 

def marketEnterBTC(enterNow): 
  
    while(enterNow==0):
        
        #Get all price data
        priceUpdaterBTC()
        my_data = genfromtxt('BTC_LATEST.csv', delimiter=',')
        close_btc = my_data[:,4]
        i=len(my_data)-1
        
        #Calculate macd values
        allIndexes=talib.MACD(close_btc, fastperiod=12, slowperiod=26, signalperiod=9)
        macd=allIndexes[2]
        
        #Check if MACD is performing an interection
        if (float(macd[i]) < -10 and float(macd[i-1]) > 0) or (float(macd[i]) > 10 and float(macd[i-1]) < 0):
            print('\033[33;94m- Entering market -\033[0m',)
            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
            enterNow=1
        else:
            print("- Waiting -")
            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
        time.sleep(117)

def priceUpdaterLTC():
    
    #Connect the Binance API
    client = Client(config.API_KEY, config.API_SECRET)

    #Open CSV file
    csvfile = open('LTC_LATEST.csv', 'w+', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    #Get candles for LTC 15 mins
    candles = client.get_historical_klines("LTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "7 days ago UTC")
    
    #Write to CSV file
    for candlestick in candles:
        candlestick_writer.writerow(candlestick) 

def marketEnterLTC(enterNow): 
  
    while(enterNow==0):
        
        #Get all price data
        priceUpdaterBTC()
        my_data = genfromtxt('LTC_LATEST.csv', delimiter=',')
        close_btc = my_data[:,4]
        i=len(my_data)-1
        
        #Calculate macd values
        allIndexes=talib.MACD(close_btc, fastperiod=12, slowperiod=26, signalperiod=9)
        macd=allIndexes[2]
        
        #Check if MACD is performing an interection
        if (float(macd[i]) < -0.07 and float(macd[i-1]) > 0) or (float(macd[i]) > 0.07 and float(macd[i-1]) < 0):
            print('\033[33;94m- Entering market -\033[0m')
            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
            enterNow=1
        else:
            print("- Waiting -")
            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
        time.sleep(100)              

#START UP#
#Choose a coin for the bot to perform trades on
try:
    print("\nThis program will automatically perform buy and sell orders for theese coins:")
    print('[1] -\033[38;5;208m BTC\033[0m')
    print('[2] -\033[38;5;122m LTC\033[0m')
    choise = int(input("Please enter your number:"))

    #Start the bot

    print('\033[33;93m\n- Staring Bot -',)
    print("================\033[0m")

    ###########
    # BTC BOT #
    ###########
    if choise == 1:
        while(True):
        #If you wish to enter market now change this to 1 otherwise it will automatically enter the market at an intersection
            marketEnterBTC(0)

            #Maintain bot after we get in the market
            while(True):
                try:
                    #Connect the Binance API
                    client = Client(config.API_KEY, config.API_SECRET)
                    
                    #Get all price data
                    priceUpdaterBTC()
                    my_data = genfromtxt('BTC_LATEST.csv', delimiter=',')
                    close_btc = my_data[:,4]
                    i=len(my_data)-1

                    #Calculate macd values
                    allIndexes=talib.MACD(close_btc, fastperiod=12, slowperiod=26, signalperiod=9)
                    macd=allIndexes[2]
                    
                    #We are at selling point
                    if float(macd[i]) < -0.5:
                        #Cancel any BTCUP orders
                        OpenOrder = client.get_open_orders(symbol='BTCUPUSDT')
                        if(len(OpenOrder) != 0):
                            orderId=OpenOrder[0].get('orderId')
                            client.cancel_order(symbol='BTCUPUSDT',orderId=orderId)
                            time.sleep(10)  
                        #Sell any BTCUP    
                        balance_BTCUP = round(float(client.get_asset_balance(asset='BTCUP').get('free')),2)+round(float(client.get_asset_balance(asset='BTCUP').get('locked')),2)-0.01
                        if (balance_BTCUP > 0.1):
                            client.order_market_sell(symbol='BTCUPUSDT',quantity=balance_BTCUP)
                            time.sleep(10)    
                        #Buy BTCDOWN
                        balance_BTCDOWN = round(float(client.get_asset_balance(asset='BTCDOWN').get('free')),2)+round(float(client.get_asset_balance(asset='BTCDOWN').get('locked')),2)
                        if(balance_BTCDOWN < 300):
                            print('\033[33;91m- Selling Point -\033[0m')
                            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                            buyingPrice = round(float(client.get_avg_price(symbol='BTCDOWNUSDT').get('price')),4)
                            balance = round(float(client.get_asset_balance(asset='USDT').get('free')),2)-0.5
                            quantity=round(balance/buyingPrice,2)
                            client.order_market_buy(symbol='BTCDOWNUSDT',quantity=quantity)
                            time.sleep(5)
                            stopLossPrice = round(buyingPrice*0.984,4)
                            takeProfitPrice = round(buyingPrice*1.07,4)
                            client.order_oco_sell(symbol='BTCDOWNUSDT', quantity=quantity, price=takeProfitPrice, stopPrice=stopLossPrice, stopLimitPrice=stopLossPrice, stopLimitTimeInForce='GTC')
                        else:
                            print("- Waiting -")
                            print(datetime.now().strftime(' %H:%M:%S %d-%m '))      
                    elif float(macd[i]) > 0.5: 
                        #Cancel any BTCDOWN orders
                        OpenOrder = client.get_open_orders(symbol='BTCDOWNUSDT')
                        if(len(OpenOrder) != 0):
                            orderId=OpenOrder[0].get('orderId')
                            client.cancel_order(symbol='BTCDOWNUSDT',orderId=orderId)
                            time.sleep(10)   
                        #Sell any BTCDOWN
                        balance_BTCDOWN = round(float(client.get_asset_balance(asset='BTCDOWN').get('free')),2)+round(float(client.get_asset_balance(asset='BTCDOWN').get('locked')),2)
                        if (balance_BTCDOWN > 0.1):
                            client.order_market_sell(symbol='BTCDOWNUSDT',quantity=balance_BTCDOWN)
                            time.sleep(10)     
                        #Buy BTCUP
                        balance_BTCUP = round(float(client.get_asset_balance(asset='BTCUP').get('free')),2)+round(float(client.get_asset_balance(asset='BTCUP').get('locked')),2)
                        if(balance_BTCUP < 0.12):
                            print('\033[33;92m- Buying Point -\033[0m')
                            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                            buyingPrice = round(float(client.get_avg_price(symbol='BTCUPUSDT').get('price')),3)
                            balance = round(float(client.get_asset_balance(asset='USDT').get('free')),2)-0.5
                            quantity=round(balance/buyingPrice,2)
                            client.order_market_buy(symbol='BTCUPUSDT',quantity=quantity)
                            time.sleep(5)
                            stopLossPrice = round(buyingPrice*0.984,3)
                            takeProfitPrice = round(buyingPrice*1.07,3)
                            client.order_oco_sell(symbol='BTCUPUSDT', quantity=quantity, price=takeProfitPrice, stopPrice=stopLossPrice, stopLimitPrice=stopLossPrice, stopLimitTimeInForce='GTC')
                        else:
                            print("- Waiting -")
                            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                    time.sleep(30)                  
                except ConnectionError as e:
                    print('\033[0;30;41m- Network Error Occured -\033[0m',)
                    print(e)
                    print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                    time.sleep(300)
                
                except BinanceAPIException as e:
                    print('\033[0;30;41m- Binance API Error Occured -\033[0m',)
                    print(e)
                    print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                    time.sleep(300)
                except KeyboardInterrupt:
                    print('\033\n[2;30;45m- Exiting -\033[0m',)
                    exit()            
    ###########
    # LTC BOT #
    ###########
    elif choise == 2:
        while(True):
        #If you wish to enter market now change this to 1 otherwise it will automatically enter the market at an intersection
            marketEnterLTC(0)
            #Maintain bot after we get in the market
            while(True):

                try:                
                    #Connect the Binance API
                    client = Client(config.API_KEY, config.API_SECRET)
                    
                    #Get all price data
                    priceUpdaterLTC()
                    my_data = genfromtxt('LTC_LATEST.csv', delimiter=',')
                    close_btc = my_data[:,4]
                    i=len(my_data)-1

                    #Calculate macd values
                    allIndexes=talib.MACD(close_btc, fastperiod=12, slowperiod=26, signalperiod=9)
                    macd=allIndexes[2]
                    
                    #We are at selling point
                    if float(macd[i]) < -0.01:
                        #Cancel any LTCUP orders
                        OpenOrder = client.get_open_orders(symbol='LTCUPUSDT')
                        if(len(OpenOrder) != 0):
                            orderId=OpenOrder[0].get('orderId')
                            client.cancel_order(symbol='LTCUPUSDT',orderId=orderId)
                            time.sleep(10)  
                        #Sell any LTCUP    
                        balance_LTCUP = round(float(client.get_asset_balance(asset='LTCUP').get('free')),2)+round(float(client.get_asset_balance(asset='LTCUP').get('locked')),2)-0.01
                        if (balance_LTCUP > 0.5):
                            client.order_market_sell(symbol='LTCUPUSDT',quantity=balance_LTCUP)
                            time.sleep(10)    
                        #Buy LTCDOWN
                        balance_LTCDOWN = round(float(client.get_asset_balance(asset='LTCDOWN').get('free')),2)+round(float(client.get_asset_balance(asset='LTCDOWN').get('locked')),2)
                        if(balance_LTCDOWN < 3000):
                            print('\033[33;91m- Selling Point -\033[0m',)
                            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                            buyingPrice = round(float(client.get_avg_price(symbol='LTCDOWNUSDT').get('price')),4)
                            balance = round(float(client.get_asset_balance(asset='USDT').get('free')),2)-0.5
                            quantity=round(balance/buyingPrice,2)
                            client.order_market_buy(symbol='LTCDOWNUSDT',quantity=quantity)
                            time.sleep(5)
                            stopLossPrice = round(buyingPrice*0.984,4)
                            takeProfitPrice = round(buyingPrice*1.07,4)
                            client.order_oco_sell(symbol='LTCDOWNUSDT', quantity=quantity, price=takeProfitPrice, stopPrice=stopLossPrice, stopLimitPrice=stopLossPrice, stopLimitTimeInForce='GTC')
                        else:
                            print("- Waiting -")
                            print(datetime.now().strftime(' %H:%M:%S %d-%m '))      
                    elif float(macd[i]) > 0.01: 
                        #Cancel any LTCDOWN orders
                        OpenOrder = client.get_open_orders(symbol='LTCDOWNUSDT')
                        if(len(OpenOrder) != 0):
                            orderId=OpenOrder[0].get('orderId')
                            client.cancel_order(symbol='LTCDOWNUSDT',orderId=orderId)
                            time.sleep(10)   
                        #Sell any LTCDOWN
                        balance_LTCDOWN = round(float(client.get_asset_balance(asset='LTCDOWN').get('free')),2)+round(float(client.get_asset_balance(asset='LTCDOWN').get('locked')),2)
                        if (balance_LTCDOWN > 2000):
                            client.order_market_sell(symbol='LTCDOWNUSDT',quantity=balance_LTCDOWN)
                            time.sleep(10)     
                        #Buy LTCUP
                        balance_LTCUP = round(float(client.get_asset_balance(asset='LTCUP').get('free')),2)+round(float(client.get_asset_balance(asset='LTCUP').get('locked')),2)
                        if(balance_LTCUP < 0.5):
                            print('\033[33;92m- Buying Point -\033[0m',)
                            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                            buyingPrice = round(float(client.get_avg_price(symbol='LTCUPUSDT').get('price')),3)
                            balance = round(float(client.get_asset_balance(asset='USDT').get('free')),2)-0.5
                            quantity=round(balance/buyingPrice,2)
                            client.order_market_buy(symbol='LTCUPUPUSDT',quantity=quantity)
                            time.sleep(5)
                            stopLossPrice = round(buyingPrice*0.984,3)
                            takeProfitPrice = round(buyingPrice*1.07,3)
                            client.order_oco_sell(symbol='LTCUPUSDT', quantity=quantity, price=takeProfitPrice, stopPrice=stopLossPrice, stopLimitPrice=stopLossPrice, stopLimitTimeInForce='GTC')
                        else:
                            print("- Waiting -")
                            print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                    time.sleep(30)                  
                except ConnectionError as e: 
                    print('\033[0;30;41m- Network Error Occured -\033[0m')
                    print(e)
                    print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                    time.sleep(300)
                
                except BinanceAPIException as e:
                    print('\033[1;30;41m- Binance API Error Occured -\033[0m')
                    print(e)
                    print(datetime.now().strftime(' %H:%M:%S %d-%m '))
                    time.sleep(300)
                except KeyboardInterrupt:
                    print('\033\n[1;30;46m- Exiting -\033[0m',)
                    exit()            
    else:
        print('\033[0;30;41m- Error please enter a valid option -\033[0m')
except KeyboardInterrupt:
    print('\033\n[1;30;46m- Exiting -\033[0m')
    exit()        
