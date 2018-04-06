#!/usr/bin/env python3


import sys
import ujson
import os
from evt.api import get_property_events
from evt.helpers import vibration_property


ATTEMPTS = 6



if __name__ == '__main__':
    config = dict(host=os.getenv('EVT_HOST'),
                  api_key=os.getenv('EVT_API_KEY'),
                  thng_id=os.getenv('THNG_ID'),
                  thng_property=os.getenv('THNG_PROPERTY'))
                  # begin=int(pd.to_datetime('2018-02-18 00:00:00').timestamp() * 1000),
                  # end=int(pd.to_datetime('2018-03-24 08:00:00').timestamp() * 1000)


    with open(os.getenv('DATA'), 'w') as fd:
        ujson.dump(list(vibration_property(*get_property_events(**config))), fd, ensure_ascii=True)