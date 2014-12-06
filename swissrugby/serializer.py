from django.forms import widgets
from rest_framework import serializers
from swissrugby.models import League, Team, Game, GameParticipation


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        #fields = ('name', 'shortCode')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        #fields = ('name', 'shortcode')

class GameParticipationSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=False, read_only=True)
    class Meta:
        model = GameParticipation
        #fields = ('name', 'shortcode')

class GameSerializer(serializers.ModelSerializer):
    host = GameParticipationSerializer(many=False, read_only=True)
    guest = GameParticipationSerializer(many=False, read_only=True)
    league = LeagueSerializer(many=False, read_only=True)
    class Meta:
        model = Game
        #fields = ('name', 'shortcode')
