import config
import csv
import numpy
import math
import talib
import config
import time
from numpy import genfromtxt
from binance.client import Client

def priceUpdater():
    client = Client(config.API_KEY, config.API_SECRET)

    csvfile = open('BTC_LATEST.csv', 'w+', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    candles = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "7 days ago UTC")
    for candlestick in candles:
        candlestick_writer.writerow(candlestick) 

client = Client(config.API_KEY, config.API_SECRET)
priceUpdater()
my_data = genfromtxt('BTC_LATEST.csv', delimiter=',')
close_btc = my_data[:,4]
i=len(my_data)-1

#Calculate macd and macd signal values
allIndexes=talib.MACD(close_btc, fastperiod=12, slowperiod=26, signalperiod=9)
macd=allIndexes[2]
print(macd[i])
print("Staring Bot")
print("================")
while(0):
    #We are at selling point
    if macd[i] < 0 and macd[i-1] > 0 and float(macd[i]) < -0.10:
        #Sell any BTCUP
        balance_BTCUP = round(float(client.get_asset_balance(asset='BTCUP').get('free')),2)
        if (balance_BTCUP > 0.1):
            client.order_market_sell(symbol='BTCUPUSDT',quantity=balance_BTCUP)
            time.sleep(10)    
        #Cancel any BTCUP orders
        OpenOrder = client.get_open_orders(symbol='BTCUPUSDT')
        if(len(OpenOrder) != 0):
            orderId=OpenOrder[0].get('orderId')
            client.cancel_order(symbol='BTCUPUSDT',orderId=orderId)    
        #Cancel any BTCDOWN orders
        OpenOrder = client.get_open_orders(symbol='BTCDOWNUSDT')
        if(len(OpenOrder) != 0):
            orderId=OpenOrder[0].get('orderId')
            client.cancel_order(symbol='BTCDOWNUSDT',orderId=orderId)
        #Buy BTCDOWN
        balance_BTCDOWN = round(float(client.get_asset_balance(asset='BTCDOWN').get('free')),2)
        if(balance_BTCDOWN < 300):
            print("Selling Point")
            buyingPrice = round(float(client.get_avg_price(symbol='BTCDOWNUSDT').get('price')),4)
            balance = round(float(client.get_asset_balance(asset='USDT').get('free')),2)-0.5
            quantity=round(balance/buyingPrice,2)
            client.order_market_buy(symbol='BTCDOWNUSDT',quantity=quantity)
            time.sleep(5)
            stopLossPrice = round(buyingPrice*0.97,4)
            takeProfitPrice = round(buyingPrice*1.08,4)
            client.order_oco_sell(symbol='BTCDOWNUSDT', quantity=quantity, price=takeProfitPrice, stopPrice=stopLossPrice, stopLimitPrice=stopLossPrice, stopLimitTimeInForce='GTC')
        else:
            print("Waiting")    
    elif macd[i] > 0 and macd[i-1] < 0 and float(macd[i]) > 0.10:    
        #Sell any BTCDOWN
        balance_BTCDOWN = round(float(client.get_asset_balance(asset='BTCDOWN').get('free')),2)
        if (balance_BTCDOWN > 0.1):
            client.order_market_sell(symbol='BTCDOWNUSDT',quantity=balance_BTCDOWN)
            time.sleep(10)    
        #Cancel any BTCDOWN orders
        OpenOrder = client.get_open_orders(symbol='BTCDOWNUSDT')
        if(len(OpenOrder) != 0):
            orderId=OpenOrder[0].get('orderId')
            client.cancel_order(symbol='BTCDOWNUSDT',orderId=orderId)    
        #Cancel any BTCUP orders
        OpenOrder = client.get_open_orders(symbol='BTCUPUSDT')
        if(len(OpenOrder) != 0):
            orderId=OpenOrder[0].get('orderId')
            client.cancel_order(symbol='BTCUPUSDT',orderId=orderId)
        
        #Buy BTCUP
        balance_BTCUP = round(float(client.get_asset_balance(asset='BTCUP').get('free')),2)
        if(balance_BTCUP < 0.12):
            print("Buying Point")
            buyingPrice = round(float(client.get_avg_price(symbol='BTCUPUSDT').get('price')),3)
            balance = round(float(client.get_asset_balance(asset='USDT').get('free')),2)-0.5
            quantity=round(balance/buyingPrice,2)
            client.order_market_buy(symbol='BTCUPUSDT',quantity=quantity)
            time.sleep(5)
            stopLossPrice = round(buyingPrice*0.97,3)
            takeProfitPrice = round(buyingPrice*1.08,3)
            client.order_oco_sell(symbol='BTCUPUSDT', quantity=quantity, price=takeProfitPrice, stopPrice=stopLossPrice, stopLimitPrice=stopLossPrice, stopLimitTimeInForce='GTC')
        else:
            print("Waiting")
    time.sleep(17)             


