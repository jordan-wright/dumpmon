![Dumpmon Logo](assets/logo-small.png?raw=true)
# dumpmon
## Twitter-bot which monitors paste sites for interesting content

For more overview, check out the blog post [here.](http://raidersec.blogspot.com/2013/03/introducing-dumpmon-twitter-bot-that.html)

## Dependencies
	[python-twitter](https://code.google.com/p/python-twitter/)
    $ pip install python-twitter
	$ pip install beautifulsoup4
	$ pip install requests
	$ pip install pymongo <-- for MongoDB support (must have mongod running!)

Next, edit the settings.py to include your Twitter application settings.

## Setting up MongoDB support
dumpmon has the ability to cache pastes using MongoDB. Simply setup an instance of mongod,
and set the following values in settings to the appropriate values:
	USE_DB = True
	DB_HOST = 'localhost'
	DB_PORT = 27017

If you do not want DB support, set USE_DB to False.

## Executing dumpmon

	python dumpmon.py