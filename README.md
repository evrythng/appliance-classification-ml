# EVRYTHNG Machine Learning

This repository contains sample applications to explore machine-learning on the EVRYTHNG platform.  You'll find a tutorial for each application on the [EVRYTHNG developer portal](https://developers.evrythng.com/docs). 

Each sample application folder contains at least

- packaged model. Currently we have a Keras example that deploys to Google Cloud ML engine
- reactor: A folder with a reactor script that provides the integration between EVRYTHNG and a machine learning API
- data: Training data for the sample application 
- scripts: Some helper scripts to process data and deploy reactor scripts
- notebook: A Jupiter notebook

All projects share the [evt](evt) folder, which contains basic Python code to get data from and to your EVRYTHNG account.
