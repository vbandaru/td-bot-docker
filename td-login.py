from tda import auth, client, debug
import json
import config
from tda.utils import Utils

debug.enable_bug_report_logging()

print(config)


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

# r = c.get_price_history('AAPL',
#         period_type=client.Client.PriceHistory.PeriodType.YEAR,
#         period=client.Client.PriceHistory.Period.TWENTY_YEARS,
#         frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
#         frequency=client.Client.PriceHistory.Frequency.DAILY)
# assert r.ok, r.raise_for_status()

# r = c.get_quote('BA')

# # print(json.dumps(r.json(), indent=4))


# r = c.get_instrument('BA')

# print(json.dumps(r.json(), indent=4))


# # gives vol 1d, 10d, 3m avg, low, high etc
# r = c.search_instruments(['BA'], c.Instrument.Projection.FUNDAMENTAL)

# print(json.dumps(r.json(), indent=4))


# r = c.get_option_chain('BA')

# print(json.dumps(r.json(), indent=4))


# r = c.get_option_chain('BA', contract_type='CALL')
# r = c.get_option_chain('BA', contract_type=c.Options.ContractType.CALL)

## won't work, convert string date to date obj < TODO
# r = c.get_option_chain('BA', contract_type=c.Options.ContractType.CALL, strike=300, strike_from_date='2020-06-24', strike_to_date='2020-07-24')
# r = c.get_option_chain('BA', contract_type=c.Options.ContractType.CALL, strike=300)


# print(json.dumps(r.json(), indent=4))




#### Place Orders ##########


# from tda.orders import OrderBuilder, Duration, Session
# from tda.orders.generic import OrderBuilder
from tda.orders.common import Duration, Session
#
#
# builder = OrderBuilder(enforce_enums=True)
# builder.set_instruction(OrderBuilder.Instruction.BUY)
# builder.set_order_type(OrderBuilder.OrderType.MARKET) # or LIMIT
# builder.set_duration(Duration.DAY) # GOOD_TILL_CANCEL
# builder.set_session(Session.NORMAL) # AM or #PM

from tda.orders.equities import equity_buy_limit
from tda.orders.common import Duration, Session

order = (equity_buy_limit('AMD', 1, 40.0)
 .set_duration(Duration.GOOD_TILL_CANCEL)).build()


c.place_order(config.account_id, order)

#
#  assert r.ok
#
# # Assume client and order already exist and are valid
# assert r.ok, r.raise_for_status()
# order_id = Utils(config.account_id, client).extract_order_id(r)
# assert order_id is not None
#
# print(order_id)
