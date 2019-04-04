import os

from swissrugbystats.core.SeasonManager import SeasonManager
from swissrugbystats.core.models import Competition, League
from swissrugbystats.crawler.crawler.AbstractCrawler import AbstractCrawler
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger


class CompetitionCrawler(AbstractCrawler):

    @classmethod
    def crawl_by_url(cls, competition: Competition, url: str):
        raise NotImplementedError('must define crawl_by_url to use this base class')

    @classmethod
    def crawl_competition(cls, competition: Competition, follow_pagination: bool = False) -> int:
        raise NotImplementedError('must define crawl_competition to use this base class')

    @classmethod
    def crawl_current(cls) -> int:
        """
        TODO: counter needs to count competition
        :return: number of leagues created
        """
        count = 0
        logger = CrawlerLogger.get_logger_for_class(cls)
        season = SeasonManager.get_current_season()

        soup = cls.get_soup(os.environ.get('COMPETITIONS_BASE_URL'))

        nested_nav = soup.find('ul', attrs={'class': 'nested_nav'})

        items = nested_nav.find_all('li', recursive=False, attrs={'class': 'page_item'})

        for item in items:
            a = item.find('a')
            name = a.find(text=True)
            description = a['href']
            shortcode = description[description.rfind('/') + 1:description.rfind('.')]

            if name in 'Overview':
                continue

            found_leagues = League.objects.filter(shortcode=shortcode)

            if len(found_leagues) == 0:
                count = count + 1
                logger.log("Create new league {} ({})".format(name, shortcode))
                league = League()
                league.shortcode = shortcode
            else:
                league = found_leagues[0]
                logger.log("Update existing league {} ({})".format(name, shortcode))

            league.description = description
            league.name = name
            league.save()

            matching_competition = Competition.objects.filter(league=league, season=season)

            if not len(matching_competition) > 0:
                logger.log("Create new Competition: " + league.__str__() + ", " + season.__str__())
                competition = Competition()
                competition.league = league
                competition.season = season
                competition.save()

        return count

    @classmethod
    def crawl_archive(cls) -> int:
        # TODO
        return 0

    @classmethod
    def crawl(cls) -> int:
        """
        TODO: create competitions
        :return:
        """
        count: int = 0

        count = count + cls.crawl_current()
        count = count + cls.crawl_archive()

        return count
