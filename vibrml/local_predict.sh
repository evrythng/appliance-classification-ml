#!/usr/bin/env bash


source venv/bin/activate

python setup.py build
python setup.py install


export JOB_DIR=vibrml_keras

export MOTION_DATA=data
export PREDICT_FILE=$MOTION_DATA/predict.json


gcloud ml-engine local predict  \
                            --model-dir=$JOB_DIR/export \
                            --json-instances $PREDICT_FILE \
