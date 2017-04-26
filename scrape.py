#!/usr/bin/env python2.7

import requests
import sys
import csv
import os
import Queue

# Functions

def usage(status=0):
    print '''Usage: {} [ -l LENGTH -s SYMBOL ]
    -l LENGTH        How many days to use for time average (recommended: 10)
    -s SYMBOL        Symbol for desired stock (if no symbol, display list of top 10 recommended stocks from S&P 500)
    -m               MACD will run on every stock in S&P 500 and display any indexes with buy recommendations
    '''.format(
        os.path.basename(sys.argv[0])
    )
    sys.exit(status)

def getClosePrices(function, symbol, apikey, length, printPrices):
    link = 'http://www.alphavantage.co/query?function=' + function + '&symbol=' + symbol + '&apikey=' + apikey

    r = requests.get(link)

    data = r.json()
    dates = data['Time Series (Daily)'].keys()
    dates.sort();
    closePrices = []
    for i in range(1, length + 1):
        closePrices.append(float(data['Time Series (Daily)'][dates[-1 * i]].get('4. close', None)))
        if printPrices:
            print data['Time Series (Daily)'][dates[-1 * i]].get('4. close', None)
    return closePrices

def getMean(function, symbol, apikey, length, printPrices):
    closePrices = getClosePrices(function, symbol, apikey, length, printPrices)

    priceSum = 0
    for i in range(0, length):
        priceSum += closePrices[i]

    mean = priceSum / length
    data = []
    data.append(mean)
    data.append(closePrices)
    return data

def MACD(function, symbol, interval, series_type, apikey, length):
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


# Main portion of code

length = 10
args = sys.argv[1:]
singleStock = 0
SP500MACD = 0

while len(args) and args[0].startswith('-') and len(args[0]) > 1:
    arg = args.pop(0)
    if arg == '-s':
       symbol = args.pop(0)
       singleStock = 1
    elif arg == '-l':
       length = int(args.pop(0))
    elif arg == '-m':
        SP500MACD = 1
    elif arg == '-h':
       usage(0)
    else:
       usage(1)
    
function = 'TIME_SERIES_DAILY'
apikey = 'ZK41'
sp500link = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
r = requests.get(sp500link)
fileName = 'indexes.csv'
indexes = []

with open(fileName, 'w') as file:
    file.writelines(r.content)

<<<<<<< HEAD
with open(fileName, 'r') as file:
    reader = csv.reader(file, delimiter=',')
    l = list(reader)
    for stock in l:
        indexes.append(stock[0])
=======
data = r.json()

for resource in data['Time Series (Daily)'][]:
	print resource['Time Series (Daily)'][].get('4. close', None)
>>>>>>> 24b8d76cf27714e1c1f3c2fbb85ae707f6b169b6

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


elif singleStock:
    data = getMean(function, symbol, apikey, length, 1)
    MACDResult = MACD('MACD', symbol, 'daily', 'close', apikey, length)
    print "Mean Price over Period:", data[0]
    print "Current Price:", data[1][0]

    if data[1][0] < data[0] and MACDResult == 1:
        print "MACD Result: BUY"
        print "Suggestion: STRONG BUY"
    elif data[1][0] < data[0]:
        print "MACD Result: Inconclusive"
        print "Suggestion: WEAK BUY"
    elif data[1][0] > data[0] and MACDResult == -1:
        print "MACD Result: SELL"
        print "Suggestion: STRONG SELL"
    else:
        print "MACD Result: Inconclusive"
        print "Suggestion: WEAK SELL" 

else:


    #stockRank = [] # Priority Queue for ranking stocks
    q = Queue.PriorityQueue()

    for count, index in enumerate(indexes):
        if count is 0:
            continue
<<<<<<< HEAD
        if count > 50:
            break
        if '.' in index:
            continue
        print 'Processing', index, '...'
        data = getMean(function, index, apikey, length, 0)
        percentDiff = data[1][0] / data[0]
        tup = (percentDiff, index)
        '''if count < 11:
            #stockRank.append(tup)
            q.put(tup)
            #stockRank.sort()
        else:
            #myTuple = stockRank[9]
            myTuple = q[9]
            percent = myTuple[0]
            if percentDiff < percent:
                stockRank.pop()
                stockRank.append(tup)
                stockRank.sort()'''
        q.put(tup)

    print
    print 
    print "Top 10"
    '''for count, stock in enumerate(q):
        print count + 1, stock[1], stock[0]'''
    for i in range(10):
        stock = q.get()
        print i + 1, stock[1], stock[0]
=======
    else:
        print '{:3d}'.format(count + 1) + '.' , '{:8}'.format('Title:'), z
        print '{:13}'.format('     Author:'), details["author"]
        print '{:13}'.format('     Link:'), 'http://www.reddit.com' + l
        t = requests.get('http://is.gd/create.php', params={'format':'json', 'url':l})
        print '{:13}'.format('     Short:'), t.json()['shorturl']
        if count == NUMBER - 1:
            break"""
>>>>>>> 24b8d76cf27714e1c1f3c2fbb85ae707f6b169b6
