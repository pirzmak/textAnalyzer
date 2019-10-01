import pickle

from matplotlib import pyplot as plt
from matplotlib import dates
from pandas.plotting import register_matplotlib_converters
import pandas as pd

from config import *


def get_money_value(x):
    actions = x['actions']
    prices = x['prices']
    money = x['money']
    for name, value in actions.items():
        money = money + value * prices[name]
    return money


def make_plot_value_price(x, value, price, name):
    fig, ax1 = plt.subplots()

    d = dates.date2num(x)

    color = 'tab:blue'
    ax1.set_xlabel('time')
    ax1.set_ylabel('value', color=color)  # we already handled the x-label with ax1
    ax1.bar(d, value, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('price', color=color)
    ax2.plot_date(d, price, linestyle='solid', marker='None', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(name + '.png', bbox_inches='tight', dpi=300)


def make_models_plot(x, no_model, model, name):
    fig, ax1 = plt.subplots()

    d = dates.date2num(x)

    color = 'tab:red'
    ax1.set_xlabel('time')
    ax1.set_ylabel('price', color=color)
    ax1.plot_date(d, model, linestyle='solid', marker='None', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    color = 'tab:blue'
    ax1.plot_date(d, no_model, linestyle='solid', marker='None', color=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(name + '.png', bbox_inches='tight', dpi=300)


def make_plot_trend_price(x, price, trend):
    fig, ax1 = plt.subplots()

    d = dates.date2num(x)

    color = 'tab:red'
    ax1.set_xlabel('time')
    ax1.set_ylabel('price', color=color)
    ax1.plot_date(d, price, linestyle='solid', marker='None', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('trend', color=color)  # we already handled the x-label with ax1
    ax2.stem(d, trend)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig('trend2.png', bbox_inches='tight', dpi=300)


with open("resources/results_no_model.model", "rb") as fp:
    history = pickle.load(fp)

model_x = list(map(lambda x: x['date'], history))
no_model_y = list(map(lambda x: get_money_value(x), history))

with open("resources/results_model.model", "rb") as fp:
    history = pickle.load(fp)


model_y = list(map(lambda x: get_money_value(x), history))

register_matplotlib_converters()

make_models_plot(model_x, no_model_y, model_y, "model_and_no_model")

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

make_plot_value_price(model_x, amzn_value, amzn_price, AMAZON_NAME)
make_plot_value_price(model_x, adobe_value, adobe_price, ADOBE_NAME)
make_plot_value_price(model_x, gs_value, gs_price, GOLDMAN_NAME)
make_plot_value_price(model_x, jpm_value, jpm_price, MORGAN_NAME)
make_plot_value_price(model_x, apc_value, apc_price, ANDARKO_NAME)
#
# price = []
#
# for a1, a2, a3, a4, a5 in zip(amzn_price, adobe_price, gs_price, jpm_price, apc_price):
#     price.append(a1 + a2 + a3 + a4 + a5)
#
# trend = list(map(lambda x: x['trend'] - 2, model_y))
#
# make_plot_trend_price(model_x, price, trend)
