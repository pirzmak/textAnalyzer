from newsarticlemodule.main import get_all_articles_from_dict
from dataBase.mango_db import insert_many, how_many_records, select, select_by_tag, select_all, clear
from stockmarketmodule.getstockmarketapi import get_stock_after_before_actual_price
import config
from config import DBNAMES
from datetime import datetime
from learningmodule import learn, save_data_to_file

#
# for i in range(26, 30):
#     get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), config.petroleum_dict, config.PETROLEUM_NAME)
# print(config.PETROLEUM_NAME)
# for i in range(26, 30):
#     get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), config.stock_dict, config.STOCK_NAME)
# print(config.STOCK_NAME)
# for i in range(26, 30):
#     get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), config.businnes_dict, config.BUSINNES_NAME)
# print(config.BUSINNES_NAME)
# for i in range(26, 30):
#     get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), config.technology_dict, config.TECH_NAME)
# print(config.TECH_NAME)
for i in range(26, 30):
    get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), config.amazon_dict, config.AMAZON_NAME)
print(config.AMAZON_NAME)
# for i in range(19, 25):
#     get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), config.adobe_dict, config.ADOBE_NAME)
# print(config.ADOBE_NAME)
# for i in range(19, 25):
#     get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), config.goldman_dict, config.GOLDMAN_NAME)
# print(config.GOLDMAN_NAME)
# for i in range(19, 25):
#     get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), config.morgan_dict, config.MORGAN_NAME)
# print(config.MORGAN_NAME)
# for i in range(19, 25):
#     get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), config.andarko_dict, config.ANDARKO_NAME)
# print(config.ANDARKO_NAME)

# learn(DBNAMES.BAGS_OF_WORDS, config.AMAZON_NAME, [config.AMAZON_NAME, config.STOCK_NAME])

# for i in select_all(DBNAMES.BAGS_OF_WORDS):
#     print(i)


print(how_many_records(DBNAMES.BAGS_OF_WORDS))

