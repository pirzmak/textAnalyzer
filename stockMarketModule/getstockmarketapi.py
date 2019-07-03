from iexfinance.stocks import get_historical_intraday
from dateutil import parser
import math
import config
from .mysessiondate import *

myCache = {}
CACHE_SIZE = config.config['cache_size']


def get_stock_prices(name: str, date: datetime):
    date = to_first_day_session_if_needed(date)
    date = to_next_day_session_if_needed(date)

    key = name+str(datetime(date.year, date.month, date.day, date.hour, date.minute, 0))

    if len(myCache) == CACHE_SIZE:
        myCache.clear()

    if key in myCache:
        return myCache[key]
    else:
        date_list = get_day_market_prices(name, date)

        for i in date_list:
            i_key = name + str(i[0])
            if i_key not in myCache:
                myCache[i_key] = i[1]
            if date.day != i[0].day:
                key = name + str(datetime(date.year, date.month, date.day, i[0].hour, i[0].minute, 0))
                myCache[key] = date_list[0][1]

        if key not in myCache:
            myCache[key] = math.nan
        if math.isnan(myCache[key]):
            return try_to_get_nearly_price(name, date)

        return myCache[key]


def try_to_get_nearly_price(name: str, date: datetime):
    for i in range(1, 5):
        date = datetime(date.year, date.month, date.day, date.hour, date.minute, 0) + timedelta(minutes=i)
        key = name+str(date)
        if key in myCache:
            return myCache[key]
        date = datetime(date.year, date.month, date.day, date.hour, date.minute, 0) - timedelta(minutes=i)
        key = name+str(date)
        if key in myCache:
            return myCache[key]
    return 'nan'


def get_day_market_prices(name: str, date: datetime):
    date_list = list()
    tmp_date = date

    while not date_list:
        response = get_historical_intraday(name, tmp_date, output_format='pandas', token=config.config["IEX_API_KEY"])
        date_list = list(map(lambda x: (parser.parse(x[3] + " " + x[5]), x[0]), response.values))
        tmp_date = next_day(tmp_date)
        print(tmp_date)

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
