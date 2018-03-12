#!/usr/bin/env bash

source venv/bin/activate

python setup.py build
python setup.py install



MOTION_DATA='data'
JOB_DIR=vibr_keras
TRAIN_FILE="$MOTION_DATA/x_train.json $MOTION_DATA/y_train.json"
EVAL_FILE="$MOTION_DATA/x_val.json $MOTION_DATA/y_val.json"


rm -rf $JOB_DIR

export TRAIN_STEPS=100
export EPOCS=20


gcloud ml-engine local train --package-path trainer \
                             --module-name trainer.task \
                             -- \
                             --train-files $TRAIN_FILE \
                             --eval-files $EVAL_FILE \
                             --job-dir $JOB_DIR \
                             --distributed \
                             --train-steps $TRAIN_STEPS \
                             --train-batch-size 128 \
                             --num-epochs $EPOCS \
                             --config config.yaml \
                             --runtime-version 1.4
