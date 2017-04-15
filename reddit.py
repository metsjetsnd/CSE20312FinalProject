#!/usr/bin/env python2.7

'''
For whatever reason the shebang wasn't working, 
the script works when you use it as an argument to the python command though
'''
import atexit
import os
import re
import shutil
import sys
import tempfile

import requests

# Global variables

FIELD     = 'title'
NUMBER       = 10
SUBREDDIT    = 'linux'
REGEX = [False, '']

# Functions

def usage(status=0):
    print '''Usage: {} [ -f FIELD -s SUBREDDIT ] regex
    -f FIELD        Which field to search (default: title)
    -n LIMIT        Limit number of articles to report (default: 10)
    -s STEPSIZE     Which subreddit (default: linux)'''.format(
        os.path.basename(sys.argv[0])
    )
    sys.exit(status)

# Parse command line options

args = sys.argv[1:]

while len(args) and args[0].startswith('-') and len(args[0]) > 1:
    arg = args.pop(0)
    if arg == '-f':
	   FIELD = '"' + args.pop(0) + '"'
    elif arg == '-n':
	   NUMBER = int(args.pop(0))
    elif arg == '-s':
	   SUBREDDIT = args.pop(0)
    elif arg == '-h':
	   usage(0)
    else:
       usage(1)

if len(args) > 0:
    REGEX[0] = True
    REGEX[1] = args[0]

# Main execution

link = 'https://www.reddit.com/r/' + SUBREDDIT + '/.json'

headers  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
r = requests.get(link, headers=headers)

data = r.json()["data"]
children = data["children"]

printed = 1
for count, child in enumerate(children):

    details = child["data"]
    if FIELD in details:
        z = details[FIELD]
    else:
        print "Invalid Field"
        sys.exit(1)
    l = 'http://www.reddit.com' + details["permalink"]
    if REGEX[0] == True:
        search = re.findall(REGEX[1], z)
        if search:
            print '{:3d}'.format(printed) + '.' , '{:8}'.format('Title:'), z
            print '{:13}'.format('     Author:'), details["author"]
            print '{:13}'.format('     Link:'), 'http://www.reddit.com' + l
            t = requests.get('http://is.gd/create.php', params={'format':'json', 'url':l})
            print '{:13}'.format('     Short:'), t.json()['shorturl']
            printed = printed + 1
            if printed == NUMBER + 1:
                break
        else:
            continue
    else:
        print '{:3d}'.format(count + 1) + '.' , '{:8}'.format('Title:'), z
        print '{:13}'.format('     Author:'), details["author"]
        print '{:13}'.format('     Link:'), 'http://www.reddit.com' + l
        t = requests.get('http://is.gd/create.php', params={'format':'json', 'url':l})
        print '{:13}'.format('     Short:'), t.json()['shorturl']
        if count == NUMBER - 1:
            break







