import config
from datetime import datetime


def get_market_prices(name: str, date):
    from alpha_vantage.timeseries import TimeSeries
    ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=name, interval='1min', outputsize='full')

    return data.to_csv("resources/" + name + "/" + str(date.date()) + '.csv')


get_market_prices(config.EOG_NAME, datetime(2019, 7, 15))
