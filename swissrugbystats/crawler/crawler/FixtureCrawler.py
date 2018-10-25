from swissrugbystats.core.models import Competition
from swissrugbystats.crawler.crawler import AbstractCrawler
from swissrugbystats.crawler.models import CrawlerLogMessage
from swissrugbystats.crawler.parser import FSRAbstractParser, FSRFixtureParser


class FixtureCrawler(AbstractCrawler):

    @classmethod
    def crawl_per_league(cls, url, follow_pagination=False):
        """
            Fetch all fixtures of a specific league.
            :param url: url to fetch fixtures from
            :param deep_crawl: deep_crawl: follow pagination?
            :param lock: ?
            :return: number of fetched fixtures
        """
        count = 0
        try:
            print(url)
            table = FSRAbstractParser.get_table(url)
            competition = Competition.objects.get(id=url[2])

            for row in table.findAll('tr'):
                try:
                    FSRFixtureParser.parse_row(row, competition)

                except Exception as e:
                    CrawlerLogMessage.objects.create(
                        message_type=CrawlerLogMessage.ERROR,
                        message="crawl_fixtures_per_league, {}".format(
                            e.__str__())
                    )
            if follow_pagination:
                # recursively parse all next sites if there are any
                pagination = FSRAbstractParser.get_pagination(url)
                if pagination:
                    current = pagination.find('span',
                                              attrs={'class': 'current'})
                    if current and int(current.find(text=True)) == 1:
                        print(u"Follow pagination, {} pages.".format(
                            len(pagination)))
                        for page in pagination.findAll('a', attrs={
                            'class': 'inactive'}):
                            if int(page.find(text=True)) > current:
                                nextUrl = [(competition.league.shortcode,
                                            page['href'], competition.id)]
                                cls.crawl(nextUrl)
        except Exception as e:
            CrawlerLogMessage.objects.create(
                message_type=CrawlerLogMessage.ERROR,
                message=u"crawl_fixture_per_league, {}".format(e.__str__())
            )

        # TODO: statistics
        # if lock:
        #     with lock:
        #         self.statistics['fixtures'] += count
        # else:
        #     self.statistics['fixtures'] += count

        return count
