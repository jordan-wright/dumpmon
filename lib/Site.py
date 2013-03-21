from Queue import Queue
import requests
from requests import ConnectionError

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