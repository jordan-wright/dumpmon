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
import twitter
import settings

def record(text):
	'''
	record(text) : Records text to the tweet_history file

	'''
	with open(settings.tweet_history, 'a') as history:
		history.append(tweet + '\n')

def monitor():
	'''
	monitor() - Main function... monitors for new pastes, produces tweets, etc.
				Basically the bot's operation

	'''
	print '[*] Monitoring...'
	print '[*] Ctrl+C to quit'
	bot = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                      consumer_secret=settings.CONSUMER_SECRET,
                      access_token_key=settings.ACCESS_TOKEN,
                      access_token_secret=settings.ACCESS_TOKEN_SECRET)
	pastie = Pastebin()
	pastie.update()
	try:
		while(1):
			while not pastie.empty():
				paste = pastie.get()
				pastie.ref_id = paste.id
				print 'Checking ' + paste.url
				paste.text = requests.get(paste.url).text
				tweet = build_tweet(result)
				if tweet:
					record(tweet)
					bot.PostUpdate(paste.url, tweet)
			pastie.update()
			# If no new results... sleep for 5 sec
			while pastie.empty():
				print 'No results... sleeping'
				time.sleep(10)
				pastie.update()
	except KeyboardInterrupt:
		print 'Stopped.'

def build_tweet(url, paste):
	'''
	build_tweet(url, paste) - Determines if the paste is interesting and, if so, builds and returns the tweet accordingly

	'''
	tweet = None
	if paste.matches():
		tweet = url
		if tweet.type == 'db_dump'
			if paste.num_emails > 0: tweet += ' Emails: ' + str(paste.num_emails)
			if paste.num_hashes > 0: tweet += ' Hashes: ' + str(paste.num_hashes)
			if paste.num_hashes > 0 and paste.num_emails > 0: tweet += 'E/H: ' + str(round(paste.num_emails / float(paste.num_hashes)), 2)
			tweet += 'Keywords: ' + str(tweet.db_dump_percent)
		elif tweet.type in ['Cisco', 'Juniper']:
			tweet += ' Possible ' + tweet.type + ' configuration'
		elif tweet.type == 'ssh_private':
			tweet += ' Possible SSH private key'


if __name__ == "__main__":
	monitor()