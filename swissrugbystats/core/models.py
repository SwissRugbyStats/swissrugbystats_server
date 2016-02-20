from __future__ import unicode_literals
from django_admin_conf_vars.global_vars import config
from django.db import models
from django.db.models import Q
from django_resized import ResizedImageField
from datetime import datetime
from swissrugbystats import settings
from simple_history.models import HistoricalRecords


class Association(models.Model):
    """
    Represents an association.
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    abbreviation = models.CharField(max_length=10, null=False, unique=True)
    parent_association = models.ForeignKey('self', verbose_name="Parent Association", related_name="child_associations", null=True, blank=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return "{} ({})".format(self.name, self.abbreviation)


class Club(models.Model):
    """
    Represents a Rugby Club.
    """
    name = models.CharField(max_length=255, null=False)
    abbreviation = models.CharField(max_length=10, null=False)
    website = models.CharField(max_length=255, null=True, blank=True)
    associations = models.ManyToManyField(Association, related_name="clubs", blank=True)
    history = HistoricalRecords()

    def get_associations(self):
        return ", ".join([str(a) for a in self.associations.all()])

    def __unicode__(self):
        return self.name


class League(models.Model):
    """
    Todo: document.
    """
    name = models.CharField(max_length=50, null=True)
    shortcode = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    def get_league_url(self):
        return "{}{}{}".format(config.COMPETITIONS_BASE_URL, self.shortcode, config.LEAGUE_URL_ENDING)

    def get_fixtures_url(self):
            return "{}{}{}".format(config.COMPETITIONS_BASE_URL, self.shortcode, config.FIXTURES_URL_ENDING)

    def get_results_url(self):
            return "{}{}{}".format(config.COMPETITIONS_BASE_URL, self.shortcode, config.RESULTS_URL_ENDING)

    def get_archive_league_url(self, season_slug):
        return "{}{}/{}{}".format(config.ARCHIVE_BASE_URL, season_slug, self.shortcode, config.LEAGUE_URL_ENDING)

    def get_archive_fixtures_url(self, season_slug):
        return "{}{}/{}{}".format(config.ARCHIVE_BASE_URL, season_slug, self.shortcode, config.FIXTURES_URL_ENDING)

    def get_archive_results_url(self, season_slug):
        return "{}{}/{}{}".format(config.ARCHIVE_BASE_URL, season_slug, self.shortcode, config.RESULTS_URL_ENDING)

    def __unicode__(self):
        return self.name


class Season(models.Model):
    """
    Todo: document.
    """
    name = models.CharField(max_length=50, null=True)
    fsr_url_slug = models.CharField(max_length=50, unique=True, null=True, blank=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.name


class Competition(models.Model):
    """
    Todo: document.
    """
    league = models.ForeignKey(League, verbose_name="League", related_name='league_competitions')
    season = models.ForeignKey(Season, verbose_name="Season", related_name='season_competitions')
    history = HistoricalRecords()

    unique_together = ("league", "season")

    def get_league_url(self):
        print("get_league_url {}".format(self.__unicode__()))
        if self.season.id == int(config.CURRENT_SEASON):
            return self.league.get_league_url()
        else:
            return self.league.get_archive_league_url(self.season.fsr_url_slug)

    def get_fixtures_url(self):
        if self.season.id == int(config.CURRENT_SEASON):
            return self.league.get_fixtures_url()
        else:
            return self.league.get_archive_fixtures_url(self.season.fsr_url_slug)

    def get_results_url(self):
        if self.season.id == int(config.CURRENT_SEASON):
            return self.league.get_results_url()
        else:
            return self.league.get_archive_results_url(self.season.fsr_url_slug)

    def __unicode__(self):
        return "{} ({})".format(self.league, self.season)


class Team(models.Model):
    """
    Todo: document.
    """
    name = models.CharField(max_length=50)
    fsr_logo = models.CharField(max_length=200, null=True, blank=True)
    custom_logo = ResizedImageField(size=[500, 500], upload_to='logos/', blank=True, null=True, help_text='Custom team logo.')
    club = models.ForeignKey(Club, null=True, blank=True)
    history = HistoricalRecords()

    def get_logo(self):
        """
        :return: URL to the current team logo.
        """
        if self.custom_logo:
            return self.custom_logo.url
        else:
            return self.fsr_logo

    def get_point_count(self):
        """

        :return:
        """
        games = Game.objects.all()
        points = 0

        for g in [x for x in games if (x.host.team == self) & (x.host.score is not None)]:
            points += g.get_host_points()

        for g in [x for x in games if (x.guest.team == self) & (x.guest.score is not None)]:
            points += g.get_guest_points()

        return points

    def get_card_count(self):
        """

        :return:
        """
        games = GameParticipation.objects.filter(team=self)
        cards = 0
        for game in games:
            if game.redCards:
                cards += game.redCards
        return cards

    def get_try_count(self):
        """

        :return:
        """
        games = GameParticipation.objects.filter(team=self)
        tries = 0
        for game in games:
            if game.tries:
                tries += game.tries
        return tries

    def get_win_count(self):
        """

        :return:
        """
        games = Game.objects.all()
        wins = 0

        for g in [x for x in games if x.host.team == self]:
            if g.get_host_points() >= 4:
                wins += 1

        for g in [x for x in games if x.guest.team == self]:
            if g.get_guest_points() >= 4:
                wins += 1

        return wins

    def get_draw_count(self):
        """

        :return:
        """
        games = Game.objects.all()
        draws = 0

        for g in [x for x in games if x.host.team == self]:
            if g.get_host_points() == 2:
                draws += 1

        for g in [x for x in games if x.guest.team == self]:
            if g.get_guest_points() == 2:
                draws += 1

        return draws

    def get_loss_count(self):
        """

        :return:
        """
        games = Game.objects.all()
        losses = 0

        for g in [x for x in games if (x.host.team == self) & (x.host.score is not None)]:
            if g.get_host_points() <= 1:
                losses += 1

        for g in [x for x in games if (x.guest.team == self) & (x.guest.score is not None)]:
            if g.get_guest_points() <= 1:
                losses += 1

        return losses

    def get_game_count(self):
        """

        :return:
        """
        #return GameParticipation.objects.filter(Q(team=self) & Q(score__isnull=False)).count()
        games = Game.objects.all()
        count = 0

        for g in [x for x in games if (x.host.team == self) & (x.host.score is not None)]:
            count += 1

        for g in [x for x in games if (x.guest.team == self) & (x.guest.score is not None)]:
            count += 1

        return count

    def get_games(self):
        """

        :return:
        """
        gps = GameParticipation.objects.filter(Q(team=self))
        games = Game.objects.filter(Q(host__in=gps) | Q(guest__in=gps)).order_by('date')

        return games

    def get_games_by_season(self, season):
        """

        :param season:
        :return:
        """
        gps = GameParticipation.objects.filter(Q(team=self))
        games = Game.objects.filter(competition__season=season).filter(Q(host__in=gps) | Q(guest__in=gps)).order_by('date')
        return games

    def get_next_game(self):
        """

        :return:
        """
        gps = list(GameParticipation.objects.filter(Q(team=self)))
        games = list(Game.objects.filter(date__gt=datetime.today()))
        for g in games:
            for gp in gps:
                if (g.host == gp) | (g.guest == gp):
                    return g
        return None

    def get_last_game(self):
        """

        :return:
        """
        gps = list(GameParticipation.objects.filter(Q(team=self)))
        games = list(Game.objects.filter(date__lt=datetime.today()).order_by('-date'))
        for g in games:
            for gp in gps:
                if (g.host == gp) | (g.guest == gp):
                    return g
        return None

    def __unicode__(self):
        return self.name


class Venue(models.Model):
    """
    Todo: document.
    """
    name = models.CharField(max_length=100)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.name


class Referee(models.Model):
    """
    Todo: document.
    """
    name = models.CharField(max_length=100)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.name


class GameParticipation(models.Model):
    """
    Todo: document.
    """
    team = models.ForeignKey(Team, verbose_name="Team", related_name="Team_set")
    score = models.IntegerField(verbose_name="Score", blank=True, null=True)
    tries = models.IntegerField(verbose_name="Tries", blank=True, null=True)
    redCards = models.IntegerField(verbose_name="Red Cards", blank=True, null=True)
    points = models.IntegerField(verbose_name="Points", blank=True, null=True)
    history = HistoricalRecords()

    def get_game(self):
        if self.hostTeam_set.all():
            game = self.hostTeam_set.all().first()
        else:
            game = self.guestTeam_set.all().first()

        return "{}: {}".format(game.competition.league.__str__(), game.__str__())

    def __unicode__(self):
        return self.team.name + " " + str(self.score) + " (" + str(self.tries) + "/" + str(self.redCards) + "/" + str(self.points) + ")"


class Game(models.Model):
    """
    Todo: document.
    """
    fsrID = models.CharField(max_length=10, blank=True, null=True, verbose_name="FSR ID")
    fsrUrl = models.CharField(max_length=100, blank=True, null=True, verbose_name="FSR Url")
    competition = models.ForeignKey(Competition, verbose_name="Competition", related_name="competition_games")
    venue = models.ForeignKey(Venue, blank=True, null=True, verbose_name="Venue")
    referee = models.ForeignKey(Referee, blank=True, null=True, verbose_name="Referee")
    date = models.DateTimeField(verbose_name="KickOff")
    host = models.ForeignKey(GameParticipation, verbose_name="Host Participation", related_name="hostTeam_set")
    guest = models.ForeignKey(GameParticipation, verbose_name="Guest Participation", related_name="guestTeam_set")
    history = HistoricalRecords()

    def __unicode__(self):
        return self.date.strftime('%d.%m.%Y') + ": " + self.host.team.name + " vs " + self.guest.team.name

    def get_host_points(self):
        """
        Todo: document.
        :return:
        """
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

    def get_guest_points(self):
        """
        Todo: document.
        :return:
        """
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
    """
    Todo: document.
    """
    team = models.ForeignKey(Team, verbose_name="Team", related_name="Team")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="User", related_name="Owner")
    history = HistoricalRecords()