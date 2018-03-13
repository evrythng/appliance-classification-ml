#!/usr/bin/env bash



source ../evt_config/google_cloud.conf

gcloud ml-engine predict --model $MODEL_NAME --json-instances $PREDICT_FILE
