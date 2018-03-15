# Setup

The folder evt_config contains sensitive data. Files in this folder will not be pushed to git. chairml contains all the files to train and the deploy model. chairml is the working directory for this project.

## Local environment and EVT project
1. `./setup.sh` to create the Python environment the first time this command is executed or update the environment. You must have Python 3 installed.
2. In our EVT account, create a project and an application. The application will contain a reactor script that provides the link between EVT and Google's CloudML. Also create an action type `_eventClassification`. The reactor script will publish the results from cloudML using this action.
3. Add all the necessary identifiers and keys in [../evt_config](../evt_config). It Contains:  
	- application_default_credentials.json: Gogole cloud credentials
	- evt_predict.env: A test thng for post-training predictions
	- google_cloud.env: All config paramters (Google and EVT) directly related to the ML workflow
	- One or more training collections, which is called by `./prepare_training_data.sh`. E.g.

```
# download generated training data
source ../evt_config/evt_training_generated.env
./scripts/download_records.py

# download training data from real pycom devices
source ../evt_config/evt_training_appliance.conf
./scripts/download_records.py
```


## Model training and testing locally

1. Download data: `./prepare_training_data.sh` and `./prepare_prediction_sample.sh`
2. Train the model locally `./local_train.sh`. If you see ERROR: (gcloud.ml-engine.local.predict) RuntimeError: Bad magic number in .pyc file, that's cloud ml not using python 3.5, but 2.7 instead. I don't know why [config.yaml](config.yaml) doesn't work for the local option.
3. Use the model with an untested thng `./local_predict.sh`

## Model training and testing using Google CloudML
1. If you haven't downloaded the training data, execute `./prepare_training_data.sh` and `./prepare_prediction_sample.sh`.
2. Before every iteration, increment `JOB_NAME` in [../evt_config/google_cloud.env](../evt_config/google_cloud.env).
3. Train in the cloud `./cloud_train.sh`
4. Deploy the model `./cloud_deploy.ch`
5. Make sure predictions make sense `./cloud_predict.sh`
6. And deploy a new reactor script with the latest feature normalisation parameters `./deploy_to_evt.sh`. If this deployment was successful, you will see `_eventClassification` actions when a `magnitude` property changes.