#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import ujson
import numpy as np

from functools import reduce
from trainer.preprocess import transform, fit_min_max_scaler as fit_training_data, transform_min_max_scaling as normalize_features, MAX_LEN

if __name__ == '__main__':

    data = ([i['value'] for i in d] for d in ujson.load(open(os.getenv('RAW_DATA'))).values())
    data = reduce(lambda x, y: x + y, data)

    train_x, test_x = data[:int(len(data)*0.8)], data[int(len(data)*0.8):]

    fit_params = fit_training_data(np.vstack(train_x)[:, 1:], os.getenv('FIT_PARAMS'))

    train_x = (normalize_features(np.array(x)[:,1:], fit_params) for x in train_x)
    test_x = (normalize_features(np.array(x)[:,1:], fit_params) for x in test_x)

    train_x = transform(train_x, MAX_LEN)
    test_x = transform(test_x, MAX_LEN)

    if np.all(test_x == train_x):
        raise Exception('train_x and test_x are the same')

    ujson.dump(train_x, open(os.getenv('TRAIN_FILE'), 'w'),ensure_ascii=True)
    ujson.dump(test_x, open(os.getenv('EVAL_FILE'), 'w'),ensure_ascii=True)

