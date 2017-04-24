#!/usr/bin/env python

import time, os, sys, datetime, csv, urllib2, socket, re

def fetchData(url):
    response = urllib2.urlopen(url, timeout=1)
    cr = csv.reader(response)
    haveReadFirstRow = False
    for row in cr:
        if(haveReadFirstRow):
            return row
        haveReadFirstRow = True
    return "No Data"

def csv_append(file_name, somedata):
    """Function to append (or write) data to a csv file

        This function makes sure a USB flash drive is plugged into the node and creates
        a file in it for the current experiment. NOTE: THIS FUNCTION IS HALTING.

        Args:
        file_name: the string name of the file you want to append to
        somedata: a list of all the data you want to append, formatted [thing1,thing2,etc]

        Returns:
        none

        Edits:
        CSV: Appends to a CSV file.

    """
    with open(file_name, "a") as csvfile:
        testwriter = csv.writer(csvfile)
        testwriter.writerow(somedata)

    csvfile.close()

urls = []
leases = open(/var/lib/misc/dnsmasq.leases, "r")
for line in leases:
    match = re.search(r"172\.16\.1\.\d{10, 20}", line)
    if match:
        print match
        urls.append(match)

urls.append("http://172.16.1.23")
localFile = "info.csv"
numSuccess = 0
numFail = 0
while(True):
    for url in urls:
        try:
            data = fetchData(url)
            csv_append(localFile, data)
            numSuccess += 1
            print("%s -- %d successes and %d failures" %(data, numSuccess, numFail))
        except socket.timeout as e:
            numFail += 1
            print("Failed to connect to %s -- %d success and %d failures" % (url, numSuccess, numFail))
	except urllib2.URLError as e:
	    numFail += 1
            print("Failed to connect to %s -- %d success and %d failures" % (url, numSuccess, numFail))
    time.sleep(1)


