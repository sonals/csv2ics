#!/usr/bin/env python3
#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2022 sonal.santan@gmail.com
#

"""
This is a python script to convert a calendar in CSV format to ICS format which
can be imported by a standard calendar application. For a compatible CSV schema
see https://mypanchang.com/2022americacanadawestindiesfestivals.php

"""

import argparse
import sys
import csv
import datetime
import ics

SKIPSET = ["Major Cities", "Countries"]

def parseCommandLine(args):
    msg = "Convert a calendar in CSV to multiple ICS, one for each timezone"
    parser = argparse.ArgumentParser(description = msg, exit_on_error = False)
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
        # Malformed record for this event
        return
    for i in range(0, len(timezones)):
        evt = ics.Event(name = row[0])
        evt.begin = datetime.datetime.strptime(row[i + 1], "%b %d, %y")
        evt.make_all_day()
        (timezones[i])[1].events.add(evt)
    print(f"Processed event \"{row[0]}\"")

def writeAllICS(timezones):
    for pair in timezones:
        with open(pair[0] + ".ics", mode="wt", encoding="utf8") as fd:
            fd.write(pair[1].serialize())

def extractAllICS(festivalTab):
    timezones = []
    for row in festivalTab:
        if (row[0] in SKIPSET):
            print(f"Skipped row with key \"{row[0]}\"")
            continue
        if (row[0] == "Timezones"):
            timezones = openAllICS(row[1:])
            continue
        createEvents(timezones, row)
    writeAllICS(timezones)

def parseCSV(csvName):
    with open(csvName, mode="r", encoding="utf8") as csvFile:
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
        return o.errno
    except AssertionError as a:
        print(f"AssertionError {a}")
        return 1
    except Exception as e:
        print(e)
        return 1

if __name__ == "__main__":
    RESULT = main(sys.argv)
    sys.exit(RESULT)
