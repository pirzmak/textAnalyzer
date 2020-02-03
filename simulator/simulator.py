from config import TRENDS
import math

from learningmodule import normalize_data
from stockmarketmodule import get_price
import tensorflow as tf
import numpy as np
import pickle
import copy
from config import DBNAMES
import gc
import random


class Wallet:
    def __init__(self, actions, money):
        self.actions = actions
        self.money = money


# amzn_model = tf.keras.models.load_model('./resources/model/names_entities/AMZN/one_4096_relu.h5')
# adbe_model = tf.keras.models.load_model('./resources/model/names_entities/ADBE/one_4096_relu.h5')
# gs_model = tf.keras.models.load_model('./resources/model/names_entities/GS/one_4096_relu.h5')
# jpm_model = tf.keras.models.load_model('./resources/model/names_entities/JPM/one_4096_relu.h5')

last_prices = {}

def get_model(sign):
    # if sign == "AMZN":
    #     return amzn_model
    # if sign == "ADBE":
    #     return adbe_model
    # if sign == "GS":
    #     return gs_model
    if sign == "JPM":
        return jpm_model


def get_prices(date):
    set_one_price("AMZN", date)
    set_one_price("ADBE", date)
    set_one_price("GS", date)
    set_one_price("JPM", date)

    return last_prices


def set_one_price(name, date):
    price = get_price(name, date)
    if price['actual'] == 0:
        if price['before'] == 0:
            best_price = price['after']
        else:
            best_price = price['before']
    else:
        best_price = price['actual']

    if price['actual'] is math.nan or best_price == 0:
        print(price, last_prices)

    last_prices[name] = best_price if best_price > 0 else last_prices.get(name, 0)


def buy_single(name, number, price, wallet: Wallet):
    wallet.money = wallet.money - number * price
    wallet.actions[name] = wallet.actions.get(name, 0) + number
    return wallet


def sell_single(name, number, price, wallet: Wallet):
    wallet.money = wallet.money + number * price
    wallet.actions[name] = wallet.actions[name] - number
    return wallet


def buy(stat, name, prices, wallet: Wallet):
    if wallet.money < prices[name]:
        for n, v in wallet.actions.items():
            wallet = sell(n, stat * 0.5, prices[n], wallet)

    number = math.ceil(wallet.money * 0.2 / prices[name])

    if wallet.money >= number * prices[name]:
        wallet = buy_single(name, number, prices[name], wallet)
    else:
        wallet = buy_single(name, math.floor(wallet.money / prices[name]), prices[name], wallet)

    return wallet


def sell(stat, name, prices, wallet: Wallet):
    if name in wallet.actions:
        wallet = sell_single(name, math.ceil(wallet.actions[name] * stat), prices[name], wallet)
    return wallet


def simulate_single_article(article_vector, article_date, name: str, wallet: Wallet, type):
    if type == DBNAMES.BAGS_OF_WORDS or type == DBNAMES.NOUNS:
        shape = (1, len(article_vector))
    if type == DBNAMES.NAMES_ENTITIES:
        max_len = len(article_vector[0])
        shape = (1, 18, max_len)

    article_vector = article_vector.reshape(shape)

    model = get_model(name)

    prediction = model.predict(article_vector)
    trend = TRENDS.get_trends(prediction.argmax())

    prices = get_prices(article_date)
    if prices[name] and prices[name] > 0:
        if trend == TRENDS.BIG_DECREASE and name in wallet.actions:
            sell(1, name, prices, wallet)
        if trend == TRENDS.DECREASE and name in wallet.actions:
            sell(0.5, name, prices, wallet)
        if trend == TRENDS.INCREASE:
            buy(0.05, name, prices, wallet)
        if trend == TRENDS.BIG_INCREASE:
            buy(0.2, name, prices, wallet)

    return wallet, prices, trend


