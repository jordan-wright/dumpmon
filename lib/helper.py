'''
helper.py - provides misc. helper functions
Author: Jordan

'''

import requests


r = requests.Session()

def download(url, headers=None):
	if not headers: headers = None
	if headers:
		r.headers.update(headers)
	try:
		response = r.get(url).text
	except requests.ConnectionError:
		print '[!] Critical Error - Cannot connect to Pastebin'
		time.sleep(5)
		print '[!] Retrying...'
		response = self.download(url)
	return response