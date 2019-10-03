import config
from config import DBNAMES
from learningmodule import learn

learn(DBNAMES.NAMES_ENTITIES, config.AMAZON_NAME)
# learn(DBNAMES.BAGS_OF_WORDS, config.ADOBE_NAME)
# learn(DBNAMES.BAGS_OF_WORDS, config.GOLDMAN_NAME)
# learn(DBNAMES.BAGS_OF_WORDS, config.MORGAN_NAME)
# learn(DBNAMES.BAGS_OF_WORDS, config.ANDARKO_NAME)