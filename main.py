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

# for i in range(20, 31):
#     get_all_articles_from_dict('2019-06-' + str(i), '2019-06-' + str(i), dictionares.amazon_dict, 'AMZN')
#
# how_many_records(BAGS_OF_WORDS)

#save_prices_to_db(BAGS_OF_WORDS, "AMZN", [{'tag': 'Tech'}, {'tag': 'AMZN'}])

for x in select_all(BAGS_OF_WORDS):
    print(x['before_price'], x['actual_price'], x['after_price'])