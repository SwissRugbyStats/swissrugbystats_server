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
- djangorestframework
- django-cors-headers


some notes
----------

### setup the server
just run

    ./setup.sh

### activate virtualenv

    source env/bin/activate

### run webcrawler
without logging:

    python crawler/dbupdater.py > /dev/null 2> /dev/null &

### install rabbitmq

    wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
    sudo apt-key add rabbitmq-signing-key-public.asc
    sudo apt-get install rabbitmq-server

### 

### export packages to requirements.txt

    pip freeze -> requirements.txt

### install packages from requirements.txt

    pip install -r requirements.txt

### create virtualenv and install dependencies from requirements.txt

    virtualenv --no-site-packages --distribute ./env && source ./env/bin/activate && pip install -r requirements.txt
    
source: [https://stackoverflow.com/questions/6590688/is-it-bad-to-have-my-virtualenv-directory-inside-my-git-repository/6590783#6590783]()

### setup cronjob for the crawler
Create a script that runs your crawler, i.e. named update_srs.sh with the following content

    srsdir="/path/to/your/installation"
    cd $srsdir
    source env/bin/activate
    python crawler/dbupdater.py > /path/to/your/script/update_srs.log 2> /path/to/your/script/update_srs_err.log


Open your crontab for editing with `crontab -e` and add the following lines:

    SHELL=/bin/bash   # important! otherwise the source command to use virtualenv won't work!
    # get latest data from suisserugby.com
    0 3 * * * /path/to/script/update_srs.sh

