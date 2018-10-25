from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger


class CrawlerLogMixin(object):

    def __init__(self):
        self.logger = CrawlerLogger.get_logger_for_instance(self)

    def log(self, msg, db=False, slack=False):
        self.logger.log(msg, db, slack)