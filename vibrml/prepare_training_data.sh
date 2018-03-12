#!/usr/bin/env bash


source venv/bin/activate

python setup.py build
python setup.py install

export EVT_API_KEY=
export EVT_HOST=api.evrythng.com
export EVT_THNG_PROPERTY=magnitude
export EVT_COLLECTION_ID=UHk8nhmNeD8aQKRwahshfgTe

export MOTION_DATA=data
export JOB_DIR=chairml_keras
export TRAIN_FILE=$MOTION_DATA/train.json
export EVAL_FILE=$MOTION_DATA/eval.json
export RAW_DATA=$MOTION_DATA/rawdata.json
export FIT_PARAMS=$MOTION_DATA/fit_params.p
rm -rf $MOTION_DATA


mkdir $MOTION_DATA

./scripts/download_records.py
./scripts//prepare_training_data.py


export BUCKET_NAME=connected-machine-learning
export GCS_TRAIN_FILE="gs://$BUCKET_NAME/$TRAIN_FILE"
export GCS_EVAL_FILE="gs://$BUCKET_NAME/$EVAL_FILE"

gsutil cp $TRAIN_FILE $GCS_TRAIN_FILE
gsutil cp $EVAL_FILE $GCS_EVAL_FILE