def simulate_single_article2(trend, article_date, name: str, wallet: Wallet):
    prices = get_prices(article_date)
    trend = random.randint(0, 4)
    if prices[name] and prices[name] > 0:
        if trend == TRENDS.BIG_DECREASE and name in wallet.actions:
            sell(1, name, prices, wallet)
        if trend == TRENDS.DECREASE and name in wallet.actions:
            sell(0.5, name, prices, wallet)
        if trend == TRENDS.INCREASE:
            buy(0.05, name, prices, wallet)
        if trend == TRENDS.BIG_INCREASE:
            buy(0.2, name, prices, wallet)

    return wallet, prices, trend


def simulate(inputs, name, type):
    sorted_list = sorted(inputs, key=lambda k: k['date'])

    if type == DBNAMES.BAGS_OF_WORDS or type == DBNAMES.NOUNS:
        input_data = normalize_data([el["data"] for el in sorted_list])
    if type == DBNAMES.NAMES_ENTITIES:
        input_data = list(map(lambda x: np.asarray(normalize_data(x)), [el["data"] for el in sorted_list if el["sign"] == "JPM"]))

    input_date = [el["date"] for el in sorted_list]
    input_sign = [el["sign"] for el in sorted_list]

    history = []

    wallet = Wallet({}, 100000)

    for article_vector, article_date, sign in zip(input_data, input_date, input_sign):
        wallet, prices, trend = simulate_single_article(article_vector, article_date, sign, wallet, type)
        test = {
            'date': article_date,
            'trend': trend,
            'trend_name': sign
        }
        history.append(test)

    with open("resources/" + name, "wb") as fp:
        pickle.dump(history, fp)

def simulate2(inputs, name, type):
    # sorted_list = sorted(inputs, key=lambda k: k['date'])
    #
    # if type == DBNAMES.BAGS_OF_WORDS or type == DBNAMES.NOUNS:
    #     input_data = normalize_data([el["data"] for el in sorted_list])
    # if type == DBNAMES.NAMES_ENTITIES:
    #     input_data = list(map(lambda x: np.asarray(normalize_data(x)), [el["data"] for el in sorted_list]))
    #
    # input_date = [el["date"] for el in sorted_list]
    # input_sign = [el["sign"] for el in sorted_list]

    history = []

    wallet = Wallet({}, 100000)
    #
    # with open("resources/test.data", "wb") as fp:
    #     pickle.dump(zip(input_data, input_date, input_sign), fp)

    inputs = []

    with open("resources/adbe_trends", "rb") as fp:
        inputs = inputs + pickle.load(fp)
    with open("resources/amzn_trends", "rb") as fp:
        inputs = inputs + pickle.load(fp)
    with open("resources/gs_trends", "rb") as fp:
        inputs = inputs + pickle.load(fp)
    with open("resources/jpm_trends", "rb") as fp:
        inputs = inputs + pickle.load(fp)

    with open("resources/adbe_trends2", "rb") as fp:
        inputs = inputs + pickle.load(fp)
    with open("resources/amzn_trends2", "rb") as fp:
        inputs = inputs + pickle.load(fp)
    with open("resources/gs_trends2", "rb") as fp:
        inputs = inputs + pickle.load(fp)
    with open("resources/jpm_trends2", "rb") as fp:
        inputs = inputs + pickle.load(fp)

    with open("resources/adbe_trends3", "rb") as fp:
        inputs = inputs + pickle.load(fp)
    with open("resources/amzn_trends3", "rb") as fp:
        inputs = inputs + pickle.load(fp)
    with open("resources/gs_trends3", "rb") as fp:
        inputs = inputs + pickle.load(fp)
    with open("resources/jpm_trends3", "rb") as fp:
        inputs = inputs + pickle.load(fp)

    inputs = sorted(inputs, key=lambda k: k['date'])

    print((len(inputs)))
    i = 0
    for el in inputs:
        print(i)
        i=i+1
        wallet, prices, trend = simulate_single_article2(el["trend"], el["date"], el["trend_name"], wallet)
        test = {
            'date': el["date"],
            'trend': trend,
            'trend_name': el["trend_name"],
            'money': wallet.money,
            'actions': copy.copy(wallet.actions),
            'prices': copy.copy(prices)
        }
        history.append(test)

    with open("resources/results_" + name + "_" + type + ".model", "wb") as fp:
        pickle.dump(history, fp)
