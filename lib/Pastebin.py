from Site import Site
from Paste import Paste
from bs4 import BeautifulSoup
import helper
from time import sleep
from settings import SLEEP_PASTEBIN
from twitter import TwitterError

class PastebinPaste(Paste):
	def __init__(self, id):
		self.id = id
		self.headers = None
		self.url = 'http://pastebin.com/raw.php?i=' + self.id
		super(PastebinPaste, self).__init__()

class Pastebin(Site):
	def __init__(self, last_id=None):
		if not last_id: last_id = None
		self.ref_id = last_id
		self.BASE_URL = 'http://pastebin.com'
		super(Pastebin, self).__init__()
	def update(self):
		'''update(self) - Fill Queue with new Pastebin IDs'''
		print '[*] Retrieving Pastebin ID\'s'
		results = BeautifulSoup(helper.download(self.BASE_URL + '/archive')).find_all(lambda tag: tag.name=='td' and tag.a and '/archive/' not in tag.a['href'] and tag.a['href'][1:])	
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
	def monitor(self, bot, l_lock, t_lock):
		self.update()
		while(1):
			while not self.empty():
				paste = self.get()
				self.ref_id = paste.id
				with l_lock:
					helper.log('[*] Checking ' + paste.url)
				paste.text = helper.download(paste.url)
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
				sleep(SLEEP_PASTEBIN)
				self.update()