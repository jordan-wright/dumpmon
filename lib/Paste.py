from .regexes import regexes
import settings
import logging


def log(text):
    '''
    log(text): Logs message to both STDOUT and to .output_log file

    '''
    if text:
        print(text.encode('utf-8'))
        with open(settings.log_file, 'a') as logfile:
            logfile.write(text.encode('utf-8') + '\n')


class Paste(object):
    def __init__(self):
        '''
        class Paste: Generic "Paste" object to contain attributes of a standard paste

        '''
        self.emails = 0
        self.hashes = 0
        self.num_emails = 0
        self.num_hashes = 0
        self.text = None
        self.type = None
        self.db_keywords = 0.0

    def match(self):
        '''
        Matches the paste against a series of regular expressions to determine if the paste is 'interesting'

        Sets the following attributes:
                self.emails
                self.hashes
                self.num_emails
                self.num_hashes
                self.db_keywords
                self.type

        '''
        # Get the amount of emails
        self.emails = list(set(regexes['email'].findall(self.text)))
        self.hashes = regexes['hash32'].findall(self.text)
        self.num_emails = len(self.emails)
        self.num_hashes = len(self.hashes)
        for regex in regexes['db_keywords']:
            if regex.search(self.text):
                logging.debug('\t[+] ' + regex.search(self.text).group(1))
                self.db_keywords += round(1/float(
                    len(regexes['db_keywords'])), 2)
        for regex in regexes['blacklist']:
            if regex.search(self.text):
                logging.debug('\t[-] ' + regex.search(self.text).group(1))
                self.db_keywords -= round(1.25 * (
                    1/float(len(regexes['db_keywords']))), 2)
        if (self.num_emails >= settings.EMAIL_THRESHOLD) or (self.num_hashes >= settings.HASH_THRESHOLD) or (self.db_keywords >= settings.DB_KEYWORDS_THRESHOLD):
            self.type = 'db_dump'
        if regexes['cisco_hash'].search(self.text) or regexes['cisco_pass'].search(self.text):
            self.type = 'Cisco'
        if regexes['honeypot'].search(self.text):
            self.type = 'honeypot'
        if regexes['google_api'].search(self.text):
            self.type = 'google_api'
        # if regexes['juniper'].search(self.text): self.type = 'Juniper'
        return self.type
