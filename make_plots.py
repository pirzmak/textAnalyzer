import pickle

from config import *
from plots import make_models_plot, make_plot_value_price, make_plot_trend_price


def get_money_value(x):
    actions = x['actions']
    prices = x['prices']
    money = x['money']
    for name, value in actions.items():
        money = money + value * prices[name]
    return money


with open("resources/results_no_model.model", "rb") as fp:
    history = pickle.load(fp)

model_x = list(map(lambda x: x['date'], history))
no_model_y = list(map(lambda x: get_money_value(x), history))

with open("resources/results__nouns.model", "rb") as fp:
    history_nouns = pickle.load(fp)

with open("resources/results__names_entities.model", "rb") as fp:
    history_names_entities = pickle.load(fp)

with open("resources/results__bags_of_words.model", "rb") as fp:
    history_bags_of_words = pickle.load(fp)

model_bags_of_words_y = list(map(lambda x: get_money_value(x), history_bags_of_words))
model_names_entities_y = list(map(lambda x: get_money_value(x), history_names_entities))
model_nouns_y = list(map(lambda x: get_money_value(x), history_nouns))

# make_models_plot(model_x, no_model_y, model_bags_of_words_y, model_names_entities_y, model_nouns_y, "resources/plots/all_models")

amzn_value = list(map(lambda x: x['actions'].get(AMAZON_NAME, 0), history_nouns))
amzn_price = list(map(lambda x: x['prices'][AMAZON_NAME], history_nouns))
adobe_value = list(map(lambda x: x['actions'].get(ADOBE_NAME, 0), history_nouns))
adobe_price = list(map(lambda x: x['prices'][ADOBE_NAME], history_nouns))
gs_value = list(map(lambda x: x['actions'].get(GOLDMAN_NAME, 0), history_nouns))
gs_price = list(map(lambda x: x['prices'][GOLDMAN_NAME], history_nouns))
jpm_value = list(map(lambda x: x['actions'].get(MORGAN_NAME, 0), history_nouns))
jpm_price = list(map(lambda x: x['prices'][MORGAN_NAME], history_nouns))
apc_value = list(map(lambda x: x['actions'].get(ANDARKO_NAME, 0), history_nouns))
apc_price = list(map(lambda x: x['prices'][ANDARKO_NAME], history_nouns))

make_plot_value_price(model_x, amzn_value, amzn_price, "resources/plots/nouns/" + AMAZON_NAME)
make_plot_value_price(model_x, adobe_value, adobe_price, "resources/plots/nouns/" + ADOBE_NAME)
make_plot_value_price(model_x, gs_value, gs_price, "resources/plots/nouns/" + GOLDMAN_NAME)
make_plot_value_price(model_x, jpm_value, jpm_price, "resources/plots/nouns/" + MORGAN_NAME)
make_plot_value_price(model_x, apc_value, apc_price, "resources/plots/nouns/" + ANDARKO_NAME)

a = {}

for x in history_nouns:
    a[x['date'].date()] = x

history = a.values()

model_x = list(map(lambda x: x['date'], history))

amzn_value = list(map(lambda x: x['actions'].get(AMAZON_NAME, 0), history))
amzn_price = list(map(lambda x: x['prices'][AMAZON_NAME], history))
adobe_value = list(map(lambda x: x['actions'].get(ADOBE_NAME, 0), history))
adobe_price = list(map(lambda x: x['prices'][ADOBE_NAME], history))
gs_value = list(map(lambda x: x['actions'].get(GOLDMAN_NAME, 0), history))
gs_price = list(map(lambda x: x['prices'][GOLDMAN_NAME], history))
jpm_value = list(map(lambda x: x['actions'].get(MORGAN_NAME, 0), history))
jpm_price = list(map(lambda x: x['prices'][MORGAN_NAME], history))
apc_value = list(map(lambda x: x['actions'].get(ANDARKO_NAME, 0), history))
apc_price = list(map(lambda x: x['prices'][ANDARKO_NAME], history))

price = []

for a1, a2, a3, a4, a5 in zip(amzn_price, adobe_price, gs_price, jpm_price, apc_price):
    price.append(a1 + a2 + a3 + a4 + a5)

trend = list(map(lambda x: x['trend'] - 2, history))

make_plot_trend_price(model_x, price, trend, "resources/plots/nouns/trends")
