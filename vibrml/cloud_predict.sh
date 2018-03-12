#!/usr/bin/env bash



MOTION_DATA=data
PREDICT_FILE=$MOTION_DATA/predict.json
MODEL_NAME=keras_vibrml

gcloud ml-engine predict --model $MODEL_NAME --json-instances $PREDICT_FILE
