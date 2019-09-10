from newsarticlemodule.main import get_all_articles_from_dict
import config

date_from, date_to = 26, 30


def get_articles(dict, name):
    for i in range(date_from, date_to):
        get_all_articles_from_dict('2019-08-' + str(i), '2019-08-' + str(i), dict, name)
    print(name)


get_articles(config.petroleum_dict, config.PETROLEUM_NAME)
get_articles(config.stock_dict, config.STOCK_NAME)
get_articles(config.businnes_dict, config.BUSINNES_NAME)
get_articles(config.technology_dict, config.TECH_NAME)

get_articles(config.amazon_dict, config.AMAZON_NAME)
get_articles(config.adobe_dict, config.ADOBE_NAME)
get_articles(config.goldman_dict, config.GOLDMAN_NAME)
get_articles(config.morgan_dict, config.MORGAN_NAME)
get_articles(config.andarko_dict, config.ANDARKO_NAME)

