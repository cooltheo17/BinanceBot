import config
import csv
from binance.client import Client

#Connect to Binance clieant
client = Client(config.API_KEY, config.API_SECRET)

print("This program will fetch data for the coin selected for the last 10 days in 15 minute candles.")
print("[1] - BTC")
print("[2] - ETH")
print("[3] - BNB")
print("[4] - LTC")
print("[5] - All the above")
choise = int(input("Please enter your number:"))

#Create csv file of bitcoin prices in the last 10 days
if(choise == 1 or choise == 5):
    csvfile = open('PARA_BTC_15M.csv', 'w+', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    candles = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "10 days ago UTC")
    for candlestick in candles:
        candlestick_writer.writerow(candlestick) 

#Create csv file of etherium prices in the last 10 days
if(choise == 2 or choise == 5):
    csvfile = open('PARA_ETH_15M.csv', 'w+', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    candles = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_15MINUTE, "10 days ago UTC")
    for candlestick in candles:
        candlestick_writer.writerow(candlestick)

#Create csv file of BNB prices in the last 10 days
if(choise == 3 or choise == 5):
    csvfile = open('PARA_BNB_15M.csv', 'w+', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    candles = client.get_historical_klines("BNBUSDT", Client.KLINE_INTERVAL_15MINUTE, "10 days ago UTC")
    for candlestick in candles:
        candlestick_writer.writerow(candlestick)      

#Create csv file of LTC prices in the last 10 days
if(choise == 4 or choise == 5):
    csvfile = open('PARA_LTC_15M.csv', 'w+', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    candles = client.get_historical_klines("LTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "10 days ago UTC")
    for candlestick in candles:
        candlestick_writer.writerow(candlestick)
if(choise < 1 or choise >5):            
    print("Error please try again.")
else:            
    print("Succesfully finished!")       