#!/usr/bin/env bash


source venv/bin/activate


source ../evt_config/google_cloud.env



gcloud ml-engine local predict  \
                            --model-dir=$JOB_DIR/export \
                            --json-instances $PREDICT_FILE \
