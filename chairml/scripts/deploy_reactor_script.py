#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from zipfile import ZipFile
import requests
import os
import ujson



if __name__ == '__main__':
    config = dict(host=os.getenv('EVT_HOST'),
                  api_key=os.getenv('EVT_API_KEY'),
                  thng_prop=os.getenv('EVT_THNG_PROPERTY'),
                  collection_id=os.getenv('EVT_COLLECTION_ID'))

    with ZipFile('spam.zip', 'w') as build:
        build.write(os.getenv('FIT_PARAMS')+'.json')
        build.write(os.getenv('GOOGLE_CREDENTIALS'))
        for f in filter(os.path.isfile, os.listdir(os.getenv('REACTOR_DIR'))):
            build.write(os.path.join(os.getenv('REACTOR_DIR'), f))
