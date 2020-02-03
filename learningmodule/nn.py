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
import time
from datetime import datetime
import pandas as pd


def preprocesssing_data(type, sign, tags, all):
    inputs, outputs = [], []
    for x in select(type, {'tag': {'$in': tags}}):
        if x['date'] > datetime(2019, 10, 15):
            try:
                prices = get_price(sign, x['date'])
                print(prices)
                if not math.isnan(prices['actual']):
                    if type == DBNAMES.BAGS_OF_WORDS or type == DBNAMES.NOUNS:
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
    query = select(type, {'tag': {'$in': tags}})
    if type == DBNAMES.BAGS_OF_WORDS or type == DBNAMES.NOUNS:
        all = get_all_words(query)
    if type == DBNAMES.NAMES_ENTITIES:
        all = get_all_named_entities(query)

    inputs, outputs = preprocesssing_data(type, sign, tags, all)

    preI, postI = [s for s in inputs if s["date"] < datetime(2019, 10, 15)],\
                  [s for s in inputs if s["date"] > datetime(2019, 10, 15)]

    oLen = len(preI)

    preO, postO = outputs[:oLen], outputs[oLen:]

    preli, postli = list(zip(preI, preO)), list(zip(postI, postO))

    shuffle(preli)
    shuffle(postli)

    preI, preO = zip(*preli)
    postI, postO = zip(*postli)

    x_test = postI

    y_test = postO

    inputs, outputs, preI, postI, preO, postO, preli, postl = [], [], [], [], [], [], [], []

    filename = "resources/data/x_train_" + type + "_" + sign + ".txt"
    df = pd.DataFrame(x_train)
    df.to_csv(path_or_buf=filename, index=False)

    filename = "resources/data/x_test_" + type + "_" + sign + ".txt"
    df = pd.DataFrame(x_test)
    df.to_csv(path_or_buf=filename, index=False)

    filename = "resources/data/y_train_" + type + "_" + sign + ".txt"
    df = pd.DataFrame(y_train)
    df.to_csv(path_or_buf=filename, index=False)

    filename = "resources/data/y_test_" + type + "_" + sign + ".txt"
    df = pd.DataFrame(y_test)
    df.to_csv(path_or_buf=filename, index=False)

    filename = "resources/data/all_" + type + "_" + sign + ".txt"
    df = pd.DataFrame.from_dict(all, orient="index")
    df.to_csv(path_or_buf=filename, index=False)


def normalize_data(inputs):
    ret = []
    if len(inputs) > 0:
        for x in np.asarray(inputs):
            ret.append(normalize(np.array(x, dtype=np.float16)[:, np.newaxis], axis=0).ravel())
    print("normalize")
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
        all = pd.read_csv(fp)
    print("all")
    with open("resources/data/x_train_" + type + "_" + sign + ".txt", "rb") as fp:
        x_train = [el["data"] for ix, el in pd.read_csv(fp).iterrows()]
    print("x_train")
    with open("resources/data/x_test_" + type + "_" + sign + ".txt", "rb") as fp:
        x_test = [el["data"] for ix, el in pd.read_csv(fp).iterrows()]
    print("x_test")
    with open("resources/data/y_train_" + type + "_" + sign + ".txt", "rb") as fp:
        y_train = [el for ix, el in pd.read_csv(fp).iterrows()]
    print("y_train")
    with open("resources/data/y_test_" + type + "_" + sign + ".txt", "rb") as fp:
        y_test = [el for ix, el in pd.read_csv(fp).iterrows()]
    print("y_test")

    normalized_x_train, normalized_x_test = [], []
    shape = 0

    if type == DBNAMES.BAGS_OF_WORDS or type == DBNAMES.NOUNS:
        normalized_x_train = normalize_data(list(map(lambda x: eval(x), x_train)))
        normalized_x_test = normalize_data(list(map(lambda x: eval(x), x_test)))
        shape = (len(all), )
    if type == DBNAMES.NAMES_ENTITIES:
        all = []
        normalized_x_train = list(map(lambda x: np.asarray(normalize_data(eval(x))), x_train))
        normalized_x_test = list(map(lambda x: np.asarray(normalize_data(eval(x))), x_test))
        shape = (18, 11186)

    for size in [4096]:
        model = tf.keras.models.Sequential([
          tf.keras.layers.Flatten(input_shape=shape),
          tf.keras.layers.Dense(size, activation='relu'),
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Dense(5, activation='softmax')
        ])

        start_time = time.time()

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        all = []

        x_test = normalized_x_test

        history = model.fit(np.asarray(normalized_x_train), np.asarray(y_train), batch_size=64, epochs=3)

        results = model.evaluate(np.asarray(x_test), np.asarray(y_test))

        elapsed_time = time.time() - start_time

        model_type = 'one_' + str(size) +'_relu'
        string = type + "/" + sign + "/" + model_type
        model.save('resources/model/' + string + ".h5")

        np.savetxt('resources/metrics/' + string + "_time.csv", np.asarray([elapsed_time]))

        cls = model(np.asarray(x_test))

        np.savetxt('resources/metrics/' + string + "_loss.csv", np.asarray(history.history['loss']), delimiter=",")
        np.savetxt('resources/metrics/' + string + "_accuracy.csv", np.asarray(history.history['accuracy']), delimiter=",")
        np.savetxt('resources/metrics/' + string + "_val_results.csv", np.asarray(results), delimiter=",")

        toSave = []

        for i in cls:
            toSave.append(i.numpy())

        np.savetxt('resources/metrics/' + string + "_results.csv", np.asarray(toSave), delimiter=",")
        np.savetxt('resources/metrics/' + string + "_data.csv", np.asarray(y_test), delimiter=",")