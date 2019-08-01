from newsArticleModule.main import get_all_articles_from_dict
from dataBase.mango_db import insert_many, how_many_records, select, select_by_tag, select_all, clear
from stockMarketModule.getstockmarketapi import get_stock_after_before_actual_price
import config
from config import DBNAMES
from datetime import datetime
from learningmodule import learn


for i in range(22, 29):
    get_all_articles_from_dict('2019-07-' + str(i), '2019-07-' + str(i), config.morgan_dict, config.MORGAN_NAME)


# learn(DBNAMES.BAGS_OF_WORDS, config.AMAZON_NAME, [config.AMAZON_NAME, config.STOCK_NAME])

# for i in select_all(DBNAMES.BAGS_OF_WORDS):
#     print(i)




