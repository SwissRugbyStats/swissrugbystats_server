from rest_framework import serializers
from swissrugby.models import League, Team, Game, GameParticipation, Referee, Venue, Season, Favorite
from swissrugbystats import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League


class SeasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Season


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team


class GameParticipationSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=False, read_only=True)

    class Meta:
        model = GameParticipation
        #fields = ('name', 'shortcode')


class RefereeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referee


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue


class GameSerializer(serializers.ModelSerializer):
    host = GameParticipationSerializer(many=False, read_only=True)
    guest = GameParticipationSerializer(many=False, read_only=True)
    league = LeagueSerializer(many=False, read_only=True)

    class Meta:
        model = Game
        ordering = 'date'


class GameDetailSerializer(serializers.ModelSerializer):
    host = GameParticipationSerializer(many=False, read_only=True)
    guest = GameParticipationSerializer(many=False, read_only=True)
    league = LeagueSerializer(many=False, read_only=True)
    season = SeasonSerializer(many=False, read_only=True)
    referee = RefereeSerializer(many=False, read_only=True)
    venue = VenueSerializer(many=False, read_only=True)

    class Meta:
        model = Game


class TeamInsightSerializer(serializers.ModelSerializer):
    pointCount = serializers.ReadOnlyField(source='getPointCount')
    gameCount = serializers.ReadOnlyField(source='getGameCount')
    winCount = serializers.ReadOnlyField(source='getWinCount')
    drawCount = serializers.ReadOnlyField(source='getDrawCount')
    lossCount = serializers.ReadOnlyField(source='getLossCount')
    nextGame = GameSerializer(source='getNextGame')
    lastGame = GameSerializer(source='getLastGame')

    class Meta:
        model = Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name')


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class FavoriteSerializer(serializers.ModelSerializer):
    # team = TeamSerializer(many=False, read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'team')


class FavoriteDetailSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=False, read_only=True)
    user = UserSerializer2(many=False, read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'team')


class LeagueDetailSerializer(serializers.ModelSerializer):
    league_games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = League
        fields = ('id', 'name', 'shortCode', 'league_games')