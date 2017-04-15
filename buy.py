#!/usr/bin/env python2.7

#list of growth rates of index fund
rate = [27, 11, 18, 33, 26]

value = [0,0,0,0,0]

#loop calculating initial value and value after appreciation with
#a 1000 initial investment
for i in range(5):
	value[i] = 1000+(1000*rate[i]*0.01)
	
choice = 0
top = 0
for i in range(5):
	growth = value[i] - 1000
	if growth > top:
		choice = i

print "Index fund number ",choice," should be purchased, with an appreciation of ",growth," dollars."
