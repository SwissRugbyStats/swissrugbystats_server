from __future__ import absolute_import

from crawler.celery import app
from crawler import dbupdater


@app.task(name='crawler.updateAll')
def update_all():
    dbupdater.update_all()


@app.task(name='crawler.update_latest')
def update_latest():
    dbupdater.update_all(True)


@app.task(name='crawler.blubb')
def blubb():
    return "blubb"
