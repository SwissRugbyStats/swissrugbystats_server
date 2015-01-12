#!/bin/sh
./setup/get-pip.py
virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt
