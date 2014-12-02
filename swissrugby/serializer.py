from django.forms import widgets
from rest_framework import serializers
from swissrugby.models import League, Team, Game, GameParticipation


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        #fields = ('name', 'shortCode')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        #fields = ('name', 'shortcode')


class GameParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameParticipation
        #fields = ('name', 'shortcode')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        #fields = ('name', 'shortcode')