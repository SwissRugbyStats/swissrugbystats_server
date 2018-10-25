# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import DO_NOTHING, CASCADE

from swissrugbystats.core.models import Club, Game, GameParticipation


class Position(models.Model):
    """
    Represents a player's position.
    """
    name = models.CharField(max_length=50, null=False, blank=False, help_text='')

    def __str__(self):
        return self.name


class Player(models.Model):
    """
    Represents a (rugby) player.
    """
    first_name = models.CharField(max_length=50, help_text='First name of the player.')
    last_name = models.CharField(max_length=50, help_text='Last name of the player.')
    photo = models.ImageField(upload_to='players/', blank=True, null=True, help_text='Portrait photo of the player.')
    default_positions = models.ManyToManyField(Position, blank=True,
                                               help_text='The positions this player usually plays on.')
    club = models.ForeignKey(Club, help_text='The main club the player belongs to.', on_delete=CASCADE)

    birth_date = models.DateField(blank=True, null=True, help_text='Date of birth. Used to calculate the age.')
    height = models.IntegerField(null=True, blank=True, help_text='Current height of the player.')
    weight = models.IntegerField(null=True, blank=True, help_text='Current weight of the player.')

    def get_full_name(self):
        return u"{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()


class TrophyType(models.Model):
    """
    Represents a trophy that can be awarded to players after a game.
    i.e. "Man of the Match" or "Tackle of the Match"
    """
    name = models.CharField(max_length=255,
                            help_text='Name of the trophy, i.e. "Man of the Match" or "Tackle of the Match"')

    # club
    # public

    def __str__(self):
        return self.name


class Trophy(models.Model):
    trophy_type = models.ForeignKey(TrophyType, help_text='', on_delete=CASCADE)
    game = models.ForeignKey(Game, help_text='', on_delete=CASCADE)
    player = models.ForeignKey(Player, help_text='', on_delete=CASCADE)

    def __str__(self):
        return u"{} in {} is {}".format(self.trophy_type, self.game, self.player)


class LineUp(models.Model):
    """
    Represents the lineup of a team for a specific game.
    """
    game = models.ForeignKey(GameParticipation, help_text='', on_delete=CASCADE)

    def __str__(self):
        return self.game


class LineUpPosition(models.Model):
    """
    Represents the lineup of a team for a specific game.
    """
    player = models.ForeignKey(Player, help_text='', on_delete=CASCADE)
    position_number = models.IntegerField(help_text='')
    lineup = models.ForeignKey(LineUp, help_text='', on_delete=CASCADE)

    def __str__(self):
        return u"{}: {}".format(self.position_number, self.player)


class Substitution(models.Model):
    """
    Represents a substitution of a player
    """
    player_in = models.ForeignKey(Player, related_name='player_in', on_delete=CASCADE)
    player_out = models.ForeignKey(Player, related_name='player_out', on_delete=CASCADE)


class PointType(models.Model):
    """
    Represents a type of point that can be scored during a game.
    i.e. "Try", "Penalty", "Conversion"
    """
    name = models.CharField(max_length=50, help_text='Name of the point type (i.e. "Try" or "Goal")')
    value = models.IntegerField(help_text='Numeric value of the point type (i.e. 5 for a try, 3 for a penalty)')

    def __str__(self):
        return u"{} ({} points)".format(self.name, self.value)


class Point(models.Model):
    """
    Represents a point made during a game.
    """
    point_type = models.ForeignKey(PointType, help_text='Type of point that was made.', on_delete=CASCADE)
    game = models.ForeignKey(Game, help_text='Game during which this point has been scored.', on_delete=CASCADE)
    player = models.ForeignKey(Player, help_text='Player who actually scored the point.', on_delete=CASCADE)

    def __str__(self):
        return "{} by {}".format(self.pointType.name, self.player.get_name())


class CardType(models.Model):
    """
    Represents a type of card players can get punished with.
    Todo: hard coded?
    """
    name = models.CharField(max_length=50, help_text='Name of the card type.')

    def __str__(self):
        return self.name


class Card(models.Model):
    """
    Represents a card received by a player during a specific game.
    """
    card_type = models.ForeignKey(CardType, help_text='Type of card which was received.', on_delete=CASCADE)
    player = models.ForeignKey(Player, help_text='Player that actually received the card.', on_delete=CASCADE)
    game = models.ForeignKey(Game, help_text='Game during which this card has been received.', on_delete=CASCADE)
    notes = models.CharField(max_length=255, null=True, blank=True,
                             help_text='Additional notes regarding the card, i.e. "High Tackle" or similar.')

    def __str__(self):
        return u"{} ({}) in {}".format(self.cardType.name, self.player.get_full_name(), self.game)
