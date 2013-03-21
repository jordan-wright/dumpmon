from regexes import regexes
from .. import settings

class Paste(object):
	def __init__(self, ):
		self.emails = 0
		self.hashes = 0
		self.num_emails = 0
		self.num_hashes = 0
		self.text = None
		self.type = None
		self.db_keywords = 0.0

	def match(self):
		# Get the amount of emails
		self.emails = list(set(regexes['email'].findall(self.text)))
		self.hashes = list(set(regexes['hash32'].findall(self.text)))
		self.num_emails = len(self.emails)
		self.num_hashes = len(self.hashes)
		for regex in regexes['db_keywords']:
			if regex.search(self.text): self.db_keywords += 1/len(regexes['db_keywords']

		if num_emails >= settings.EMAILTHRESHOLD or self.db_keywords >= settings.DB_KEYWORDS_THRESHOLD:
			self.type = 'db_dump'

		if regexes['cisco_hash'].search(self.text) or regexes['cisco_pass']: self.type = 'cisco'
		if regexes['google_api'].search(self.text): self.type = 'google_api'

		#if regexes['juniper'].search(self.text): self.type = 'juniper'