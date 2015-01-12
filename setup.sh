#!/bin/sh
./setup/get-pip.py
pip install virtualenv
virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt
