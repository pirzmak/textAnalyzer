from vectorize import vectorize
from vectorize import get_all_words
from pricetrend import get_price_trend
from stockmarketmodule import get_price
from dataBase.mango_db import select
import math
import numpy as np
import tensorflow as tf
from random import shuffle
import pickle


def preprocesssing_data(type, sign, tags, all):
    inputs, outputs = [], []

    for x in select(type, {'tag': {'$in': tags}}):
        prices = get_price(sign, x['date'])
        if not math.isnan(prices['actual']):
            inputs.append(vectorize(x['text_vector'], all))
            outputs.append(get_price_trend(prices['before'], prices['actual'], prices['after']))

    li = list(zip(inputs, outputs))

    shuffle(li)

    inputs, outputs = zip(*li)
    inputs, outputs = np.asarray(inputs), np.asarray(outputs)

    for x in inputs:
        x /= np.max(x, axis=0)

    return inputs, outputs


def save_data_to_file(type, sign, tags):
    all = get_all_words(select(type, {'tag': {'$in': tags}}))
    inputs, outputs = preprocesssing_data(type, sign, tags, all)

    with open("resources/data/inputs_" + sign + ".txt", "wb") as fp:
        pickle.dump(inputs, fp)

    with open("resources/data/outputs_" + sign + ".txt", "wb") as fp:
        pickle.dump(outputs, fp)


def learn(type, sign, tags, divide=0.8):
    all = get_all_words(select(type, {'tag': {'$in': tags}}))

    with open("resources/data/inputs_" + sign + ".txt", "rb") as fp:
        inputs = pickle.load(fp)

    with open("resources/data/outputs_" + sign + ".txt", "rb") as fp:
        outputs = pickle.load(fp)

    to = int(len(inputs) * divide)
    x_train, x_test = inputs[0:to], inputs[to: len(inputs)]
    y_train, y_test = outputs[0:to], outputs[to: len(outputs)]

    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(len(all), )),
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
        print(i.numpy(), j)
