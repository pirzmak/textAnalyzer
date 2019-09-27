import pickle

from matplotlib import pyplot as plt
from matplotlib import dates
from pandas.plotting import register_matplotlib_converters

def getPlotData(x):
    actions = x['actions']
    prices = x['prices']
    money = x['money']
    for name, value in actions.items():
        money = money + value * prices[name]
    return money


with open("resources/history.txt", "rb") as fp:
    history = pickle.load(fp)

x = list(map(lambda x: x['date'], history))
y = list(map(lambda x: getPlotData(x), history))

register_matplotlib_converters()
dates = dates.date2num(x)

with plt.style.context('fivethirtyeight'):
    plt.plot_date(dates, y, linestyle='solid', marker='None')
    plt.show()
