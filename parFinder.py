#Import libraries
import numpy
import talib
import config
from numpy import genfromtxt

#--------------------------------
#Perform calculations for bitcoin
#--------------------------------
print("(Time period: 10 days)\n")

my_data = genfromtxt('PARA_BTC_15M.csv', delimiter=',')
close_btc = my_data[:,4]
i=len(close_btc)-1
#Calculate macd and macd signal values
allIndexes=talib.MACD(close_btc, fastperiod=12, slowperiod=26, signalperiod=9)
macd=allIndexes[0]
macdsignal=allIndexes[1]

#print table titles
print('{:-^{width}}'.format('', width=34))
print("|"+'{: ^{width}}'.format('\033[38;5;208m- BTC -\033[0m', width=47)+"|")
print("+"+'{:-^{width}}'.format('', width=32)+"+")

#Calculate alpha profit (if we just invested and left the money)
balance=100
alphaInvestment=round((balance/close_btc[0]*close_btc[i])-balance,2)

#print alpha profit
print("|"+'{: ^{width}}'.format('Alpha profit: '+str(alphaInvestment)+" $", width=32)+"|")
print("+"+'{:-^{width}}'.format('', width=32)+"+")

#Buy bitcoin at buying point and sell at selling point (Simple MACD)
balance=100
btcAmount=0
for x in range(1, i):
    if(macd[x] < macdsignal[x]) and (macd[x-1] > macdsignal[x-1]):
        btcAmount = balance/close_btc[x]
        balance = 0

    elif(macd[x] > macdsignal[x]) and (macd[x-1] < macdsignal[x-1]) and btcAmount != 0:
        balance = btcAmount * close_btc[x]
        btcAmount = 0    

#Convert BTC to usdt
if(btcAmount != 0):
    balance = btcAmount * close_btc[i]
simpleInvestment=round(balance-100,2)

