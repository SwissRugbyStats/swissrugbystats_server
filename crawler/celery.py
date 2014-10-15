# start worker with
# $ celery -A crawler worker -B -l info

from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab

app = Celery('crawler',
             broker='amqp://',
             backend='amqp://',
             include=['crawler.tasks'])

# schedule
app.conf.CELERY_TIMEZONE = 'Europe/Zurich'

app.conf.CELERYBEAT_SCHEDULE = {
    # executes every night at 23:00
    'every-night': {
        'task': 'crawler.updateAll',
        'schedule': crontab(hour=23, minute=00)
    }
}


# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()