from swissrugbystats.crawler.crawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.models import CrawlerLogMessage
from swissrugbystats.crawler.parser import FSRLeagueParser


class TeamCrawler(AbstractCrawler):

    @classmethod
    def crawl_per_league(cls, url, follow_pagination=False):
        """
        Fetch all the teams that are participating in a league.
        :param url:
        :param follow_pagination:
        :return: count
        """
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)

        logger.log("crawl {}".format(url[1]))
        try:
            tables = FSRLeagueParser.get_tables(url)

            for table in tables:
                for row in table.findAll('tr'):
                    try:
                        if FSRLeagueParser.parse_row(row):
                            count = count + 1
                    except Exception as e:
                        CrawlerLogMessage.objects.create(
                            message_type=CrawlerLogMessage.ERROR,
                            message=u"crawl_teams_per_league, {}".format(e.__str__())
                        )
        except Exception as e:
            print(u"exception {}".format(e))
            CrawlerLogMessage.objects.create(
                message_type=CrawlerLogMessage.ERROR,
                message=u"crawl_teams_per_league, {}".format(e.__str__())
            )

        # TODO: statistics
        # if lock:
        #     with lock:
        #         self.statistics['teams'] += count
        # else:
        #     self.statistics['teams'] += count

        return count
