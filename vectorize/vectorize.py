def vectorize(data, all):
    vector = [0] * len(all)
    for k, v in data.items():
        if k in all:
            vector[all[k]] = v
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
    return filtered_all

