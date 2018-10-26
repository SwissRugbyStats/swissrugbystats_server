class FSRAbstractParser(object):

    @staticmethod
    def parse_row(row, competition=None):
        raise NotImplementedError('must define parseRow to use this base class')
