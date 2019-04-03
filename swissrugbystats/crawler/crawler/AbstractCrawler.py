from typing import List, Any

import requests
from bs4 import BeautifulSoup

from swissrugbystats.core.models import Competition
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger


class AbstractCrawler(object):

    @classmethod
    def get_request_headers(cls) -> Any:
        return {'User-Agent': 'Mozilla 5.0'}

    @classmethod
    def get_soup(cls, url: str) -> Any:
        r = requests.get(url, headers=cls.get_request_headers())
        # raise exception in case of 404 or 500
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")

    @classmethod
    def get_pagination(cls, url: str) -> Any:
        soup = cls.get_soup(url)
        return soup.find('div', attrs={'class': 'pagination'})

    @classmethod
    def get_table(cls, url: str) -> Any:
        soup = AbstractCrawler.get_soup(url)
        return soup.find('table', attrs={'class': 'table'})

    @classmethod
    def get_tables(cls, url: str) -> List[Any]:
        soup = cls.get_soup(url)
        if soup:
            tables = soup.findAll('table', attrs={'class': 'table'})
            print(u"{} tables found.".format(len(tables)))
            return tables
        else:
            return []
        # raise NotImplementedError('must define get_tables to use this base class')

    @classmethod
    def crawl(cls, competitions: List[Competition], follow_pagination: bool = False) -> int:
        """
        TODO: check that urls is a list
        :param competitions:
        :param follow_pagination:
        :return:
        """
        count: int = 0
        for competition in competitions:
            count = count + cls.crawl_competition(competition, follow_pagination)
        return count
        # raise NotImplementedError('must define crawl to use this base class')

    @classmethod
    def crawl_by_url(cls, competition: Competition, url: str):
        """
        Crawls exactly one URL.
        Called by handle_pagination and crawl_competition.
        :param competition:
        :param url:
        :return:
        """
        raise NotImplementedError('must define crawl_by_url to use this base class')

    @classmethod
    def crawl_competition(cls, competition: Competition, follow_pagination: bool = False) -> int:
        """
        Starts crawling on a competition.
        :param competition:
        :param follow_pagination:
        :return:
        """
        raise NotImplementedError('must define crawl_competition to use this base class')

    @classmethod
    def follow_pagination(cls, competition: Competition, url: str) -> int:
        """

        :param competition:
        :param url:
        :return: number of objects created
        """
        logger = CrawlerLogger.get_logger_for_class(cls)
        count = 0

        # recursively parse all next sites if there are any
        pagination = cls.get_pagination(url)
        if pagination:
            current = pagination.find('span', attrs={'class': 'current'})

            if current:
                current_page_number = int(current.find(text=True))

                if current_page_number == 1:

                    inactive_pages = pagination.findAll('a', attrs={'class': 'inactive'})

                    logger.log(u"Follow pagination, {} pages.".format(inactive_pages + 1))

                    for page in inactive_pages:
                        page_number = int(page.find(text=True))
                        logger.log(u"Next Page: {}, Current Page: {}".format(page_number, current_page_number))

                        if page_number > current_page_number:
                            count = count + cls.crawl_by_url(competition, page['href'])
        return count
