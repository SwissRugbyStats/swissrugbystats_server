from datetime import datetime
from typing import List

from django.utils import timezone

from swissrugbystats.core.models import Team, Venue, Game, GameParticipation, Referee
from swissrugbystats.crawler.log.CrawlerLogger import CrawlerLogger


class FSRGameParser(object):

    @staticmethod
    def get_host_team_logo(row: any) -> str:
        return row.findAll('td')[0].find('img')['src']

    @staticmethod
    def getGuestTeamLogo(row: any) -> str:
        return row.findAll('td')[2].find('img')['src']

    @staticmethod
    def parseTeams(rows: List[any]) -> (Team, Team):
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
    def parse_rows(rows: List[any], fsr_url: str, competition: any) -> bool:
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
        :param competition:
        :return:
        """
        logger = CrawlerLogger.get_logger_for_class(FSRGameParser)

        game: Game = None

        host: Team = None
        guest: Team = None

        host_participation: GameParticipation = None
        guest_participation: GameParticipation = None

        venue: Venue = None

        score_row: int = 4  # number of the row where the score should be located

        if len(rows) > 1:

            host, guest = FSRGameParser.parseTeams(rows)

            if not host or not guest:
                return False

            game, host_participation, guest_participation = FSRGameParser.get_game(fsr_url, host, guest)

            host.fsr_logo = FSRGameParser.get_host_team_logo(rows[1])
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

            # set competition
            game.competition = competition

            print("get venue")

            # get venue
            venue_name = rows[3].findAll('td')[1].find(text=True)  # venue

            print("venue name" + venue_name)

            if not Venue.objects.filter(name=venue_name):
                venue = Venue()
                venue.name = venue_name
                logger.log(u"Venue {} created".format(venue_name))
            else:
                venue = Venue.objects.filter(name=venue_name)[0]
                print("venue already exists " + venue.__str__())

        # if there are more rows than the score row, check for Forfait
        if len(rows) > score_row:
            if rows[score_row].findAll('td')[1].find(text=True).strip() == "Forfait":
                score_row += 1
                # save forfait in db
                if rows[score_row].findAll('td')[0].find(text=True).strip() != "":
                    logger.log("host forfait")
                    host_participation.forfait = True
                elif rows[score_row].findAll('td')[2].find(text=True).strip() != "":
                    logger.log("guest forfait")
                    guest_participation.forfait = True

            # get the score
            host_participation.score = int(rows[score_row].findAll('td')[0].find(text=True))  # score host
            guest_participation.score = int(rows[score_row].findAll('td')[2].find(text=True))  # score guest

            # get tries, cards and referee
        if len(rows) >= score_row + 1:
            host_participation.tries = int(rows[score_row + 1].findAll('td')[0].find(text=True))  # tries host
            guest_participation.tries = int(rows[score_row + 1].findAll('td')[2].find(text=True))  # tries guest

        if len(rows) >= score_row + 2:
            host_participation.redCards = int(
                rows[score_row + 2].findAll('td')[0].find(text=True))  # red cards host
            guest_participation.redCards = int(
                rows[score_row + 2].findAll('td')[2].find(text=True))  # red cards guest

        # referee is not always there
        if len(rows) >= score_row + 5:
            ref_name = rows[score_row + 4].findAll('td')[1].find(text=True).strip()  # referee
            # TODO: save performance by not reassigning referee if already set
            if not Referee.objects.filter(name=ref_name):
                referee = Referee()
                referee.name = ref_name
                logger.log(u"Referee {} created".format(ref_name))
            else:
                referee = Referee.objects.filter(name=ref_name)[0]
            referee.save()
            game.referee = referee

        if host and host_participation:
            host.save()
            host_participation.team = host
            host_participation.save()

        if guest and guest_participation:
            guest.save()
            guest_participation.team = guest
            guest_participation.save()

        if host_participation and guest_participation:
            game.host = host_participation
            game.guest = guest_participation

        if venue:
            venue.save()
            game.venue = venue

        game.save()

        logger.log(u"Game {} created / updated".format(Game.objects.get(id=game.id).__str__()))

        return True
