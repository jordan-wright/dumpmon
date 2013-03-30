# dumpmon.py
# Author: Jordan Wright
# Version: 0.0 (in dev)

# ---------------------------------------------------
# To Do:
#
#	- Refine Regex
#	- Create/Keep track of statistics

from lib.regexes import regexes
from lib.Pastebin import Pastebin, PastebinPaste
from lib.Slexy import Slexy, SlexyPaste
from lib.Pastie import Pastie, PastiePaste
from lib.helper import log
from time import sleep
import threading
import logging


def monitor():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="more verbose", action="store_true")
    args = parser.parse_args()
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s', level=level)
    logging.info('Monitoring...')

    pastebin_thread = threading.Thread(target=Pastebin().monitor)
    slexy_thread = threading.Thread(target=Slexy().monitor)
    pastie_thead = threading.Thread(target=Pastie().monitor)

    for thread in (pastebin_thread, slexy_thread, pastie_thead):
        thread.daemon = True
        thread.start()

    try:
        while(1):
            sleep(5)
    except KeyboardInterrupt:
        logging.warn('Stopped.')


if __name__ == "__main__":
    monitor()
