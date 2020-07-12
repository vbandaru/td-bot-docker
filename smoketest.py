import alpaca_trade_api as alpaca
import pandas as pd
import sys
import talib

import logging

logger = logging.getLogger()

import slack
import os

import schedule
import datetime
import time


fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=fmt)
fh = logging.FileHandler('console_smoketest.log')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter(fmt))
logger.addHandler(fh)

# import xyz

def job():

    logger.info("Job running current time : {}".format(time.ctime()))



if __name__ == "__main__":
    import schedule
    import datetime
    import time

    nowtime = str(datetime.datetime.now())

    for i in ["10:00", "12:00", "14:00", "16:00"]:
        schedule.every().monday.at(i).do(job)

    schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()

        time.sleep(5)

