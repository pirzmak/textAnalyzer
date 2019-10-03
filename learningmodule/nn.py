from vectorize import vectorize, get_all_named_entities, vectorize_named_entities
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
from config import DBNAMES


def preprocesssing_data(type, sign, tags, all):
    inputs, outputs = [], []

    for x in select(type, {'tag': {'$in': tags}}):
        try:
            prices = get_price(sign, x['date'])
            print(prices)
            if not math.isnan(prices['actual']):
                if type == DBNAMES.BAGS_OF_WORDS:
                    inputs.append({"data": vectorize(x['text_vector'], all), "date": x['date']})
                if type == DBNAMES.NAMES_ENTITIES:
                    inputs.append({"data": vectorize_named_entities(x['text_vector'], all), "date": x['date']})
                outputs.append(get_price_trend(prices['before'], prices['actual'], prices['after']))
        except pymongo.errors.CursorNotFound:
            print("cursor error")

    return inputs, outputs


def get_names_entities_vector(data):
    max_len = max(list(map(lambda x: max(list(map(lambda xx: len(xx), x))), data)))
    padded = []
    for x in data:
        tmp = []
        for v in x:
            pad = [[0, max_len - len(v)]]
            tmp.append(tf.pad(v, pad, mode='CONSTANT'))
        padded.append(tmp)
    return padded


def save_data_to_file(type, sign, tags, divide=0.8):
    if type == DBNAMES.BAGS_OF_WORDS:
        all = get_all_words(select(type, {'tag': {'$in': tags}}))
    if type == DBNAMES.NAMES_ENTITIES:
        all = get_all_named_entities(select(type, {'tag': {'$in': tags}}))

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
    if len(inputs) > 0:
        for x in np.asarray(inputs):
            ret.append(normalize(np.array(x, dtype=np.float16)[:, np.newaxis], axis=0).ravel())
    return ret


def get_names_entities_vector(data):
    max_len = max(list(map(lambda x: max(list(map(lambda xx: len(xx), x))), data)))
    vec = list(map(lambda x: normalize_data(x), data))
    padded = []
    for x in vec:
        tmp = []
        for v in x:
            pad = [[0, max_len - len(v)]]
            tmp.append(tf.pad(v, pad, mode='CONSTANT'))
        padded.append(tmp)
    return np.asarray(padded)


def get_names_entities_shape(data):
    max_len = max(list(map(lambda x: max(list(map(lambda xx: len(xx), x))), data)))
    return (18, max_len)


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

    normalized_x_train, normalized_x_test = [], []
    shape = 0


    if type == DBNAMES.BAGS_OF_WORDS:
        normalized_x_train = normalize_data(x_train)
        normalized_x_test = normalize_data(x_test)
        shape = (len(all), )
    if type == DBNAMES.NAMES_ENTITIES:
        all = []
        normalized_x_train = list(map(lambda x: np.asarray(normalize_data(x)), x_train))
        normalized_x_test = list(map(lambda x: np.asarray(normalize_data(x)), x_test))
        shape = get_names_entities_shape(x_train)

    model = tf.keras.models.Sequential([
      tf.keras.layers.Input(shape=(18, 6834)),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(5, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    all = []

    to = int(len(x_train) * 0.5)
    x_train_1 = normalized_x_train[:to]
    x_train_2 = normalized_x_train[to:]
    x_test = normalized_x_test

    normalized_x_train, normalized_x_test = [], []

    y_train_1 = y_train[:to]
    y_train_2 = y_train[to:]

    y_test = y_test

    model.fit(np.asarray(x_train_1), np.asarray(y_train_1), epochs=1)

    x_train_1, y_train_1 = [], []

    model.fit(np.asarray(x_train_2), np.asarray(y_train_2), epochs=1)

    x_train_12, y_train_2 = [], []

    model.evaluate(np.asarray(x_test), np.asarray(y_test))
    cls = model(np.asarray(x_test))

    model.save('resources/model/' + type + "_" + sign + ".h5")

    for i, j in zip(cls, y_test):
        print(i.numpy(), j)
