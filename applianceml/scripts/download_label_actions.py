#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import ujson
from evt.api import get_actions

if __name__ == '__main__':
    actions = get_actions(os.getenv('EVT_HOST'), os.getenv('EVT_API_KEY'), os.getenv('ACTION_TYPE'))
    labels = [dict(createdAt=a['createdAt'], label=a['customFields']['shape']) for a in actions]
    with open(os.getenv('ACTIONS'), 'w') as fd:
        ujson.dump(labels, fd, ensure_ascii=True)