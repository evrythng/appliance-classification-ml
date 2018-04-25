# EVRYTHNG Machine Learning

This is the repository for our tutorial [Intelligent Appliance Classification](https://developers.evrythng.com/docs/intelligent-appliance-classification). Please follow this guide on how to use the EVRYTHNG Platform in combination with Google Cloud ML Engine.

Content:

- [applianceml](applianceml) is a trainer package using Keras.
	- [reactor](applianceml/reactor): A folder with a reactor script that provides the integration between EVRYTHNG and a machine learning API
	- [data](applianceml/data): Training data for the sample application
	- [scripts](applianceml/scripts): Some helper scripts to process data and deploy reactor scripts
	- [notebooks](applianceml/notebooks): A Jupiter notebook
- [evt](evt) contains basic Python code to get data from and to your EVRYTHNG account.
