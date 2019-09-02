from config import TRENDS

NO_CHANGE_VALUE = 0.0005


def get_price_trend(before, actual, after):
    to_d, from_d = before - actual, actual - after
    if (no_change(actual, to_d) and no_change(actual, from_d)) or \
            (to_d > 0 and from_d > 0) or (to_d < 0 and from_d < 0):
        return TRENDS.NO_CHANGE
    elif (no_change(actual, to_d) and from_d > 0) or (to_d < 0 and no_change(actual, from_d)):
        return TRENDS.DECREASE
    elif (no_change(actual, to_d) and from_d < 0) or (to_d > 0 and no_change(actual, from_d)):
        return TRENDS.INCREASE
    elif to_d < 0 < from_d:
        return TRENDS.BIG_DECREASE
    elif to_d > 0 > from_d:
        return TRENDS.BIG_INCREASE


def no_change(value, different):
    return value == 0 or abs(different/value) < NO_CHANGE_VALUE
