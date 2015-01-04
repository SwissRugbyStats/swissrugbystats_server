from rest_framework import serializers
from swissrugby.models import League, Team, Game, GameParticipation, Referee, Venue, Season


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team

class TeamInsightSerializer(serializers.ModelSerializer):
    pointCount = serializers.Field(source='getPointCount')
    gameCount = serializers.Field(source='getGameCount')
    class Meta:
        model = Team
        fields = ('id', 'name', 'pointCount', 'gameCount')

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

class GameDetailSerializer(serializers.ModelSerializer):
    host = GameParticipationSerializer(many=False, read_only=True)
    guest = GameParticipationSerializer(many=False, read_only=True)
    league = LeagueSerializer(many=False, read_only=True)
    season = SeasonSerializer(many=False, read_only=True)
    referee = RefereeSerializer(many=False, read_only=True)
    venue = VenueSerializer(many=False, read_only=True)
    class Meta:
        model = Game