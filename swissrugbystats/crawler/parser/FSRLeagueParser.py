from swissrugbystats.core.models import Team
from swissrugbystats.crawler.parser import FSRAbstractParser


class FSRLeagueParser(FSRAbstractParser):

    @staticmethod
    def create_or_update(team):
        """

        :param team:
        :return:
        """
        if not Team.objects.filter(name=team.name):
            t = Team(name=team.name)
            t.save()
            print(u"Team {0} created".format(t.__str__()))
        else:
            print(u"Team {0} already in DB".format(Team.objects.filter(name=team.name).first().__str__()))

    @staticmethod
    def parse_row(row):
        """

        :param row:
        :return: Team
        """
        cells = row.findAll('td')
        if len(cells) > 0:
            # check if we are looking at the season table and not a playdown / playoff / finals table
            if len(cells) > 5:
                team_name_raw = cells[1].find(text=True)
                print("Found {}".format(team_name_raw))
                try:
                    # parse Teamname and remove leading and tailing spaces
                    team_name_unicode = u"{}".format(team_name_raw.strip())

                    team = Team(name=team_name_unicode)
                    FSRLeagueParser.create_or_update(team)

                except Exception as e:
                    raise Exception('Error while parsing Teamname {}: {}'.format(team_name_raw, e.__str__()))
            else:
                print(u"Less than 5 columns, must be finals table or similar. --> ignore")

