#!/usr/bin/env python2.7

import requests
import calendar

function = 'TIME_SERIES_DAILY'
symbol = 'AAPL'
apikey = 'ZK41'
link = 'http://www.alphavantage.co/query?function=' + function + '&symbol=' + symbol + '&apikey=' + apikey

#headers  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
r = requests.get(link)

print r.json()


"""data = r.json()["data"]
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
            break"""