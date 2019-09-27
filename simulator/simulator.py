from config import TRENDS
import math

from learningmodule import normalize_data
from stockmarketmodule import get_price
import tensorflow as tf
import pickle
import copy


class Wallet:
    def __init__(self, actions, money):
        self.actions = actions
        self.money = money


amzn_model = tf.keras.models.load_model('./resources/model/bags_of_words_AMZN.h5')
adbe_model = tf.keras.models.load_model('./resources/model/bags_of_words_ADBE.h5')
apc_model = tf.keras.models.load_model('./resources/model/bags_of_words_APC.h5')
gs_model = tf.keras.models.load_model('./resources/model/bags_of_words_GS.h5')
jpm_model = tf.keras.models.load_model('./resources/model/bags_of_words_JPM.h5')

last_prices = {}

def get_model(sign):
    if sign == "AMZN":
        return amzn_model
    if sign == "ADBE":
        return adbe_model
    if sign == "APC":
        return apc_model
    if sign == "GS":
        return gs_model
    if sign == "JPM":
        return jpm_model


def get_prices(date):
    set_one_price("AMZN", date)
    set_one_price("ADBE", date)
    set_one_price("APC", date)
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


def simulate_single_article(article_vector, article_date, name: str, wallet: Wallet):
    article_vector = article_vector.reshape((1, len(article_vector)))

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


def simulate(inputs):
    sorted_list = sorted(inputs, key=lambda k: k['date'])

    input_data = normalize_data([el["data"] for el in sorted_list])
    input_date = [el["date"] for el in sorted_list]
    input_sign = [el["sign"] for el in sorted_list]

    history = []

    wallet = Wallet({}, 100000)

    for article_vector, article_date, sign in zip(input_data, input_date, input_sign):
        wallet, prices, trend = simulate_single_article(article_vector, article_date, sign, wallet)
        test = {
            'date': article_date,
            'trend': trend,
            'trend_name': sign,
            'money': wallet.money,
            'actions': copy.copy(wallet.actions),
            'prices': copy.copy(prices)
        }
        print(test)
        history.append(test)

    with open("resources/history.txt", "wb") as fp:
        pickle.dump(history, fp)

