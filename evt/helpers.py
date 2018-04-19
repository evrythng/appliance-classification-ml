# -*- coding: utf-8 -*-
import sys
import ujson
import numpy as np
import pandas as pd

from evt.api import get_thngs, get_property_events


def vibration_property(*data):
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


def property_updates_to_df(property_updates):
    data = []
    for t, v in map(lambda x: (x['createdAt'], x['value']), property_updates):
        a = np.array(v, dtype=float)
        if np.any(a.max(axis=0)[1:] > 4) or np.any(a.min(axis=0)[1:] < -4):
            continue
        a = np.hstack([a[:, 0:1], a])
        a[:, 0] *= 1000
        a[:, 0] += t
        data.append(a)
    df = pd.DataFrame(np.vstack(data), columns=['ts','t', 'x', 'y', 'z'])
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df.set_index('ts', inplace=True)
    return df.sort_index()


def evt_training_data(host, api_key, thng_prop, collection_id):
    for thng in get_thngs(host, api_key, collection_id):
        if thng_prop in thng['properties']:
            yield thng['id'], get_property_events(host, api_key, thng['id'], thng_prop)