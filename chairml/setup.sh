#!/usr/bin/env bash

source ../evt_config/google_cloud.conf

if [ ! -d venv ]
    then
        echo "Creating a new Python 3 environemnt"
        virtualenv --no-site-packages -p python3 venv
        source venv/bin/activate
        echo "Insalling packages"
        pip install -r requirements.txt

    else
        echo "Your environment is already setup"
        source venv/bin/activate
        echo "Removing build files"
        rm -rf build dist trainer.egg-info
        echo "Removing model checkpoints in $OUTPUT_DIR"
        rm $OUTPUT_DIR
fi

echo "Building the project"
python setup.py build
python setup.py install