#!/bin/sh
./setup/get-pip.py
pip install virtualenv
virtualenv --no-site-packages --distribute -p python3 ./env && source ./env/bin/activate && pip install -r requirements.txt
python manage.py migrate