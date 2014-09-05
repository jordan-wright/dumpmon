![Dumpmon Logo](assets/logo-small.png?raw=true)
# dumpmon
## Twitter-bot ([@dumpmon](http://twitter.com/dumpmon)) which monitors paste sites for interesting content

For more overview, check out the blog post [here.](http://raidersec.blogspot.com/2013/03/introducing-dumpmon-twitter-bot-that.html)

## Dependencies
	twitter library - https://pypi.python.org/pypi/twitter
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

## License
The MIT License (MIT)

Copyright (c) 2014 Jordan Wright

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
