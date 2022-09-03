#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

# Copyright (C) 2022 sonal.santan@gmail.com

import argparse
import sys
import csv
import datetime
import ics


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
        print(f"Constructing calendar for {pair[0]}")
    return timezones

def createEvents(timezones, row):
    if (len(row) != len(timezones) + 1):
        return
    for i in range(0, len(timezones)):
        evt = ics.Event(name = row[0])
        evt.begin = datetime.datetime.strptime(row[i + 1], "%b %d, %y")
        evt.make_all_day()
        (timezones[i])[1].events.add(evt)
    print(f"Processed event {row[0]}")

def writeAllICS(timezones):
    for pair in timezones:
        with open(pair[0] + ".ics", "wt") as fd:
            fd.write(pair[1].serialize())

def extractAllICS(festivalTab):
    timezones = []
    begin = False
    for row in festivalTab:
        if (row[0] == "Timezones"):
            timezones = openAllICS(row[1:])
            begin = True
            continue
        if (row[0] == "Major Cities"):
            continue
        if (begin):
            createEvents(timezones, row)
    writeAllICS(timezones)

def parseCSV(csvName):
    with open(csvName, "r") as csvFile:
        festivalTab = csv.reader(csvFile)
        extractAllICS(festivalTab)

def main(args):
    try:
        argtab = parseCommandLine(args)
        print(f"Processing CSV file {argtab.fname[0]}")
        parseCSV(argtab.fname[0])
        return 0
    except OSError as o:
        print(o)
        return -o.errno

    except AssertionError as a:
        print(a)
        return -1
    except Exception as e:
        print(e)
        return -1

if __name__ == "__main__":
    RESULT = main(sys.argv)
    sys.exit(RESULT)
