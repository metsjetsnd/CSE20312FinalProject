#!/usr/bin/env python2.7

import requests
import sys
import csv
import os

def usage(status=0):
    print '''Usage: {} [ -l LENGTH -s SYMBOL ]
    -l LENGTH        How many days to use for time average (recommended: 10)
    -s SYMBOL        Symbol for desired stock (if no symbol, display list of top 10 recommended stocks)
    '''.format(
        os.path.basename(sys.argv[0])
    )
    sys.exit(status)

# Parse command line options

length = 10
args = sys.argv[1:]
singleStock = 0

while len(args) and args[0].startswith('-') and len(args[0]) > 1:
    arg = args.pop(0)
    if arg == '-s':
       symbol = args.pop(0)
       singleStock = 1
    elif arg == '-l':
       length = int(args.pop(0))
    elif arg == '-h':
       usage(0)
    else:
       usage(1)


if singleStock:
    function = 'TIME_SERIES_DAILY'
    apikey = 'ZK41'
    link = 'http://www.alphavantage.co/query?function=' + function + '&symbol=' + symbol + '&apikey=' + apikey

    r = requests.get(link)

    data = r.json()
    dates = data['Time Series (Daily)'].keys()
    dates.sort();

    closePrices = []

    for i in range(1, length + 1):
        closePrices.append(float(data['Time Series (Daily)'][dates[-1 * i]].get('4. close', None)))
        print data['Time Series (Daily)'][dates[-1 * i]].get('4. close', None)

    priceSum = 0
    for i in range(0, length):
        priceSum += closePrices[i]

    mean = priceSum / length
    if closePrices[0] < mean:
        print "Suggestion: BUY"
    else:
        print "Suggestion: SELL"

else:
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

    stockRank = []

    for count, index in enumerate(indexes):
        if count is 0:
            continue
        if count > 50:
            break
        if '.' in index:
            continue
        function = 'TIME_SERIES_DAILY'
        apikey = 'ZK41'
        link = 'http://www.alphavantage.co/query?function=' + function + '&symbol=' + index + '&apikey=' + apikey

        r = requests.get(link)
        print 'Processing', index, '...'
        data = r.json()
        dates = data['Time Series (Daily)'].keys()
        dates.sort();

        closePrices = []

        for i in range(1, length + 1):
            closePrices.append(float(data['Time Series (Daily)'][dates[-1 * i]].get('4. close', None)))

        priceSum = 0
        for i in range(0, length):
            priceSum += closePrices[i]

        mean = priceSum / length
        percentDiff = closePrices[0] / mean
        tup = (percentDiff, index)
        if count < 11:
            stockRank.append(tup)
            stockRank.sort()
        else:
            myTuple = stockRank[9]
            percent = myTuple[0]
            if percentDiff < percent:
                stockRank.pop()
                stockRank.append(tup)
                stockRank.sort()
    print
    print 
    print "Top 10"
    for count, stock in enumerate(stockRank):
        print count + 1, stock[1], stock[0]
            








