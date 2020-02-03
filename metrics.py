from metrics.metrics import get_one_to_one_metric, get_best_two_metric, get_trend_metric, get_loss_acc_time
import config
from config import DBNAMES
from plots.plots import make_plot_loss_acc_time, make_histogram

model = 'one_8192_relu'


def get_one_metrics(type, tag):
    g1, b1 = get_one_to_one_metric(type, tag, model)
    print(g1,b1)
    g2, b2 = get_best_two_metric(type, tag)
    print(g2,b2)
    gt, bt = get_trend_metric(type, tag)
    print(gt,bt)

    return g1/(g1+b1), b1/(g1+b1), g2/(g2+b2), b2/(g2+b2), gt/(gt+bt), bt/(gt+bt)


def get_metrics(type):
    one, two, trends = 0, 0, 0
    one_b, two_b, trends_b = 0, 0, 0
    print("------AMZN-------")
    g1, b1, g2, b2, gt, bt = get_one_metrics(type, config.AMAZON_NAME)
    one, two, trends = one + g1, two + g2, trends + gt
    one_b, two_b, trends_b = one_b + b1, two_b + b2, trends_b + bt
    print("------ADB-------")
    g1, b1, g2, b2, gt, bt = get_one_metrics(type, config.ADOBE_NAME)
    one, two, trends = one + g1, two + g2, trends + gt
    one_b, two_b, trends_b = one_b + b1, two_b + b2, trends_b + bt
    print("------MRG-------")
    g1, b1, g2, b2, gt, bt = get_one_metrics(type, config.MORGAN_NAME)
    one, two, trends = one + g1, two + g2, trends + gt
    one_b, two_b, trends_b = one_b + b1, two_b + b2, trends_b + bt
    print("------GS-------")
    g1, b1, g2, b2, gt, bt = get_one_metrics(type, config.GOLDMAN_NAME)
    one, two, trends = one + g1, two + g2, trends + gt
    one_b, two_b, trends_b = one_b + b1, two_b + b2, trends_b + bt

    one, two, trends = one/5, two/5, trends/5
    one_b, two_b, trends_b = one_b/5, two_b/5, trends_b/5

    print("------ALL-------")
    print(one, one_b)
    print(two, two_b)
    print(trends, trends_b)


def loss_and_acc_and_time(type, models, model, tag):
    all_loss, all_acc, all_time = [], [], []
    x = []

    for m in models:
        l, a, t = get_loss_acc_time(type, tag, m)
        all_loss.append(l)
        all_acc.append(a)
        all_time.append(t)
        x.append(m)

    make_plot_loss_acc_time(x, all_loss, all_acc, all_time,
                            "resources/plots/metrics/" + type + "_" + tag + "_" + model + "_loss_acc_time")


get_metrics(DBNAMES.BAGS_OF_WORDS)

# model_one = ['one_1024_elu', 'one_1024_relu', 'one_1024_hard_sigmoid', 'one_1024_sigmoidalna']
# model_two = ['liniowa', 'relu', 'progowa', 'sigmoidalna']
# model_four = ['four_256_relu', 'four_512_relu', 'four_1024_relu', 'four_2048_relu', 'four_4096_relu', 'four_8192_relu']
#
# loss_and_acc_and_time(DBNAMES.BAGS_OF_WORDS, model_one, "one", config.ADOBE_NAME)
# loss_and_acc_and_time(DBNAMES.NAMES_ENTITIES, model_two, "two", config.AMAZON_NAME)
# loss_and_acc_and_time(DBNAMES.NAMES_ENTITIES, model_four, "four", config.AMAZON_NAME)


make_histogram(["Statystyczne 1", "Statystyczne 2", "Sentymentalne 1", "Sentymentalne 2", "Moje"], [58.2, 57.73, 70.59,
                                                                                                    78.75, 92.24],
               "resources/plots/metrics/other")
