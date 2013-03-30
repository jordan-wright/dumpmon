Forked from: https://github.com/jordan-wright/dumpmon - original
version is a twitter-bot, this version save everything in a redis
database.

# dumpmon
Monitors paste sites (pastebin, slexy, paste) for leaked content

# install
## requirements:

    $ pip install beautifulsoup4
    $ pip install requests
    $ pip install redis
    $ cp settings.py-example settings.py

edit settings.py file

    $ python dumpmon.py

