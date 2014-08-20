#!/usr/bin/env python
#
# Copyright (c) 2014, Jacques Pharand <phar0032@algonquinlive.com>
# This is Free Software. See LICENSE for license information.

# Replace with Sphynx style documentation
__author__  = "Jacques Pharand"
__date__    = "12/08/2014"
__version__ = "0.4"


import os
import sys
import argparse
import string
import csv
import re
import urllib2


CSV_FILE       = "%s/files.csv" % os.getcwd()  # Change this variable to a absolute path if desired.
DESCRIPTION    = """Search the ExploitDB more precisely without changing any existing file structure or resources."""
BANNER         = " Description%sPath\n%s %s\n" % ((" " * 70), ("-" * 80), ("-" * 25))


def update():

    repo = "https://raw.githubusercontent.com/offensive-security/exploit-database/master/files.csv"
    print("[ ok ] Attempting to update local files.csv")
    try:
        s = urllib2.urlopen(repo)
        f = open(CSV_FILE, 'w')
        f.write(s.read())
        f.close()
        print("[ ok ] ExploidDB updated successfully")
    except(IOError):
        sys.stderr.write("[ fail ] ExploitDB file could not be written")
    except(urllib2.URLError):
        sys.stderr.write("[ fail ] Could not contact ExploitDB git repo")
    finally:
        sys.exit()

def formatString(description, location):
    """Format each entry to match the original searchsploit formatting."""
    if len(description) < 80:
        while len(description) != 80:
            description += " "
    return "%s %s\n" % (description, location[9:])


def searchDescriptionField(list, regex):
    """Search the description field for a keyword regex match."""
    _temp = []
    for item in list:
        match = re.search(regex.lower(), item[2].lower())
        if match == None: pass
        else:
            _temp.append(item)
    return _temp


def searchCsvColumn(list, value, column):
    """Search for value in a desired column"""
    _temp = []
    for item in list:
        if item[column].lower() == value.lower():
            _temp.append(item)
    return _temp


def verboseStatus(length, verbose, action):
    if length == 0 and verbose:
        print("[ fail ] %s search found no results" % action)
    elif length > 0 and verbose:
        print("[ ok ] %s search succeded" % action)


def main():
    parser = argparse.ArgumentParser(prog="searchsploit2", description=DESCRIPTION)
    parser.add_argument("TERM", nargs="*", action="store", help="Terms to search for in exploit description")
    parser.add_argument("--date", "-d", metavar="YYYY-MM-DD", action="store", help="Exploits published on or after YYYY-MM-DD")
    parser.add_argument("--platform","-o", metavar="PLATFORM", action="store",help="Platform/OS to search")
    parser.add_argument("--port", "-p", metavar="PORT", action="store", help="Affected port number")
    parser.add_argument("--type", "-t", metavar="TYPE", action="store", help="Type of exploit to search")
    parser.add_argument("--update", "-u", action='store_true', help="Update your local ExploitDB copy")
    parser.add_argument("--verbose", "-v", action="store_true", help="Turn on verbose output")
    args = parser.parse_args()

    if os.path.isfile(CSV_FILE) is False:
        sys.stderr.write("%s: ExploitDB CSV file %s could not be found: Exiting now" % (sys.argv[0], CSV_FILE))
        sys.exit(1)

    if args.update:
        update()
		
    if not args.platform and not args.type and not args.date and not args.port and len(args.TERM) == 0:
        i = raw_input("Would you like to display all entries? [y/N] ")
        if i.lower() == 'y' or i.lower() == 'yes':
            pass
        else:
            sys.exit(0)

    masterList = []
    with open(CSV_FILE, "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            masterList.append(row)

    if args.date:
        skipFirstRow, _temp = True, []
        for row in masterList:
            if len(_temp) == 0 and skipFirstRow:
                skipFirstRow = False
                continue
            publishDate = str(row[-5]).split('-')
            searchDate = args.date.split('-')
            if int(publishDate[0]) >= int(searchDate[0]) and int(publishDate[1]) >= int(searchDate[1]) and int(publishDate[2]) >= int(searchDate[2]):
                _temp.append(row)
        masterList = _temp
        verboseStatus(len(masterList), args.verbose, "Publish date")

    if args.platform:
        masterList = searchCsvColumn(masterList, args.platform, 5)
        verboseStatus(len(masterList), args.verbose, "Platform search")

    if args.port:
        masterList = searchCsvColumn(masterList, args.port, -1)
        verboseStatus(len(masterList), args.verbose, "Port")

    if args.type:
        masterList = searchCsvColumn(masterList, args.type, -2)
        verboseStatus(len(masterList), args.verbose, "Exploit type")

    for term in args.TERM:
        try:
            masterList = searchDescriptionField(masterList, term)
        except:
            sys.stderr.write('%s: Caught an unknown exception during regex search: Exiting now' % sys.argv[0])
            sys.exit(2)

    output = BANNER
    for line in masterList:
        output += formatString(line[2], line[1])
    print(string.rstrip(output))


if __name__ == "__main__":
    try:
        main()
    except(KeyboardInterrupt):
        print()
