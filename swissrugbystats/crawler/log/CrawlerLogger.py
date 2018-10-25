import logging

from django.conf import settings
from django.urls import reverse

from swissrugbystats.crawler.models import CrawlerLogMessage


class CrawlerLogger(object):

    def __init__(self, classname):
        self.classname = classname

    @staticmethod
    def get_logger_for_instance(instance):
        return CrawlerLogger(instance.__class__.__name__)

    @staticmethod
    def get_logger_for_class(cls):
        return CrawlerLogger(cls.__name__)

    def log(self, msg, db=False, slack=False):
        """
        helper method that should be put into separate class.
        actually logging should be completely moved into the crawler
        :param msg:
        :param db:
        :param slack:
        :return:
        """

        msg = u'[{}]:(INFO) {}'.format(self.classname, msg)

        print(msg)

        if db:
            log_message = CrawlerLogMessage.objects.create(message=msg)

            if slack and settings.SLACK_WEBHOOK_URL:
                # post update to slack
                try:
                    import requests
                    import json

                    r = 'admin:{}_{}_change'.format(log_message._meta.app_label,
                                                    log_message._meta.model_name)

                    text = log_message.message + "\n<{}{}|Click here>".format(
                        settings.BASE_URL,
                        reverse(r, args=(log_message.id,))
                    )
                    url = settings.SLACK_WEBHOOK_URL
                    payload = {"text": text}
                    headers = {'content-type': 'application/json'}

                    response = requests.post(url, data=json.dumps(payload),
                                             headers=headers)

                except Exception as e:
                    print(e)

    def error(self, msg, db=True, slack=False):
        """

        :param self:
        :param msg:
        :param db:
        :param slack:
        :return:
        """

        msg = u'[{}]:(ERROR): {}'.format(self.classname, msg)

        logging.error(msg)

        if db:
            CrawlerLogMessage.objects.create(message_type=CrawlerLogMessage.ERROR, message=msg)
