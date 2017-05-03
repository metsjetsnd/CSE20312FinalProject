#!/usr/bin/env python2.7

import requests
import sys
import csv
import os
import Queue

# Functions

#Usage function, called when -h flag or an incorrect flag is passed as a command line argument
def usage(status=0):
    print '''Usage: {} [ -l LENGTH -s SYMBOL ]
    -l LENGTH        How many days to use for time average (recommended: 30) (max: 100)
    -s SYMBOL        Symbol for desired stock (if no symbol, display list of top 10 recommended stocks from S&P 500)
    -m               MACD will run on every stock in S&P 500 and display any indexes with buy recommendations
    '''.format(
        os.path.basename(sys.argv[0])
    )
    sys.exit(status)

#Get Close Prices function, called when mean reversion algorithm is run
#Downloads appropriate data from API and returns a list containing the closing prices from the past (length) days
def getClosePrices(function, symbol, apikey, length, printPrices):
    # scrape json data
    link = 'http://www.alphavantage.co/query?function=' + function + '&symbol=' + symbol + '&apikey=' + apikey
    r = requests.get(link)
    data = r.json()
    dates = data['Time Series (Daily)'].keys()

    dates.sort();#sort dates so data is iterated through in chronological order
    closePrices = []
    
    # append closePrices array and output the data if specified
    for i in range(1, length + 1):
        closePrices.append(float(data['Time Series (Daily)'][dates[-1 * i]].get('4. close', None)))
        if printPrices:
            print data['Time Series (Daily)'][dates[-1 * i]].get('4. close', None)
    return closePrices

#Get Mean function, called when mean reversion algorithm is run
#Calls getClosePrices algorithm and calculates mean value of list that function returns
#returns a list containing both the mean of the list of prices and the list of prices itself
def getMean(function, symbol, apikey, length, printPrices):
    closePrices = getClosePrices(function, symbol, apikey, length, printPrices)

    priceSum = 0
    
    # calculate total sum of all of the closing prices
    for i in range(0, length):
        priceSum += closePrices[i]

    # calculate and return mean value
    mean = priceSum / length
    data = []
    data.append(mean)
    data.append(closePrices)
    return data

#MACD function, used when running MACD algorithm
def MACD(function, symbol, interval, series_type, apikey, length):
    # scrape json data for MACD using API
    link = 'http://www.alphavantage.co/query?function=' + function + '&symbol=' + symbol + '&interval=' + interval + '&series_type=' + series_type + '&apikey=' + apikey
    r = requests.get(link)
    data = r.json()
    dates = data['Technical Analysis: MACD'].keys()
    dates.sort();

    indicatorNow = float(data['Technical Analysis: MACD'][dates[-1]].get('MACD', None))
    signalNow = float(data['Technical Analysis: MACD'][dates[-1]].get('MACD_Signal', None))
    indicatorLast = float(data['Technical Analysis: MACD'][dates[-2]].get('MACD', None))
    signalLast = float(data['Technical Analysis: MACD'][dates[-2]].get('MACD_Signal', None))

    
    if indicatorNow - signalNow > 0 and indicatorLast - signalLast < 0:
        return 1
    elif indicatorNow - signalNow < 0 and indicatorLast - signalLast > 0:
        return -1
    else:
        return 0


# MAIN PORTION OF CODE

length = 30
args = sys.argv[1:]
singleStock = 0
SP500MACD = 0

#Parse command line arguments
while len(args) and args[0].startswith('-') and len(args[0]) > 1:
    arg = args.pop(0)
    if arg == '-s':
       symbol = args.pop(0)
       singleStock = 1
    elif arg == '-l':
       length = int(args.pop(0))
       if (length > 100):
          print "Length can not be longer than 100. Length will be set at max length of 100"
          length = 100
    elif arg == '-m':
        SP500MACD = 1
    elif arg == '-h':
       usage(0)
    else:
       usage(1)

#variables used in API call    
function = 'TIME_SERIES_DAILY'
apikey = 'ZK41'

#Code for downloading list of indexes currently in S&P 500
sp500link = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
r = requests.get(sp500link)
fileName = 'indexes.csv'
indexes = []

with open(fileName, 'w') as file:
    file.writelines(r.content)

with open(fileName, 'r') as file:
    reader = csv.reader(file, delimiter=',')
    l = list(reader)
    for stock in l:
        indexes.append(stock[0])

#If -m flag is passed as command line argument
#Run MACD algorithm on each index in S&P 500. If index passes MACD test, also run mean reversion algorithm on index (since so few stocks pass MACD test)
if SP500MACD:
    for count, index in enumerate(indexes):
        if count is 0:
            continue
        if count > 50:
            break
        if '.' in index:
            continue
        MACDResult = MACD('MACD', index, 'daily', 'close', apikey, length)
        print 'Processing', index, '...',
        if MACDResult:
            print "MACD suggests BUY"
            data = getMean(function, index, apikey, length, 0)
            print "Mean Price over Period:", data[0]
            print "Current Price:", data[1][0]

            if data[1][0] < data[0]:
                print "Mean Reversion Suggests BUY"
                print "STRONG BUY"
        else:
            print

#If single stock option is chosen by user with -s flag
#Run both MACD algorithm and mean reversion algorithm on stock and make suggestion
elif singleStock:
    data = getMean(function, symbol, apikey, length, 1)
    MACDResult = MACD('MACD', symbol, 'daily', 'close', apikey, length)
    print "Mean Price over Period:", data[0]
    print "Current Price:", data[1][0]

    if data[1][0] < data[0] and MACDResult == 1:#Passes both algorithms
        print "MACD Result: BUY"
        print "Suggestion: STRONG BUY"
    elif data[1][0] < data[0]:#Passes mean reversion only
        print "MACD Result: Inconclusive"
        print "Suggestion: WEAK BUY"
    elif data[1][0] > data[0] and MACDResult == -1: #Fails both algorithms
        print "MACD Result: SELL"
        print "Suggestion: STRONG SELL"
    else:
        print "MACD Result: Inconclusive"
        print "Suggestion: WEAK SELL" 

else:
    q = Queue.PriorityQueue() #Priority Queue for holding top 10 stocks

    for count, index in enumerate(indexes):
        if count is 0:
            continue
        if count > 50:
            break
        if '.' in index:
            continue
        print 'Processing', index, '...'
        data = getMean(function, index, apikey, length, 0)
        percentDiff = data[1][0] / data[0]
        tup = (percentDiff, index)     
        q.put(tup)

    print
    print 
    print "Top 10"
    for i in range(10):
        stock = q.get()
        print i + 1, stock[1], stock[0]
