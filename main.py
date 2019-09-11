from simulator.simulator import simulate
import pickle

inputs = []

with open("resources/data/inputs_bags_of_words_AMZN.txt", "rb") as fp:
    new_in = pickle.load(fp)
    for e in new_in:
        e['sign'] = 'AMZN'
    inputs = inputs + new_in

# with open("resources/data/inputs_bags_of_words_ADBE.txt", "rb") as fp:
#     new_in = pickle.load(fp)
#     for e in new_in:
#         e['sign'] = 'ADBE'
#     inputs = inputs + new_in
#
#
# with open("resources/data/inputs_bags_of_words_APC.txt", "rb") as fp:
#     new_in = pickle.load(fp)
#     for e in new_in:
#         e['sign'] = 'APC'
#     inputs = inputs + new_in
#
# with open("resources/data/inputs_bags_of_words_GS.txt", "rb") as fp:
#     new_in = pickle.load(fp)
#     for e in new_in:
#         e['sign'] = 'GS'
#     inputs = inputs + new_in
#
#
# with open("resources/data/inputs_bags_of_words_JPM.txt", "rb") as fp:
#     new_in = pickle.load(fp)
#     for e in new_in:
#         e['sign'] = 'JPM'
#     inputs = inputs + new_in


simulate(inputs[:500])
