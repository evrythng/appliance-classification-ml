#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from zipfile import ZipFile
import os
import io
from libs import evt

if __name__ == '__main__':
    config = dict(host=os.getenv('EVT_HOST'),
                  api_key=os.getenv('EVT_API_KEY'),
                  thng_prop=os.getenv('EVT_THNG_PROPERTY'),
                  collection_id=os.getenv('EVT_COLLECTION_ID'))
    fp = io.BytesIO()
    with ZipFile(fp, 'w') as bundle:
        print('Adding ' + (os.getenv('FIT_PARAMS') + '.json').split('/')[-1])
        bundle.write(os.getenv('FIT_PARAMS') + '.json', (os.getenv('FIT_PARAMS') + '.json').split('/')[-1])
        print('Adding ' + os.getenv('GOOGLE_CREDENTIALS').split('/')[-1])
        bundle.write(os.getenv('GOOGLE_CREDENTIALS'), os.getenv('GOOGLE_CREDENTIALS').split('/')[-1])
        for f in filter(lambda x: x[0] != '.', os.listdir(os.getenv('REACTOR_DIR'))):
            print('Adding ' + f)
            bundle.write(os.path.join(os.getenv('REACTOR_DIR'), f), f)
    fp.flush()
    fp.seek(0)
    app_context = evt.get_app_key_context(os.getenv('EVT_HOST'), os.getenv('INTEGRATOR_TRUSTED_APP_API_KEY'))
    res = evt.deploy_reactor_script(os.getenv('EVT_HOST'),
                              os.getenv('OPERATOR_API_KEY'),
                              app_context['project_id'],
                              app_context['app_id'],
                              fp)
    print(res.json())
