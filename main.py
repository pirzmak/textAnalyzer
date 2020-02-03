from simulator.simulator import simulate2
import pickle
from dataBase import select_by_tag, select_all, how_many_records
from config import DBNAMES
import pandas as pd
from datetime import datetime

from stockmarketmodule import get_stock_prices

x_test = []

with open("resources/data/x_test_names_entities_JPM.txt", "rb") as fp:
    new_in = [{
        "data": eval(el["data"]),
        "date": datetime.strptime(el["date"], '%Y-%m-%d %H:%M:%S'),
        "sign": 'JPM'} for ix, el in pd.read_csv(fp, nrows=3000).iterrows()]
    x_test = x_test + new_in

with open("resources/data/x_test_names_entities_JPM.txt", "rb") as fp:
    new_in = [{
        "data": eval(el["data"]),
        "date": datetime.strptime(el["date"], '%Y-%m-%d %H:%M:%S'),
        "sign": 'JPM'} for ix, el in pd.read_csv(fp, nrows=3000, skiprows=[i for i in range(1,3000)]).iterrows()]
    x_test = x_test + new_in

with open("resources/data/x_test_names_entities_JPM.txt", "rb") as fp:
    new_in = [{
        "data": eval(el["data"]),
        "date": datetime.strptime(el["date"], '%Y-%m-%d %H:%M:%S'),
        "sign": 'JPM'} for ix, el in pd.read_csv(fp, skiprows=[i for i in range(1,6000)]).iterrows()]
    x_test = x_test + new_in

with open("resources/data/x_test_nouns_ADBE.txt", "rb") as fp:
    new_in = [{
        "data": eval(el["data"]),
        "date": datetime.strptime(el["date"], '%Y-%m-%d %H:%M:%S'),
        "sign": 'ADBE'} for ix, el in pd.read_csv(fp).iterrows()]
    x_test = x_test + new_in

with open("resources/data/x_test_nouns_GS.txt", "rb") as fp:
    new_in = [{
        "data": eval(el["data"]),
        "date": datetime.strptime(el["date"], '%Y-%m-%d %H:%M:%S'),
        "sign": 'GS'} for ix, el in pd.read_csv(fp).iterrows()]
    x_test = x_test + new_in

with open("resources/data/x_test_nouns_JPM.txt", "rb") as fp:
    new_in = [{
        "data": eval(el["data"]),
        "date": datetime.strptime(el["date"], '%Y-%m-%d %H:%M:%S'),
        "sign": 'JPM'} for ix, el in pd.read_csv(fp).iterrows()]
    x_test = x_test + new_in


print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "ADBE").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "APC").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "GS").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "JPM").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "Tech").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "STOCK").count())
print(select_by_tag(DBNAMES.BAGS_OF_WORDS, "BISS").count())
