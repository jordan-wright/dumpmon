# dumpmon.py 
# Author: Jordan Wright
# Version: 0.0 (in dev)

# ---------------------------------------------------
# To Do:
#
#	- Create More/Better regular 
#	- Create/Keep track of statistics

from Queue import Queue
import requests
from lib.regexes import regexes
import time
from bs4 import BeautifulSoup

class Site(object):
	# I would have used the built-in queue, but there is no support for a peek() method
	# that I could find... So, I decided to implement my own queue with a few changes
	def __init__(self, queue=None):
		if queue is None: self.queue = []
	def empty(self):
		return len(self.queue) == 0
	def get(self):
		if not self.empty():
			result = self.queue[0]
			del self.queue[0]
		else:
			result = None
		return result
	def put(self, item):
		self.queue.append(item)
	def peek(self):
		return self.queue[0] if not self.empty() else None
	def tail(self):
		return self.queue[-1] if not self.empty() else None
	def length(self):
		return len(self.queue)
	def clear(self):
		self.queue = []
	def list(self):
		print '\n'.join(url for url in self.queue)
	# Also wanted to make some helper functions for downloads
	def download(self, url):
		try:
			response = requests.get(url).text
		except requests.ConnectionError:
			print '[!] Critical Error - Cannot connect to Pastebin'
			time.sleep(5)
			print '[!] Retrying...'
			response = self.download(url)
		return response

class PastebinPaste:
	def __init__(self, id):
		self.id = id
		self.url = 'http://pastebin.com/raw.php?i=' + self.id

class Pastebin(Site):
	def __init__(self, last_id=None):
		if not last_id: last_id = None
		self.ref_id = last_id
		self.BASE_URL = 'http://pastebin.com'
		super(Pastebin, self).__init__()
	def update(self):
		'''update(self) - Fill Queue with new Pastebin IDs'''
		print '[*] Retrieving Pastebin ID\'s'
		results = BeautifulSoup(self.download('http://pastebin.com/archive')).find_all(lambda tag: tag.name=='td' and tag.a and '/archive/' not in tag.a['href'] and tag.a['href'][1:])	
		new_pastes = []
		if not self.ref_id: results = results[:60]
		for entry in results:
			paste = PastebinPaste(entry.a['href'][1:])
			# Check to see if we found our last checked URL
			if paste.id == self.ref_id:
				break
			new_pastes.append(paste)
		for entry in new_pastes[::-1]:
			print '[+] Adding URL: ' + entry.url
			self.put(entry)

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