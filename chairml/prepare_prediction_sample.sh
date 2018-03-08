#!/usr/bin/env bash

source venv/bin/activate



export EVT_API_KEY=
export EVT_HOST=api.evrythng.com
export EVT_THNG_PROPERTY=magnitude
export EVT_THNG_ID=UnFNVHbBVgsRtpaRaDT7Ha2k

export MOTION_DATA=data
export FIT_PARAMS=$MOTION_DATA/fit_params.p
export PREDICT_FILE=$MOTION_DATA/predict.json

export BUCKET_NAME=connected-machine-learning

./scripts/prepare_predict_data.py $PREDICT_FILE


gsutil cp $PREDICT_FILE gs://$BUCKET_NAME/data/$PREDICT_FILE