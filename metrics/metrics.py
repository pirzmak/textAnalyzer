from numpy import genfromtxt

from config import TRENDS


def get_data(type, tag, model):
    results = genfromtxt('resources/metrics/' + type + "/" + tag + '_' + model + '_results.csv', delimiter=',')
    data = genfromtxt('resources/metrics/' + type + "/" + tag + '_' + model + '_data.csv', delimiter=',')

    return results, data


def get_loss_acc_time(type, tag, model):
    tmp = genfromtxt('resources/metrics/' + type + "/" + tag + '/' + model + '_val_results.csv', delimiter=',')
    time = genfromtxt('resources/metrics/' + type + "/" + tag + '/' + model + '_time.csv', delimiter=',')

    return tmp[0], tmp[1], time


def check_in_range(results, data, limit = 1):
    limit = range(min(limit, len(results[0])))

    good = 0
    bad = 0
    all = 0

    for r, d in zip(results, data):
        en = sorted(enumerate(r), key=lambda tup: -tup[1])
        is_good = False
        for n in limit:
            if en[n][0] == d:
                is_good = True
                break

        if is_good:
            good = good + 1
        else:
            bad = bad + 1

        all = all + 1

    return good, bad, all


def get_one_to_one_metric(type, tag, model):
    results, data = get_data(type, tag, model)

    good, bad, all = check_in_range(results, data)

    return good/all, bad/all


def get_best_two_metric(type, tag):
    results, data = get_data(type, tag)

    good, bad, all = check_in_range(results, data, 2)

    return good/all, bad/all


def is_increase(r):
    return TRENDS.get_trends(r) == TRENDS.INCREASE or TRENDS.get_trends(r) == TRENDS.BIG_INCREASE


def is_decrease(r):
    return TRENDS.get_trends(r) == TRENDS.DECREASE or TRENDS.get_trends(r) == TRENDS.BIG_DECREASE


def is_the_same_trend(r,d):
    return is_increase(r) and is_increase(d) or is_decrease(r) and is_decrease(d) or r == TRENDS.NO_CHANGE and d == TRENDS.NO_CHANGE


def get_trend_metric(type, tag):
    results, data = get_data(type, tag)

    good = 0
    bad = 0
    all = 0

    for r, d in zip(results, data):
        if is_the_same_trend(r.argmax(), d):
            good = good + 1
        else:
            bad = bad + 1

        all = all + 1

    return good/all, bad/all