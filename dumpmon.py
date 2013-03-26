# dumpmon.py 
# Author: Jordan Wright
# Version: 0.0 (in dev)

# ---------------------------------------------------
# To Do:
#
#	- Refine Regex
#	- Create/Keep track of statistics

from lib.regexes import regexes
from lib.Pastebin import Pastebin, PastebinPaste
from lib.Slexy import Slexy, SlexyPaste
from lib.helper import log
from time import sleep
import twitter
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import threading

def monitor():
	'''
	monitor() - Main function... creates and starts threads

	'''
	log('[*] Monitoring...')
	log('[*] Ctrl+C to quit')
	bot = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_TOKEN_SECRET)
	pastie = Pastebin()
	slexy = Slexy()
	# Create lock for both output log and tweet action
	log_lock = threading.Lock()
	tweet_lock = threading.Lock()
	pastebin_thread = threading.Thread(target=pastie.monitor, args=[bot,log_lock, tweet_lock])
	pastebin_thread.daemon = True
	pastebin_thread.start()
	slexy_thread = threading.Thread(target=slexy.monitor, args=[bot,log_lock, tweet_lock])
	slexy_thread.daemon = True
	slexy_thread.start()
	try:
		while(1):
			sleep(5)
	except KeyboardInterrupt:
		log('Stopped.')


if __name__ == "__main__":
	monitor()