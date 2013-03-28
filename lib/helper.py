'''
helper.py - provides misc. helper functions
Author: Jordan

'''

import requests
import settings
from time import sleep, strftime


r = requests.Session()

def download(url, headers=None):
	if not headers: headers = None
	if headers:
		r.headers.update(headers)
	try:
		response = r.get(url).text
	except requests.ConnectionError:
		print '[!] Critical Error - Cannot connect to Pastebin'
		sleep(5)
		print '[!] Retrying...'
		response = self.download(url)
	return response

def record(text):
	'''
	record(text) : Records text to the tweet_history file

	'''
	with open(settings.tweet_history, 'a') as history:
		history.write(strftime('[%b %d, %Y %I:%M:%S]') + text + '\n')

def log(text):
	'''
	log(text): Logs message to both STDOUT and to .output_log file

	'''
	print text
	with open(settings.log_file, 'a') as logfile:
		logfile.write(text + '\n')

def build_tweet(paste):
	'''
	build_tweet(url, paste) - Determines if the paste is interesting and, if so, builds and returns the tweet accordingly

	'''
	tweet = None
	if paste.match():
		tweet = paste.url
		if paste.type == 'db_dump':
			if paste.num_emails > 0:
				tweet += ' Emails: ' + str(paste.num_emails)
			if paste.num_hashes > 0: tweet += ' Hashes: ' + str(paste.num_hashes)
			if paste.num_hashes > 0 and paste.num_emails > 0: tweet += ' E/H: ' + str(round(paste.num_emails / float(paste.num_hashes), 2))
			tweet += ' Keywords: ' + str(paste.db_keywords)
			tweet += ' #infoleak'
		elif paste.type == 'google_api':
			tweet += ' Found possible Google API key(s)'
		elif paste.type in ['Cisco', 'Juniper']:
			tweet += ' Possible ' + paste.type + ' configuration'
		elif paste.type == 'ssh_private':
			tweet += ' Possible SSH private key'
		elif paste.type == 'honeypot':
			tweet += ' Dionaea Honeypot Log'
	if paste.num_emails > 0:
		print paste.emails
	return tweet