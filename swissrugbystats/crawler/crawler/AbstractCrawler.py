from typing import List, Any

import requests
from bs4 import BeautifulSoup

from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger


class AbstractCrawler(object):

    @classmethod
    def get_request_headers(cls) -> Any:
        return {'User-Agent': 'Mozilla 5.0'}

    @classmethod
    def get_soup(cls, url: str) -> Any:
        r = requests.get(url[1], headers=cls.get_request_headers())
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
    def crawl(cls, urls: List[str], follow_pagination: bool = False) -> int:
        """
        TODO: check that urls is a list
        :param urls:
        :param follow_pagination:
        :return:
        """
        count = 0
        for url in urls:
            count = count + cls.crawl_single_url(url, follow_pagination)
        return count
        # raise NotImplementedError('must define crawl to use this base class')

    @classmethod
    def crawl_single_url(cls, url: str, follow_pagination : bool = False) -> Any:
        """

        :param url:
        :param follow_pagination:
        :return:
        """
        raise NotImplementedError('must define crawl_per_league to use this base class')

    @classmethod
    def follow_pagination(cls, url: str, competition: int) -> int:
        """

        :param url:
        :param competition:
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
                            next_url = [(competition.league.shortcode, page['href'], competition.id)]
                            count = count + cls.crawl(next_url)
        return count
