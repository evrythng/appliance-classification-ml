#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import sys

if __name__ == '__main__':
    config = dict(host=os.getenv('EVT_HOST'),
                  api_key=os.getenv('EVT_API_KEY'),
                  collection_id = os.getenv('EVT_COLLECTION_ID'))
    thngs = []
    for i in sys.stdin:
        thng_id = i.strip()
        if len(thng_id) != 24:
            print("THNG ID is invalid " + thng_id, file=sys.stderr)
            sys.exit(1)
        thngs.append(thng_id)

    print(thngs)
    res = requests.put("https://{host}/collections/{collection_id}/thngs".format(**config),
                        headers={"Authorization": config['api_key'], "Content-Type": "application/json"}, json=thngs)
