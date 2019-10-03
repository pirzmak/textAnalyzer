from simulator.simulator import simulate
import pickle

x_test = []

with open("resources/data/x_test_nouns_AMZN.txt", "rb") as fp:
    new_in = list(pickle.load(fp))
    for e in new_in:
        e['sign'] = 'AMZN'
    x_test = x_test + new_in
#
# with open("resources/data/x_test_bags_of_words_ADBE.txt", "rb") as fp:
#     new_in = list(pickle.load(fp))
#     for e in new_in:
#         e['sign'] = 'ADBE'
#     x_test = x_test + new_in
#
#
# with open("resources/data/x_test_bags_of_words_APC.txt", "rb") as fp:
#     new_in = list(pickle.load(fp))
#     for e in new_in:
#         e['sign'] = 'APC'
#     x_test = x_test + new_in
#
# with open("resources/data/x_test_bags_of_words_GS.txt", "rb") as fp:
#     new_in = list(pickle.load(fp))
#     for e in new_in:
#         e['sign'] = 'GS'
#     x_test = x_test + new_in
#
#
# with open("resources/data/x_test_bags_of_words_JPM.txt", "rb") as fp:
#     new_in = list(pickle.load(fp))
#     for e in new_in:
#         e['sign'] = 'JPM'
#     x_test = x_test + new_in

simulate(x_test, "amzn", "nouns")

