#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libs.evt import evt_training_data
import os
import ujson
from trainer.preprocess import vibration_property_value

if __name__ == '__main__':
    config = dict(host=os.getenv('EVT_HOST'),
                  api_key=os.getenv('EVT_API_KEY'),
                  thng_prop=os.getenv('EVT_THNG_PROPERTY'),
                  collection_id=os.getenv('EVT_COLLECTION_ID'))

    thngs_properties = dict(evt_training_data(**config))
    dataset = {}
    for thng in thngs_properties:
        for events in (vibration_property_value(x) for x in thngs_properties[thng]):
            for e in events:
                if len(e['value']) >= 2:
                    if thng not in dataset:
                        dataset[thng] = []
                    dataset[thng].append(e)

    ujson.dump(dataset,open(os.getenv('RAW_DATA'), 'w'),ensure_ascii=True)
