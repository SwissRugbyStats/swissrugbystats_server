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


class Game(models.Model):
    fsrID = models.CharField(max_length=10, blank=True, null=True, verbose_name="FSR ID")
    fsrUrl = models.CharField(max_length=100, blank=True, null=True, verbose_name="FSR Url")
    league = models.ForeignKey(League, verbose_name="League")
    date = models.DateTimeField(verbose_name="KickOff")
    hostTeam = models.ForeignKey(Team, verbose_name="Host", related_name="hostTeam_set")
    guestTeam = models.ForeignKey(Team, verbose_name="Guest", related_name="guestTeam_set")
    hostScore = models.IntegerField(verbose_name="Host Score", blank=True, null=True)
    guestScore = models.IntegerField(verbose_name="Guest Score", blank=True, null=True)

    def __unicode__(self):
        return self.date.strftime('%Y-%m-%d %H:%M') + ": " + str(self.hostTeam) + " vs " + str(self.guestTeam)