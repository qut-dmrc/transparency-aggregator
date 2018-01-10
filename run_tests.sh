#!/bin/bash

echo "Setting up environment"
virtualenv python_env
source python_env/bin/activate
pip install pandas
pip install docopt
# pip install unittest

echo "Running Tests"
python -m unittest discover tests

deactivate
