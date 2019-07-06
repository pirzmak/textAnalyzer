from dataBase.mango_db import select, update
from stockMarketModule.getstockmarketapi import get_stock_after_before_actual_price


def save_prices_to_db(name: str, sign: str, tags: []):
    i = 0
    for x in select(name, {'$or': tags}):
        prices = get_stock_after_before_actual_price(sign, x['date'])
        print(i)
        i += 1
        update(name, {'_id': x['_id']}, {"$set": {"before_price": prices['before'],
                                                  "actual_price": prices['actual'],
                                                  "after_price": prices['after']}})