#print simple mac profit
print("|"+'{: ^{width}}'.format('Simple MACD profit: '+str(simpleInvestment)+" $", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")

#Buy bitcoin at buying point and sell at selling point
# with take profits and stop limits (Complex MACD)
balance=100
btcAmount=0
btcPrice=0
takeProfit=5
bestParameter=0
bestBalance=0

for p in range(-6,0):
    for x in range(1, i):
        if(macd[x] < macdsignal[x]) and (macd[x-1] > macdsignal[x-1]):
            btcAmount = balance/close_btc[x]
            btcPrice = close_btc[x]
            balance = 0

        elif(macd[x] > macdsignal[x]) and (macd[x-1] < macdsignal[x-1]) and btcAmount != 0:
            balance = btcAmount * close_btc[x]
            btcAmount = 0
    
        if(btcAmount > 0):
            percentageChange = 100*(close_btc[x] - btcPrice)/btcPrice
            if (percentageChange < p):
                balance = btcAmount * close_btc[x]
                btcAmount = 0   

    if(btcAmount != 0):
        balance = btcAmount * close_btc[i]
        simpleInvestment=round(balance-100,2)
    if(balance > bestBalance):
        bestBalance = balance
        bestParameter = p


complexInvestment=round(bestBalance-100,2)
print("|"+'{: ^{width}}'.format('Complex MACD profit: '+str(complexInvestment)+" $", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")
print("|"+'{: ^{width}}'.format('Stop Limit: '+str(bestParameter)+" %", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")

#--------------------------------
#Perform calculations for etherium
#--------------------------------

my_data = genfromtxt('PARA_ETH_15M.csv', delimiter=',')
close_eth = my_data[:,4]

#Calculate macd and macd signal values
allIndexes=talib.MACD(close_eth, fastperiod=12, slowperiod=26, signalperiod=9)
macd=allIndexes[0]
macdsignal=allIndexes[1]

#print table titles
print("|"+'{: ^{width}}'.format('\033[38;5;75m- ETH -\033[0m', width=46)+"|")
print("+"+'{:-^{width}}'.format('', width=32)+"+")
#Calculate alpha profit (if we just invested and left the money)
balance=100
alphaInvestment=round((balance/close_eth[0]*close_eth[i])-balance,2)
print("|"+'{: ^{width}}'.format('Alpha profit: '+str(alphaInvestment)+" $", width=32)+"|")
print("+"+'{:-^{width}}'.format('', width=32)+"+")

balance=100
ethAmount=0

for x in range(1, i):
    if(macd[x] > macdsignal[x]) and (macd[x-1] < macdsignal[x-1]):
        ethAmount = balance/close_eth[x]
        balance = 0

    elif(macd[x] < macdsignal[x]) and (macd[x-1] > macdsignal[x-1]) and ethAmount != 0:
        balance = ethAmount * close_eth[x]
        ethAmount = 0

#Convert ETH to usdt
if(ethAmount != 0):
    balance = ethAmount * close_eth[i]
simpleInvestment=round(balance-100,2)
#print simple mac profit
print("|"+'{: ^{width}}'.format('Simple MACD profit: '+str(simpleInvestment)+" $", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")

#Buy ethereum at buying point and sell at selling point
# with take profits and stop limits (Complex MACD)
balance=100
ethAmount=0
ethPrice=0
bestParameter=0
bestBalance=0

for p in range(-6,0):
    for x in range(1, i):
        if(macd[x] < macdsignal[x]) and (macd[x-1] > macdsignal[x-1]):
            ethAmount = balance/close_eth[x]
            ethPrice = close_eth[x]
            balance = 0

        elif(macd[x] > macdsignal[x]) and (macd[x-1] < macdsignal[x-1]) and ethAmount != 0:
            balance = ethAmount * close_eth[x]
            ethAmount = 0
    
        if(ethAmount > 0):
            percentageChange = 100*(close_eth[x] - ethPrice)/ethPrice
            if (percentageChange < p):
                balance = ethAmount * close_eth[x]
                ethAmount = 0

    if(ethAmount != 0):
        balance = ethAmount * close_eth[i]
    simpleInvestment=round(balance-100,2)
    if(balance > bestBalance):
        bestBalance = balance
        bestParameter = p

complexInvestment=round(bestBalance-100,2)
print("|"+'{: ^{width}}'.format('Complex MACD profit: '+str(complexInvestment)+" $", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")
print("|"+'{: ^{width}}'.format('Stop Limit: '+str(bestParameter)+" %", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")
#--------------------------------
#Perform calculations for BNB
#--------------------------------

my_data = genfromtxt('PARA_BNB_15M.csv', delimiter=',')
close_bnb = my_data[:,4]

#Calculate macd and macd signal values
allIndexes=talib.MACD(close_bnb, fastperiod=12, slowperiod=26, signalperiod=9)
macd=allIndexes[0]
macdsignal=allIndexes[1]

#print table titles
print("|"+'{: ^{width}}'.format('\033[38;5;226m- BNB -\033[0m', width=47)+"|")
print("+"+'{:-^{width}}'.format('', width=32)+"+")

#Calculate alpha profit (if we just invested and left the money)
balance=100
alphaInvestment=round((balance/close_bnb[0]*close_bnb[i])-balance,2)
print("|"+'{: ^{width}}'.format('Alpha profit: '+str(alphaInvestment)+" $", width=32)+"|")
print("+"+'{:-^{width}}'.format('', width=32)+"+")

balance=100
bnbAmount=0
for x in range(1, i):
    if(macd[x] > macdsignal[x]) and (macd[x-1] < macdsignal[x-1]):
        bnbAmount = balance/close_bnb[x]
        balance = 0

    elif(macd[x] < macdsignal[x]) and (macd[x-1] > macdsignal[x-1]) and bnbAmount != 0:
        balance = bnbAmount * close_bnb[x]
        bnbAmount = 0 

#Convert BNB to usdt
if(bnbAmount != 0):
    balance = bnbAmount * close_bnb[i]
simpleInvestment=round(balance-100,2)

#print simple mac profit
print("|"+'{: ^{width}}'.format('Simple MACD profit: '+str(simpleInvestment)+" $", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")

#Buy BNB at buying point and sell at selling point
# with take profits and stop limits (Complex MACD)
balance=100
bnbAmount=0
bnbPrice=0
bestParameter=0
bestBalance=0

for p in range(-6,0):
    for x in range(1, i):
        if(macd[x] < macdsignal[x]) and (macd[x-1] > macdsignal[x-1]):
            bnbAmount = balance/close_bnb[x]
            bnbPrice = close_bnb[x]
            balance = 0

        elif(macd[x] > macdsignal[x]) and (macd[x-1] < macdsignal[x-1]) and bnbAmount != 0:
            balance = bnbAmount * close_bnb[x]
            bnbAmount = 0
    
        if(bnbAmount > 0):
            percentageChange = 100*(close_bnb[x] - bnbPrice)/bnbPrice
            if (percentageChange < p):
                balance = bnbAmount * close_bnb[x]
                bnbAmount = 0   

    if(bnbAmount != 0):
        balance = bnbAmount * close_bnb[i]
    simpleInvestment=round(balance-100,2)
    if(balance > bestBalance):
        bestBalance = balance
        bestParameter = p


complexInvestment=round(bestBalance-100,2)
print("|"+'{: ^{width}}'.format('Complex MACD profit: '+str(complexInvestment)+" $", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")
print("|"+'{: ^{width}}'.format('Stop Limit: '+str(bestParameter)+" %", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")

#--------------------------------
#Perform calculations for LTC
#--------------------------------

my_data = genfromtxt('PARA_LTC_15M.csv', delimiter=',')
close_ltc = my_data[:,4]

#Calculate macd and macd signal values
allIndexes=talib.MACD(close_ltc, fastperiod=12, slowperiod=26, signalperiod=9)
macd=allIndexes[0]
macdsignal=allIndexes[1]

#print table titles
print("|"+'{: ^{width}}'.format('\033[38;5;122m- LTC -\033[0m', width=47)+"|")
print("+"+'{:-^{width}}'.format('', width=32)+"+")

#Calculate alpha profit (if we just invested and left the money)
balance=100
alphaInvestment=round((balance/close_ltc[0]*close_ltc[i])-balance,2)
print("|"+'{: ^{width}}'.format('Alpha profit: '+str(alphaInvestment)+" $", width=32)+"|")
print("+"+'{:-^{width}}'.format('', width=32)+"+")

balance=100
ltcAmount=0
for x in range(1, i):
    if(macd[x] > macdsignal[x]) and (macd[x-1] < macdsignal[x-1]):
        ltcAmount = balance/close_ltc[x]
        balance = 0

    elif(macd[x] < macdsignal[x]) and (macd[x-1] > macdsignal[x-1]) and ltcAmount != 0:
        balance = ltcAmount * close_ltc[x]
        ltcAmount = 0 

#Convert LTC to usdt
if(ltcAmount != 0):
    balance = ltcAmount * close_ltc[i]
simpleInvestment=round(balance-100,2)

#print simple mac profit
print("|"+'{: ^{width}}'.format('Simple MACD profit: '+str(simpleInvestment)+" $", width=32)+"|")
print("+"+'{:-^{width}}'.format('', width=32)+"+")    

#Buy litecoin at buying point and sell at selling point
# with take profits and stop limits (Complex MACD)
balance=100
ltcAmount=0
ltcPrice=0
bestParameter=0
bestBalance=0

for p in range(-6,0):
    for x in range(1, i):
        if(macd[x] < macdsignal[x]) and (macd[x-1] > macdsignal[x-1]):
            ltcAmount = balance/close_ltc[x]
            ltcPrice = close_ltc[x]
            balance = 0

        elif(macd[x] > macdsignal[x]) and (macd[x-1] < macdsignal[x-1]) and ltcAmount != 0:
            balance = ltcAmount * close_ltc[x]
            ltcAmount = 0
    
        if(ltcAmount > 0):
            percentageChange = 100*(close_ltc[x] - ltcPrice)/ltcPrice
            if (percentageChange < p):
                balance = ltcAmount * close_ltc[x]
                ltcAmount = 0   

    if(ltcAmount != 0):
        balance = ltcAmount * close_ltc[i]
    simpleInvestment=round(balance-100,2)
    if(balance > bestBalance):
        bestBalance = balance
        bestParameter = p


complexInvestment=round(bestBalance-100,2)
print("|"+'{: ^{width}}'.format('Complex MACD profit: '+str(complexInvestment)+" $", width=32)+"|")    
print("+"+'{:-^{width}}'.format('', width=32)+"+")
print("|"+'{: ^{width}}'.format('Stop Limit: '+str(bestParameter)+" %", width=32)+"|")    
print('{:-^{width}}'.format('', width=34))
print("")
