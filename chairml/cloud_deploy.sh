#!/usr/bin/env bash



source ../evt_config/google_cloud.env


gcloud ml-engine models create $MODEL_NAME --regions=us-central1

MODEL_BINARIES=$JOB_DIR/export

gsutil ls -r $MODEL_BINARIES

gcloud ml-engine versions create v2 \
      --model $MODEL_NAME \
      --origin $MODEL_BINARIES \
      --runtime-version 1.5
