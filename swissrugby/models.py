from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
'''
-------------------------------------------
'''


class League(models.Model):
    name = models.CharField(max_length=50, null=True)
    shortCode = models.CharField(max_length=50)

    def getLeagueUrl(self):
        return "http://www.suisserugby.com/competitions/" + self.shortCode + ".html"

    def getFixturesUrl(self):
        return "http://www.suisserugby.com/competitions/" + self.shortCode + "/lt/fixtures.html"

    def getResultsUrl(self):
        return "http://www.suisserugby.com/competitions/" + self.shortCode + "/lt/results.html"

    def __unicode__(self):
        return self.name


'''
-------------------------------------------
'''


class Season(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.name


'''
-------------------------------------------
'''


class Team(models.Model):
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=200, null=True, blank=True) # move to club class, once it exists

    def getPointCount(self):
        games = Game.objects.all()
        points = 0

        for g in [x for x in games if (x.host.team == self) & (x.host.score is not None)]:
            points += g.getHostPoints()

        for g in [x for x in games if (x.guest.team == self) & (x.guest.score is not None)]:
            points += g.getGuestPoints()

        return points

    def getCardCount(self):
        games = GameParticipation.objects.filter(team=self)
        cards = 0
        for game in games:
            if game.redCards:
                cards += game.redCards
        return cards

    def getTryCount(self):
        games = GameParticipation.objects.filter(team=self)
        tries = 0
        for game in games:
            if game.tries:
                tries += game.tries
        return tries

    def getWinCount(self):
        games = Game.objects.all()
        wins = 0

        for g in [x for x in games if x.host.team == self]:
            if g.getHostPoints() >= 4:
                wins += 1

        for g in [x for x in games if x.guest.team == self]:
            if g.getGuestPoints() >= 4:
                wins += 1

        return wins

    def getDrawCount(self):
        games = Game.objects.all()
        draws = 0

        for g in [x for x in games if x.host.team == self]:
            if g.getHostPoints() == 2:
                draws += 1

        for g in [x for x in games if x.guest.team == self]:
            if g.getGuestPoints() == 2:
                draws += 1

        return draws

    def getLossCount(self):
        games = Game.objects.all()
        losses = 0

        for g in [x for x in games if (x.host.team == self) & (x.host.score is not None)]:
            if g.getHostPoints() <= 1:
                losses += 1

        for g in [x for x in games if (x.guest.team == self) & (x.guest.score is not None)]:
            if g.getGuestPoints() <= 1:
                losses += 1

        return losses

    def getGameCount(self):
        #return GameParticipation.objects.filter(Q(team=self) & Q(score__isnull=False)).count()
        games = Game.objects.all()
        count = 0

        for g in [x for x in games if (x.host.team == self) & (x.host.score is not None)]:
            count += 1

        for g in [x for x in games if (x.guest.team == self) & (x.guest.score is not None)]:
            count += 1

        return count

    def getGames(self):
        gps = list(GameParticipation.objects.filter(Q(team=self)))
        games = list(Game.objects.all())
        result = []
        for g in games:
            for gp in gps:
                if (g.host == gp) | (g.guest == gp):
                    gps.remove(gp)
                    result.append(g)
                if len(gps) <= 0:
                    break
        return result

    def getNextGame(self):
        gps = list(GameParticipation.objects.filter(Q(team=self)))
        games = list(Game.objects.filter(date__gt=datetime.today()))
        for g in games:
            for gp in gps:
                if (g.host == gp) | (g.guest == gp):
                    return g
        return 0

    def getLastGame(self):
        gps = list(GameParticipation.objects.filter(Q(team=self)))
        games = list(Game.objects.filter(date__lt=datetime.today()).order_by('-date'))
        for g in games:
            for gp in gps:
                if (g.host == gp) | (g.guest == gp):
                    return g
        return 0


    def __unicode__(self):
        return self.name


'''
-------------------------------------------
'''


class Venue(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


'''
-------------------------------------------
'''


class Referee(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


'''
-------------------------------------------
'''


class GameParticipation(models.Model):
    team = models.ForeignKey(Team, verbose_name="Team", related_name="Team_set")
    score = models.IntegerField(verbose_name="Score", blank=True, null=True)
    tries = models.IntegerField(verbose_name="Tries", blank=True, null=True)
    redCards = models.IntegerField(verbose_name="Red Cards", blank=True, null=True)
    points = models.IntegerField(verbose_name="Points", blank=True, null=True)

    def __unicode__(self):
        return self.team.name + " " + str(self.score) + " (" + str(self.tries) + "/" + str(self.redCards) + "/" + str(self.points) + ")"


'''
-------------------------------------------
'''


class Game(models.Model):
    fsrID = models.CharField(max_length=10, blank=True, null=True, verbose_name="FSR ID")
    fsrUrl = models.CharField(max_length=100, blank=True, null=True, verbose_name="FSR Url")
    league = models.ForeignKey(League, verbose_name="League", related_name='league_games')
    season = models.ForeignKey(Season, verbose_name="Season", related_name='season_games')
    venue = models.ForeignKey(Venue, blank=True, null=True, verbose_name="Venue")
    referee = models.ForeignKey(Referee, blank=True, null=True, verbose_name="Referee")
    date = models.DateTimeField(verbose_name="KickOff")
    host = models.ForeignKey(GameParticipation, verbose_name="Host Participation", related_name="hostTeam_set")
    guest = models.ForeignKey(GameParticipation, verbose_name="Guest Participation", related_name="guestTeam_set")

    def __unicode__(self):
        return self.date.strftime('%d.%m.%Y') + ": " + self.host.team.name + " vs " + self.guest.team.name

    def getHostPoints(self):
        if (self.guest.score is None) | (self.host.score is None):
            return None
        points = 0
        if self.host.score > self.guest.score:
            points += 4
            if self.host.tries >= 4:
                points += 1
        elif self.host.score == self.guest.score:
            points += 2
        elif self.guest.score - self.host.score <= 7:
            points += 1

        return points


    def getGuestPoints(self):
        if (self.guest.score is None) | (self.host.score is None):
            return None
        points = 0
        if self.guest.score > self.host.score:
            points += 4
            if self.guest.tries >= 4:
                points += 1
        elif self.host.score == self.guest.score:
            points += 2
        elif self.host.score - self.guest.score <= 7:
            points += 1

        return points

class Favorite(models.Model):
    team = models.ForeignKey(Team, verbose_name="Team", related_name="Team")
    user = models.ForeignKey(User, verbose_name="User", related_name="Owner")