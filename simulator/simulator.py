from config import TRENDS
import math
from stockmarketmodule import get_price
import tensorflow as tf
import pickle


class Wallet:
    def __init__(self, actions, money, model):
        self.actions = actions
        self.money = money
        self.model = model


wallet = Wallet({}, 100000, tf.keras.models.load_model('./resources/model/bags_of_words_AMZN.h5'))


def simulate_single_article(article_vector, article_date, name: str):
    article_vector = article_vector.reshape((1, len(article_vector)))
    prediction = wallet.model.predict(article_vector)
    trend = TRENDS.get_trends(prediction.argmax())
    price = get_price(name, article_date)['actual']
    if trend == TRENDS.BIG_DECREASE and name in wallet.actions:
        wallet.money = wallet.money + wallet.actions[name] * price
        wallet.actions[name] = 0
    if trend == TRENDS.DECREASE and name in wallet.actions:
        number = math.ceil(wallet.actions[name] * 0.5)
        wallet.money = wallet.money + number * price
        wallet.actions[name] = wallet.actions[name] - number
    if trend == TRENDS.INCREASE:
        number = math.ceil(wallet.money * 0.05 / price)
        wallet.money = wallet.money - number * price
        wallet.actions[name] = wallet.actions.get(name, 0) + number
    if trend == TRENDS.BIG_INCREASE:
        number = math.ceil(wallet.money * 0.2 / price)
        wallet.money = wallet.money - number * price
        wallet.actions[name] = wallet.actions.get(name, 0) + number

    print(trend, wallet.money, wallet.actions)


