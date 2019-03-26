from typing import Any


class FSRAbstractParser(object):

    @staticmethod
    def parse_row(row: Any, competition: Any = None):
        raise NotImplementedError('must define parseRow to use this base class')
