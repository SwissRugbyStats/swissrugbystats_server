from swissrugbystats.core.models import Team
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger
from swissrugbystats.crawler.parser.FSRAbstractParser import FSRAbstractParser


class FSRLeagueParser(FSRAbstractParser):

    @staticmethod
    def parse_row(row):
        """

        :param row:
        :return: Team
        """
        logger = CrawlerLogger.get_logger_for_class(FSRLeagueParser)

        cells = row.findAll('td')
        if len(cells) > 0:
            # check if we are looking at the season table and not a playdown / playoff / finals table
            if len(cells) > 5:
                team_name_raw = cells[1].find(text=True)
                try:
                    # parse Teamname and remove leading and tailing spaces
                    team_name_unicode = u"{}".format(team_name_raw.strip())

                    if not Team.objects.filter(name=team_name_unicode):
                        t = Team(name=team_name_unicode)
                        t.save()
                        logger.log(u"Team {0} created".format(t.__str__()))
                        return True
                    else:
                        logger.log(u"Team {0} already in DB".format(Team.objects.filter(name=team_name_unicode).first().__str__()))

                except Exception as e:
                    raise Exception('Error while parsing Teamname {}: {}'.format(team_name_raw, e.__str__()))
            else:
                logger.log(u"Less than 5 columns, must be finals table or similar. --> ignore")

