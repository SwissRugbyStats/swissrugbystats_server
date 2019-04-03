from swissrugbystats.core.models import Competition


class FSRAbstractParser(object):

    @staticmethod
    def parse_row(row: any, competition: Competition):
        raise NotImplementedError('must define parseRow to use this base class')
