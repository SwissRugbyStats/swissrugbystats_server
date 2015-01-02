from django.shortcuts import render
from swissrugby.models import League, Game, Team, GameParticipation
from swissrugby.serializer import LeagueSerializer, GameSerializer, TeamSerializer, GameParticipationSerializer, TeamInsightSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


''' --------------------------------

    API

-------------------------------- '''

# API root
@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'leagues': reverse('leagues', request=request, format=format),
        'games': reverse('games', request=request, format=format),
        'game-participations': reverse('game-participations', request=request, format=format),
        'teams': reverse('teams', request=request, format=format)
    })

# League list
class LeagueList(generics.ListAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

# League detail
class LeagueDetail(generics.RetrieveAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


# Game list
class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


# Game detail
class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


# GameParticipation list
class GameParticipationList(generics.ListAPIView):
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


# GameDetail detail
class GameParticipationDetail(generics.RetrieveAPIView):
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


# Team list
class TeamList(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


# Team detail
class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer