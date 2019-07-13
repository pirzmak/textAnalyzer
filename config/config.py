import json
import os, ssl

with open("config/config.conf") as json_file:
    config = json.load(json_file)

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context


class TRENDS:
    BIG_DECREASE = 0
    DECREASE = 1
    NO_CHANGE = 2
    INCREASE = 3
    BIG_INCREASE = 4
