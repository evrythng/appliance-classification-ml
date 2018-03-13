#!/usr/bin/env bash


source venv/bin/activate

python setup.py build
python setup.py install

source ../evt_config/evt_predict.conf
source ../evt_config/google_cloud.conf

rm -rf $MOTION_DATA
mkdir $MOTION_DATA

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
export GCS_TRAIN_FILE="gs://$BUCKET_NAME/$TRAIN_FILE"
export GCS_EVAL_FILE="gs://$BUCKET_NAME/$EVAL_FILE"

gsutil cp $TRAIN_FILE $GCS_TRAIN_FILE
gsutil cp $EVAL_FILE $GCS_EVAL_FILE