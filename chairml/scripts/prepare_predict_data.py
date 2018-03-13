#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.evt import *
import os
import ujson
import pickle
import numpy as np
from trainer.preprocess import padding, transform_std as normalize_features, MAX_LEN,vibration_property


config = dict(host=os.getenv('EVT_HOST'),
              api_key=os.getenv('EVT_API_KEY'),
              thng_id=os.getenv('EVT_THNG_ID'),
              thng_prop=os.getenv('EVT_THNG_PROPERTY'))

if __name__ == '__main__':
    # Download properties from a thng that was not used in the training or test set
    # Let's see how well the newly trained model can deal with it
    data = get_property_events(**config)

    # Deserialize json 'value' paylod
    data = vibration_property(*data)

    # Create a 3d array with (property event, step, sensor vector)
    data = map(lambda x: x['value'], data)

    # Normalize data
    with open(os.getenv('FIT_PARAMS')+'.p','rb') as fd:
        fit_params = pickle.load(fd)
    data = map(lambda x: normalize_features(np.array(x)[:,:], fit_params), data)

    # Pad the data so that each property event has the same shape
    data = padding(data, MAX_LEN)

    # dict(instances=d
    # Serialize using signature expecgted by our model. This file can e used locally and in the cloud
    # TODO serialise multiple events
    inputs = [dict(instances=d) for d in data]
    # ujson.dump(dict(instances=data[1]), fd, ensure_ascii=True)
    with open(os.getenv('PREDICT_FILE'), 'w') as fd:
        ujson.dump(inputs[3], fd,ensure_ascii=True)
