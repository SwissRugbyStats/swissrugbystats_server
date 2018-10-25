from swissrugbystats.crawler.log import CrawlerLogger
from swissrugbystats.crawler.parser import FSRAbstractParser


class AbstractCrawler(object):

    @classmethod
    def crawl(cls, urls, follow_pagination=False):
        """

        :param urls:
        :param follow_pagination:
        :return:
        """
        count = 0
        for url in urls:
            count = count + cls.crawl_per_league(url, follow_pagination)
        return count
        # raise NotImplementedError('must define crawl to use this base class')

    @classmethod
    def crawl_per_league(cls, url, follow_pagination=False):
        """

        :param url:
        :param follow_pagination:
        :return:
        """
        raise NotImplementedError('must define crawl_per_league to use this base class')

    @classmethod
    def follow_pagination(cls, url, competition):
        """

        :param url:
        :param competition:
        :return: number of objects created
        """
        logger = CrawlerLogger.get_logger_for_class(cls)
        count = 0

        # recursively parse all next sites if there are any
        pagination = FSRAbstractParser.get_pagination(url)
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
