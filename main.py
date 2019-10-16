from simulator.simulator import simulate
import pickle
from dataBase import select_by_tag
from config import DBNAMES

x_test = []

# with open("resources/data/x_test_nouns_AMZN.txt", "rb") as fp:
#     new_in = list(pickle.load(fp))
#     for e in new_in:
#         e['sign'] = 'AMZN'
#     x_test = x_test + new_in
#
# with open("resources/data/x_test_nouns_ADBE.txt", "rb") as fp:
#     new_in = list(pickle.load(fp))
#     for e in new_in:
#         e['sign'] = 'ADBE'
#     x_test = x_test + new_in
#
# with open("resources/data/x_test_nouns_APC.txt", "rb") as fp:
#     new_in = list(pickle.load(fp))
#     for e in new_in:
#         e['sign'] = 'APC'
#     x_test = x_test + new_in
#
# with open("resources/data/x_test_nouns_GS.txt", "rb") as fp:
#     new_in = list(pickle.load(fp))
#     for e in new_in:
#         e['sign'] = 'GS'
#     x_test = x_test + new_in
#
# with open("resources/data/x_test_nouns_JPM.txt", "rb") as fp:
#     new_in = list(pickle.load(fp))
#     for e in new_in:
#         e['sign'] = 'JPM'
#     x_test = x_test + new_in
#
# simulate(x_test, "", "nouns")

print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "ADBE").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "APC").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "GS").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "JPM").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "Tech").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "STOCK").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "BISS").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "PETR").count())