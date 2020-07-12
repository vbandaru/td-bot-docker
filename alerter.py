import alpaca_trade_api as alpaca
import pandas as pd
import sys
import talib

import logging

logger = logging.getLogger()

import slack
import os

fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=fmt)
fh = logging.FileHandler('console.log')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter(fmt))
logger.addHandler(fh)

api = alpaca.REST()
slack_client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])


def send_slack(msg):
    if "SLACK_ENABLE" not in os.environ or os.environ["SLACK_ENABLE"] == 'true':
        slack_client.chat_postMessage(channel="#algo-trading", text=msg)

    logger.info(msg)

def job():

    logger.info("10s job current time : {}".format(time.ctime()))

    # symbols = set(os.environ["SYMBOLS"].split(','))  # rm dups with set # os.environ["STOCKS"].split(",")

    symbols = ['CHTR', 'NFLX', 'RNG', 'AAPL', 'AMZN', 'ETSY', 'TJX', 'CMG', 'SAM', 'COST', 'BURL', 'DPZ', 'MA', 'PAYC',
               'PYPL', 'MKTX', 'BMY', 'DHR', 'LLY', 'CVS', 'UNH', 'AMED', 'TDOC', 'TNDM', 'DXCM', 'EHTH', 'NVCR',
               'IRTC', 'VRTX', 'HUM', 'BA', 'LMT', 'NVDA', 'ADBE', 'ADSK', 'AMD', 'SHOP', 'TWLO', 'TTD', 'COUP', 'OKTA',
               'ASML', 'EQIX', 'CCI']
    # symbols = ['AMD']
    logger.info(",".join(symbols))

    now = pd.Timestamp.now(tz='America/New_York')
    end = now.strftime('%Y-%m-%d')
    start = (now - pd.Timedelta('400day')).strftime('%Y-%m-%d')

    logger.info("getting data from {} to {}".format(start, end))

    sma_list = [50, 200]  # 20
    ema_list = []  # 9, 21, 55

    for symbol in symbols:
        df = api.polygon.historic_agg_v2(symbol, 1, 'day', start, end, unadjusted=False).df

        # skip first 200 bars
        # df = df.iloc[200:]

        closes = df.close.values
        lows = df.low.values

        for sma in sma_list:
            df['sma' + str(sma)] = df.close.rolling(sma).mean().round(2)
            # df['sma' + str(sma) + 'cross'] = (df['close'].shift(1) < df['sma' + str(sma)].shift(1)) & (
            #             df['close'] > df['sma' + str(sma)])

        for ema in ema_list:
            df['ema' + str(ema)] = df['close'].ewm(span=ema, adjust=False).mean().round(2)
            # df['sma' + str(sma) + 'cross'] = (df['close'].shift(1) < df['sma' + str(sma)].shift(1)) & (
            #             df['close'] > df['sma' + str(sma)])


        logger.debug("Bars for {}: \n\n{}".format(symbol, df.tail()))

        # for i in df.index:
        #     for sma in smas:
        #         if df['sma' + str(sma) + 'cross'][i]:
        #             msg = "on {} {} crossed above {} SMA".format(i, symbol, sma)
        #             logger.debug(msg)

        for sma in sma_list:
            smas = df['sma' + str(sma)].values
            if closes[-2] < smas[-2] and closes[-1] > smas[-1]:
                msg = ":arrow_up {} crossed above {} SMA close: {} SMA: {}".format(symbol, sma, closes[-1], smas[-1])
                send_slack(msg)

            if closes[-2] > smas[-2] and closes[-1] < smas[-1]:
                msg = ":small_red_triangle_down {} crossed below {} SMA close: {} SMA: {}".format(symbol, sma, closes[-1], smas[-1])
                send_slack(msg)

        for ema in ema_list:
            emas = df['ema' + str(ema)].values
            if closes[-2] < emas[-2] and closes[-1] > emas[-1]:
                msg = ":arrow_up {} crossed above {} EMA close: {} EMA: {}".format(symbol, ema, closes[-1], emas[-1])
                logger.info(msg)

            if closes[-2] > emas[-2] and closes[-1] < emas[-1]:
                msg = ":small_red_triangle_down {} crossed below {} EMA close: {} EMA: {}".format(symbol, ema, closes[-1], emas[-1])
                logger.info(msg)

        days = [ -7, -30, -90]

        for day in days:
            if lows[-1]  < lows[day -1 :-2].min():
                msg = ":arrow_up {} new {} day low current: {} low: {}".format(symbol, day, closes[-1], lows[-1])


if __name__ == "__main__":
    import schedule
    import datetime
    import time

    nowtime = str(datetime.datetime.now())

    for i in ["10:00", "12:00", "14:00", "16:00"]:
        schedule.every().monday.at(i).do(job)
        schedule.every().tuesday.at(i).do(job)
        schedule.every().wednesday.at(i).do(job)
        schedule.every().thursday.at(i).do(job)
        schedule.every().friday.at(i).do(job)

    # schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()

        time.sleep(30)