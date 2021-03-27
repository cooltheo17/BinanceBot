import config
import csv
import numpy
import math
import talib
import time
from datetime import datetime
from numpy import genfromtxt
from binance.client import Client

def priceUpdater():
    
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

print("Staring Bot")
print("================")

#If you wihs to enter market now change this to 0 otherwise it will automatically enter the market at an intersection
enterNow=1
while(enterNow==0):
    #Connect the Binance API
    client = Client(config.API_KEY, config.API_SECRET)
    
    #Get all price data
    priceUpdater()
    my_data = genfromtxt('BTC_LATEST.csv', delimiter=',')
    close_btc = my_data[:,4]
    i=len(my_data)-1
    
    #Calculate macd values
    allIndexes=talib.MACD(close_btc, fastperiod=12, slowperiod=26, signalperiod=9)
    macd=allIndexes[2]
    
    #Check if MACD is performing an interection
    if (float(macd[i]) < -10 and float(macd[i-1]) > 0) or (float(macd[i]) > 10 and float(macd[i-1]) < 0):
        print("- Entering market -")
        print(datetime.now().strftime('%H:%M:%S %d-%m '))
        enterNow=1
    else:
        print("- Waiting -")
        print(datetime.now().strftime('%H:%M:%S %d-%m '))
    time.sleep(17)      

#Maintain bot after we get in the market
while(True):
    #Connect the Binance API
    client = Client(config.API_KEY, config.API_SECRET)
    
    #Get all price data
    priceUpdater()
    my_data = genfromtxt('BTC_LATEST.csv', delimiter=',')
    close_btc = my_data[:,4]
    i=len(my_data)-1

    #Calculate macd values
    allIndexes=talib.MACD(close_btc, fastperiod=12, slowperiod=26, signalperiod=9)
    macd=allIndexes[2]
    
    #We are at selling point
    if float(macd[i]) < -10:
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
            print("Selling Point")
            print(datetime.now().strftime('%H:%M:%S %d-%m '))
            buyingPrice = round(float(client.get_avg_price(symbol='BTCDOWNUSDT').get('price')),4)
            balance = round(float(client.get_asset_balance(asset='USDT').get('free')),2)-0.5
            quantity=round(balance/buyingPrice,2)
            client.order_market_buy(symbol='BTCDOWNUSDT',quantity=quantity)
            time.sleep(5)
            stopLossPrice = round(buyingPrice*0.97,4)
            takeProfitPrice = round(buyingPrice*1.08,4)
            client.order_oco_sell(symbol='BTCDOWNUSDT', quantity=quantity, price=takeProfitPrice, stopPrice=stopLossPrice, stopLimitPrice=stopLossPrice, stopLimitTimeInForce='GTC')
        else:
            print("- Waiting -")
            print(datetime.now().strftime('%H:%M:%S %d-%m '))      
    elif float(macd[i]) > 10: 
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
            print("Buying Point")
            print(datetime.now().strftime('%H:%M:%S %d-%m '))
            buyingPrice = round(float(client.get_avg_price(symbol='BTCUPUSDT').get('price')),3)
            balance = round(float(client.get_asset_balance(asset='USDT').get('free')),2)-0.5
            quantity=round(balance/buyingPrice,2)
            client.order_market_buy(symbol='BTCUPUSDT',quantity=quantity)
            time.sleep(5)
            stopLossPrice = round(buyingPrice*0.97,3)
            takeProfitPrice = round(buyingPrice*1.08,3)
            client.order_oco_sell(symbol='BTCUPUSDT', quantity=quantity, price=takeProfitPrice, stopPrice=stopLossPrice, stopLimitPrice=stopLossPrice, stopLimitTimeInForce='GTC')
        else:
            print("- Waiting -")
            print(datetime.now().strftime('%H:%M:%S %d-%m '))    
    time.sleep(177)             


