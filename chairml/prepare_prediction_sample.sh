#!/usr/bin/env bash

source venv/bin/activate


source ../evt_config/evt_predict.env

source ../evt_config/google_cloud.env

./scripts/prepare_predict_data.py $PREDICT_FILE

if [ $? -eq 1 ]
then
    echo Exiting due to error
else
    gsutil cp $PREDICT_FILE gs://$BUCKET_NAME/data/$PREDICT_FILE
fi