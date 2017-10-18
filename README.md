swissrugbystats_server
======================

!['Circle CI Status'](https://circleci.com/gh/SwissRugbyStats/swissrugbystats_server.svg?style=shield&circle-token=b93da3c79f6767c85fcd0e8e972f0ed7e9583f14)


Run the project locally:

    heroku local:start -f Procfile_dev

Run any manage.py cmds:

    heroku local:run python manage.py <cmd>



TODO: 
- [ ] rewrite README.md
- [ ] media files to external storage
- [x] Postgres instead of sqlite in PROD
- [ ] Postgres instead of sqlite in DEV
- [x] global vars from os.environ
- [ ] easier way to start crawler
- [ ] migrate data
- [x] django-jet
- [ ] crawler cronjob (jet dashboard?)


main components
---------------

- api: json-API to access data
- crawler: Webcrawler to get teams, fixtures and results from suisserugby.com
- swissrugby: back- and frontend for the webapplication
- docs: documentation

some notes
----------

### setup the server
just run

    ./setup.sh

### activate virtualenv

    source env/bin/activate

### run webcrawler
without logging:

    python manage.py crawl_and_update > /dev/null 2> /dev/null &

### update team statistics

    python manage.py update_statistics

### export packages to requirements.txt

    pip freeze -l -> requirements.txt

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
    python manage.py crawl_and_update > /path/to/your/script/update_srs.log 2> /path/to/your/script/update_srs_err.log
    python manage.py update_statistics


Open your crontab for editing with `crontab -e` and add the following lines:

    SHELL=/bin/bash   # important! otherwise the source command to use virtualenv won't work!
    # get latest data from suisserugby.com
    0 3 * * * /path/to/script/update_srs.sh

