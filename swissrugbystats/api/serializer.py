# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from swissrugbystats.coach.models import Player
from swissrugbystats.core.models import Club, Competition, League, Team, Game, GameParticipation, Referee, Venue, \
    Season, Favorite


class PlayerSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """

    class Meta:
        fields = '__all__'
        model = Player


class ClubSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """

    class Meta:
        fields = '__all__'
        model = Club


class LeagueSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """

    class Meta:
        fields = '__all__'
        model = League


class SeasonSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """

    class Meta:
        fields = '__all__'
        model = Season


class CompetitionSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """
    league = LeagueSerializer(many=False, read_only=True)
    season = SeasonSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Competition


class TeamSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """
    logo = serializers.ReadOnlyField(source='get_logo')

    class Meta:
        fields = '__all__'
        model = Team


class GameParticipationSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """
    team = TeamSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = GameParticipation


class RefereeSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """

    class Meta:
        fields = '__all__'
        model = Referee


class VenueSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """

    class Meta:
        fields = '__all__'
        model = Venue


class GameSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """
    host = GameParticipationSerializer(many=False, read_only=True)
    guest = GameParticipationSerializer(many=False, read_only=True)
    league = LeagueSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Game
        ordering = 'date'


class GameDetailSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """
    host = GameParticipationSerializer(many=False, read_only=True)
    guest = GameParticipationSerializer(many=False, read_only=True)
    league = LeagueSerializer(many=False, read_only=True)
    season = SeasonSerializer(many=False, read_only=True)
    referee = RefereeSerializer(many=False, read_only=True)
    venue = VenueSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Game


class TeamInsightSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """
    logo = serializers.ReadOnlyField(source='get_logo')
    nextGame = GameSerializer(source='get_next_game')
    lastGame = GameSerializer(source='get_last_game')

    class Meta:
        fields = '__all__'
        model = Team


class UserSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name')


class UserSerializer2(serializers.ModelSerializer):
    """
    Todo: document.
    """

    class Meta:
        model = User
        fields = ('id', 'username')


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """

    # team = TeamSerializer(many=False, read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'team')


class FavoriteDetailSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """
    team = TeamSerializer(many=False, read_only=True)
    user = UserSerializer2(many=False, read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'team')


class LeagueDetailSerializer(serializers.ModelSerializer):
    """
    Todo: document.
    """
    league_games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = League
        fields = ('id', 'name', 'shortcode', 'league_games')
