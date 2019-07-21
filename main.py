from newsArticleModule.main import get_all_articles_from_dict
from dataBase.mango_db import insert_many, how_many_records, select, select_by_tag, select_all, clear
from stockMarketModule.getstockmarketapi import get_stock_after_before_actual_price
import config
from datetime import datetime
from learningmodule import learn

BAGS_OF_WORDS = config.config['DB_collections_name_bags_of_words']
NAMES_ENTITIES = config.config['DB_collections_name_names_entities']
NOUNS = config.config['DB_collections_name_nouns']

# for i in range(15, 21):
#     get_all_articles_from_dict('2019-07-' + str(i), '2019-07-' + str(i), config.stock_dict, config.STOCK_NAME)

# get_all_articles_from_dict('2019-06-22', '2019-06-22', config.businnes_dict, config.BUSINNES_NAME)
how_many_records(BAGS_OF_WORDS)
# get_stock_after_before_actual_price(config.AMAZON_NAME, datetime(2019, 7, 15))

# learn(BAGS_OF_WORDS, config.AMAZON_NAME, [{'tag': config.AMAZON_NAME}])


