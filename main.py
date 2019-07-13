from newsArticleModule.main import get_all_articles_from_dict
from dataBase.mango_db import insert_many, how_many_records, select, select_by_tag, select_all
from stockMarketModule.main import save_prices_to_db
import config

BAGS_OF_WORDS = config.config['DB_collections_name_bags_of_words']
NAMES_ENTITIES = config.config['DB_collections_name_names_entities']
NOUNS = config.config['DB_collections_name_nouns']

# dictionares.amazon_dict.extend(dictionares.technology_dict)
# 06.03 - 06.30 - tech
# get_all_articles_from_dict('2019-06-09', '2019-06-09', dictionares.technology_dict, 'Tech')
# do 18
# for i in range(21, 25):
#     get_all_articles_from_dict('2019-06-' + str(i), '2019-06-' + str(i), config.adobe_dict, config.ADOBE_NAME)

# get_all_articles_from_dict('2019-06-22', '2019-06-22', config.businnes_dict, config.BUSINNES_NAME)
#how_many_records(NOUNS)

# save_prices_to_db(BAGS_OF_WORDS, "AMZN", [{'tag': 'Tech'}, {'tag': 'AMZN'}])

