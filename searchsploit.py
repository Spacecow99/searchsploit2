#!/usr/bin/env python

################################################################################
#The MIT License (MIT)
#
#Copyright (c) 2014 Jacques Pharand
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
################################################################################

__author__  = "Spacecow"
__date__    = "1/13/14"
__version__ = "0.2"

import os
import sys
import argparse
import string
import csv
import re


CSV_FILE       = "%s/files.csv" % os.getcwd()  # Change this variable to a absolute path if desired.
DESCRIPTION    = """Search the ExploitDB more precisely without changing any existing file structure or resources."""
BANNER         = " Description%sPath\n%s %s\n" % ((" " * 70), ("-" * 80), ("-" * 25))


def formatString(description, location):
    """Format each entry for pretty."""
    if len(description) < 80:
        while len(description) != 80:
            description += " "
    return "%s %s\n" % (description, location[9:])

# Rename this function
def parseListForRegex(list, regex):
    """Search the description field for a keyword regex match."""
    _temp = []
    for item in list:
        match = re.search(regex.lower(), item[2].lower())
        if match == None: pass
        else:
            _temp.append(item)
            #print("We have a match %s -> %s" % (regex, item[2]))
    return _temp

# Rename this function
def parseListItems(list, value, position):
    """Function used to whittle down the entries to search."""
    _temp = []
    for item in list:
        if item[position] == value:
            _temp.append(item)
    return _temp


def main():
    parser = argparse.ArgumentParser(prog="searchsploit2", description=DESCRIPTION)
    parser.add_argument("TERM", nargs="*", action="store", help="Terms to search for in exploit description")
    parser.add_argument("--platform","-p", metavar="PLATFORM", action="store",help="Platform/OS to search")
    parser.add_argument("--type", "-t", metavar="TYPE", action="store", help="Type of exploit to search")
    args = parser.parse_args()

    if os.path.isfile(CSV_FILE) is False:
        print >> sys.stderr, "[!] ExploitDB csv %s could not be found." % CSV_FILE
        sys.exit(1)
		
    masterList = []
    with open(CSV_FILE, "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            masterList.append(row)

    if args.platform:
        masterList = parseListItems(masterList, args.platform, 5)

    if args.type:
        masterList = parseListItems(masterList, args.type, -2)

    for term in args.TERM:
        try:
            masterList = parseListForRegex(masterList, term)
        except:
            print('[!] Caught an unknown exception during regex search.')
            sys.exit(2)

    output = BANNER
    for line in masterList:
        output += formatString(line[2], line[1])
    print string.rstrip(output)


if __name__ == "__main__":
    try:
        main()
    except(KeyboardInterrupt):
        print()
