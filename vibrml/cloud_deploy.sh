#!/usr/bin/env bash

export BUCKET_NAME=connected-machine-learning

export JOB_NAME=vibr_single
export JOB_DIR="gs://$BUCKET_NAME/$JOB_NAME"

MODEL_NAME=keras_vibrml

gcloud ml-engine models create $MODEL_NAME --regions=us-central1

MODEL_BINARIES=$JOB_DIR/export

gsutil ls -r $MODEL_BINARIES

gcloud ml-engine versions create v1 \
      --model $MODEL_NAME \
      --origin $MODEL_BINARIES \
      --runtime-version 1.4
