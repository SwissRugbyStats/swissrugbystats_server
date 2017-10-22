# -*- coding: utf-8 -*-
import threading
from swissrugbystats.crawler.SRSCrawler import SRSCrawler

class SRSAsyncCrawler(SRSCrawler):
    """
    Todo: document, fix bugs.
    """

    def crawl_teams(self, league_urls):
        """
        TODO: write doc.
        """
        lock = threading.Lock()
        self.statistics['teams'] = 0
        threads = []
        for url in league_urls:
            t = threading.Thread(target=self.crawl_teams_per_league, args=(url,lock))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        return self.statistics['teams']

    def crawl_results(self, league_results_urls, deep_crawl=False):
        """
        :param league_results_urls:    list of tuples [(league_shortcode, league_url), ..]
        :param deep_crawl:  defaults to False. Set True to follow pagination
        :return: -
        """
        # url is tupel of (leagueName, leagueUrl)
        lock = threading.Lock()
        self.statistics['results'] = 0
        threads = []
        for url in league_results_urls:
            t = threading.Thread(target=self.crawl_results_per_league, args=(url, deep_crawl, lock))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        return self.statistics['results']

    def crawl_fixtures(self, league_fixtures_urls, deep_crawl=False):
        """
        Fetch all the fixtures asynchronously and add the AsynchronousResults to fixture_tasks
        :param league_fixtures_urls:
        :param deep_crawl:
        :return:
        """
        lock = threading.Lock()
        self.statistics['fixtures'] = 0
        threads = []
        for url in league_fixtures_urls:
            t = threading.Thread(target=self.crawl_fixture_per_league, args=(url, deep_crawl, lock))
            t.start()
            threads.append(t)
        return self.statistics['fixtures']