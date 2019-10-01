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
from sklearn.preprocessing import normalize
import pymongo


def preprocesssing_data(type, sign, tags, all):
    inputs, outputs = [], []

    for x in select(type, {'tag': {'$in': tags}}):
        try:
            prices = get_price(sign, x['date'])
            print(prices)
            if not math.isnan(prices['actual']):
                inputs.append({"data": vectorize(x['text_vector'], all), "date": x['date']})
                outputs.append(get_price_trend(prices['before'], prices['actual'], prices['after']))
        except pymongo.errors.CursorNotFound:
            print("cursor error")

    return inputs, outputs


def save_data_to_file(type, sign, tags, divide=0.8):
    all = get_all_words(select(type, {'tag': {'$in': tags}}))
    inputs, outputs = preprocesssing_data(type, sign, tags, all)

    li = list(zip(inputs, outputs))

    shuffle(li)

    inputs, outputs = zip(*li)

    to = int(len(inputs) * divide)
    x_train, x_test = inputs[0:to], inputs[to: len(inputs)]
    y_train, y_test = outputs[0:to], outputs[to: len(outputs)]

    with open("resources/data/x_train_" + type + "_" + sign + ".txt", "wb") as fp:
        pickle.dump(x_train, fp)

    with open("resources/data/x_test_" + type + "_" + sign + ".txt", "wb") as fp:
        pickle.dump(x_test, fp)

    with open("resources/data/y_train_" + type + "_" + sign + ".txt", "wb") as fp:
        pickle.dump(y_train, fp)

    with open("resources/data/y_test_" + type + "_" + sign + ".txt", "wb") as fp:
        pickle.dump(y_test, fp)

    with open("resources/data/all_" + type + "_" + sign + ".txt", "wb") as fp:
        pickle.dump(all, fp)


def normalize_data(inputs):
    ret = []
    for x in np.asarray(inputs):
        ret.append(normalize(np.array(x)[:, np.newaxis], axis=0).ravel())

    return ret


def learn(type, sign):
    with open("resources/data/all_" + type + "_" + sign + ".txt", "rb") as fp:
        all = pickle.load(fp)

    with open("resources/data/x_train_" + type + "_" + sign + ".txt", "rb") as fp:
        x_train = [el["data"] for el in pickle.load(fp)]

    with open("resources/data/x_test_" + type + "_" + sign + ".txt", "rb") as fp:
        x_test = [el["data"] for el in pickle.load(fp)]

    with open("resources/data/y_train_" + type + "_" + sign + ".txt", "rb") as fp:
        y_train = pickle.load(fp)

    with open("resources/data/y_test_" + type + "_" + sign + ".txt", "rb") as fp:
        y_test = pickle.load(fp)

    x_train, x_test = np.asarray(normalize_data(x_train)), np.asarray(normalize_data(x_test))
    y_train, y_test = np.asarray(y_train), np.asarray(y_test)

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

    model.evaluate(x_test, y_test)
    cls = model(x_test)

    model.save('resources/model/' + type + "_" + sign + ".h5")

    for i, j in zip(cls, y_test):
        print(i.numpy(), j)
