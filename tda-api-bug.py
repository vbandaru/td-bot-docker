from tda import auth, client, debug
import config

# debug.enable_bug_report_logging()

try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager

    ## use easy driver manager
    # https://stackoverflow.com/questions/60296873/sessionnotcreatedexception-message-session-not-created-this-version-of-chrome

    with webdriver.Chrome(ChromeDriverManager().install()) as driver:
        # with webdriver.Chrome('/home/vijay/tools/chromedriver_linux64/chromedriver') as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path)


from tda.orders.equities import equity_buy_limit
from tda.orders.common import Duration, Session

# order = (equity_buy_limit('AMD', 1, 40.0)
#          .set_duration(Duration.GOOD_TILL_CANCEL)).build()
#
# r = c.place_order(config.account_id, order)
#
# assert r.ok, r.raise_for_status()

from tda.utils import Utils

# order_id = Utils(c, config.account_id).extract_order_id(r)
# assert order_id is not None
#
# print(order_id)

o = c.get_orders_by_path(config.account_id, max_results=5, status=client.Client.Order.Status.WORKING)

assert o.ok, o.raise_for_status()
data = o.json()

# print(orders)

for order in data:
    print(order['orderId'])
    print(order['orderLegCollection'][0]['instrument']['symbol'])
    print(order['orderLegCollection'][0]['instruction'])
    print(order['orderLegCollection'][0]['quantity'])

    print("------------------------------")

    c.cancel_order(order_id=order['orderId'], account_id=config.account_id)

import pandas as pd
from pandas.io.json import json_normalize

df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')

# df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')

# df = pd.json_normalize(data)

# df.columns = df.columns.map(lambda x: x.split(".")[-1])


print(df)

df.to_csv ('demo.csv', index = False, header=True)
