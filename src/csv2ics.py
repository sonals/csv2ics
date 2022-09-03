#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

# Copyright (C) 2022 sonal.santan@gmail.com

import argparse
import sys
import csv
import os
import ics
import datetime

def parseCommandLine(args):
    parser = argparse.ArgumentParser(description ='Convert from CVS to ICS')
    parser.add_argument(dest ='fname', metavar ='csv', nargs = 1)
    # strip out the argv[0]
    return parser.parse_args(args[1:])

def openAllICS(row):
    timezones = []
    for tz in row:
        pair = tuple((tz, ics.Calendar()))
        timezones.append(pair)
        print("Constructing calendar for %s" % pair[0]);
    return timezones

def createEvents(timezones, row):
    if (len(row) != len(timezones) + 1):
        return
    for i in range(0, len(timezones)):
        e = ics.Event(name = row[0])
        e.begin = datetime.datetime.strptime(row[i + 1], "%b %d, %y")
        (timezones[i])[1].events.add(e)
    print("Processed event %s" % row[0])

def writeAllICS(timezones):
    for pair in timezones:
        fd = open(pair[0] + ".ics", "w")
        fd.write(pair[1].serialize())
        fd.close()

def extractAllICS(festivalTab):
    timezones = []
    begin = False
    for row in festivalTab:
        if (row[0] == "Timezones"):
            timezones = openAllICS(row[1:])
            begin = True
            continue
        if (row[0] == "Major Cities"):
            continue;
        if (begin):
            createEvents(timezones, row)
    writeAllICS(timezones)

def parseCSV(csvName):
    print(csvName)
    csvFile = open(csvName)
    festivalTab = csv.reader(csvFile)
    print(festivalTab)
    extractAllICS(festivalTab)
    csvFile.close()

def main(args):
    argtab = parseCommandLine(args)
    print(argtab)
    print("Processing CSV file %s" % argtab.fname[0]);
    parseCSV(argtab.fname[0])
    return 0

if __name__ == "__main__":
    result = main(sys.argv)
    sys.exit(result)
