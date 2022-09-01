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


def parseCSV(csvName):
    print(csvName)
    csvFile = open(csvName)
    festivalTab = csv.reader(csvFile)
    print(festivalTab)
    for row in festivalTab:
        print(row)
    close(csvFile)


def main(args):
    argtab = parseCommandLine(args)
    print(argtab)
    print("Processing CSV file %s\n" % argtab.fname[0]);
    parseCSV(argtab.fname[0])
    return 0

if __name__ == "__main__":
    result = main(sys.argv)
    sys.exit(result)
