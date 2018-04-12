#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from zipfile import ZipFile
import os
import io
import evt.utils
import ujson

if __name__ == '__main__':

    with open(os.getenv('MODEL_CONFIG_PARAMS')) as fd:
        model_config = ujson.load(fd)
    model_config['google_project'] = os.getenv('GOOGLE_PROJECT')
    model_config['model_name'] = os.getenv('MODEL_NAME')

    with open(os.getenv('MODEL_CONFIG_PARAMS'), 'w') as fd:
        ujson.dump(model_config, fd, ensure_ascii=True)

    fp = io.BytesIO()
    with ZipFile(fp, 'w') as bundle:
        print('Adding ' + os.getenv('GOOGLE_CREDENTIALS').split('/')[-1])
        bundle.write(os.getenv('GOOGLE_CREDENTIALS'), os.getenv('GOOGLE_CREDENTIALS').split('/')[-1])
        for f in filter(lambda x: x[0] != '.', os.listdir(os.getenv('REACTOR_DIR'))):
            print('Adding ' + f)
            bundle.write(os.path.join(os.getenv('REACTOR_DIR'), f), f)
    fp.flush()
    fp.seek(0)
    app_context = evt.utils.get_app_key_context(os.getenv('EVT_HOST'), os.getenv('INTEGRATOR_TRUSTED_APP_API_KEY'))
    res = evt.utils.deploy_reactor_script(os.getenv('EVT_HOST'),
                                          os.getenv('OPERATOR_API_KEY'),
                                          app_context['project_id'],
                                          app_context['app_id'],
                                          fp)
    print(res.json())
