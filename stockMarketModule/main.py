from stockMarketModule.getstockmarketapi import get_stock_after_before_actual_price


def get_price(sign: str, date):
    prices = get_stock_after_before_actual_price(sign, date)

    return prices
