swissrugbystats_server
======================

[!['Circle CI Status'](https://circleci.com/gh/SwissRugbyStats/swissrugbystats_server.svg?style=shield&circle-token=b93da3c79f6767c85fcd0e8e972f0ed7e9583f14)](https://circleci.com/gh/SwissRugbyStats/swissrugbystats_server)


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
- [x] easier way to start crawler
- [x] REST Endpoint to start crawler
- [x] Refactor crawler
- [ ] migrate data
- [x] django-jet
- [ ] crawler cronjob (jet dashboard?)
- [x] document crawler API
- [ ] setup email config
- [x] migrate pip & virtualenv to pipenv


main components
---------------

- **api:** json-API to access data
- **crawler:** Webcrawler to get teams, fixtures and results from suisserugby.com
- **swissrugby:** back- and frontend for the webapplication
- **docs:** documentation

some notes
----------

### activate virtualenv

We recently migrated from pip and virtualenv to pipenv.

If you don't have pipenv installed yet, install it via

    pip install pipenv
    
Then run

    pipenv install
    
to setup the virtualenv and install all the packages.

To activate the virtualenv in the shell, just run

    pipenv shell
  

### run webcrawler (might be outdated)
without logging:

    python manage.py crawl_and_update > /dev/null 2> /dev/null &

### update team statistics (might be outdated)

    python manage.py update_statistics

### export packages to requirements.txt

    pipenv lock -> requirements.txt

### setup cronjob for the crawler (might be outdated)
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


### Oauth Login notes

- https://django-allauth.readthedocs.io/
- https://django-rest-auth.readthedocs.io/
