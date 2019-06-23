from datetime import datetime
from datetime import timedelta
from iexfinance.stocks import get_historical_intraday
from dateutil import parser
import config

myCash = {}


def get_stock_prices_day(name: str, date: datetime):
    if date.hour < 9 or (date.hour == 9 and date.minute < 30):
        date = datetime(date.year, date.month, date.day, 9, 30, 0)
    if date.hour > 15:
        date += timedelta(days=1)
        date = datetime(date.year, date.month, date.day, 9, 30, 0)
    key = name+str(date)
    if key in myCash:
        return myCash[key]
    else:
        date_list = list()
        while not date_list:
            response = get_historical_intraday(name, date, output_format='pandas', token=config.config["IEX_API_KEY"])
            date_list = list(map(lambda x: (parser.parse(x[3] + " " + x[5]), x[0]), response.values))

        for i in date_list:
            i_key = name + str(i[0])
            if i_key not in myCash:
                myCash[i_key] = i[1]
            if date.day != i[0].day:
                i_key = name + str(datetime(date.year, date.month, date.day, i[0].hour, i[0].minute, i[0].hour))
                myCash[i_key] = date_list[0][1]
        return myCash[key]



