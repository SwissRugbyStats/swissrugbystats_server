from rest_framework import serializers
from swissrugbystats.core.models import Competition, League, Team, Game, GameParticipation, Referee, Venue, Season, Favorite
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League


class CompetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competition


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
    pointCount = serializers.ReadOnlyField(source='get_point_count')
    gameCount = serializers.ReadOnlyField(source='get_game_count')
    winCount = serializers.ReadOnlyField(source='get_win_count')
    drawCount = serializers.ReadOnlyField(source='get_draw_count')
    lossCount = serializers.ReadOnlyField(source='get_loss_count')
    nextGame = GameSerializer(source='get_next_game')
    lastGame = GameSerializer(source='get_last_game')

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