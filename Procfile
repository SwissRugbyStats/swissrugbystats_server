release: python manage.py migrate && python manage.py collectstatic
web: gunicorn swissrugbystats.wsgi --timeout 30 --graceful-timeout 30 --log-level debug --log-file -