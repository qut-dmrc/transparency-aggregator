#!/bin/bash

echo "Setting up environment"
virtualenv python_env
source venv/bin/activate
pip install pandas
pip install docopt
# pip install unittest

echo "Running Tests"
python -m unittest discover tests

deactivate
