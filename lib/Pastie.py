from Site import Site
from Paste import Paste
from bs4 import BeautifulSoup
import helper
from time import sleep
from settings import SLEEP_PASTIE
from twitter import TwitterError

class PastiePaste(Paste):
	def __init__(self, id):
		self.id = id
		self.headers = None
		self.url = 'http://pastie.org/pastes' + self.id + '/text'
		super(PastiePaste, self).__init__()

class Pastie(Site):
	def __init__(self, last_id=None):
		if not last_id: last_id = None
		self.ref_id = last_id
		self.BASE_URL = 'http://pastie.org'
		super(Pastie, self).__init__()
	def update(self):
		'''update(self) - Fill Queue with new Pastie IDs'''
		print '[*] Retrieving Pastie ID\'s'
		results = [tag for tag in BeautifulSoup(helper.download(self.BASE_URL + '/pastes')).find_all('p','link') if tag.a]	
		new_pastes = []
		if not self.ref_id: results = results[:60]
		for entry in results:
			paste = PastiePaste(entry.a['href'].replace(self.BASE_URL + '/pastes', ''))
			# Check to see if we found our last checked URL
			if paste.id == self.ref_id:
				break
			new_pastes.append(paste)
		for entry in new_pastes[::-1]:
			print '[+] Adding URL: ' + entry.url
			self.put(entry)
	def monitor(self, bot, l_lock, t_lock):
		self.update()
		while(1):
			while not self.empty():
				paste = self.get()
				self.ref_id = paste.id
				with l_lock:
					helper.log('[*] Checking ' + paste.url)
				# goober pastie - Not actually showing *raw* text.. Still need to parse it out
				paste.text = BeautifulSoup(helper.download(paste.url)).pre.text
				with l_lock:
					tweet = helper.build_tweet(paste)
				if tweet:
					print tweet
					with t_lock:
						helper.record(tweet)
						try:
							bot.PostUpdate(tweet)
						except TwitterError:
							pass
			self.update()
			# If no new results... sleep for 5 sec
			while self.empty():
				with l_lock:
					helper.log('[*] No results... sleeping')
				sleep(SLEEP_PASTIE)
				self.update()