from Site import Site
from bs4 import BeautifulSoup

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