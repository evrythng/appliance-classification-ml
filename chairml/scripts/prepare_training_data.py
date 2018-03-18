#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import ujson
import numpy as np

from functools import reduce
from trainer.preprocess import padding, fit_std_scaler as fit_training_data, transform_std as normalize_features, MAX_LEN, FEATURES
from sklearn.preprocessing import LabelEncoder
if __name__ == '__main__':

    with open(os.getenv('RAW_DATA')) as fd:
        datasets = ujson.load(fd)
    data = []
    for s in datasets:
        _data = datasets[s]
        _data = ([[i['value'],s] for i in d] for d in _data.values())
        data = reduce(lambda x, y: x + y, _data, data)

    np.random.shuffle(data)
    train, test = data[:int(len(data)*0.7)], data[int(len(data)*0.7):]
    train_x, train_y = zip(*train)
    test_x, test_y = zip(*test)
    train_y, test_y = np.array(train_y), np.array(test_y)

    label_ohe = LabelEncoder()
    label_ohe.fit(train_y)

    train_y, test_y = label_ohe.transform(train_y).reshape(-1,1), label_ohe.transform(test_y).reshape(-1,1)
    with open(os.getenv('LABELS_ENC'),'w') as fd:
        ujson.dump(label_ohe.classes_, fd, ensure_ascii=True)
    # train_y = np.array(train_y == np.arange(len(label_ohe.classes_)),dtype=float)
    # test_y = np.array(test_y == np.arange(len(label_ohe.classes_)),dtype=float)
    train_y, test_y = np.array(train_y,dtype=float), np.array(test_y,dtype=float)
    fit_params = fit_training_data(np.vstack(train_x)[:, :], os.getenv('FIT_PARAMS'))

    # train_x = (normalize_features(np.array(x)[:,1:], fit_params) for x in train_x)
    # test_x = (normalize_features(np.array(x)[:,1:], fit_params) for x in test_x)

    train_x = (normalize_features(np.array(x)[:, :], fit_params) for x in train_x)
    test_x = (normalize_features(np.array(x)[:, :], fit_params) for x in test_x)

    train_x = np.array(padding(train_x, MAX_LEN))
    test_x = np.array(padding(test_x, MAX_LEN))

    train_x = train_x.reshape(-1, MAX_LEN, FEATURES)
    test_x = test_x.reshape(-1, MAX_LEN, FEATURES)


    if np.all(test_x == train_x):
        raise Exception('train_x and test_x are the same')

    with open(os.getenv('TRAIN_FILE'), 'w') as fd:
        ujson.dump((train_x,train_y), fd,ensure_ascii=True)

    with open(os.getenv('EVAL_FILE'), 'w') as fd:
        ujson.dump((test_x,test_y), fd, ensure_ascii=True)

