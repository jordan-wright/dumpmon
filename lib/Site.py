try:
    from queue import Queue # python3
except ImportError:
    from Queue import Queue # python2
import requests
import time
from requests import ConnectionError
import logging
import redis
import json


class Site(object):
    '''
    Site - parent class used for a generic
    'Queue' structure with a few helper methods
    and features. Implements the following methods:

            empty() - Is the Queue empty
            get(): Get the next item in the queue
            put(item): Puts an item in the queue
            tail(): Shows the last item in the queue
            peek(): Shows the next item in the queue
            length(): Returns the length of the queue
            clear(): Clears the queue
            list(): Lists the contents of the Queue
            download(url): Returns the content from the URL

    '''
    # I would have used the built-in queue, but there is no support for a peek() method
    # that I could find... So, I decided to implement my own queue with a few
    # changes
    redisc = redis.StrictRedis(host='localhost', port=6379, db=0)

    def __init__(self, queue=None):
        if queue is None:
            self.queue = []

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
        print('\n'.join(url for url in self.queue))

    def monitor(self):
        self.update()
        while(1):
            while not self.empty():
                paste = self.get()
                self.ref_id = paste.id
                logging.debug('Checking ' + paste.url)
                paste.text = self.get_paste_text(paste)
                if paste.match():
                    logging.info('Found interesting stuff')
                    self.redisc.set(paste.url, paste.text)
            self.update()
            while self.empty():
                logging.debug('No results... sleeping')
                time.sleep(self.sleep)
                self.update()

