from matplotlib import pyplot as plt
from matplotlib import dates
from pandas.plotting import register_matplotlib_converters
import numpy as np


register_matplotlib_converters()


def make_plot_value_price(x, value, price, path):
    fig, ax1 = plt.subplots()
    d = dates.date2num(x)

    color = 'tab:blue'
    ax1.set_xlabel('Czas')
    ax1.set_ylabel('Wartość', color=color)  # we already handled the x-label with ax1
    ax1.bar(d, value, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Cena', color=color)
    ax2.plot_date(d, price, linestyle='solid', marker='None', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)


def make_models_plot(x, no_model, bags_of_words, names_entities, nouns, path):
    fig, ax1 = plt.subplots()

    d = dates.date2num(x)

    plt.yticks(np.arange(98000, 120000, 1000.0))

    color = 'black'
    ax1.set_xlabel('Czas')
    ax1.set_ylabel('Wartość', color=color)
    color = 'white'
    ax1.plot_date(d, [108000] * len(no_model), linestyle='solid', marker='None', color=color, label='')
    color = 'tab:red'
    ax1.plot_date(d, [x if x < 103000 else x - 3000 for x in no_model], linestyle='solid', marker='None', color=color, label='Bez modelu')
    color = 'tab:blue'
    ax1.plot_date(d, names_entities, linestyle='solid', marker='None', color=color, label='Metoda worka słów')
    color = 'yellow'
    ax1.plot_date(d, names_entities, linestyle='solid', marker='None', color=color, label='Metoda fraz rzeczownikowych')
    color = 'tab:green'
    ax1.plot_date(d, names_entities, linestyle='solid', marker='None', color=color, label='Metoda nazwanych encji')

    ax1.legend()

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)


def make_plot_trend_price(x, price, trend, path):
    fig, ax1 = plt.subplots()

    d = dates.date2num(x)

    color = 'tab:red'
    ax1.set_xlabel('Czas')
    ax1.set_ylabel('Cena', color=color)
    ax1.plot_date(d, price, linestyle='solid', marker='None', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Trend', color=color)  # we already handled the x-label with ax1
    ax2.stem(d, trend)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)

def make_histogram(x, y, path):
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_ylabel('Wartość')  # we already handled the x-label with ax1
    ax1.bar(x, y, color=color)
    ax1.tick_params(axis='y')

    w = 0.0
    r = np.arange(len(x))

    for i, v in enumerate(x):
        ax1.text(i - .1,
                 y[i],
                 round(y[i] * 1000) / 1000,
                 fontsize=12)

    ax1.legend()

    plt.xlabel('Badanie', fontweight='bold')
    plt.xticks([r + w for r in range(len(x))], x)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)

def make_plot_loss_acc_time(x, loss, acc, time, path):
    fig, ax1 = plt.subplots()

    w = 1
    r = np.arange(len(x))
    r1 = [x - w for x in r]
    r2 = [x + w for x in r]

    ax1.set_ylabel('Wartość[%]')
    ax1.bar(r1, acc, width=w, color='r')
    ax1.bar(r2, loss, width=w, color='g')

    for i, v in enumerate(x):
        ax1.text(i - .3,
                 loss[i],
                 round(loss[i] * 1000) / 1000,
                 fontsize=12)

    ax1.legend()

    plt.xlabel('Typ', fontweight='bold', fontsize=40)
    plt.xticks([r + w for r in range(len(x))], x)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Time[s]')
    ax2.plot(x, time, linestyle='solid', marker='None', color='b')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)


def make_plot_loss(x, loss, path):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_ylabel('Loss', color=color)  # we already handled the x-label with ax1
    ax1.plot(x, loss, linestyle='solid', marker='None', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)


def make_plot_loss_mul(x, loss_one, loss_two, loss_four, path):
    fig, ax1 = plt.subplots()

    color = 'black'
    ax1.set_ylabel('Loss', color=color)
    color = 'tab:red'
    ax1.plot_date(x, loss_one, linestyle='solid', marker='None', color=color, label='Jedna warstwa ukryta')
    color = 'tab:blue'
    ax1.plot_date(x, loss_two, linestyle='solid', marker='None', color=color, label='Dwie warstwy ukryte')
    color = 'yellow'
    ax1.plot_date(x, loss_four, linestyle='solid', marker='None', color=color, label='Cztery warstwy ukryte')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)


def make_plot_time(x, time, path):
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_ylabel('Czas[s]', color=color)  # we already handled the x-label with ax1
    ax1.plot(x, time, linestyle='solid', marker='None', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)


def make_plot_acc_mul(x, acc_one, acc_two, acc_four, path):
    fig, ax1 = plt.subplots()

    color = 'black'
    ax1.set_ylabel('Loss', color=color)
    color = 'tab:red'
    ax1.plot_date(x, loss_one, linestyle='solid', marker='None', color=color, label='Jedna warstwa ukryta')
    color = 'tab:blue'
    ax1.plot_date(x, loss_two, linestyle='solid', marker='None', color=color, label='Dwie warstwy ukryte')
    color = 'yellow'
    ax1.plot_date(x, loss_four, linestyle='solid', marker='None', color=color, label='Cztery warstwy ukryte')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)


def make_plot_acc(x, acc, path):
    fig, ax1 = plt.subplots()

    color = 'tab:green'
    ax1.set_ylabel('Acc', color=color)  # we already handled the x-label with ax1
    ax1.plot(x, acc, linestyle='solid', marker='None', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)