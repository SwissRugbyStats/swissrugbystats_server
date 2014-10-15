from __future__ import absolute_import

from crawler.celery import app
from crawler import dbupdater


@app.task(name='crawler.updateAll')
def updateAll():
    dbupdater.updateAll()

@app.task(name='crawler.updateAll')
def blubb():
    return "blubb"
