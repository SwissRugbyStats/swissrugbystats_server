from django_admin_conf_vars.global_vars import config
from django.db import models
from swissrugbystats import settings
from swissrugbystats.core.models import Game
from simple_history.models import HistoricalRecords


class Trophy(models.Model):
    """
    Represents a trophy that can be awarded to players after a game.
    i.e. "Man of the Match" or "Tackle of the Match"
    """
    # name
    # club
    # public
    # history
    pass


class Position(models.Model):
    """
    Represents a player's position.
    """
    # name
    # number
    # history
    pass


class Player(models.Model):
    """
    Represents a (rugby) player.
    """
    # first_name
    # last_name
    # photo
    # position
    # club
    # birthdate
    # (height & weight)
    # nationality
    pass


class LineUp(models.Model):
    """
    Represents the lineup of a team for a specific game.
    """
    # game
    # player - position
    pass


class Substitution(models.Model):
    """
    Represents a substitution of a player
    """
    player_in = models.ForeignKey(Player)
    player_out = models.ForeignKey(Player)


class PointType(models.Model):
    """
    Represents a type of point that can be scored during a game.
    i.e. "Try", "Penalty", "Conversion"
    """
    # name
    # value
    pass


class Point(models.Model):
    """
    Represents a point made during a game.
    """
    point_type = models.ForeignKey(PointType)
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)

    def __unicode__(self):
        return self.pointType.name+' by '+self.player.get_name()


class CardType(models.Model):
    """
    Represents a type of card players can get punished with.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Card(models.Model):
    """
    Represents a card received by a player during a specific game.
    """
    card_type = models.ForeignKey(CardType)
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)

    def __unicode__(self):
        return self.cardType.name+" ("+self.player.get_name()+")"
