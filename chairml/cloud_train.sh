#!/usr/bin/env bash

source venv/bin/activate

python setup.py build
python setup.py install


source ../evt_config/google_cloud.env



export TRAIN_STEPS=100
export EPOCS=50


gcloud ml-engine jobs submit training $JOB_NAME \
                                    --stream-logs \
                                    --config config.yaml \
                                    --runtime-version 1.5 \
                                    --job-dir $JOB_DIR \
                                    --package-path trainer \
                                    --module-name trainer.task \
                                    --region us-central1 \
                                    -- \
                                    --train-files $GCS_TRAIN_FILE \
                                    --eval-files $GCS_EVAL_FILE \
                                    --train-steps $TRAIN_STEPS


