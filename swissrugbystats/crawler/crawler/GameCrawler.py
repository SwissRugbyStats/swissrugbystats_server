from swissrugbystats.crawler.crawler import AbstractCrawler
from swissrugbystats.crawler.parser import FSRAbstractParser


class GameCrawler(AbstractCrawler):

    @classmethod
    def crawl_single_url(cls, url, follow_pagination=False):
        """
        TODO:
        - get host & guest
        - get game
        :param url:
        :param follow_pagination:
        :return:
        """

        # Game details & team logos

        # TODO:
        # get

        # make new request to game detail page
        soup2 = FSRAbstractParser.get_soup(url)
        game_detail_table = soup2.find('table', attrs={'class': None})

        rows = game_detail_table.findAll('tr')

        if len(rows) > 1:
            host.fsr_logo = FSRGameParser.getHostTeamLogo(rows[1])
            guest.fsr_logo = FSRGameParser.getGuestTeamLogo(rows[1])

            if len(rows) > 3:
                venueName = rows[3].findAll('td')[1].find(text=True)     # venue
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
                        hostParticipant.forfait = True
                    elif rows[scoreRow].findAll('td')[2].find(text=True).strip() != "":
                        logger.log("guest forfait")
                        guestParticipant.forfait = True

                hostParticipant.score = int(rows[scoreRow].findAll('td')[0].find(text=True))          # score host
                guestParticipant.score = int(rows[scoreRow].findAll('td')[2].find(text=True))         # score guest

                if len(rows) >= scoreRow+1:
                    hostParticipant.tries = int(rows[scoreRow+1].findAll('td')[0].find(text=True))          # tries host
                    guestParticipant.tries = int(rows[scoreRow+1].findAll('td')[2].find(text=True))         # tries guest
                    if len(rows) >= scoreRow+2:
                        hostParticipant.redCards = int(rows[scoreRow+2].findAll('td')[0].find(text=True))       # red cards host
                        guestParticipant.redCards = int(rows[scoreRow+2].findAll('td')[2].find(text=True))      # red cards guest

                        # referee is not always there
                        if len(rows)>=scoreRow+5:
                            refName = rows[scoreRow+4].findAll('td')[1].find(text=True).strip()     # referee
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
        hostParticipant.team = host
        hostParticipant.save()
        guestParticipant.team = guest
        guestParticipant.save()
        game.host = hostParticipant
        game.guest = guestParticipant

        venue.save()
        game.venue = venue

        game.save()

        logger.log(u"GameResult {} created / updated".format(Game.objects.get(id=game.id).__str__()))
