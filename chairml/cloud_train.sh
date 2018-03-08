#!/usr/bin/env bash

source venv/bin/activate

python setup.py build
python setup.py install


export BUCKET_NAME=connected-machine-learning

# set the same job name/id in cloud_deploy.sh
export JOB_NAME=chair_single_14
export JOB_DIR="gs://$BUCKET_NAME/$JOB_NAME"

export MOTION_DATA='data'
export TRAIN_FILE=$MOTION_DATA/train.json
export EVAL_FILE=$MOTION_DATA/eval.json

export GCS_TRAIN_FILE="gs://$BUCKET_NAME/$TRAIN_FILE"
export GCS_EVAL_FILE="gs://$BUCKET_NAME/$EVAL_FILE"



export TRAIN_STEPS=100
export EPOCS=4000


gcloud ml-engine jobs submit training $JOB_NAME \
                                    --stream-logs \
                                    --config config.yaml \
                                    --runtime-version 1.4 \
                                    --job-dir $JOB_DIR \
                                    --package-path trainer \
                                    --module-name trainer.task \
                                    --region us-central1 \
                                    -- \
                                    --train-files $GCS_TRAIN_FILE \
                                    --eval-files $GCS_EVAL_FILE \
                                    --train-steps $TRAIN_STEPS


