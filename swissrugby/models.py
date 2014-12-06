from django.db import models

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


class Team(models.Model):
    name = models.CharField(max_length=50)

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


class GameParticipation(models.Model):
    team = models.ForeignKey(Team, verbose_name="Team", related_name="Team_set")
    score = models.IntegerField(verbose_name="Score", blank=True, null=True)
    tries = models.IntegerField(verbose_name="Score", blank=True, null=True)
    redCards = models.IntegerField(verbose_name="Red Cards", blank=True, null=True)
    points = models.IntegerField(verbose_name="Score", blank=True, null=True)

    def __unicode__(self):
        return self.team.name + " " + str(self.score) + " (" + str(self.tries) + "/" + str(self.redCards) + "/" + str(self.points) + ")"


'''
-------------------------------------------
'''


class Game(models.Model):
    fsrID = models.CharField(max_length=10, blank=True, null=True, verbose_name="FSR ID")
    fsrUrl = models.CharField(max_length=100, blank=True, null=True, verbose_name="FSR Url")
    league = models.ForeignKey(League, verbose_name="League")
    date = models.DateTimeField(verbose_name="KickOff")
    host = models.ForeignKey(GameParticipation, verbose_name="Host Participation", related_name="hostTeam_set")
    guest = models.ForeignKey(GameParticipation, verbose_name="Guest Participation", related_name="guestTeam_set")

    def __unicode__(self):
        return self.date.strftime('%d.%m.%Y') + ": " + self.host.team.name + " vs " + self.guest.team.name