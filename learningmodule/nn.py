from vectorize import vectorize
from vectorize import get_all_words
from pricetrend import get_price_trend
from dataBase.mango_db import select_all
import math
import numpy as np
import tensorflow as tf
import config
from random import shuffle

BAGS_OF_WORDS = config.config['DB_collections_name_bags_of_words']
NAMES_ENTITIES = config.config['DB_collections_name_names_entities']
NOUNS = config.config['DB_collections_name_nouns']


def preprocesssing_data(all):
    inputs, outputs = [], []

    for x in select_all(BAGS_OF_WORDS):
        if "" != x['before_price'] and "" != x['actual_price'] and "" != x['after_price']:
            if not math.isnan(x['before_price']) and not math.isnan(x['actual_price']) and not math.isnan(
                    x['after_price']) \
                    and x['before_price'] > 0 and x['actual_price'] > 0 and x['after_price'] > 0:
                inputs.append(vectorize(x['text_vector'], all))
                outputs.append(get_price_trend(x['before_price'], x['actual_price'], x['after_price']))

    li = list(zip(inputs, outputs))

    shuffle(li)

    inputs, outputs = zip(*li)
    inputs, outputs = np.asarray(inputs), np.asarray(outputs)

    for x in inputs:
        x /= np.max(x, axis=0)

    return inputs, outputs


def learn(divide=0.8):
    all = get_all_words(select_all(BAGS_OF_WORDS))
    inputs, outputs = preprocesssing_data(all)

    to = len(inputs) * divide
    x_train, x_test = inputs[0:to], inputs[to: len(inputs)]
    y_train, y_test = outputs[0:to], outputs[to: len(outputs)]

    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(21843, )),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(5, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=1)

    res = []

    model.evaluate(x_test, y_test)
    cls = model(x_test)

    for i, j in zip(cls, y_test):
        print(np.argmax(i.numpy()), j)
