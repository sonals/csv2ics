#!/usr/bin/env python3
#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2022-2023 sonal.santan@gmail.com
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

SKIPSET = ["Major Cities", "Countries", "Timezones/ Countries", "Major Cities in the Timezone"]

DATEFORMAT = ["%b %d, %y", "%m/%d/%y"]

def parseCommandLine(args):
    msg = "Convert a calendar in CSV to multiple ICS, one for each timezone"
    parser = argparse.ArgumentParser(description = msg, exit_on_error = False)
    parser.add_argument(dest ='fname', metavar ='csv', nargs = 1)
    # strip out the argv[0]
    return parser.parse_args(args[1:])

def openAllICS(row):
    timezones = []
    for tz in row:
        pair = tuple((tz.strip(), ics.Calendar()))
        timezones.append(pair)
        print(f"Constructing calendar for {pair[0]}")
    return timezones

def parseDateTime(string):
    value = None
    for formatstr in DATEFORMAT:
        try:
            value = datetime.datetime.strptime(string, formatstr)
        except ValueError as e:
            continue
        break
    return value

def createEvents(timezones, row):
    if (len(row) != len(timezones) + 1):
        # Malformed record for this event
        return
    for i in range(0, len(timezones)):
        evt = ics.Event(name = row[0].strip())
        evt.begin = parseDateTime(row[i + 1].strip())
        if (evt.begin is None):
            print(f"Unable to parse data time \"{row[i + 1].strip()}\" for event \"{evt.name}\"")
            continue
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
        key = row[0].strip()
        if (key in SKIPSET):
            print(f"Skipped row with key \"{key}\"")
            continue
        if (key == "Timezones"):
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
        print(a)
        return 1
    except Exception as e:
        print(e)
        return 1

if __name__ == "__main__":
    RESULT = main(sys.argv)
    sys.exit(RESULT)
