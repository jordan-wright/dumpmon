# dumpmon.py 
# Author: Jordan Wright
# Version: 0.0 (in dev)

# ---------------------------------------------------
# To Do:
#
#	- Create More/Better regular regex
#	- Create/Keep track of statistics

import requests
from lib.regexes import regexes
from lib.Pastebin import Pastebin, PastebinPaste
import time
import python-twitter

CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'

def monitor():
	print '[*] Monitoring...'
	print '[*] Ctrl+C to quit'
	pastie = Pastebin()
	pastie.update()
	try:
		while(1):
			while not pastie.empty():
				paste = pastie.get()
				pastie.ref_id = paste.id
				print 'Checking ' + paste.url
				result = requests.get(paste.url).text
				for key, regex in regexes.iteritems():
					if key == 'db_leak': continue
					# Get the matches - remove the duplicates
					matches = list(set(regex.findall(result)))
					if len(matches) != 0: print '\t' + key + ' ' + '\n'.join('\t[*]' + finding for finding in matches)
			pastie.update()
			# If no new results... sleep for 5 sec
			while pastie.empty():
				print 'No results... sleeping'
				time.sleep(10)
				pastie.update()
	except KeyboardInterrupt:
		print 'Stopped.'


if __name__ == "__main__":
	monitor()