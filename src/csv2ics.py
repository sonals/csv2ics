import argparse
import sys
import csv
import os

def parseCommandLine(args):
    parser = argparse.ArgumentParser(description ='Convert from CVS to ICS')

    parser.add_argument(dest ='fname', metavar ='csv', nargs =1)
    parser.add_argument('-c', '--column', metavar ='column',
                        required = True, dest ='col',
                        action ='store', help ='date column')
    parser.add_argument('-o', '--output', metavar='ics', dest ='outfile',
                        required = True, action ='store', help ='output ICS file')
    # strip out the argv[0]
    return parser.parse_args(args[1:])

def openICS(zone):
    fd = open(zone + ".ics", "w")
    fd.write("BEGIN:VCALENDAR\n")
    fd.write("PRODID:-//Dharmic//Calendar //EN\n")
    fd.write("VERSION:2.0\n")
    fd.write("CALSCALE:GREGORIAN\n")
    fd.write("METHOD:PUBLISH\n")
    fd.write("X-WR-CALNAME: 2022 Hindu Calendar For %s\n" % zone)
    fd.write("X-WR-CALDESC: 2022 Hindu Calendar For %s\n" % zone)
    return fd

def openAllICS(row):
    timezones = []
    for tz in row:
        timezones.append(openICS(tz))
    return timezones

def closeAllICS(timezones):
    for fd in timezones:
        fd.write("END:VCALENDAR\n")
        fd.close()

def printAllICS(festivalTab):
    timezones = []
    for row in festivalTab:
        print(row)
        if (row[0] == "Timezones"):
            timezones = openAllICS(row[1:])
    closeAllICS(timezones)


def parseCSV(csvName):
    print(csvName)
    csvFile = open(csvName)
    festivalTab = csv.reader(csvFile)
    print(festivalTab)
#    for row in festivalTab:
#        print(row)
    printAllICS(festivalTab)
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
