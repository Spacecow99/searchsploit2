Searchsploit 2
==============

Sort of like a command-line Google for your exploits. You do publish your PoCs right?

##Description

An alternative to the original searchsploit script that provides a finer level of control as well as verbose output for help find
where your searches are going wrong. Usefull if you're like me and wondering how you got a Plan9 local privellege escalation PoC when 
searching for a remote exploit for Windows... 

Usage
=====

`python searchsploit.py [-v] [-dopt VALUE] [term ...]`

* `--verbose/-v` Verbose output telling you if and where your query failed.
* `--date/-d YYYY-MM-DD` Search for exploits published on or before YYYY-MM-DD.
* `--platform/-o PLATFORM` Search exploits by platform/OS.
* `--port/-p PORT` Search exploits by affected port number (0 for local/irrelevant).
* `--type/-t TYPE` Search exploits by type e.g remote, local, dos, etc.
* `TERM` String to search for in exploit description.

##Examples

```python searchsploit.py --platform windows --type remote MS08-067
python searchsploit.py -v -o plan9 -t remote
python searchsploit.py --date 2014-01-01 -p 80
python searchsploit.py```

Issues
======

Currently the functionality to download a copy of the latest files.csv (the ExploitDB) is not complete therefor it requires that
the user either download it himself or already have a copy of the original searchsploit tool installed. This tool does not provide
the actual PoC files, simply a way to search for those in the current copy of files.csv available to it at the time.

TODO
====

* Add `--update/-u` argument to download the current copy of files.csv from Offensive Security.
* Add `--yes/-y` argument to skip prompt when invoking searchsploit2 with no search parameters.
* Update `--date/-d` option in order to validate that YYYY-MM-DD parameter is in the proper format.
* Replace current docstrings with proper sphynx style documentation because standards.
* Add more llamas, not enough llama's in InfoSec... What's wrong with you people? 
