from config import TRENDS
import math

from learningmodule import normalize_data
from stockmarketmodule import get_price
import tensorflow as tf
import pickle


class Wallet:
    def __init__(self, actions, money):
        self.actions = actions
        self.money = money


amzn_model = tf.keras.models.load_model('./resources/model/bags_of_words_AMZN.h5')
adbe_model = tf.keras.models.load_model('./resources/model/bags_of_words_ADBE.h5')
apc_model = tf.keras.models.load_model('./resources/model/bags_of_words_APC.h5')
gs_model = tf.keras.models.load_model('./resources/model/bags_of_words_GS.h5')
jpm_model = tf.keras.models.load_model('./resources/model/bags_of_words_JPM.h5')

wallet = Wallet({}, 100000)


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
    return {
        "ADBE": get_price("ADBE", date)['actual'],
        "AMZN": get_price("AMZN", date)['actual'],
        "APC": get_price("APC", date)['actual'],
        "GS": get_price("GS", date)['actual'],
        "JPM": get_price("GS", date)['actual']
    }


def simulate_single_article(article_vector, article_date, name: str):
    article_vector = article_vector.reshape((1, len(article_vector)))
    model = get_model(name)
    prediction = model.predict(article_vector)
    trend = TRENDS.get_trends(prediction.argmax())
    prices = get_prices(article_date)
    price = prices[name]

    if trend == TRENDS.BIG_DECREASE and name in wallet.actions:
        wallet.money = wallet.money + wallet.actions[name] * price
        wallet.actions[name] = 0
    if trend == TRENDS.DECREASE and name in wallet.actions:
        number = math.ceil(wallet.actions[name] * 0.5)
        wallet.money = wallet.money + number * price
        wallet.actions[name] = wallet.actions[name] - number
    if trend == TRENDS.INCREASE:
        number = math.ceil(wallet.money * 0.05 / price)
        if wallet.money >= number * price:
            wallet.money = wallet.money - number * price
            wallet.actions[name] = wallet.actions.get(name, 0) + number
    if trend == TRENDS.BIG_INCREASE:
        number = math.ceil(wallet.money * 0.2 / price)
        if wallet.money >= number * price:
            wallet.money = wallet.money - number * price
            wallet.actions[name] = wallet.actions.get(name, 0) + number

    print({
        'date': article_date,
        'trend': trend,
        'trend_name': name,
        'money': wallet.money,
        'actions': wallet.actions,
        'prices': prices
    })
    return {
        'date': article_date,
        'trend': trend,
        'trend_name': name,
        'money': wallet.money,
        'actions': wallet.actions,
        'prices': prices
    }


def simulate(inputs):
    sorted_list = sorted(inputs, key=lambda k: k['date'])[:500]

    input_data = normalize_data([el["data"] for el in sorted_list])
    input_date = [el["date"] for el in sorted_list]
    input_sign = [el["sign"] for el in sorted_list]

    history = []

    for x, y, s in zip(input_data, input_date, input_sign):
        history.append(simulate_single_article(x, y, s))

    with open("resources/history.txt", "wb") as fp:
        pickle.dump(history, fp)

