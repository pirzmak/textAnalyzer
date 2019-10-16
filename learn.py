import config
from config import DBNAMES
from learningmodule import learn

learn(DBNAMES.NAMES_ENTITIES, config.AMAZON_NAME)
learn(DBNAMES.NAMES_ENTITIES, config.ADOBE_NAME)
learn(DBNAMES.NAMES_ENTITIES, config.GOLDMAN_NAME)
learn(DBNAMES.NAMES_ENTITIES, config.MORGAN_NAME)
learn(DBNAMES.NAMES_ENTITIES, config.ANDARKO_NAME)