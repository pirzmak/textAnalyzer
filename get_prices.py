import config
from datetime import datetime


def get_market_prices(name: str, date):
    from alpha_vantage.timeseries import TimeSeries
    ts = TimeSeries(key=config["STOCK_API_KEY"], output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=name, interval='1min', outputsize='full')

    return data.to_csv(config.resources_path(name + "/" + str(date.date()) + '.csv'))


get_market_prices(config.EOG_NAME, datetime(2019, 7, 15))
