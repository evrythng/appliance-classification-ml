#!/usr/bin/env python3
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
import ujson
import os

def predict_json(project, model, instances, version=None):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    # Create the ML Engine service object.
    # To authenticate set the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
    service = discovery.build('ml', 'v1')
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']


# Store your full project ID in a variable in the format the API needs.


# Get application default credentials (possible only if the gcloud tool is
#  configured on your machine).
credentials = GoogleCredentials.get_application_default()


# Make the call.
try:
    with open(os.getenv('PREDICT_FILE')) as fd:
        for i in ujson.load(fd):
            print(predict_json('connected-machine-learning','keras_chairml',i))

except errors.HttpError as err:
    # Something went wrong, print out some information.
    print('There was an error creating the model. Check the details:')
    print(err._get_reason())
