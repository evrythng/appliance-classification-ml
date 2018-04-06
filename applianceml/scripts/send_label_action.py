#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from zipfile import ZipFile
import os
import sys
import requests

if __name__ == '__main__':
    config = dict(host=os.getenv('EVT_HOST'),
                  api_key=os.getenv('EVT_API_KEY'),
                  thng_id=os.getenv('THNG_ID'),
                  action_type=os.getenv('ACTION_TYPE'))


    res = requests.post(f"https://{config['host']}/thngs/{config['thng_id']}/actions/{config['action_type']}",
                        headers={"Authorization": config['api_key'], "Content-Type":"application/json"},
                        json=dict(type=config['action_type'],customFields=dict(shape=sys.argv[1])))
    print(res.json())