#!/usr/bin/python

import csv
import matplotlib.pyplot as pyplot
import numpy as np


f = open('data.csv','r')

#countries = ('US', 'GB', 'DE', 'JP', 'IE', 'CN','RU','None')
countries = ('AU', 'CA', 'DE', 'IN', 'KR', 'MX', 'PH', 'SE', 'TR')

freader = csv.reader(f)
hist_data = dict()

for line in freader :
    #print line
    if line.__len__() > 0 :
        country = line[2].split(' ')[0]

    if country == '' :
        country = 'None'

    if hist_data.has_key(country):
        hist_data[country] = hist_data[country] + 1
    else:
        hist_data[country] = 1
f.close()

f = open('binned_data.csv','w')

fwriter = csv.writer(f)
for country in hist_data.keys():
    fwriter.writerow([country, hist_data[country]])
f.close()


x = np.arange(0, countries.__len__())

counts = list()
for country in countries:
    counts.append(hist_data[country]) 

pyplot.bar(x, counts)
pyplot.xticks(x + 0.5, countries)
#pyplot.yscale('symlog')
pyplot.ylabel('Nodes')
pyplot.show()
