#!/usr/bin/env bash

source venv/bin/activate

python setup.py build
python setup.py install


export BUCKET_NAME=connected-machine-learning

# set the same job name/id in cloud_deploy.sh
export JOB_NAME=vibr_single
export JOB_DIR="gs://$BUCKET_NAME/$JOB_NAME"

export MOTION_DATA='data'
export GCS_TRAIN_FILE="gs://$BUCKET_NAME/$MOTION_DATA/x_train.json gs://$BUCKET_NAME/$MOTION_DATA/y_train.json"
export GCS_EVAL_FILE="gs://$BUCKET_NAME/$MOTION_DATA/x_val.json gs://$BUCKET_NAME/$MOTION_DATA/y_val.json"

export TRAIN_STEPS=100
export EPOCS=40

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
