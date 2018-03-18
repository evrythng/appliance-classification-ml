#!/usr/bin/env bash

source venv/bin/activate


source ../evt_config/google_cloud.env

rm -rf $OUTPUT_DIR

export TRAIN_STEPS=10
export EPOCS=100


gcloud ml-engine local train \
                             --job-dir $OUTPUT_DIR \
                             --package-path trainer \
                             --module-name trainer.task \
                             -- \
                             --train-files $TRAIN_FILE \
                             --eval-files $EVAL_FILE \
                             --train-steps $TRAIN_STEPS \
                             --num-epochs $EPOCS
