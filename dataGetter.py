import config
import csv
from binance.client import Client
from binance.exceptions import BinanceAPIException
from requests.exceptions import ConnectionError

try:
    #Connect to Binance clieant
    client = Client(config.API_KEY, config.API_SECRET)

    print("\nThis program will fetch data for the coin selected for the last 10 days in 15 minute candles.\n")
    print("Please select a coin:")
    print('[1] -\033[38;5;208m BTC\033[0m')
    print('[2] -\033[38;5;75m ETH\033[0m')
    print('[3] -\033[38;5;226m BNB\033[0m')
    print('[4] -\033[38;5;122m LTC\033[0m')
    print('[5] -\033[38;5;135m All the above\033[0m')
    choise = int(input("Enter your number: "))

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
        print('\033[0;30;41m- Invalid Input -\033[0m',)            
    else:            
        print('\033[38;5;40m - Successfully finished -\033[0m')    

except ValueError as e: 
    print('\033[0;30;41m- Invalid Input -\033[0m',)
    print(e)

except ConnectionError as e: 
    print('\033[0;30;41m- Network Error Occured -\033[0m',)
    print(e)

except BinanceAPIException as e:
    print('\033[1;30;41m- Binance API Error Occured -\033[0m',)
    print(e)
except KeyboardInterrupt:
    print('\033\n[1;30;46m- Exiting -\033[0m',)
    exit()