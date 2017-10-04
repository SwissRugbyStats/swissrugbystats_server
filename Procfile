release: bin/addon-wait && yes | python manage.py migrate
web: gunicorn swissrugbystats.wsgi --timeout 30 --graceful-timeout 30 --log-level debug --log-file -