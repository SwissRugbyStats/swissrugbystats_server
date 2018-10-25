from swissrugbystats.crawler.crawler import AbstractCrawler
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
        print("crawl {}".format(url[1]))
        try:
            tables = FSRLeagueParser.get_tables(url)

            for table in tables:
                for row in table.findAll('tr'):
                    try:
                        FSRLeagueParser.parse_row(row)
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
