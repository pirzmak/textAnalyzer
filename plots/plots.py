from matplotlib import pyplot as plt
from matplotlib import dates
from pandas.plotting import register_matplotlib_converters

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

    color = 'black'
    ax1.set_xlabel('Czas')
    ax1.set_ylabel('Wartość', color=color)
    color = 'tab:red'
    ax1.plot_date(d, no_model, linestyle='solid', marker='None', color=color, label='Bez modelu')
    color = 'tab:blue'
    ax1.plot_date(d, bags_of_words, linestyle='solid', marker='None', color=color, label='Worek słów')
    color = 'tab:green'
    ax1.plot_date(d, names_entities, linestyle='solid', marker='None', color=color, label='Nazwane encje')
    color = 'yellow'
    ax1.plot_date(d, nouns, linestyle='solid', marker='None', color=color, label='Frazy rzeczownikowe')

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


def make_plot_histogram(x, value, percents, path):
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_ylabel('Wartość', color=color)  # we already handled the x-label with ax1
    ax1.bar(x, value, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Procent', color=color)
    ax2.plot(x, percents, linestyle='solid', marker='None', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 7)
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)