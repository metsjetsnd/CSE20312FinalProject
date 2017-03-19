#!/usr/bin/env python2.7

import os
import sys
import requests
for url in sys.argv[1:]:
  	r = requests.get(url)
  	n = os.path.basename(url)
	with open(n, 'wb') as fs:
		fs.write(r.content)
