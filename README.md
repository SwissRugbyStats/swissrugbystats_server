swissrugbystats_server
======================

- api: json-API to access data
- crawler: Webcrawler to get teams, fixtures and results from suisserugby.com
- swissrugby: back- and frontend for the webapplication


required python packages
------------------------
- virtualenv
- django
- pytz
- celery
- rabbitmq
- requests
- pygments
- BeautifulSoup

some notes
----------

### activate virtualenv
source env/bin/activate

### run webcrawler
python crawler/dbupdater.py

### install rabbitmq
wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
sudo apt-key add rabbitmq-signing-key-public.asc
sudo apt-get install rabbitmq-server

### export packages to requirements.txt
pip freeze -> requirements.txt

### install packages from requirements.txt
pip install -r requirements.txt

### create virtualenv and install dependencies from requirements.txt
virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt
source: https://stackoverflow.com/questions/6590688/is-it-bad-to-have-my-virtualenv-directory-inside-my-git-repository/6590783#6590783
