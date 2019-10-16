import config
from config import DBNAMES
from dataBase.mango_db import select
from plots.plots import make_plot_histogram
from vectorize import get_all_words, get_all_named_entities


def get_stats(tag, type):
    query = select(type, {'tag': {'$in': [tag]}})
    all, filtered = get_all_words(query)

    print(type, tag)
    length = len(all)
    # print(length)
    suma = sum(all.values())
    print(sorted(all.items(), key=lambda kv: -kv[1])[:20])
    a = list(map(lambda x: x/suma, all.values()))
    a = sorted(a)
    a.reverse()
    # print(a[:20])
    suma = sum(filtered.values())
    make_plot_histogram(range(len(filtered)), filtered.values(), list(map(lambda x: x/suma, filtered.values())), "resources/plots/nouns/vector-"+ tag)
    print(suma)


def get_stats_names_entities(tag, type):
    query = select(type, {'tag': {'$in': [tag]}})
    all, filtered = get_all_named_entities(query)

    print(type, tag)
    l = []
    fl = []
    sl = []
    ss = []
    for k in sorted(all.keys()):
        length = len(all[k])
        suma = sum(all[k].values())
        s = sorted(all[k].items(), key=lambda kv: -kv[1])[:20]
        a = list(map(lambda x: x, all[k].values()))
        a = sorted(a)
        a.reverse()
        l.append(length)
        fl.append(len(filtered[k]))
        ss.append(suma)
        sl.append("" + s[0][0] + " (" + str(a[0]) + ")")
        make_plot_histogram(range(len(filtered[k])), filtered[k].values(), list(map(lambda x: x / suma, filtered[k].values())),
                            "resources/plots/namesentities/vector-" + k)

    print(l)
    print(fl)
    print(ss)
    print(sl)


get_stats_names_entities(config.TECH_NAME, DBNAMES.NAMES_ENTITIES)
# get_stats(config.AMAZON_NAME, DBNAMES.BAGS_OF_WORDS)
# get_stats(config.ANDARKO_NAME, DBNAMES.BAGS_OF_WORDS)
# get_stats(config.GOLDMAN_NAME, DBNAMES.BAGS_OF_WORDS)
# get_stats(config.MORGAN_NAME, DBNAMES.BAGS_OF_WORDS)
# get_stats(config.TECH_NAME, DBNAMES.BAGS_OF_WORDS)
# get_stats(config.BUSINNES_NAME, DBNAMES.BAGS_OF_WORDS)
# get_stats(config.PETROLEUM_NAME, DBNAMES.BAGS_OF_WORDS)
# get_stats(config.STOCK_NAME, DBNAMES.BAGS_OF_WORDS)