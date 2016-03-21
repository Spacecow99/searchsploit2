Searchsploit2
==============

A command-line script to provide fine grain search queries to specific fields in the exploit-database. 

##Description

An alternative to the original searchsploit script that provides a finer level of control as well as verbose output for help find
where your searches are going wrong. The search logic searches by `author => date => platform => type => port => description`. Searchsploit2 also supports updating your local exploit-database CSV copy and mimicks the output format of the original searchsploit script.

Usage
=====

	searchsploit2 [-h] [--file PATH] [--author AUTHOR] [--date YYYY-MM-DD]
	[--platform PLATFORM] [--type TYPE] [--port PORT] [--description TERM]
	[--update] [--verbose] [--version]

* `--file/-f PATH` Path to exploit-db CSV file.
* `--author/-a AUTHOR` Search for exploit author's name.
* `--date/-d YYYY-MM-DD` Search for exploits published on YYYY-MM-DD.
* `--platform/-o PLATFORM` Search exploits by platform / OS.
* `--type/-t TYPE` Search by exploit type.
* `--port/-p PORT` Search exploits by affected port number.
* `--description/-d TERM` Search exploit description for term.
* `--update/-u` Update local copy of exploit-db and exit.
* `--verbose/-v` Enable verbose output to track troublesome queries.
* `--version` Show program's version number and exit.

##Examples

    python3 searchsploit2.py --platform windows --type remote --description MS08-067
    python3 searchsploit2.py -v -o plan9 -t remote
    python3 searchsploit2.py --date 2014-01-01 -p 80
    python3 searchsploit2.py --author TurboBorland --file ~/.searchsploit2/files.csv

Issues
======

Currently the search functionality does not accept regular expressions such as " * ", this feature may be implemented in the future. Please report any additional issues found to `https://github.com/Spacecow99/searchsploit/issues`.


