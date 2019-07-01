from datetime import datetime
from datetime import timedelta
from iexfinance.stocks import get_historical_intraday
from dateutil import parser
import math
import config

myCash = {}


def get_stock_prices(name: str, date: datetime):
    if date.hour < 9 or (date.hour == 9 and date.minute < 30):
        date = datetime(date.year, date.month, date.day, 9, 30, 0)
    if date.hour > 15 or (date.hour == 15 and date.minute > 30):
        date += timedelta(days=1)
        date = datetime(date.year, date.month, date.day, 9, 30, 0)
    key = name+str(datetime(date.year, date.month, date.day, date.hour, date.minute, 0))
    if key in myCash:
        return myCash[key]
    else:
        date_list = list()
        tmp_date = date
        while not date_list:
            response = get_historical_intraday(name, tmp_date, output_format='pandas', token=config.config["IEX_API_KEY"])
            date_list = list(map(lambda x: (parser.parse(x[3] + " " + x[5]), x[0]), response.values))
            tmp_date = tmp_date + timedelta(days=1)
            tmp_date = datetime(tmp_date.year, tmp_date.month, tmp_date.day, 9, 30, 0)

        for i in date_list:
            i_key = name + str(i[0])
            if i_key not in myCash:
                myCash[i_key] = i[1]
            if date.day != i[0].day:
                key = name + str(datetime(date.year, date.month, date.day, i[0].hour, i[0].minute, 0))
                myCash[key] = date_list[0][1]
        return myCash[key]


def get_stock_after_before_actual_price(name: str, date: datetime, delta=40):
    before = date - timedelta(minutes=delta)

    if date.hour > 15:
        date += timedelta(days=1)
        date = datetime(date.year, date.month, date.day, 9, 30, 0)

    after = date + timedelta(minutes=delta)

    if before.hour < 9 or (before.hour == 9 and before.minute < 30):
        before -= timedelta(days=1)
        before = datetime(before.year, before.month, before.day, 15, 0, 0)
    if before.hour > 15:
        before = datetime(before.year, before.month, before.day, 15, 0, 0)

    if after.hour < 9 or (after.hour == 9 and after.minute < 30):
        after = datetime(after.year, after.month, after.day, 9, 30, 0)

    before_price = get_stock_prices(name, before)
    actual_price = get_stock_prices(name, date)
    after_price = get_stock_prices(name, after)

    if math.isnan(before_price):
        if math.isnan(actual_price):
            if math.isnan(after_price):
                before_price = after_price
            else:
                before_price = 0
        else:
            before_price = actual_price

    if math.isnan(actual_price):
        if math.isnan(before_price):
            if math.isnan(after_price):
                actual_price = after_price
            else:
                actual_price = 0
        else:
            actual_price = before_price

    if math.isnan(after_price):
        if math.isnan(actual_price):
            if math.isnan(before_price):
                after_price = before_price
            else:
                after_price = 0
        else:
            after_price = actual_price

    return {"before": before_price,
            "actual": actual_price,
            "after": after_price}

