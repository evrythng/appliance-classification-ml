#!/usr/bin/env bash


source venv/bin/activate

python setup.py build
python setup.py install


source ../evt_config/google_cloud.conf



gcloud ml-engine local predict  \
                            --model-dir=$JOB_DIR/export \
                            --json-instances $PREDICT_FILE \
