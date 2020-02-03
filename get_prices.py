import config
from datetime import datetime


def get_market_prices(name: str, date):
    from alpha_vantage.timeseries import TimeSeries
    ts = TimeSeries(key=config.config["STOCK_API_KEY"], output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=name, interval='1min', outputsize='full')

    return data.to_csv(config.resources_path("stockprices/" + name + "/" + str(date.date()) + '.csv'))

# get_market_prices(config.AMAZON_NAME, datetime(2019, 11, 23))
# get_market_prices(config.ADOBE_NAME, datetime(2019, 11, 23))
# get_market_prices(config.GOLDMAN_NAME, datetime(2019, 11, 23))
# get_market_prices(config.MORGAN_NAME, datetime(2019, 11, 23))
