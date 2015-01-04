from django.shortcuts import render
from swissrugby.models import League, Game, Team, GameParticipation, Referee, Venue, Season
from swissrugby.serializer import LeagueSerializer, GameSerializer, TeamSerializer, GameParticipationSerializer, TeamInsightSerializer, RefereeSerializer, VenueSerializer, SeasonSerializer
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
        'teams': reverse('teams', request=request, format=format),
        'referees': reverse('referees', request=request, format=format),
        'seasons': reverse('seasons', request=request, format=format),
        'venues': reverse('venues', request=request, format=format)
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
    serializer_class = GameDetailSerializer


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

# Referee list
class RefereeList(generics.ListAPIView):
    queryset = Referee.objects.all()
    serializer_class = RefereeSerializer

# Venue list
class VenueList(generics.ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

# Season list
class SeasonList(generics.ListAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer