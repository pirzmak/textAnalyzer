from matplotlib import pyplot as plt
from matplotlib import dates
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


def make_plot_value_price(x, value, price, path):
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
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)


def make_models_plot(x, no_model, model, path):
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
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)


def make_plot_trend_price(x, price, trend, path):
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
    plt.savefig(path + '.png', bbox_inches='tight', dpi=300)