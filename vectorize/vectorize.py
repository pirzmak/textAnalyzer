import tensorflow as tf


def vectorize(data, all):
    vector = [0] * len(all)
    for k, v in data.items():
        if k in all:
            vector[all[k]] = v / 1.0
    return vector


def vectorize_named_entities(data, all):
    vector = [0] * len(all)
    index = {}
    i = 0
    max_len = max(list(map(lambda x: len(x), all.values())))

    for k in all.keys():
        vector[i] = [0] * max_len
        index[k] = i
        i = i + 1
    for k, v in data.items():
        for q, w in v.items():
            if q in all[k]:
                vector[index[k]][all[k][q]] = w / 1.0
    return vector


def get_all_words(data):
    all = {}
    filtered_all = {}
    for x in data:
        for n in x['text_vector'].keys():
            if n not in all:
                all[n] = 1
            else:
                all[n] += 1

    for k, v in all.items():
        if v > 5:
            filtered_all[k] = len(filtered_all)
    return all, filtered_all


def get_all_named_entities(data):
    all = {}
    filtered_all = {}
    for x in data:
        for k, v in x['text_vector'].items():
            if k not in all:
                all[k] = {}
            for w in v:
                if w not in all[k]:
                    all[k][w] = 1
                else:
                    all[k][w] += 1

    for k, v in all.items():
        if k not in filtered_all:
            filtered_all[k] = {}
        for q, w in v.items():
            if w > 5:
                filtered_all[k][q] = len(filtered_all[k])
    return all, filtered_all

