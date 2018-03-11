#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.evt import *
import os
import ujson
import pickle
import numpy as np
from trainer.preprocess import transform, transform_min_max_scaling as normalize_features, MAX_LEN,motion_property_value


config = dict(host=os.getenv('EVT_HOST'),
              api_key=os.getenv('EVT_API_KEY'),
              thng_id=os.getenv('EVT_THNG_ID'),
              thng_prop=os.getenv('EVT_THNG_PROPERTY'))

if __name__ == '__main__':
    # Download properties from a thng that was not used in the training or test set
    # Let's see how well the newly trained model can deal with it
    data = get_property_events(**config)

    # Deserialize json 'value' paylod
    data = motion_property_value(*data)

    # Create a 3d array with (property event, step, sensor vector)
    data = map(lambda x: x['value'], data)

    # Normalize data
    with open(os.getenv('FIT_PARAMS'),'rb') as fd:
        fit_params = pickle.load(fd)
    data = map(lambda x: normalize_features(np.array(x)[:,1:], fit_params), data)

    # Pad the data so that each property event has the same shape
    data = transform(data, MAX_LEN)

    # Serialize using signature expecgted by our model. This file can e used locally and in the cloud
    # TODO serialise multiple events
    with open(os.getenv('PREDICT_FILE'), 'w') as fd:
        ujson.dump(dict(instances=data[1]), fd,ensure_ascii=True)
