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
