#!/usr/bin/env python2.7

#Example list containing closing prices which will be downloaded from yahoo finance
closePrices = [10, 11, 12, 10, 9, 8, 11, 10, 9, 8, 10, 11, 13]
priceSum = 0
shouldBuy = 0
for i in range(10):
	priceSum += closePrices[-1*(i+1)]
mean = priceSum / 10
if closePrices[-1] < mean:
	shouldBuy = 1
if shouldBuy:
	print "This stock should be purchased"
else:
	print "This stock should not be purchased"

		
