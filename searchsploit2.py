#!/usr/bin/env python3
##################################
#        Searchsploit2.py        #
#  Exploit-Database Search Tool  #
#       Coded By Spacecow        #
#     Blacksun Hackers Club      #
##################################

import os
import re
import sys
import csv
import argparse
import urllib.request
import urllib.error


class Colour(object):
    """
    That's colour with a 'u', you Yankee bastards!
    """
    RED = '\033[91m'
    GREEN = '\033[92m'
    ENDC = '\033[0m'


class ExploitCSV(object):
    """
    Exploit-Database CSV file object

    Attributes:
        csv_file: The path to the local exploit-db CSV file.
        parsed_results: List of results matching the search criterias.
    """

    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise IOError("File {0} could not be found".format(filename))
        self.csv_file = filename
        self.parsed_results = None

    def search(self, term, field, verbose):
        """
        Parse field found search term and store results in self.parsed_results

        Args:
            term: Match term to use during search.
            field: CSV field to perform search on.
            verbose: Print status of completed search.

        Raises:
            IOError: Error when reading CSV file.
        """
        results = list()
        if self.parsed_results is None:  # Must be the first pass
            with open(self.csv_file, 'r') as _csv:
                try:
                    reader = csv.DictReader(_csv)
                except csv.Error as e:
                    raise IOError(str(e))

                for row in reader:
                    if re.search(term, row[field], re.IGNORECASE):
                        results.append(row)
        else:
            for row in self.parsed_results:
                if re.search(term, row[field], re.IGNORECASE):
                    results.append(row)

        if verbose:
            if len(results) == 0:
                print(("[  {0}FAIL{1}  ] 0 results "
                       "found for term '{2}'".format(Colour.RED,
                                                   Colour.ENDC,
                                                   term)))
            else:
                print(("[   {0}OK{1}   ] {2} results "
                       "found for term '{3}'".format(Colour.GREEN,
                                                   Colour.ENDC,
                                                   len(results),
                                                   term)))
        self.parsed_results = results

    def pprint(self):
        """
        Pretty print the search results with familiar searchsploit banner
        """
        banner = " Description{0}Path\n{1} {2}".format((" " * 70),
                                                       ("-" * 80),
                                                       ("-" * 25))
        print(banner)
        if self.parsed_results is None:
            print()
        else:
            for result in self.parsed_results:
                print(result['description'],
                      " " * (79 - len(result['description'])),
                      result['file'][9:])

    @staticmethod
    def update(path):
        """
        Update exploit-db CSV file from the offensive-security
        git repo and exit.

        Args:
            path: Path to CSV file to write to.
        """
        repo = (r"http://raw.githubusercontent.com"
                r"/offensive-security/exploit-database/master/files.csv")
        if os.path.isfile(path):
            os.replace(path, "{0}.old".format(path))  # Move path to path.old
        try:
            status = 0
            urllib.request.urlretrieve(repo, filename=path)
            print(("[   {0}OK{1}   ] Updated local "
                   "exploit-db CSV succesfully".format(Colour.GREEN,
                                                       Colour.ENDC)))
        except urllib.error.URLError as e:
            sys.stderr.write("{0}: URLError: {1}\n".format(sys.argv[0], e))
            status = 10
        except IOError as e:
            sys.stderr.write("{0}: IOError: {1}\n".format(sys.argv[0], e))
            status = 11
        sys.exit(status)

def main():
    parser = argparse.ArgumentParser(prog='searchsploit2')
    parser.add_argument('--file', '-f', metavar='PATH', action='store',
                        default=("{0}/.searchsploit/"
                                 "exploitdb.csv".format(os.getenv('HOME'))),
                        help='Path to exploit-db CSV file')
    parser.add_argument('--author', '-a', metavar='AUTHOR', action='store',
                        help='Search for exploit author\'s name')
    parser.add_argument('--date', '-y', metavar='YYYY-MM-DD', action='store',
                        help=('Search for exploits published on '
                              'YYYY-MM-DD'))
    parser.add_argument('--platform', '-o', metavar='PLATFORM',
                        action='store',
                        help='Search for exploit affecting OS platform')
    parser.add_argument('--type', '-t', metavar='TYPE', action='store',
                        help='Search for exploit type')
    parser.add_argument('--port', '-p', metavar='PORT', action='store',
                        help='Search for exploit affecting port')
    parser.add_argument('--description', '-d', metavar='TERM',
                        action='store',
                        help='Search exploit description for term')
    parser.add_argument('--update', '-u', action='store_true',
                        help='Update local copy of exploit-db')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--version', action='version',
                        version="Searchsploit2 0.8")
    args = parser.parse_args()

    if not os.path.isdir("{0}/.searchsploit/".format(os.getenv('HOME'))):
        try:
            os.mkdir("{0}/.searchsploit/".format(os.getenv('HOME')))
        except os.OSError as e:
            if args.verbose:
                sys.stderr.write('{0}: OSError: {1}\n'.format(sys.argv[0], e))

    if args.update:  # Perform updates and exit
        ExploitCSV.update(args.file)

    try:
        exploitdb = ExploitCSV(args.file)
    except IOError:
        sys.stderr.write(("{0}: File error: File '{1}' "
                          "not found\n".format(sys.argv[0], args.file)))
        sys.exit(1)

    if args.author:
        exploitdb.search(args.author, 'author', args.verbose)

    if args.date:
        if re.match(r'[\d|\D]{4}-[\d|\D]{2}-[\d|\D]{2}', args.date) is None:
            sys.stderr.write(("{0}: DateError: Improper "
                              "date format '{1}'\n".format(sys.argv[0],
                                                           args.date)))
            sys.exit(2)
        try:
            exploitdb.search(args.date, 'date', args.verbose)
        except IOError as e:
            sys.stderr.write("{0}: IOError: {1}".format(sys.argv[0], e))
            sys.exit(3)

    if args.platform:
        try:
            exploitdb.search(args.platform, 'platform', args.verbose)
        except IOError as e:
            sys.stderr.write("{0}: IOError: {1}".format(sys.argv[0], e))
            sys.exit(3)

    if args.type:
        try:
            exploitdb.search(args.type, 'type', args.verbose)
        except IOError as e:
            sys.stderr.write("{0}: IOError: {1}".format(sys.argv[0], e))
            sys.exit(3)

    if args.port:
        try:
            exploitdb.search(args.port, 'port', args.verbose)
        except IOError as e:
            sys.stderr.write("{0}: IOError: {1}".format(sys.argv[0], e))
            sys.exit(3)

    if args.description:
        try:
            exploitdb.search(args.description, 'description', args.verbose)
        except IOError as e:
            sys.stderr.write("{0}: IOError: {1}".format(sys.argv[0], e))
            sys.exit(3)

    exploitdb.pprint()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
