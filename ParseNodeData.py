#!/usr/bin/python

import time
import datetime
import dateutil.parser as dateparser
import subprocess
import csv
import sys

#################################################
# Config options
#################################################
url_base='http://blockchain.info/ip-log'
interval_hours = 720; # duration of interval
start_offset_hours = 0; # number of house in the past to start
start_offset_seconds = start_offset_hours * 3600 
interval_seconds = interval_hours * 3600
sleep_time = 0 # second sleep time 
outputfile = 'data.csv'
#################################################

firsttime_found = False
finished = False
page_num = 0

nodes = list()
while finished == False:
    cmd = ['wget', url_base + '/' +  str(page_num)]
    print cmd
    subprocess.call(cmd) 
    cmd = ['./parse.sh', str(page_num)] 
    print cmd
    subprocess.call(cmd) 
    filename = str(page_num) + "_parsed"
    f = open(filename)
    line = f.readline().rstrip('\n')
    nodes_added = 0
    last_timestamp = 0 
    last_isoformat = ''
    while line :
        ip = line
	line = f.readline().rstrip('\n')

	ts = dateparser.parse(line)
	timestamp = time.mktime(ts.timetuple())

	if firsttime_found == False:
            now = timestamp
	    min_ts = now
	    start_seconds = now - start_offset_seconds
	    end_seconds = now - start_offset_seconds - interval_seconds
            print "Looking at from ", str(end_seconds) , " to " , start_seconds 
            firsttime_found = True	

	line = f.readline().rstrip('\n')
	country = line
	if timestamp < min_ts :
            min_ts = timestamp
	if ((timestamp > end_seconds) & (timestamp < start_seconds) ) :
	    nodes.append([timestamp,ts.isoformat(),country,ip])
	    nodes_added = nodes_added + 1 
 	    last_timestamp = timestamp 
            last_isoformat = ts.isoformat() 
	if min_ts < end_seconds :
	    finished = True 
	line = f.readline().rstrip('\n')
    print "Nodes added: " , str(nodes_added) 
    print "Last timestamp : ", ts.isoformat() , "(" , str(last_timestamp), ")" 
    print "Min timestamp : " , str(min_ts)
    page_num = page_num + 1
    time.sleep(sleep_time)


outfile = open(outputfile, "w")
out_writer = csv.writer(outfile, delimiter = ',')
for i in range(0,nodes.__len__()):
    out_writer.writerow(nodes[i]);
outfile.close()
