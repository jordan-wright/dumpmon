#!/bin/sh
find . -name "*.py" -or -name "settings.py-example" | xargs autopep8 -i


