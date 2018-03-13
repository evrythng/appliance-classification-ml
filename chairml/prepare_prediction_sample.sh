#!/usr/bin/env bash

source venv/bin/activate

python setup.py build
python setup.py install

source ../evt_config/evt_predict.conf

source ../evt_config/google_cloud.conf

./scripts/prepare_predict_data.py $PREDICT_FILE

if [ $? -eq 1 ]
then
    echo Exiting due to error
else
    gsutil cp $PREDICT_FILE gs://$BUCKET_NAME/data/$PREDICT_FILE
fi