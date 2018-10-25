import requests
from bs4 import BeautifulSoup


class FSRAbstractParser(object):

    @staticmethod
    def get_soup(url):
        r = requests.get(url[1], headers=FSRAbstractParser.get_request_headers())
        return BeautifulSoup(r.text, "html.parser")

    @staticmethod
    def get_pagination(url):
        soup = FSRAbstractParser.get_soup(url)
        return soup.find('div', attrs={'class': 'pagination'})

    @staticmethod
    def get_table(url):
        soup = FSRAbstractParser.get_soup(url)
        return soup.find('table', attrs={'class': 'table'})

    @staticmethod
    def get_tables(url):
        soup = FSRAbstractParser.get_soup(url)
        if soup:
            tables = soup.findAll('table', attrs={'class': 'table'})
            print(u"{} tables found.".format(len(tables)))
            return tables
        else:
            return []
        # raise NotImplementedError('must define get_tables to use this base class')

    @staticmethod
    def parse_row(row, competition=None):
        raise NotImplementedError('must define parseRow to use this base class')

    @staticmethod
    def create_or_update(team):
        raise NotImplementedError('must define parseRow to use this base class')

    @staticmethod
    def get_request_headers():
        return {'User-Agent': 'Mozilla 5.0'}
