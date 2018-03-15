#!/usr/bin/env bash


source venv/bin/activate

source ../evt_config/google_cloud.env

rm -rf $MOTION_DATA

mkdir -p $MOTION_DATA

# download generated training data
source ../evt_config/evt_training_generated.env
./scripts/download_records.py

# download training data from real pycom devices
source ../evt_config/evt_training_appliance.conf
./scripts/download_records.py

if [ $? -eq 1 ]
then
    exit 1
fi

./scripts//prepare_training_data.py

if [ $? -eq 1 ]
then
    exit 1
fi

export BUCKET_NAME=connected-machine-learning


gsutil cp $TRAIN_FILE $GCS_TRAIN_FILE
gsutil cp $EVAL_FILE $GCS_EVAL_FILE