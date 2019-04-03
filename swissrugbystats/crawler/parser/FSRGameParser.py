from datetime import datetime
from typing import Any, List

from django.utils import timezone

from swissrugbystats.core.models import Team, Venue, Game, GameParticipation, Referee
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger


class FSRGameParser(object):

    @staticmethod
    def getHostTeamLogo(row: Any) -> Any:
        return row.findAll('td')[0].find('img')['src']

    @staticmethod
    def getGuestTeamLogo(row: Any) -> Any:
        return row.findAll('td')[2].find('img')['src']

    @staticmethod
    def parseTeams(rows: List[Any]) -> Any:
        """

        :param rows:
        :return: Host: Team, Guest: Team
        """
        logger = CrawlerLogger.get_logger_for_class(FSRGameParser)

        first_row_cells = rows[0].findAll('td')
        host_name = first_row_cells[0].find(text=True).strip()
        guest_name = first_row_cells[2].find(text=True).strip()
        host_team = Team.objects.filter(name=host_name)
        guest_team = Team.objects.filter(name=guest_name)

        if not host_team:
            logger.error(u"Hostteam not found: ".format(host_name))
            return None, None
        else:
            host = host_team[0]
        if not guest_team:
            logger.log(u"Guestteam not found: ".format(guest_name))
            return False
        else:
            guest = guest_team[0]

        return host, guest

    @staticmethod
    def get_game(fsr_url: str, host: Team, guest: Team) -> (Game, GameParticipation, GameParticipation):
        # check if game is already stored, if so, update the existing one
        if not Game.objects.filter(fsrUrl=fsr_url):
            return Game(), GameParticipation(team=host), GameParticipation(team=guest)
        else:
            game = Game.objects.filter(fsrUrl=fsr_url)[0]
            return game, game.host, game.guest

    @staticmethod
    def parse_rows(rows: List[Any], fsr_url: str) -> bool:
        """
        Row contents (3 cols):

        Attention: colspans!

        0:  Host                    | 'versus'      | Guest
        1:  Logo                    |               | Logo
        2:  'Kickoff date and time' | datetime
        3:  'Venue'                 | Venue

        4?: Forfait                 | 'Forfait'     | Forfait

        4:  Host Score              | 'Score'       | Guest Score
        5:  Host Tries              | 'Tries'       | Guest Tries
        6:  Host Red Cards          | 'Red cards'   | Guest Red Cards
        7:  Host Bonus points       | 'Bonus'       | Guest Bonus points

        :param rows:
        :param fsr_url:
        :return:
        """
        logger = CrawlerLogger.get_logger_for_class(FSRGameParser)

        if len(rows) > 1:

            host, guest = FSRGameParser.parseTeams(rows)

            if not host or not guest:
                return False

            game, host_participation, guest_participation = FSRGameParser.get_game(fsr_url, host, guest)

            host.fsr_logo = FSRGameParser.getHostTeamLogo(rows[1])
            guest.fsr_logo = FSRGameParser.getGuestTeamLogo(rows[1])

            if len(rows) > 3:
                # parse date and set timezone
                date = rows[2].findAll('td')[1].find(text=True)
                d1 = timezone.get_current_timezone().localize(datetime.strptime(date, '%d.%m.%Y %H:%M'))
                d2 = d1.strftime('%Y-%m-%d %H:%M%z')
                game.date = d2

                # TODO: set fsrId
                # game.fsrID = cells[0].find(text=True)

                # set fsrUrl
                game.fsrUrl = fsr_url

                # TODO: get & set competition
                # game.competition = competition

                # get venue
                venueName = rows[3].findAll('td')[1].find(text=True)  # venue
                if not Venue.objects.filter(name=venueName):
                    venue = Venue()
                    venue.name = venueName
                    logger.log(u"Venue {} created".format(venueName))
                else:
                    venue = Venue.objects.filter(name=venueName)[0]

            scoreRow = 4

            if len(rows) > scoreRow:
                if rows[scoreRow].findAll('td')[1].find(text=True).strip() == "Forfait":
                    scoreRow += 1
                    # save forfait in db
                    if rows[scoreRow].findAll('td')[0].find(text=True).strip() != "":
                        logger.log("host forfait")
                        host_participation.forfait = True
                    elif rows[scoreRow].findAll('td')[2].find(text=True).strip() != "":
                        logger.log("guest forfait")
                        guest_participation.forfait = True

                host_participation.score = int(rows[scoreRow].findAll('td')[0].find(text=True))  # score host
                guest_participation.score = int(rows[scoreRow].findAll('td')[2].find(text=True))  # score guest

                if len(rows) >= scoreRow + 1:
                    host_participation.tries = int(rows[scoreRow + 1].findAll('td')[0].find(text=True))  # tries host
                    guest_participation.tries = int(rows[scoreRow + 1].findAll('td')[2].find(text=True))  # tries guest
                    if len(rows) >= scoreRow + 2:
                        host_participation.redCards = int(
                            rows[scoreRow + 2].findAll('td')[0].find(text=True))  # red cards host
                        guest_participation.redCards = int(
                            rows[scoreRow + 2].findAll('td')[2].find(text=True))  # red cards guest

                        # referee is not always there
                        if len(rows) >= scoreRow + 5:
                            refName = rows[scoreRow + 4].findAll('td')[1].find(text=True).strip()  # referee
                            # TODO: save performance by not reassigning referee if already set
                            if not Referee.objects.filter(name=refName):
                                referee = Referee()
                                referee.name = refName
                                logger.log(u"Referee {} created".format(refName))
                            else:
                                referee = Referee.objects.filter(name=refName)[0]
                            referee.save()
                            game.referee = referee

        host.save()
        guest.save()
        host_participation.team = host
        host_participation.save()
        guest_participation.team = guest
        guest_participation.save()
        game.host = host_participation
        game.guest = guest_participation

        venue.save()
        game.venue = venue

        game.save()

        logger.log(u"Game {} created / updated".format(Game.objects.get(id=game.id).__str__()))

        return True
