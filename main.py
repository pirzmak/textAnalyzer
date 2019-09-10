from newsarticlemodule.main import get_all_articles_from_dict
from dataBase.mango_db import insert_many, how_many_records, select, select_by_tag, select_all, clear
from simulator.simulator import simulate_single_article
from stockmarketmodule.getstockmarketapi import get_stock_after_before_actual_price
import config
from config import DBNAMES
from datetime import datetime
from learningmodule import learn, save_data_to_file, normalize_data
import pickle
import numpy as np

# learn(DBNAMES.BAGS_OF_WORDS, config.AMAZON_NAME, [config.AMAZON_NAME, config.STOCK_NAME])


with open("resources/data/inputs_bags_of_words_AMZN.txt", "rb") as fp:
    inputs = pickle.load(fp)

input_data = normalize_data([el["data"] for el in inputs])
input_date = [el["date"] for el in inputs]

for x,y in zip(input_data,input_date):
    simulate_single_article(x, y, "AMZN")
