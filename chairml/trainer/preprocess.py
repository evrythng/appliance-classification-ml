from keras.preprocessing import sequence
import pickle
import sys

import ujson

MAX_LEN = 40
CHANNELS = 3
INPUT_SHAPE = (CHANNELS, MAX_LEN)


def fit_training_data_decorator(fit_fn):
    def call(train_data, file):
        p = fit_fn(train_data)
        with open(file + '.p', 'wb') as fd:
            pickle.dump(p, fd)
            print('Creating pickle fit params {file} for training purposes'.format(file=file + '.p'))
        with open(file + '.json', 'w') as fd:
            ujson.dump(p, fd)
            print('Creating json fit params {file} for the reactor information pipeline'.format(file=file + '.p'))
        return p
    return call


def normalize_features_decorator(transform_fn):
    def call(data, fit_params):
        return transform_fn(data, fit_params)
    return call


def fit_std_scaler(train_data):
    mean = train_data.mean(axis=0)
    train_data -= mean
    std = train_data.std(axis=0)
    return dict(std=std, mean=mean)


@fit_training_data_decorator
def fit_min_max_scaler(train_data):
    return dict(min=train_data.min(axis=0), max=train_data.max(axis=0))


def transform_standardization(data, fit_params):
    return (data - fit_params['mean']) / fit_params['std']


@normalize_features_decorator
def transform_min_max_scaling(data, fit_params):
    return (data - fit_params['min']) / (fit_params['max'] - fit_params['min'])


def fit_meean_normalization(train_data):
    return dict(min=train_data.min(axis=0), max=train_data.max(axis=0))


def transform(data, maxlen=40):
    return [sequence.pad_sequences(list(zip(*d)), padding='post', truncating='post', dtype='float', maxlen=maxlen) for d
            in data]


def vibration_property_value(*data):
    for d in data:
        if type(d['value']) is str:
            try:
                d['value'] = ujson.loads(d['value'])
                if type(d['value']) is list and d['value']:
                    yield d
                else:
                    print('empty {}'.format(d))
                    continue
            except ValueError as e:
                print(e, file=sys.stderr)
