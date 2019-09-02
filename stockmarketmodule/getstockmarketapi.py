from iexfinance.stocks import get_historical_intraday
import pandas as pd
import math
import config
from dateutil import parser
from .mysessiondate import *

myCache = {}
CACHE_SIZE = config.config['cache_size']


def get_stock_prices(name: str, date: datetime):
    date = to_first_day_session_if_needed(date)
    date = to_next_day_session_if_needed(date)
    monday = date - timedelta(days=date.weekday())

    key = str(datetime(date.year, date.month, date.day, date.hour, date.minute, 0))

    if len(myCache) == CACHE_SIZE:
        myCache.clear()

    if key in myCache:
        return myCache[key]
    else:
        try:
            prices = get_market_prices(name, str(monday.date()))
            for i in prices:
                myCache[i[0]] = i[1]
            return myCache[key]
        except:
            return float('nan')


def get_market_prices(name: str, date: str):
    data = pd.read_csv('resources/stockprices/' + name + "/" + date + ".csv")

    to_ret = list()
    for index, row in data.iterrows():
        to_ret.append((row[0], row[1]))

    return to_ret


def get_day_market_prices(name: str, date: datetime):
    date_list = list()
    tmp_date = datetime(date.year, date.month, date.day)

    while not date_list:
        response = get_historical_intraday(name, tmp_date, output_format='pandas', token=config.config["IEX_API_KEY"])
        date_list = list(map(lambda x: (parser.parse(x[3] + " " + x[5]), x[0]), response.values))
        tmp_date = next_day(tmp_date)

    return date_list


def get_stock_after_before_actual_price(name: str, date: datetime, delta=40):
    before = date - timedelta(minutes=delta)

    date = to_next_day_session_if_needed(date)

    after = date + timedelta(minutes=delta)

    before = to_previous_day_session_if_needed(before)

    before = to_last_day_session_if_needed(before)

    after = to_first_day_session_if_needed(after)

    before_price = get_stock_prices(name, before)
    actual_price = get_stock_prices(name, date)
    after_price = get_stock_prices(name, after)

    before_price = find_no_nan(before_price, actual_price, after_price)
    actual_price = find_no_nan(actual_price, before_price, after_price)
    after_price = find_no_nan(after_price, actual_price, before_price)

    return {"before": before_price,
            "actual": actual_price,
            "after": after_price}


def find_no_nan(p1, p2, p3):
    if math.isnan(p1):
        if math.isnan(p2):
            if math.isnan(p3):
                return p3
            else:
                return 0
        else:
            return p2
    else:
        return p1
